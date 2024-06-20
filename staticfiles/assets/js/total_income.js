		fetch('http://192.168.0.29:5000/total_income')
		  .then(function(response) {
		    return response.json();
		  })
		  .then(function(myJson) {
		     $("#total_income").append(numeral(JSON.stringify(myJson.Total)).format('0,0'));
		});