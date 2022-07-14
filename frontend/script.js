const form = document.querySelector('form')
form.addEventListener('submit', event => {
    // submit event detected
    event.preventDefault()
    event.stopPropagation(); 
    previewFile()
    predict()
})

function previewFile() {
    var preview_org = document.getElementById('preview_org');
    var file_org = document.getElementById('original_img').files[0];
    var preview_mask = document.getElementById('preview_mask');
    var file_mask = document.getElementById('mask_img').files[0];
    preview_org.src = URL.createObjectURL(file_org);
    preview_org.onload = function () {
        URL.revokeObjectURL(preview_org.src)
        preview_org.style.display = 'block';
    }
    preview_mask.src = URL.createObjectURL(file_mask);
    preview_mask.onload = function () {
        URL.revokeObjectURL(preview_mask.src)
        preview_mask.style.display = 'block';
    }
}

function predict() {
    var file_org = document.getElementById('original_img').files[0];
    var file_mask = document.getElementById('mask_img').files[0];

    const formData = new FormData();

    formData.append('img', file_org);
    formData.append('mask', file_mask);

    // const options = {
    //     method: 'POST',
    //     body: formData
    // };
    // fetch('http://127.0.0.1:5000/predict', options
    // ).then(
    //     response => response.json() // if the response is a JSON object
    // ).then(
    //     success => {
    //         console.log(success)
    //     }
    // ).catch(
    //     error => console.log(error) // Handle the error response object
    // );
    $.ajax({
        url: "http://127.0.0.1:5000/predict",
        data: formData,
        processData: false,
        contentType: false,
        type: 'POST',
        success: function (data, status) {
            // alert("Data: " + data + "\nStatus: " + status);
            masked = data.result[0]
            predicted = data.result[1]
            var preview_masked = document.getElementById('preview_masked');
            preview_masked.src = 'data:image/png;base64,'+masked
            preview_masked.style.display = 'block';
            var preview_predicted = document.getElementById('preview_predicted');
            preview_predicted.src = 'data:image/png;base64,'+predicted
            preview_predicted.style.display = 'block';
        }
    });
}

function main() {
    var preview_org = document.getElementById('preview_org');
    preview_org.style.display = 'none';
    var preview_mask = document.getElementById('preview_mask');
    preview_mask.style.display = 'none';
    var preview_masked = document.getElementById('preview_masked');
    preview_masked.style.display = 'none';
    var preview_predicted = document.getElementById('preview_predicted');
    preview_predicted.style.display = 'none';
}

main()