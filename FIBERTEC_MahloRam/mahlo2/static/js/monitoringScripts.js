function SendUserName(xssl=false, xserver='dkmsspc0007') {
	// console.log("SEND USER NAME function")
	//alert("here in function")
	//console.log("here in function SendUserName")

	var newURL;
	if (xserver == 'dkmsspc0007') {
		if (xssl == true){
			newURL = 'https://dkmsspc0007.miba.com/getwinuser'
		}else{
			newURL = 'http://dkmsspc0007:5000/getwinuser'
		}
	}else{
		if (xssl == true){
			newURL = 'https://msolutions-mec.miba.com:5927/getLoggedUser/'
		}else{
			newURL = 'http://shrepmib001.miba.com:5027/getLoggedUser/'
		}
		
	}
	// console.log("SendUserName: " + newURL)

	$.getJSON(
		{
			url:newURL,
			xhrFields: {withCredentials: true},
		success:function(data){
			// console.log("DATA >>>>>");
			// console.log("xserver: " + xserver)
			// console.log(data);
			// console.log("DATA <<<<<");

			username = "";
			if (xserver == 'dkmsspc0007') {username = data.username;}
			if (xserver == 'shrepmib001') {username = data[0].domain_name;}

			// var username;
			// var member;
			// var domain_name;
			// var currentURL = window.location.href;

			// username = data.username;

			// alert("USER NAME:" + username + "\n" + "MEMBER: " + member + "\n" + "DOMAIN NAME: " + domain_name);
			// console.log("USER NAME:" + username);
			// console.log("MEMBER: " + member);
			// console.log("DOMAIN NAME: " + domain_name);

			$.ajax({
				url: '/GetRemoteUserDetails',
				data: { 'userName': username, 'referer': window.location.href},
				// async:false,
				type: 'POST',
				success: function(){
					// nothing here
					// console.log("ajax success");
					// window.location.replace("/");
				},
				error: function() {
					// nothing here
					// console.log("ajax error");
					// window.location.replace("/");
				}
			});

		}}
	)
			
}
