# Audio-Augmentations
A website to display audio and its spectrogram when an augmentation/operation is applied to the audio. Additionally it allowes users to augment their own audio file  

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

### To do 

- [x] Use threads / async to load multiple augmented files - see `async_example.py`
  - [x] Approximately 1 second faster(2.54 to 1.758secs) from using threading `figure object` computation)
  - [x] Multiprocessing to compute augmentations (Doesn't seem to work as well as threading)
- [ ] Delete uuid client augmentation folder after certain time
- [ ] Why Post request gets resubmitted with same data bug
- [ ] Add pop up for all Augmentations 
  - [x] Add basic pop up
  - [ ] Flickering issue due to grid resizing? - Maybe hard code `InfoPopUp` div in `index.html`

- [ ] JavaScript for loop modal click event
  - [x] Basic functionality - Added using closures (complex ? )
  - [ ] Close pop up on outside click 
- [ ] Grid css mobile 

External libraries used

- [ ] For latex support in pop ups was support by - https://katex.org/
