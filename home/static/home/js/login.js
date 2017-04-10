$(document).ready(function() {
	
	var urls = ['/validateUser/','/register/','/forgot_pwd/']
	
	var ajaxCall = function(vals,index) {
		var token = getCookie();
		console.log(token);
		$.ajax({
			method: 'POST',
			url: urls[index],
			data: vals,
			headers: {
				'X-CSRFToken': token
			},
			error: function(rsp) {
				console.log('error');
				console.log(rsp);
			},
			success: function(rsp) {
				console.log('success');
				console.log(rsp)
				window.location.reload();
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
	            
	            if (cookie.substring(0, name.length + 1) === (name + '=')) {
	                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
	                break;
	            }
	        }
	    }
	    return cookieValue;
	};

	$('#loginbtn').click(function(){
		var empty = false;
		var vals = {}
		$('.login').find('input').each(function() {
			if (this.value == '') {
				empty = true;
			} else {
				vals[this.name] = this.value;
			}
		});
		if (empty) {
			$('#errmsg').removeClass('hide');
		} else {
			ajaxCall(vals,0);
		}
	});

	$('#login-registerbtn').click(function(){
		$('.login').addClass('hide');
		$('.signup').removeClass('hide');
	});

	$('#login-forgotbtn').click(function(){
		$('.login').addClass('hide');
		$('.forgot').removeClass('hide');
	});

	$('#signinbtn').click(function(){
		$('.signup').addClass('hide');
		$('.login').removeClass('hide');
	});

	$('#forgot-submitbtn').click(function(){
		var empty = false;
		var vals = {}
		var passwd, cpasswd;
		$('.forgot').find('input').each(function() {
			if (this.value == '') {
				empty = true;
			} else {
				vals[this.name] = this.value;
			}
		});
		if (empty) {
			$('#errmsg_2').removeClass('hide').html("Fields can't be empty.");
		} else if (vals['passwd'] !== vals['cpasswd']) {
			$('#errmsg_2').removeClass('hide').html("Password didn't match.")
		} else {
			ajaxCall(vals,2);
		}
	});

	$('#signupbtn').click(function(){
		var empty = false;
		var vals = {}
		var passwd, cpasswd;
		$('.signup').find('input').each(function() {
			if (this.value == '') {
				empty = true;
			} else {
				vals[this.name] = this.value;
			}
		});
		if (empty) {
			$('#errmsg_1').removeClass('hide').html("Fields can't be empty.");
		} else if (vals['passwd'] !== vals['cpasswd']) {
			$('#errmsg_1').removeClass('hide').html("Password didn't match.")
		} else {
			ajaxCall(vals,1);
		}
	});
});