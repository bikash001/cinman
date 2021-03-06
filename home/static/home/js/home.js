$(document).ready(function() {
	
	var ajaxCall = function() {
		var token = getCookie();
		$.ajax({
			method: 'POST',
			url: '/current_status',
			headers: {
				'X-CSRFToken': token
			},
			error: function(rsp) {
				$('.progress').addClass('hide');
				console.log('error');
				console.log(rsp);
			},
			success: function(rsp) {
				$('.progress').addClass('hide');
				console.log('success');
				console.log(rsp);
			},
		});
	};

	var getCookie = function() {
		var cookieValue = null;
	    if (document.cookie && document.cookie !== '') {
	        var cookies = document.cookie.split(';');
	        var name = "csrftoken";
	        for (var i = 0; i < cookies.length; i++) {
	            var cookie = $.trim(cookies[i]);
	            // Does this cookie string begin with the name we want?
	            if (cookie.substring(0, name.length + 1) === (name + '=')) {
	                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
	                break;
	            }
	        }
	    }
	    return cookieValue;
	};

	$('#refresh').click(function(){
		$('.progress').removeClass('hide');
		ajaxCall();
	});
});