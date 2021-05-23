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
    if request.method == 'POST':
        
        #get the uploaded file and save to static folder
        uploaded_file = request.files['file']
        save_path = 'static/audio/test.wav'
        uploaded_file.save(save_path)
        
        #load the file and compute spectrogram
        wav, _ = librosa.load('static/audio/test.wav', sr=8000)
        fig = create_figure(wav)
        pngImage = io.BytesIO()
        FigureCanvas(fig).print_png(pngImage)
        pngImageB64String = "data:image/png;base64,"
        pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
        return render_template('index.html', image=pngImageB64String)

    if request.method == 'GET':
        return render_template("index.html")

def create_figure(wav):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.specgram(wav)
    axis.set_xticks([])
    axis.set_yticks([])
    return fig


if __name__ == "__main__":
    app.run(debug=True)
