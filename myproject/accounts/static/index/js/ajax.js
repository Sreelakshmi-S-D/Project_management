

  $('#uploadImage').on('click', function(event) {
    event.preventDefault();
    $('#profileImageInput').click();
});

$('#profileImageInput').on('change', function() {
    uploadProfileImage();
});

function uploadProfileImage() {
    var formData = new FormData();
    // console.log(typeof formData)
    formData.append('profile_image', $('#profileImageInput')[0].files[0]);
    const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();  
    // console.log(formData)
    $.ajax({
        type: 'POST',
        url: '/edit_prof_pic/',
        data: formData,
        processData: false,
        contentType: false,
        headers: { 'X-CSRFToken': csrfToken }, 
        success: function(data) {
          // alert('hhh')
          // console.log('llpp',data)

            if (data.success) {
                updateProfileImage();
            }
        },
    });


    function updateProfileImage() {
    $.ajax({
        type: 'GET',
        url: '/view_prof_pic/',
        success: function(data) {
          // alert('looo')
            // $('#profileimg').attr('src', data.photo);
            $('#dpimg').attr('src', data.photo);
        },
    });
}

}

$('#removeImage').click(function(e) {
    e.preventDefault();
    const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();  

    $.ajax({
      type: 'POST',
      url: '/remove_prof_pic/',
      headers: { 'X-CSRFToken': csrfToken }, 
      success: function (data) {
        $('#dpimg').attr('src', '/static/Login/images/default_profile.jpg');
      },
      error: function (xhr, errmsg, err) {
      }
    });
  });

