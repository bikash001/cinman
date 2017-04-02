$(document).ready(function() {
	
	var urls = ['/home/','/home/messages/','/home/notifications/','/home/systemstats/']
	var csrftoken = undefined;

	var ajaxCall = function(arg) {
		if (csrftoken === undefined) {
			csrftoken = getCookie();
		}
		$.ajax({
			method: 'POST',
			url: urls[arg],
			headers: {
				'X-CSRFToken': csrftoken
			},
			error: function(rsp) {
				console.log('error');
				console.log(rsp);
			},
			success: function(rsp) {
				// console.log('success');
				// console.log(rsp)
				if (rsp.type === 'message') {
					var messages = rsp.data;
					var ips = {}
					for (var i=0; i<messages.length; i++) {
						if (ips[messages[i].ip] == undefined) {
							ips[messages[i].ip] = []
						}
						ips[messages[i].ip].push([messages[i].uname,messages[i].time,messages[i].msg])
					}

					$('#content').append('<div class="col-xs-4 left-no-pad"><div class="vertical-menu"></div></div>');
					for (var i in ips) {
						if (ips.hasOwnProperty(i)) {
							$('.vertical-menu').append('<a class="pointer msg" id="'+i+'" >'+i+'</a>');
						}
					}
					$('.msg').click(function() {
						$(this).addClass('active');
						$('#content').append('<div class="col-xs-8 right-no-pad"><div class="vertical-menu2"></div></div>');
						console.log(ips);
						for (var i in ips) {
							if (ips.hasOwnProperty(i)) {
								var arr = ips[i];
								console.log(arr);
								for (var k=0; k<arr.length; k++) {
									$('.vertical-menu2').append('<a>'+arr[k][0]+' @ '+arr[k][1]+'<br><br>'+arr[k][2]+'</a>');
								}
							}
						}
					});

				} else if (rsp.type === 'stats') {
					$('#content').append('<div class="row no-margin"><datalist id="ip-datas"></datalist><div style="position:relative; float:left; width:200px;"><input placeholder="ip address" list="ip-datas" style="width:200px; padding:5px;"/></div><div style="float:left;"><button id="gobtn" style="padding:5px; margin-left:5px;" class="btn btn-default">GO</button></div></div>');
					$('#content').append('<div class="row no-margin"><div class="col-xs-3 left-no-pad" style="margin-top:15px;"><div id="headers" class="list-group"></div></div><div id="detail-contents" class="col-xs-9"></div></div>')
					for (var k=0; k<rsp.data.length; k++) {
						$('#ip-datas').append('<option value="'+rsp.data[k].ip+'">'+rsp.data[k].ip+'</option>');
					}
					$('#gobtn').click(function() {
						var val = $('#content').find('input').val();
						console.log(val);
						for (var k=0; k<rsp.data.length; k++) {
							if (val == rsp.data[0].ip) {
								machineDetails(rsp.data[k].id);
								break;
							}
						}
					});
					// for (var i=0; i<rsp.size; i++) {
					// 	$('.dropdown-menu').append('<li><a class="pointer msg" id="stat-"'+rsp.data[i].id+' >'+rsp.data[i].ip+'</a></li>');
					// } 
				}
			},
		});
	};

	var machineDetails = function(arg) {
		var baseUrl = '/home/systemstats/';
		console.log(arg);
		if (csrftoken === undefined) {
			csrftoken = getCookie();
		}
		$.ajax({
			method: 'POST',
			url: baseUrl+arg+"/",
			headers: {
				'X-CSRFToken': csrftoken
			},
			error: function(rsp) {
				console.log('error');
				console.log(rsp);
			},
			success: function(rsp) {
				console.log('lol');
			}
		});
		console.log('hello');
		var list = ['Cpu','RAM','Hard Disk','Motherboard','Network Interface','Peripherals','OS','Softwares','Users','Logs'];
		for (var i=0; i<list.length; i++) {
			$('#headers').append('<a id="li-'+i+'" href="#" class="list-group-item">'+list[i]+'</a>');
		}
	};

	// var messageRequest = function(arg) {
	// 	var baseUrl = '/home/messages/';
	// 	console.log(arg);
	// 	if (csrftoken === undefined) {
	// 		csrftoken = getCookie();
	// 	}
	// 	var id = arg.currentTarget.id.split('-')[1]
	// 	console.log(id);
	// 	$.ajax({
	// 		method: 'POST',
	// 		url: baseUrl+id+"/",
	// 		headers: {
	// 			'X-CSRFToken': csrftoken
	// 		},
	// 		error: function(rsp) {
	// 			console.log('error');
	// 			console.log(rsp);
	// 		},
	// 		success: function(rsp) {
	// 			console.log('lol');
	// 		}
	// 	});
	// };

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