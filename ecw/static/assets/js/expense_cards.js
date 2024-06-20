$(document).ready(function() {
$("button").on('click',function(e) {
	 e.preventDefault();
		 var getdate = $('#datepicker-autoClose').val();
		 url = 'http://192.168.0.29:5000/total_expense_monthly?position_date='+ getdate
		 $.ajax({
		 	    type: "GET",
				cache: false,
			    url: url,
				dataType: "json",
				success: function(data) {
				    $("#total_expense").append(numeral(JSON.stringify(data.Total)).format('0,0'));
				}
		});
});
	  });