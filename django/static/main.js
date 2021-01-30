var Swal;
var Toast;

var SetPreventDubleClick = function () {
    $("button").on('mouseup', function (e) {
        var _btn = $(this);
        setTimeout(function () {
            _btn.prop('disabled', true);
        });

        setTimeout(function () {
            _btn.prop('disabled', false);
        }, 1500);
    });
}
var SetDefaultSweetAlert = function () {
    return Swal.mixin({
        allowOutsideClick: false,
        closeOnClickOutside: false,
    });
}
var SetToastSweetAlert = function() {
    return Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
        didOpen: function(toast)  {
            toast.addEventListener('mouseenter', Swal.stopTimer)
            toast.addEventListener('mouseleave', Swal.resumeTimer)
        }
    });
}
var ShowLoading = function(_show) {
    if (_show == true) {
        Swal.fire({
            title: '',
            html: '&nbsp;&nbsp;&nbsp;&nbsp;Loading ...',
            timerProgressBar: true,
            allowOutsideClick: false,
            showConfirmButton : false,
            onBeforeOpen: function () {
                Swal.showLoading();
            }
        });
    }
    else {
        setTimeout(function () {
            Swal.close();
        }, 100);
    }
}

$(function () {
    SetPreventDubleClick();
    Swal  = SetDefaultSweetAlert();
    Toast = SetToastSweetAlert();
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

var app = angular.module('myApp', []);
app.config(['$httpProvider','$interpolateProvider', function($httpProvider, $interpolateProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
}]);

$.widget.bridge('uibutton', $.ui.button)