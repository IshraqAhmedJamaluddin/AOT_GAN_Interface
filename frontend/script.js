const form1 = document.querySelector('#form1')
form1.addEventListener('submit', event => {
    // submit event detected
    event.preventDefault()
    event.stopPropagation(); 
    previewFile()
    predict()
})

const form2 = document.querySelector('#form2')
form2.addEventListener('submit', event => {
    // submit event detected
    event.preventDefault()
    event.stopPropagation(); 
    previewFile_k()
    predict_k()
})

function previewFile() {
    var org_parent = document.getElementById('preview_org');
    var preview_org = org_parent.lastElementChild;
    var file_org = document.getElementById('original_img').files[0];
    var mask_parent = document.getElementById('preview_mask');
    var preview_mask = mask_parent.lastElementChild;
    var file_mask = document.getElementById('mask_img').files[0];
    preview_org.src = URL.createObjectURL(file_org);
    preview_org.onload = function () {
        URL.revokeObjectURL(preview_org.src)
        org_parent.style.display = 'block';
    }
    preview_mask.src = URL.createObjectURL(file_mask);
    preview_mask.onload = function () {
        URL.revokeObjectURL(preview_mask.src)
        mask_parent.style.display = 'block';
    }
    var preview_masked = document.getElementById('preview_masked');
    preview_masked.style.display = 'none';
    var preview_predicted = document.getElementById('preview_predicted');
    preview_predicted.style.display = 'none';
    var loading = document.getElementById('loading');
    loading.style.display = 'block';
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
            preview_masked.lastElementChild.src = 'data:image/png;base64,'+masked
            preview_masked.style.display = 'block';
            var preview_predicted = document.getElementById('preview_predicted');
            preview_predicted.lastElementChild.src = 'data:image/png;base64,'+predicted
            preview_predicted.style.display = 'block';
            var loading = document.getElementById('loading');
            loading.style.display = 'none';
        }
    });
}

function previewFile_k() {
    var org_parent = document.getElementById('preview_org_k');
    var preview_org = org_parent.lastElementChild;
    var file_org = document.getElementById('original_img_k').files[0];
    preview_org.src = URL.createObjectURL(file_org);
    preview_org.onload = function () {
        URL.revokeObjectURL(preview_org.src)
        org_parent.style.display = 'block';
    }
    var preview_predicted_k = document.getElementById('preview_predicted_k');
    preview_predicted_k.style.display = 'none';
    var loading_k = document.getElementById('loading_k');
    loading_k.style.display = 'block';
}

function predict_k() {
    var file_org = document.getElementById('original_img_k').files[0];
    var button = document.querySelector('input[name="AB"]:checked').value;

    const formData = new FormData();

    formData.append('img', file_org);
    formData.append('choice', button)

    $.ajax({
        url: "http://127.0.0.1:5000/predictk",
        data: formData,
        processData: false,
        contentType: false,
        type: 'POST',
        success: function (data, status) {
            // alert("Data: " + data + "\nStatus: " + status);
            predicted = data.result
            var preview_predicted_k = document.getElementById('preview_predicted_k');
            preview_predicted_k.lastElementChild.src = 'data:image/png;base64,'+predicted
            preview_predicted_k.style.display = 'block';
            var loading_k = document.getElementById('loading_k');
            loading_k.style.display = 'none';
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
    var preview_org_k = document.getElementById('preview_org_k');
    preview_org_k.style.display = 'none';
    var preview_predicted_k = document.getElementById('preview_predicted_k');
    preview_predicted_k.style.display = 'none';
    var loading = document.getElementById('loading');
    loading.style.display = 'none';
    var loading_k = document.getElementById('loading_k');
    loading_k.style.display = 'none';
}

main()