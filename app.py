import time
from flask import Flask
import os
from flask import request
from flask.helpers import url_for 
import soundfile as sf
from flask import render_template, redirect, flash
import librosa
import base64
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from descriptions import description_dict

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
#max upload size of 30Mb
app.config['MAX_CONTENT_LENGTH'] = 30 * 1000 * 1000


@app.route('/', methods=['GET'])
def index():
    show_examples = True #True if you want to see pre-augmented examples
    if request.method == 'GET':
        # audio_file_paths = []
        # audio_spectrogram_paths = []
        # for file in os.listdir('static/audio'):
        #     if file.endswith(".wav"):
        #         audio_file_paths.append('static/audio/{}'.format(file))
       
        # for file in os.listdir('static/images'):
        #     if file.endswith(".png"):
        #         audio_spectrogram_paths.append('static/images/{}'.format(file))
        # print(audio_spectrogram_paths)
        # print(audio_file_paths)
        return render_template("index.html", show_examples=show_examples, audio_spectrogram_paths=None, audio_file_paths=None, description_dict=description_dict)


@app.route('/demos', methods=['GET', 'POST'])
def demos():
    if request.method == 'GET':
        return render_template('demos.html')

    if request.method == 'POST':

        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)

        #get the uploaded file and save to static folder
        uploaded_file = request.files['file']

        # if user does not select file, browser also
        # submit an empty part without filename
        if uploaded_file.filename == '':
            flash('No file selected!', "error")
            return redirect(request.url)
        
        if uploaded_file.content_type != 'audio/wav':
            flash('Please upload .wav files')
            return redirect(request.url)

        save_path = 'static/audio/test.wav'
        uploaded_file.save(save_path)
        
        #load the file and compute spectrogram
        wav, _ = librosa.load('static/audio/test.wav', sr=8000)

        #get augmented wavfiles as dict {'AugName': wav_data}
        #Less than 1.0 second to compute 8 augmentations
        #Less than 0.5 sec to process after warmup
        #Not the bottle neck
        augment_wavs_dict = augment_wav(wav)

        # create_figure function takes ~ 1.8 secs - needs to be async ?  
        # How to implement async in for loop ?  
        start = time.time()
        #get image object and save augmented audio for playing on website
        aug_imgs_dict = {}
        for key in augment_wavs_dict.keys():
            aug_imgs_dict[key] = create_figure(augment_wavs_dict[key])
            sf.write('static/audio/client_aug_wavs/{}.wav'.format(key), augment_wavs_dict[key], samplerate=8000)

        total_time = time.time() - start
        print('total_time: ', total_time)

        return render_template('demos.html', images=aug_imgs_dict, description_dict=description_dict)
        # return render_template(url_for('demos', images=aug_imgs_dict,  description_dict=description_dict))
        #return render_template(url_for('demos',  description_dict=description_dict))



def create_figure(wav):
    fig = Figure()
    
    axis = fig.add_subplot(1, 1, 1)
    axis.specgram(wav)
    
    #tricks to make the plots look clearner - removing white space (needs more work)
    # axis.set_xticks([])
    # axis.set_yticks([])
    axis.get_xaxis().set_visible(False)
    axis.get_yaxis().set_visible(False)
    axis.axis('off') # this line removes extra white spaces
    fig.tight_layout(pad=0.0, w_pad=0.0, h_pad=1.0)
    fig.bbox_inches='tight'
    
    
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
AddGaussianNoise(min_amplitude=0.001, max_amplitude=0.015, p=1.0),
AddShortNoises('static/audio/plane_noise/',
                min_time_between_sounds=3.0,
                max_time_between_sounds=3.0,
                min_snr_in_db=0,
                max_snr_in_db=24,
                p=1
              ),
TimeMask(min_band_part=0.0, max_band_part=0.50, p=1),
FrequencyMask(min_frequency_band=0.1, max_frequency_band=0.10, p=1),
TimeStretch(0.9, 1.0, leave_length_unchanged=True,  p=1),
PitchShift(min_semitones=1, max_semitones=2, p=1), 
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
    return augmented_wavs_dict 


if __name__ == "__main__":
    app.run(debug=True)
