from flask import Flask
from flask import request 
import soundfile as sf
from flask import render_template
import librosa
import base64
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    show_examples = True #True if you want to see pre-augmented examples
    if request.method == 'POST':
        show_examples=False
        #get the uploaded file and save to static folder
        uploaded_file = request.files['file']
        save_path = 'static/audio/test.wav'
        uploaded_file.save(save_path)
        
        #load the file and compute spectrogram
        wav, _ = librosa.load('static/audio/test.wav', sr=8000)

        #get augmented wavfiles as dict {'AugName': wav_data}
        augment_wavs_dict = augment_wav(wav)

        #get image object and save augmented audio for playing on website
        aug_imgs_dict = {}
        for key in augment_wavs_dict.keys():
            aug_imgs_dict[key] = create_figure(augment_wavs_dict[key])
            sf.write('static/audio/client_aug_wavs/{}.wav'.format(key), augment_wavs_dict[key], samplerate=8000)

        return render_template('index.html', images=aug_imgs_dict, show_examples=show_examples)

    if request.method == 'GET':
        return render_template("index.html", show_examples=show_examples)

def create_figure(wav):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.specgram(wav)
    axis.set_xticks([])
    axis.set_yticks([])
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    return pngImageB64String


# Augment wavefile
from audiomentations import Compose, AddGaussianNoise, TimeStretch, PitchShift, Shift,\
FrequencyMask, TimeMask, AddShortNoises, AddImpulseResponse

SAMPLE_RATE = 8000

augment = Compose([
AddShortNoises('/Users/ashishalex/Desktop/plane_noise/',
                min_time_between_sounds=3.0,
                max_time_between_sounds=3.0,
                min_snr_in_db=0,
                max_snr_in_db=24,
                p=1
              ),
AddGaussianNoise(min_amplitude=0.001, max_amplitude=0.015, p=1.0),
TimeStretch(0.9, 1.0, leave_length_unchanged=True,  p=1),
PitchShift(min_semitones=1, max_semitones=2, p=1), 
FrequencyMask(min_frequency_band=0.1, max_frequency_band=0.10, p=1),
TimeMask(min_band_part=0.0, max_band_part=0.50, p=1),
])

augment_tf = Compose([
FrequencyMask(min_frequency_band=0.1, max_frequency_band=0.10, p=1),
TimeMask(min_band_part=0.1, max_band_part=0.20, p=1, fade=True),
])

def augment_wav(wav):
    augmented_wavs_dict = {}
    augmented_wavs_dict['Un-Augmented'] = wav
    for i in range(len(augment.transforms)):
        augmented_wavs_dict[str(augment.transforms[i]).split('.')[-1].split(' ')[0]] = \
        augment.transforms[i](samples=wav, sample_rate=8000)
    
    tf_wav = augment_tf(wav, sample_rate=8000)
    augmented_wavs_dict['TF Mask'] = tf_wav
    print(augmented_wavs_dict.keys())
    return augmented_wavs_dict 





if __name__ == "__main__":
    app.run(debug=True)
