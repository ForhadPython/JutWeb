$(document).ready(function(){
    var addToFavoriteList = $('.addToFavoriteList');

    addToFavoriteList.click(function(event){
        event.preventDefault();

        var courseId = addToFavoriteList.attr('course-id');
        var token = $("input[name=csrfmiddlewaretoken]").val();

        $.ajax({
            url: '/add-to-favorite/',
            method: 'POST',
            data: {
                course: courseId,
                csrfmiddlewaretoken: token
            },

            success: function(data){
                console.log("Success return", data)
            },

            error: function (data) {
                console.log("Error return", data);
            }
        });
    });

    var submitCourseReview = $('#submitCourseReview');

    submitCourseReview.submit(function(event){
        event.preventDefault();

        var serialized_data = submitCourseReview.serialize();

        $.ajax({
            url: '/review-course/',
            method: 'POST',
            data: serialized_data,

            success: function(data){
                console.log(data)
            },

            error: function (data) {
                console.log(data)
            }
        });
    });

    var submitInstructorReview = $('#submitInstructorReview');

    submitInstructorReview.submit(function(event){
        event.preventDefault();

        var serialized_data = submitInstructorReview.serialize();

        $.ajax({
            url: '/review-instructor/',
            method: 'POST',
            data: serialized_data,

            success: function(data){
                console.log(data)
            },

            error: function (data) {
                console.log(data)
            }
        });
    });

    var bookEventSeat = $('#bookEventSeat');

    bookEventSeat.click(function(event){
        event.preventDefault();

        var eventId = bookEventSeat.attr('event-id');
        var userId = bookEventSeat.attr('user-id');
        var token = $("input[name=csrfmiddlewaretoken]").val();

        $.ajax({
            url: '/book-event-seat/',
            method: 'POST',
            data: {
                event_id: eventId,
                user_id: userId,
                csrfmiddlewaretoken: token
            },

            success: function(data){
                console.log("Success return", data)
                if (data.status == 'success') {
                    window.location.href = '/events/'
                }
            },

            error: function (data) {
                console.log("Error return", data);
            }
        });
    });

    var enrollToTheCourse = $('#enrollToTheCourse');

    enrollToTheCourse.click(function(event){
        event.preventDefault();

        var courseId = enrollToTheCourse.attr('course-id');
        var userId = enrollToTheCourse.attr('user-id');
        var token = $("input[name=csrfmiddlewaretoken]").val();

        // window.location.href = "/accounts/login/?time=first";

        $.ajax({
            url: '/enroll-to-the-course/',
            method: 'POST',
            data: {
                course_id: courseId,
                student_id: userId,
                csrfmiddlewaretoken: token
            },

            success: function(data){
                console.log("Success return", data);
                window.location.href = "/payment-guideline/";
            },

            error: function (data) {
                console.log("Error return", data);
            }
        });
    });

    var createUserForm = $('#createUserForm');

    createUserForm.submit(function(event){
        event.preventDefault();

        var serialized_data = createUserForm.serialize();

        $.ajax({
            url: '/users/create/',
            method: 'POST',
            data: serialized_data,

            success: function(data){
                console.log('success', data)
                if (data.status == 'success') {
                    $('#signupUpdate').html('Please confirm your email address to get started.')
                } else {
                    console.log('error', data)
                }
            },
            error: function (data) {
                console.log('error', data)
            }
        });
    });

    var loginUserForm = $('#loginUserForm');

    loginUserForm.submit(function(event){
        event.preventDefault();

        var serialized_data = loginUserForm.serialize();

        $.ajax({
            url: '/users/login/',
            method: 'POST',
            data: serialized_data,

            success: function(data){
                console.log('success', data)
                if (data.status == 'success') {
                    window.location.href = "/"
                } else {
                    console.log('error', data)
                }
            },
            error: function (data) {
                console.log('error', data)
            }
        });
    });
});