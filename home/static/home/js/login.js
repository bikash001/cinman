$(document).ready(function() {
	
	var urls = ['/validateUser/','/register/','/forgot_pwd/']
	
	var ajaxCall = function(vals,index) {
		var token = getCookie();
		// console.log(token);
		$.ajax({
			method: 'POST',
			url: urls[index],
			data: vals,
			headers: {
				'X-CSRFToken': token
			},
			error: function(rsp) {
				if (index == 0) {
					$('#errmsg').removeClass('hide').html('Incorrect Password.');
				} else if (index == 1) {
					console.log('register error');
				} else {
					console.log('forgot passwd', rsp);
				}
			},
			success: function(rsp) {
				if (index == 0) {
					window.location.reload();
				} else if (index == 1) {
					console.log('success register');
				} else {
					console.log('success password',rsp);
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
				return false;
			} else {
				vals[this.name] = this.value;
			}
		});
		if (empty) {
			$('#errmsg').removeClass('hide').html("Fields can't be empty.");
		} else {
			$('#errmsg').addClass('hide');
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
				return false;
			} else {
				vals[this.name] = this.value;
			}
		});
		if (empty) {
			$('#errmsg_2').removeClass('hide').html("Fields can't be empty.");
		} else if (vals['passwd'] !== vals['cpasswd']) {
			$('#errmsg_2').removeClass('hide').html("Password didn't match.")
		} else {
			$('#errmsg_2').addClass('hide');
			ajaxCall(vals,2);
		}
	});

	$('#signupbtn').click(function(){
		var empty = false;
		var vals = {}
		var passwd, cpasswd;
		$('.signup').find('input').each(function() {
			if (this.value == '') {
				// console.log('empty');
				// console.log(this.value, this.name);
				empty = true;
				return false;
			} else {
				vals[this.name] = this.value;
			}
		});
		if (empty) {
			$('#errmsg_1').removeClass('hide').html("Fields can't be empty.");
		} else if (!(/^\d+$/.test(vals['mobile']))){
			$('#errmsg_1').removeClass('hide').html("Mobile field has to be number.")
		} else if (vals['passwd'] !== vals['cpasswd']) {
			$('#errmsg_1').removeClass('hide').html("Password didn't match.")
		} else {
			$('#errmsg_1').addClass('hide');
			ajaxCall(vals,1);
		}
	});

	$('#modal-btn').click(function() {
		
	});
});