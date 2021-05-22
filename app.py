from flask import Flask
from flask import request 
import soundfile as sf
from flask import render_template
from flask import send_from_directory

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello_world(name=''):
    if request.method == 'POST':
        return '<h2> Post method was called </h2>'

    if request.method == 'GET':
        #audio_path ='/Users/ashishalex/Documents/research/tests/MiniLibriMix/val/s1/8842-304647-0004_6319-64726-0000.wav'
        #x, _ = sf.read(audio_path, )
        #return 'Hello, World! wav shape: {}'.format(x.shape)
        return render_template('index.html', name=name)

if __name__ == "__main__":
    app.run(debug=True)
