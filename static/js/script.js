let state = 0;
function textToggle(id) {
  if (
    document.getElementById(id).innerHTML ===
    '<i class="bi bi-arrow-up-square-fill"></i>'
  )
    state = 0;
  else if (
    document.getElementById(id).innerHTML ===
    '<i class="bi bi-arrow-down-square-fill"></i>'
  )
    state = 1;
  state++;
  if (state > 1) {
    state = 0;
  } else if (state < 0) {
    state = 0;
  }
  switch (state) {
    case 0:
      document.getElementById(id).innerHTML =
        '<i class="bi bi-arrow-up-square-fill"></i>';
      break;
    case 1:
      document.getElementById(id).innerHTML =
        '<i class="bi bi-arrow-down-square-fill"></i>';
      break;
  }
}

document.addEventListener("DOMContentLoaded", function () {
  const fileInput = document.getElementById("fileInput");
  fileInput.addEventListener("change", previewImage);
});

function previewImage(event) {
  const input = event.target;
  const reader = new FileReader();

  reader.onload = function () {
    const img = document.getElementById("previewImage");
    img.src = reader.result;
  };

  reader.readAsDataURL(input.files[0]);
}
