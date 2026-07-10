/* ============================================================
   UNDERTONE — upload.js
   Handles the dropzone: click-to-browse, drag-and-drop, live
   image preview, and the message character counter. Pure DOM,
   no frameworks — the actual encode logic lives server-side.
   ============================================================ */
(function () {
  var dropzone = document.getElementById('dropzone');
  var input = document.getElementById('image-input');
  var preview = document.getElementById('dropzone-preview');
  var filenameEl = document.getElementById('dropzone-filename');
  var messageInput = document.getElementById('message-input');
  var charCount = document.getElementById('char-count');

  if (dropzone && input) {
    ['dragenter', 'dragover'].forEach(function (evt) {
      dropzone.addEventListener(evt, function (e) {
        e.preventDefault();
        dropzone.classList.add('is-dragover');
      });
    });

    ['dragleave', 'drop'].forEach(function (evt) {
      dropzone.addEventListener(evt, function (e) {
        e.preventDefault();
        dropzone.classList.remove('is-dragover');
      });
    });

    dropzone.addEventListener('drop', function (e) {
      var files = e.dataTransfer.files;
      if (files && files.length) {
        input.files = files;
        showPreview(files[0]);
      }
    });

    input.addEventListener('change', function () {
      if (input.files && input.files[0]) {
        showPreview(input.files[0]);
      }
    });
  }

  function showPreview(file) {
    if (!file.type.startsWith('image/')) return;
    var reader = new FileReader();
    reader.onload = function (e) {
      preview.src = e.target.result;
      filenameEl.textContent = file.name;
      dropzone.classList.add('has-image');
    };
    reader.readAsDataURL(file);
  }

  if (messageInput && charCount) {
    messageInput.addEventListener('input', function () {
      charCount.textContent = messageInput.value.length;
    });
  }
})();
