/**
 *
 * Template : QyberHost HTML TEMPLATE
 * Author : reacthemes
 * Author URI : https://reactheme.com/ 
 *
 **/

// static/js/ajax.js
(function ($) {
    "use strict";
    $("#contact-form").submit(function (e) {
        e.preventDefault();
        let form = $(this);
        let formMessages = $("#form-messages");
        let formData = form.serialize();
        $.ajax({
            type: "POST",
            url: "/contact/",
            data: formData,
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", $('input[name=csrfmiddlewaretoken]').val());
            },
            success: function (response) {
                formMessages.removeClass("error").addClass("success").text(response.message);
                form.trigger("reset");
            },
            error: function (xhr) {
                let errors = xhr.responseJSON.errors;
                let errorMessage = "Oops! An error occurred.";
                if (errors) {
                    errorMessage = Object.values(errors).flat().join(" ");
                }
                formMessages.removeClass("success").addClass("error").text(errorMessage);
            }
        });
    });
})(jQuery);

