// function to copy password
function dispPassword(id) {
    inputId = '#password' + id
    btnId = '#eye' + id
    eyeBtnId = '#eyeBtn' + id
    // inputField = $(id).val()
    type = $(inputId).attr('type')
    if (type == 'password') {
        $(inputId).attr('type', 'text')
        $(btnId).attr('class', 'bi bi-eye-slash')
        $(eyeBtnId).attr('class', 'btn btn-sm btn-warning')
    }
    else {
        $(inputId).attr('type', 'password')
        $(btnId).attr('class', 'bi bi-eye')
        $(eyeBtnId).attr('class', 'btn btn-sm btn-primary')
    }
}

// function to copy password
function copyPassword(id) {
    inputId = 'password' + id
    $('#'+inputId).attr('type', 'text')
    var copyText = document.getElementById(inputId);
    copyText.select();
    copyText.setSelectionRange(0, 99999)
    var success = document.execCommand("copy");
    $('#'+inputId).attr('type', 'password')
}

// function to get data of credential which needs to be updated
$('#editCredentialModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget) // Button that triggered the modal
    var credentialId = button.data('id') // Extract info from data-* attributes
    var index = button.data('index') // Extract info from data-* attributes
    // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
    // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
    var credentialUrl = document.getElementById('spanCredentialUrl'+index).innerText
    var credentialName = document.getElementById('spanCredentialName'+index).innerText
    var credentialUsername = document.getElementById('spanCredentialUsername'+index).innerText
    $('#password'+index).attr('type', 'text')
    var credentialPassword = document.getElementById('password'+index).value
    $('#password'+index).attr('type', 'password')
    var modal = $(this)
    modal.find('#editCredentialId').val(credentialId)
    modal.find('#editUrl').val(credentialUrl)
    modal.find('#editName').val(credentialName)
    modal.find('#editUsername').val(credentialUsername)
    modal.find('#editPassword').val(credentialPassword)
})

// add class to pagination code
$( document ).ready(function() {
    var pagination = $('.pagination')
    pagination.find('ul').attr('class', 'pagination');
    pagination.find('li').attr('class', 'page-item');
    pagination.find('a').attr('class', 'page-link');
    
    // fix search bar not occupying full table width 
    var fancyTableSearch = $(".fancySearchRow")
    fancyTableSearch.find('th').attr('colspan', 5);
});

// fancytable js
$(".fancy-table").fancyTable({
sortColumn:0, // column number for initial sorting
sortOrder: 'ascending', // 'desc', 'descending', 'asc', 'ascending', -1 (descending) and 1 (ascending)
sortable: true,
pagination: false, // default: false
searchable: true,
globalSearch: true,
// globalSearchExcludeColumns: [2,5] // exclude column 2 & 5
});
