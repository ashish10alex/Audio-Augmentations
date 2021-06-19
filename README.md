# box-play
A simple website to display audio and its spectrogram when an augmentation/operation is applied to the audio.  

To run the web app -

```
python3 -m venv . 
source bin/activate
pip3 install -r requirements.txt

python3 app.py

#Or to run on local network 
#change host parameter in app.run followed by 

flask run -h 192.168.X.X
```

Ubuntu installation caveats
```
sudo apt-get install libsndfile1
```


and go to your web browser (e.g chrome/safari): <dl> <link> `localhost:5000` </link> </dl>

To do 

- [ ] Javascript error handling on submit 
- [ ] Multiple post requests ('test.wav' to scaleable)
- [ ] Grid css mobile 
- [ ] Add pop up for all Augmentations 
  - [ ] Load text from separate file from server side

- [ ] Javascript for loop modal click event
  - [x] Basic functionality - Added using closures (complex ? )
  - [ ] Close pop up on outside click 
- [ ] Load examples dynamically with Jinja for loop
- [ ] Use threads / async to load multiple augmented files - see `async_example.py`
- [ ] ENV variables for secret key

Documentation

- [ ] For latex support in pop ups was support by - https://katex.org/
