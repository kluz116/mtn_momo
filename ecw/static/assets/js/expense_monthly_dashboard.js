	$(function () {
  
  $(document).ready(function(){
       $.getJSON('http://192.168.0.29:5000/expense_monthly', function(res_json) {
		   
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
               const array_sixteen = [];
              const array_seventeen = [];
		      const array_month = [];

		      const  array_final = []

		      for (let x of res_json){
		            switch(x.income_name){
		            	case "ADMINISTRATION EXPENSES":
		            	      array_one.push(x.Total)
		            	break;
		            	case "BOARD EXPENSES":
		            	      array_two.push(x.Total)
		            	break;
		            		case "CORPORATION TAX":
		            	      array_three.push(x.Total)
		            	break;
		            		case "DEPRECIATION EXPENSES":
		            	      array_four.push(x.Total)
		            	break;
		            		case "GENERAL PROVISIONS BAD DEBTS EXPENSE":
		            	      array_five.push(x.Total)
		            	break;
		            	case "INSURANCE EXPENSES":
		            	      array_six.push(x.Total)
		            	break;
		            	case "INTEREST & FEES ON BORROWINGS":
		            	      array_seven.push(x.Total)
		            	break;
		            	case "INTEREST EXPENSE ON DEPOSITS":
		            	      array_eight.push(x.Total)
		            	break;
		            	case "MARKETING EXPENSES":
		            	      array_nine.push(x.Total)
		            	break;
		            	case "MOTOR VEHICLE / CYCLE EXPENSES":
		            	      array_ten.push(x.Total)
		            	break;
		            	case "OTHER OPERATING EXPENSES":
		            	      array_eleven.push(x.Total)
		            	break;
		            	case "RENT & RATES":
		            	      array_twelve.push(x.Total)
		            	break;
		            	case "SALARIES AND BENEFITS":
		            	      array_thirteen.push(x.Total)
		            	break;
		            	case "SPECIFIC PROVISIONS BAD DEBTS EXPENSE":
		            	      array_fourteen.push(x.Total)
		            	break;
		            	case "TRANSFORMATION EXPENSES":
		            	      array_fifteen.push(x.Total)
		            	break;
		            	case "TRANSPORT & TRAVEL":
		            	      array_sixteen.push(x.Total)
		            	break;
		            	case "UTILITIES":
		            	      array_seventeen.push(x.Total)
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
		          text: 'Monthly Expense Breakdown Value'
		        },
		        xAxis: {
		          categories: [...new Set(array_month)].reverse()
		        },
		        yAxis: {
		        title: {
		            text: 'Expense Value (millions)'
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
				      name: 'ADMINISTRATION EXPENSES',
				      data: array_one.reverse(),
				    }, {
				      name: 'BOARD EXPENSES',
				      data: array_two.reverse(),
				    },{
				      name: 'CORPORATION TAX',
				      data: array_three.reverse(),
				    },
				    {
				      name: 'DEPRECIATION EXPENSES',
				      data: array_four.reverse(),
				    },
				    {
				      name: 'GENERAL PROVISIONS BAD DEBTS EXPENSE',
				      data: array_five.reverse(),
				    },
				    {
				      name: 'INSURANCE EXPENSES',
				      data: array_six.reverse(),
				    },
				      {
				      name: 'INTEREST & FEES ON BORROWINGS',
				      data: array_seven.reverse(),
				    },
				      {
				      name: 'INTEREST EXPENSE ON DEPOSITS',
				      data: array_eight.reverse(),
				    },
				      {
				      name: 'MARKETING EXPENSES',
				      data: array_nine.reverse(),
				    },
				      {
				      name: 'MOTOR VEHICLE / CYCLE EXPENSES',
				      data: array_ten.reverse(),
				    },
				      {
				      name: 'OTHER OPERATING EXPENSES',
				      data: array_eleven.reverse(),
				    },
				    {
				      name: 'RENT & RATES',
				      data: array_twelve.reverse(),
				    },
				    {
				      name: 'SALARIES AND BENEFITS',
				      data: array_thirteen.reverse(),
				    },
				    {
				      name: 'SPECIFIC PROVISIONS BAD DEBTS EXPENSE',
				      data: array_fourteen.reverse(),
				    },
				    {
				      name: 'TRANSFORMATION EXPENSES',
				      data: array_fifteen.reverse(),
				    },
				    {
				      name: 'TRANSPORT & TRAVEL',
				      data: array_sixteen.reverse(),
				    },
				    {
				      name: 'UTILITIES',
				      data: array_seventeen.reverse(),
				    }]


		      });    

		  });



});