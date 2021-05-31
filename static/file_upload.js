
let file_input = document.getElementsByClassName('file-upload-input')[0];
file_input.addEventListener("change", () => {
  let upload_text = document.getElementsByClassName("drag-text")[0].children[0]
  let error_message_elem = document.getElementsByClassName('error-para')[0]
  if (error_message_elem) {
    error_message_elem.remove()
  }
  upload_text.textContent = document.getElementsByClassName('file-upload-input')[0].files[0].name
})


