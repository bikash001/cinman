$(document).ready(function() {
	
	var urls = ['/approve_user','/decline_user', '/delete_pp']
	
	var ajaxCall = function(arg, id) {
		var token = getCookie();
		console.log('id', id);
		$.ajax({
			method: 'POST',
			url: urls[arg],
			data: {
				'id': id
			},
			headers: {
				'X-CSRFToken': token
			},
			error: function(rsp) {
				console.log('error');
				console.log(rsp);
			},
			success: function(rsp) {
				console.log('success');
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

	$('.btn-success').click(function(){
		var id = this.id.split('-')[1];
		ajaxCall(0,id);
		$('#reg-'+id).remove();
	});

	$('.userreg').click(function(){
		var id = this.id.split('-')[1];
		ajaxCall(1,id);
		$('#reg-'+id).remove();
	});
	$('.ppp').click(function(){
		var id = this.id.split('-')[1];
		ajaxCall(2,id);
		$('#ppp-'+id).remove();
	});
});