$(document).ready(function() {
	$("button").on('click',function(e) {
		 e.preventDefault();
			 var getdate = $('#datepicker-autoClose').val();
			 url = 'http://192.168.0.29:5000/total_asset_monthly?position_date='+ getdate
			 $.ajax({
			 	    type: "GET",
					cache: false,
				    url: url,
					dataType: "json",
					success: function(data) {
					    $("#total_asset").append(numeral(JSON.stringify(data.Total)).format('0,0'));
					}
			});
	});
});