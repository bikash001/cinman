$(document).ready(function() {
	
	var urls = ['/home/','/home/messages/','/home/notifications/','/home/systemstats/']
	
	var ajaxCall = function(arg) {
		var token = getCookie();
		$.ajax({
			method: 'POST',
			url: urls[arg],
			headers: {
				'X-CSRFToken': token
			},
			error: function(rsp) {
				console.log('error');
				console.log(rsp);
			},
			success: function(rsp) {
				// console.log('success');
				// console.log(rsp)
				if (rsp.type === 'message') {
					console.log($('#content'));
					$('#content').empty().append('<div class="vertical-menu"></>');
					console.log(rsp.size);
					for (var i=0; i<rsp.size; i++) {
						console.log('insize', $('.vertical-menu'));
						$('.vertical-menu').append('<a class="pointer msg" id="msg-"'+rsp.data[i].id+' >'+rsp.data[i].ip+'</a>');
					}
				} else if (rsp.type === 'stats') {

				}
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

	var changeUI = function(context, urlid) {
		var obj = $('ul.nav > li.active');
		if (obj.get(0).id !== $(context).get(0).id) {
			obj.removeClass('active');
			$(context).addClass('active');
			$('#content').empty();
			ajaxCall(urlid);
		}
	};

	$('#home').click(function(){
		// console.log(getCookies());
		changeUI(this,0);
	});

	$('#message').click(function(){
		changeUI(this,1);
	});

	$('#notification').click(function(){
		changeUI(this,2);
	});	

	$('#status').click(function(){
		changeUI(this,3);
	});
});