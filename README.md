# box-play
A simple website to display audio and its spectrogram when an augmentation/operation is applied to the audio.  

To run the web app -

```
python3 app.py
```
and go to your web browser (e.g chrome/safari): <dl> <link> localhost:5000 </link> </dl>

To do 

- [x] Better file uploader  
- [x] Check if uploaded file is audio and do error handling
- [ ] Add pop up for all Augmentations - Load text from separate file from server side. 
- [ ] Split into multiple files
- [ ] Add Navbar
- [ ] Load examples dynamically with Jinja for loop
- [ ] Remove border from client audio plots
- [ ] Use threads / async to load multiple augmented files - 
    >  https://www.youtube.com/watch?v=tdIIJuPh3SI&t=5070s
    
    >  https://flask.palletsprojects.com/en/2.0.x/async-await/
- [ ] ENV variables for secret key

Documentation

- [ ] For latex support in pop ups was support by - https://katex.org/
