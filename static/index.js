let dark_mode_button = document.getElementById('dark-mode-button')
dark_mode_button.addEventListener('click', () => {
  ToogleDarkLightMode()
})

function ToogleDarkLightMode() {

  // add here to change header div background color
  let header_element = document.getElementsByClassName('header')


  let box_element = document.querySelectorAll('#box')
  box_element.forEach(e => {
    // debugger
    if (e.className == 'box-light') { e.className = 'box-dark' }
    else { e.className = 'box-light' }
  })
  let body_element = document.body;
  body_element.classList.toggle("dark-mode");
}

// Change file name when uploading
let file_input = document.getElementsByClassName('file-upload-input')[0];
file_input.addEventListener("change", () => {
  let upload_text = document.getElementsByClassName("drag-text")[0].children[0]
  let error_message_elem = document.getElementsByClassName('error-para')[0]
  if (error_message_elem){
    error_message_elem.remove()
  }
  upload_text.textContent = document.getElementsByClassName('file-upload-input')[0].files[0].name
})



//Modals
let modals = document.getElementsByClassName('modal')
// get the button elements by class name
let buttons = document.getElementsByClassName('refs')
// get the close buttons by class name
let closeButtons = document.getElementsByClassName('closeBtn')


buttons[0].addEventListener('click', () => {
    modals[0].style.display ='block'
})

 buttons[1].addEventListener('click', () => {
   console.log('click')
     modals[1].style.display ='block'
 })

closeButtons[0].addEventListener('click', () => {
    modals[0].style.display = 'none'
})

closeButtons[1].addEventListener('click', () => {
    modals[1].style.display = 'none'
})


// closeButtons[1].addEventListener('click', () => {
//     modals[1].style.display = 'none'
// })



window.addEventListener('click', (e) => {
    if(e.target == modals[0]){
        modals[0].style.display ='none'
    }

    // if(e.target == modals[1]){
    //     console.log('modal 2')
    //     modals[1].style.display='none'
    // }
})
