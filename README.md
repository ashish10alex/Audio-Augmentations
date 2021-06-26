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
For complete deployment guide on an AWS ubntu instance see [Link](https://github.com/ashish10alex/system-setup/blob/main/Ubuntu-aws.md) 


and go to your web browser (e.g chrome/safari): <dl> <link> `localhost:5000` </link> </dl>

To do 

- [ ] Use threads / async to load multiple augmented files - see `async_example.py`
  - [x] Aprroximately 1 second faster(2.54 to 1.758secs) from using threading `figure object` computation)
  - [ ] Multiprocessing to compute augmentations (Currenly ~ 0.8secs to compute 7 augmentations)
- [ ] Delete uuid client aug folder after certain time
- [ ] Post request gets resubmitted with same data bug
- [ ] Add pop up for all Augmentations 
  - [ ] Load text from separate file from server side

- [ ] Javascript for loop modal click event
  - [x] Basic functionality - Added using closures (complex ? )
  - [ ] Close pop up on outside click 
- [ ] Grid css mobile 

External libraries used

- [ ] For latex support in pop ups was support by - https://katex.org/
