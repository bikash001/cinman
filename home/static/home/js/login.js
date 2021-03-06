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
					$('#errmsg_1').removeClass('hide').html('Username already exist. Please try with a different username.');
					// console.log('register error');
					$
				} else {
					$('#errmsg_2').removeClass('hide').html('Username-email combination does not exist. Please try with a valid details.');
					console.log('forgot passwd', rsp);
				}
			},
			success: function(rsp) {
				if (index == 0) {
					window.location.reload();
				} else if (index == 1) {
					$('#myModal').removeClass('hide');
					$('#modal-message').html('You will be notified via email once the registration is successful.');
				} else {
					console.log('failuer');
					$('#myModal').removeClass('hide');
					$('#modal-message').html('Please change your password by going to the link sent to your registered email.');
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
		$('#register-form').get(0).reset();
	});

	$('#login-forgotbtn').click(function(){
		$('.login').addClass('hide');
		$('.forgot').removeClass('hide');
		$('#forgot-form').get(0).reset();
	});

	$('#signinbtn').click(function(){
		$('.signup').addClass('hide');
		$('.login').removeClass('hide');
		$('#login-form').get(0).reset();
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
			console.log('empty');
			$('#errmsg_2').removeClass('hide').html("Fields can't be empty.");
		} else if (!validateEmail(vals['email'])) {
			$('#errmsg_2').removeClass('hide').html("Enter valid email address.");
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
			$('#errmsg_1').removeClass('hide').html("Mobile field has to be number.");
		} else if (!validateEmail(vals['email'])) {
			$('#errmsg_1').removeClass('hide').html("Enter valid email address.");
		} else if (vals['passwd'] !== vals['cpasswd']) {
			$('#errmsg_1').removeClass('hide').html("Password didn't match.");
		} else {
			$('#errmsg_1').addClass('hide');
			ajaxCall(vals,1);
		}
	});

	$('#modal-btn').click(function() {
		$('#myModal').addClass('hide');
		window.location.reload();
	});

	function validateEmail(email) {
	  var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
	  return re.test(email);
	}
	$('#login-form').get(0).reset();
});