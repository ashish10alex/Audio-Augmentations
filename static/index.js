// Toogle between light and dark mode
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
  if (error_message_elem) {
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


// Modal click event in a loop
// Code from - https://stackoverflow.com/questions/8909652/adding-click-event-listeners-in-loop
// Summary -
// The below code uses closure which executes immediately, therefore preserving the state of the 
// variables at execution time. _td is the input parameter for the function which forms the closure and (bt)
// is the function being passed with the parameter bt
for (let j = 0; j < modals.length; j++) {
  bt = buttons[j]
  if (typeof window.addEventListener === 'function') {
    (function(_bt) {
      bt.addEventListener('click', () => {
        modals[j].style.display = 'block'
      });
    })
    (bt);
  }
}

for (let j = 0; j < modals.length; j++) {
  bt = closeButtons[j]
  if (typeof window.addEventListener === 'function') {
    (function(_bt) {
      bt.addEventListener('click', () => {
        modals[j].style.display = 'none'
      });
    })
    (bt);
  }
}


// Handle outside clicks 
window.addEventListener('click', (e) => {
  if (e.target == modals[0]) {
    modals[0].style.display = 'none'
  }

  // if(e.target == modals[1]){
  //     console.log('modal 2')
  //     modals[1].style.display='none'
  // }
})
