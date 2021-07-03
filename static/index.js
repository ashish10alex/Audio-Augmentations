//Nav bar 
const navSlide = () => {
  const burger = document.querySelector('.burger')
  const nav = document.querySelector('.nav-links')
  const navLinks = document.querySelectorAll('.nav-links li')

  // Toogle nav
  burger.addEventListener('click', () => {
    nav.classList.toggle('nav-active')
    navLinks.forEach((link, index) => {
      // Fade in the navbar content
      if (link.style.animation) {
        link.style.animation = ''
      } else {
        link.style.animation = `navLinksFade 0.5s ease forwards ${index / 5 + 0.2}s`
      }
    })

  //Burger animation
  burger.classList.toggle('toggle')
  });
}
navSlide()
// Will only work for the first image - fix this !!
// Find the correct css as well!!
// const imageBoxDiv =  document.getElementById('box')
const imageBoxDiv =  document.getElementsByClassName('box-dark')
const imageObject = document.getElementsByClassName('refs')[0]

// Function to create Info popup
const createInfoPopUp = (imageBoxDiv) => {
    isInfoPopup = 0 // Flag to check if a div with class name InfoPopup is already there

    // Check if the object has a class named Infopop
    for (var i = 0; i < imageBoxDiv.childNodes.length; i++) {
        if (imageBoxDiv.childNodes[i].className == 'infoPop') {
            console.log('Div InfoPop')
            isInfoPopup = 1
            imageBoxDiv.childNodes[i].textContent = "[Click to get info]"
        }        
    }

    // If a div named InfoPopup class is already not there 
    if (isInfoPopup == 0){
        console.log('Creating div cos no InfoPop')
        var node = document.createElement("div");   
        node.className = "infoPop"
        imageBoxDiv.appendChild(node)
        node.textContent = '[Click to get info]'
        imageBoxDiv.appendChild(node)
    }
}

// Function to remove Info popup
const removeInfoPopUp = (imageBoxDiv) => {
    for (var i = 0; i < imageBoxDiv.childNodes.length; i++) {
        if (imageBoxDiv.childNodes[i].className == 'infoPop') {
            imageBoxDiv.childNodes[i].innerText = ""
            console.log('Found InfoPop to remove')
        }        
    }
}


for (let j = 0; j < imageBoxDiv.length; j++) {
      imageBoxDiv[j].addEventListener('mouseenter', () => {
          createInfoPopUp(imageBoxDiv[j])
          console.log('Entered')
  })
}

for (let j = 0; j < imageBoxDiv.length; j++) {
      imageBoxDiv[j].addEventListener('mouseleave', () => {
        console.log('Exited')
        removeInfoPopUp(imageBoxDiv[j])
  })
}

// Change file name when uploading
// let file_input = document.getElementsByClassName('file-upload-input')[0];
// file_input.addEventListener("change", () => {
//   let upload_text = document.getElementsByClassName("drag-text")[0].children[0]
//   let error_message_elem = document.getElementsByClassName('error-para')[0]
//   if (error_message_elem) {
//     error_message_elem.remove()
//   }
//   upload_text.textContent = document.getElementsByClassName('file-upload-input')[0].files[0].name
// })



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
    (function (_bt) {
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
    (function (_bt) {
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

