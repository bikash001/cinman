$(document).ready(function() {
	
	var urls = ['/delete_msg']
	
	var ajaxCall = function(id) {
		var token = getCookie();
		console.log('id', id);
		$.ajax({
			method: 'POST',
			url: urls[0],
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

	$('.btn-danger').click(function(){
		var id = this.id.split('-')[1];
		ajaxCall(id);
		$('#msgbox-'+id).remove();
		if ($('.vertical-menu2').get(0).children.length <= 0) {
			$('.vertical-menu2').append('<div style="background-color: white; border-radius: 5px; padding: 10px;">\
                    <div class="text-center" style="padding: 15px;">\
                        No More Message\
                    </div>\
                </div>');
		}
	});
});