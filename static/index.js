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

