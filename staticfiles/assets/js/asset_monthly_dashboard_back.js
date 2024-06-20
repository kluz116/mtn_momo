	$(function () {
  
  $(document).ready(function(){
       $.getJSON('http://192.168.0.29:5000/asset_monthly', function(res_json) {
		   
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
              const array_eighteen = [];
              const array_nineteen = [];
		      const array_month = [];

		      const  array_final = []

		      for (let x of res_json){
		            switch(x.income_name){
		            	case "BANK BALANCES":
		            	      array_one.push(x.Total)
		            	break;
		            	case "CASH BALANCES":
		            	      array_two.push(x.Total)
		            	break;
		            		case "INTER BRANCH":
		            	      array_three.push(x.Total)
		            	break;
		            		case "INTEREST RECEIVABLE INVESTMENTS":
		            	      array_four.push(x.Total)
		            	break;
		            		case "INTEREST RECEIVABLE LOANS":
		            	      array_five.push(x.Total)
		            	break;
		            	case "INTEREST RECEIVABLE OVER DRAFT FACILITIES":
		            	      array_six.push(x.Total)
		            	break;
		            	case "INVENTORY":
		            	      array_seven.push(x.Total)
		            	break;
		            	case "LOAN MONITORING FEES RECEIVABLE":
		            	      array_eight.push(x.Total)
		            	break;
		            	case "LOANS OUTSTANDING":
		            	      array_nine.push(x.Total)
		            	break;
		            	case "LONG TERM INVESTMENTS":
		            	      array_ten.push(x.Total)
		            	break;
		            	case "OVER DRAFT FACILITIES":
		            	      array_eleven.push(x.Total)
		            	break;
		            	case "PENALTY FEES RECEIVABLE":
		            	      array_twelve.push(x.Total)
		            	break;
		            	case "PREPAYMENTS":
		            	      array_thirteen.push(x.Total)
		            	break;
		            	case "PROPERTY & EQUIPMENT":
		            	      array_fourteen.push(x.Total)
		            	break;
		            	case "RELATED PARTY TRANSACTIONS":
		            	      array_fifteen.push(x.Total)
		            	break;
		            	case "SHORT TERM INVESTMENTS":
		            	      array_sixteen.push(x.Total)
		            	break;
		            	case "STAFF DEBTORS":
		            	      array_seventeen.push(x.Total)
		            	break;
		            	case "SUNDRY RECIEVABLES":
		            	      array_eighteen.push(x.Total)
		            	break;
		            	case "TAX ASSETS":
		            	      array_nineteen.push(x.Total)
		            	break;
		            }
		            array_month.push(x.Month)
		     
		      }
		      
		      var chart = new Highcharts.Chart({
		        chart: {
		          type: 'column',
		          renderTo: 'containerx',
		           borderColor: '#EBBA95',
				      borderWidth: 1
		        },
		        title: {
		          text: 'Monthly Asset Breakdown Value'
		        },
		        xAxis: {
		          categories: [...new Set(array_month)].reverse()
		        },
		        yAxis: {
		        title: {
		            text: 'Asset Value (millions)'
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
				      name: 'BANK BALANCES',
				      data: array_one.reverse(),
				    }, {
				      name: 'CASH BALANCES',
				      data: array_two.reverse(),
				    },{
				      name: 'INTER BRANCH',
				      data: array_three.reverse(),
				    },
				    {
				      name: 'INTEREST RECEIVABLE INVESTMENTS',
				      data: array_four.reverse(),
				    },
				    {
				      name: 'INTEREST RECEIVABLE LOANS',
				      data: array_five.reverse(),
				    },
				    {
				      name: 'INTEREST RECEIVABLE OVER DRAFT FACILITIES',
				      data: array_six.reverse(),
				    },
				      {
				      name: 'INVENTORY',
				      data: array_seven.reverse(),
				    },
				      {
				      name: 'LOAN MONITORING FEES RECEIVABLE',
				      data: array_eight.reverse(),
				    },
				      {
				      name: 'LOANS OUTSTANDING',
				      data: array_nine.reverse(),
				    },
				      {
				      name: 'LONG TERM INVESTMENTS',
				      data: array_ten.reverse(),
				    },
				      {
				      name: 'OVER DRAFT FACILITIES',
				      data: array_eleven.reverse(),
				    },
				    {
				      name: 'PENALTY FEES RECEIVABLE',
				      data: array_twelve.reverse(),
				    },
				    {
				      name: 'PREPAYMENTS',
				      data: array_thirteen.reverse(),
				    },
				    {
				      name: 'PROPERTY & EQUIPMENT',
				      data: array_fourteen.reverse(),
				    },
				    {
				      name: 'RELATED PARTY TRANSACTIONS',
				      data: array_fifteen.reverse(),
				    },
				    {
				      name: 'SHORT TERM INVESTMENTS',
				      data: array_sixteen.reverse(),
				    },
				    {
				      name: 'STAFF DEBTORS"',
				      data: array_seventeen.reverse(),
				    },
				    {
				      name: 'SUNDRY RECIEVABLES',
				      data: array_eighteen.reverse(),
				    },
				    {
				      name: 'TAX ASSETS"',
				      data: array_nineteen.reverse(),
				    }]


		      });    

		  });



});