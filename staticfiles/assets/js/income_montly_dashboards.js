

 $.getJSON('http://192.168.0.29:5000/income_monthly', function(res_json) {
		   
		      const array_one = [];
		      const array_two = [];
		      const array_three = [];
		      const array_four = [];
		      const array_five = [];
		      const array_six = [];
		      const array_seven = [];
		      const array_eight = [];
		      const array_nine = [];
		      const array_ten = [];
		      const array_eleven = [];
		      const array_twelve = [];
		      const array_thirteen = [];
		      const array_fourteen = [];
              const array_fifteen = [];
		      const array_month = [];

		      const  array_final = []

		      for (let x of res_json){
		            switch(x.income_name){
		            	case "INTEREST INCOME LOANS":
		            	      array_one.push(x.Total)
		            	break;
		            	case "INTEREST INCOME FIXED DEPOSITS":
		            	      array_two.push(x.Total)
		            	break;
		            		case "SAVINGS INCOME":
		            	      array_three.push(x.Total)
		            	break;
		            		case "LOAN MONITORING FEES":
		            	      array_four.push(x.Total)
		            	break;
		            		case "Admin Fees  on Loans":
		            	      array_five.push(x.Total)
		            	break;
		            	case "Bank Guarantee  Fees":
		            	      array_six.push(x.Total)
		            	break;
		            	case "EARLY REPAYMENT CHARGE":
		            	      array_seven.push(x.Total)
		            	break;
		            	case "GRANT INCOME":
		            	      array_eight.push(x.Total)
		            	break;
		            	case "RECOVERY OF WRITTEN OFF LOANS":
		            	      array_nine.push(x.Total)
		            	break;
		            	case "OTHER INCOMES":
		            	      array_ten.push(x.Total)
		            	break;
		            	case "COMMISSIONS ON OTHER FINANCIAL SERVICES":
		            	      array_eleven.push(x.Total)
		            	break;
		            	case "LOAN COMMITMENT FEES":
		            	      array_twelve.push(x.Total)
		            	break;
		            	case "INTEREST INCOME ON OVER DRAFT FACILITIES":
		            	      array_thirteen.push(x.Total)
		            	break;
		            	case "LOAN PENALTY FEES":
		            	      array_fourteen.push(x.Total)
		            	break;
		            	case "LOAN PROCESSING FEES":
		            	      array_fifteen.push(x.Total)
		            	break;
		            }
		            array_month.push(x.Month)
		     
		      }
		      console.log(...new Set(array_one))

		      var chart = new Highcharts.Chart({
		        chart: {
		          type: 'column',
		          renderTo: 'containerx',
		           borderColor: '#EBBA95',
				      borderWidth: 1
		        },
		        title: {
		          text: 'Monthly Income Breakdown Value'
		        },
		        xAxis: {
		          categories: [...new Set(array_month)].reverse()
		        },
		        yAxis: {
		        title: {
		            text: 'Income Value (millions)'
		        }
		        },
		        legend: {
		          align: 'right',
		          x: -30,
		          verticalAlign: 'top',
		          y: 25,
		          floating: true,
		          backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || 'white',
		          borderColor: '#CCC',
		          borderWidth: 1,
		          shadow: false
		        },
		        tooltip: {
		          pointFormat: 'Total: <b>{point.y}</b>'
		        },
		        plotOptions: {
		          column: {
		            stacking: 'normal',
		            dataLabels: {
		              enabled: false,
		              color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white',
		              style: {
		                textShadow: '0 0 3px black'
		              }
		            }
		          }
		        },
		   
		           series: [{
				      name: 'INTEREST INCOME LOANS',
				      data: array_one.reverse(),
				    }, {
				      name: 'INTEREST INCOME FIXED DEPOSITS',
				      data: array_two.reverse(),
				    },{
				      name: 'SAVINGS INCOME',
				      data: array_three.reverse(),
				    },
				    {
				      name: 'LOAN MONITORING FEES',
				      data: array_four.reverse(),
				    },
				    {
				      name: 'Admin Fees  on Loans',
				      data: array_five.reverse(),
				    },
				    {
				      name: 'Bank Guarantee  Fees',
				      data: array_six.reverse(),
				    },
				      {
				      name: 'EARLY REPAYMENT CHARGE',
				      data: array_seven.reverse(),
				    },
				      {
				      name: 'GRANT INCOME',
				      data: array_eight.reverse(),
				    },
				      {
				      name: 'RECOVERY OF WRITTEN OFF LOANS',
				      data: array_nine.reverse(),
				    },
				      {
				      name: 'OTHER INCOMES',
				      data: array_ten.reverse(),
				    },
				      {
				      name: 'COMMISSIONS ON OTHER FINANCIAL SERVICES',
				      data: array_eleven.reverse(),
				    },
				    {
				      name: 'LOAN COMMITMENT FEES',
				      data: array_twelve.reverse(),
				    },
				    {
				      name: 'INTEREST INCOME ON OVER DRAFT FACILITIES',
				      data: array_thirteen.reverse(),
				    },
				    {
				      name: 'LOAN PENALTY FEES',
				      data: array_fourteen.reverse(),
				    },
				    {
				      name: 'LOAN PROCESSING FEES',
				      data: array_fifteen.reverse(),
				    }]


		      });

		    

		  });


