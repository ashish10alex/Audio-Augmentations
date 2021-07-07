import base64
import concurrent.futures
import io
import os
import shutil
import time
import uuid

import librosa
import pdbr
import soundfile as sf
from flask import Flask, flash, redirect, render_template, request
from flask.helpers import url_for
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from descriptions import description_dict
from utils import get_exectution_time

app = Flask(__name__)
app.secret_key = os.environ.get("FLASKBOXPLAYKEY")
# max upload size of 30Mb
app.config["MAX_CONTENT_LENGTH"] = 30 * 1000 * 1000

os.makedirs("static/client_audio", exist_ok=True)
os.makedirs("static/client_aug_wavs", exist_ok=True)


@app.route("/", methods=["GET"])
# @get_exectution_time
def index():
    show_examples = True  # True if you want to see pre-augmented examples
    if request.method == "GET":
        return render_template(
            "index.html",
            show_examples=show_examples,
            audio_spectrogram_paths=None,
            audio_file_paths=None,
            description_dict=description_dict,
        )


@app.route("/demos", methods=["GET", "POST"])
# @get_exectution_time
def demos():
    if request.method == "GET":
        return render_template("demos.html")

    if request.method == "POST":
        """
        These benchmarks may vary depending on server warmup time but threading definitely faster-

        Before threading -
        Total time to compute augmentations: 2.264
        Total time to process POST request: 2.546

        After threading-
        Total time to process POST request: 0.969
        Total time to compute fig object: 0.71
        Total time to compute augmentations: 0.253
        """
        start_post_request_time = time.perf_counter()

        # check is user has uploaded a file
        if "file" not in request.files:
            flash("No file part", "error")
            return redirect(request.url)

        # get the uploaded file
        uploaded_file = request.files["file"]

        # if user does not select file or submitted an empty part without filename
        if uploaded_file.filename == "":
            flash("No file selected!", "error")
            return redirect(request.url)

        if uploaded_file.content_type != "audio/wav":
            flash("Please upload .wav files")
            return redirect(request.url)

        client_uuid = str(uuid.uuid4())
        save_path = f"static/client_audio/{client_uuid}.wav"
        uploaded_file.save(save_path)

        # load the file and compute spectrogram
        wav, _ = librosa.load(f"static/client_audio/{client_uuid}.wav", sr=8000)
        # TODO - check this - is removing the path of any use
        os.remove(save_path)  # remove client audio after its processed

        # get augmented wavfiles as dict {'AugmentationName': WaveformData}
        start_aug_computation = time.perf_counter()
        augmentations_on_wav_dict = generate_augmentation_dict_from_wavfile(wav)
        time_to_compute_augs = round(
            time.perf_counter() - start_aug_computation, 3
        )  # approx 0.85 seconds

        start = time.perf_counter()
        augmented_imgs_dict = {}  # stores figure object from all augmentations
        os.makedirs(f"static/client_aug_wavs/{client_uuid}", exist_ok=True)

        # Threading for concurrent creation of figure objects from wavefiles
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # submit function returns a future object that encapsulates execution of the thread it is associated with
            results = [
                executor.submit(create_figure, augmentations_on_wav_dict[key], key)
                for key in augmentations_on_wav_dict.keys()
            ]

        # get the key and store results as dict {'AugmentationName': FigureObject}
        augment_wav_dict_keys = list(augmentations_on_wav_dict.keys())
        for idx, f in enumerate(concurrent.futures.as_completed(results)):
            # f is the future object encapsulates execution of the function - we can check if process is running, and
            # also get the results
            # f.result() is the return value of create_figure() function and returns -> ('AugmentationName', FigureObject)
            augmented_imgs_dict[f.result()[0]] = f.result()[1]

        # Threading to concurrently write client wavs to disk [IO bound]
        with concurrent.futures.ThreadPoolExecutor() as executor:
            [
                executor.submit(
                    write_wav,
                    augmentations_on_wav_dict,
                    client_uuid,
                    augment_wav_dict_keys[idx],
                )
                for idx in range(len(augment_wav_dict_keys))
            ]

        # delete directory and its contents after a certain time ? - Make it safe !!
        # shutil.rmtree(f'static/client_aug_wavs/{client_uuid}')

        time_to_compute_fig_object = round(time.perf_counter() - start, 3)

        # List of augmentation names to always display augmentations in the same order
        augment_wav_dict_keys = ["Un-Augmented"]
        for transform in augment.transforms:
            aug_name = str(transform).split(".")[-1].split(" ")[0]
            if aug_name == "Compose":
                aug_name = "TF Mask"
            augment_wav_dict_keys.append(aug_name)

        time_to_process_post_request = round(
            time.perf_counter() - start_post_request_time, 3
        )

        return render_template(
            "demos.html",
            augmented_imgs_dict=augmented_imgs_dict,
            description_dict=description_dict,  # description of each augmentation used in modal object. See `description.py`
            client_uuid=client_uuid,  # unique identifier for each client
            time_to_compute_fig_object=time_to_compute_fig_object,
            time_to_process_post_request=time_to_process_post_request,
            time_to_compute_augs=time_to_compute_augs,
            augment_wav_dict_keys=augment_wav_dict_keys,  # list of keys to display results in a consistent order
        )


# @get_exectution_time
def write_wav(augmentations_on_wav_dict, client_uuid, key):
    sf.write(
        f"static/client_aug_wavs/{client_uuid}/{key}.wav",
        augmentations_on_wav_dict[key],
        samplerate=8000,
    )


# @get_exectution_time
def create_figure(wav, key):
    """
    Generate figure object given waveform data
    wav - waveform data
    key - Name of the augmentation

    Returns -
    key - Name of the augmentation
    pngImageB64String - Figure object used for plotting
    """
    fig = Figure()

    axis = fig.add_subplot(1, 1, 1)
    axis.specgram(wav)

    axis.get_xaxis().set_visible(False)
    axis.get_yaxis().set_visible(False)
    axis.axis("off")  # this line removes extra white spaces
    fig.tight_layout(pad=0.0, w_pad=0.0, h_pad=1.0)
    fig.bbox_inches = "tight"

    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode("utf8")
    return (key, pngImageB64String)


# Augment wavefile
from audiomentations import (AddGaussianNoise, AddImpulseResponse,
                             AddShortNoises, Compose, FrequencyMask,
                             PitchShift, TimeMask, TimeStretch)

SAMPLE_RATE = 8000

augment = Compose(
    [
        AddGaussianNoise(min_amplitude=0.001, max_amplitude=0.015, p=1.0),
        AddShortNoises(
            "static/audio/plane_noise/",
            min_time_between_sounds=3.0,
            max_time_between_sounds=3.0,
            min_snr_in_db=0,
            max_snr_in_db=24,
            p=1,
        ),
        TimeMask(min_band_part=0.0, max_band_part=0.50, p=1),
        FrequencyMask(min_frequency_band=0.1, max_frequency_band=0.10, p=1),
        TimeStretch(0.9, 1.0, leave_length_unchanged=True, p=1),
        PitchShift(min_semitones=1, max_semitones=2, p=1),
    ]
)
augment_tf = Compose(
    [
        FrequencyMask(min_frequency_band=0.1, max_frequency_band=0.10, p=1),
        TimeMask(min_band_part=0.1, max_band_part=0.20, p=1, fade=True),
    ]
)
augment.transforms.append(augment_tf)


def generate_augmentation_dict_from_wavfile(wav):
    """
    returns -> {'AugNames': AugmentedWaveforms}
    """
    augmented_wavs_dict = {}
    augmented_wavs_dict["Un-Augmented"] = wav

    with concurrent.futures.ThreadPoolExecutor() as executor:
        augmented_wavs = [
            executor.submit(
                apply_augment_transform_to_waveform, augment.transforms[i], wav
            )
            for i in range(len(augment.transforms))
        ]
    for i, f in enumerate(concurrent.futures.as_completed(augmented_wavs)):
        augmented_wavs_dict[f.result()[0]] = f.result()[1]
    return augmented_wavs_dict


def apply_augment_transform_to_waveform(transform, wav, sample_rate=8000):
    """
    returns -> {'AugName': AugmentedWaveform }
    """
    AugName = str(transform).split(".")[-1].split(" ")[0]
    if AugName == "Compose":
        AugName = "TF Mask"
    return (AugName, transform(wav, sample_rate))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
