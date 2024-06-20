$(function () {
	$(document).ready(function(){
      
       	$.getJSON('http://192.168.0.29:5000/liability_monthly',function (res_json) {
       		// body...
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
              const array_twenty = [];
              const array_twenty_one = [];
              const array_twenty_two = [];
               const array_twenty_three = [];
              const array_twenty_four = [];
              const array_twenty_five = [];
              const array_twenty_six = [];
		      const array_month = [];

		      const  array_final = []

		      		      for (let x of res_json){
		            switch(x.asset_name){
		            	case "TAX PAYABLES":
		            	      array_one.push(x.Total)
		            	break;
		            	case "SUSPENDED PENALTY FEES ON LOANS":
		            	      array_two.push(x.Total)
		            	break;
		            		case "SUSPENDED LOAN MONITORING FEES ON LOANS":
		            	      array_three.push(x.Total)
		            	break;
		            		case "SUSPENDED INTEREST ON LOANS":
		            	      array_four.push(x.Total)
		            	break;
		            		case "SPECIFIC PROVISIONS BAD DEBTS":
		            	      array_five.push(x.Total)
		            	break;
		            	case "SHARE CAPITAL":
		            	      array_six.push(x.Total)
		            	break;
		            	case "RESERVES":
		            	      array_seven.push(x.Total)
		            	break;
		            	case "RELATED PARTY":
		            	      array_eight.push(x.Total)
		            	break;
		            	case "PROFIT AND LOSS(YTD)":
		            	      array_nine.push(x.Total)
		            	break;
		            	case "LONG TERM LOANS":
		            	      array_ten.push(x.Total)
		            	break;
		            	case "INTEREST PAYABLE FREE SAVINGS":
		            	      array_eleven.push(x.Total)
		            	break;
		            	case "INTEREST PAYABLE FIXED DEPOSITS":
		            	      array_twelve.push(x.Total)
		            	break;
		            	case "INTEREST PAYABLE BORROWED FUNDS":
		            	      array_thirteen.push(x.Total)
		            	break;
		            	case "NTER BRANCH":
		            	      array_fourteen.push(x.Total)
		            	break;
		            	case "GRATUITY & PENSIONS":
		            	      array_fifteen.push(x.Total)
		            	break;
		            	case "GENERAL PROVISIONS BAD DEBTS":
		            	      array_sixteen.push(x.Total)
		            	break;
		            	case "FREE SAVINGS":
		            	      array_seventeen.push(x.Total)
		            	break;
		            	case "FIXED DEPOSITS":
		            	      array_eighteen.push(x.Total)
		            	break;
		            	case "DIVIDEND PAYABLE":
		            	      array_nineteen.push(x.Total)
		            	break;
		            	case "DESIGNATED FUNDS":
		            	      array_twenty.push(x.Total)
		            	break;
		            	case "DEFERRED LOAN PROCESSING FEES":
		            	      array_twenty_one.push(x.Total)
		            	break;
		            	case "DEFERRED LOAN COMMITMENT FEES":
		            	      array_twenty_two.push(x.Total)
		            	break;
		            	case "CAPITAL GRANT":
		            	      array_twenty_three.push(x.Total)
		            	break;
		            	case "ACCUMULATED PROFITS":
		            	      array_twenty_four.push(x.Total)
		            	break;
		            	case "ACCUMMULATED DEPRECIATION":
		            	      array_twenty_five.push(x.Total)
		            	break;
		            	case "ACCOUNTS PAYABLE":
		            	      array_twenty_six.push(x.Total)
		            	break;
		            }
		            array_month.push(x.Month)
		     
		      }//End of for loop
              
              var chart = new Highcharts.Chart({
		        chart: {
		          type: 'column',
		          renderTo: 'containerx',
		           borderColor: '#EBBA95',
				      borderWidth: 1
		        },
		        title: {
		          text: 'Monthly Liability Breakdown Value'
		        },
		        xAxis: {
		          categories: [...new Set(array_month)].reverse()
		        },
		        yAxis: {
		        title: {
		            text: 'Liability Value (millions)'
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
				      name: 'TAX PAYABLES',
				      data: array_one.reverse(),
				    }, {
				      name: 'SUSPENDED PENALTY FEES ON LOANS',
				      data: array_two.reverse(),
				    },{
				      name: 'SUSPENDED LOAN MONITORING FEES ON LOANS',
				      data: array_three.reverse(),
				    },
				    {
				      name: 'SUSPENDED INTEREST ON LOANS',
				      data: array_four.reverse(),
				    },
				    {
				      name: 'SPECIFIC PROVISIONS BAD DEBTS',
				      data: array_five.reverse(),
				    },
				    {
				      name: 'SHARE CAPITAL',
				      data: array_six.reverse(),
				    },
				      {
				      name: 'RESERVES',
				      data: array_seven.reverse(),
				    },
				      {
				      name: 'RELATED PARTY',
				      data: array_eight.reverse(),
				    },
				      {
				      name: 'PROFIT AND LOSS(YTD)',
				      data: array_nine.reverse(),
				    },
				      {
				      name: 'LONG TERM LOANS',
				      data: array_ten.reverse(),
				    },
				      {
				      name: 'INTEREST PAYABLE FREE SAVINGS',
				      data: array_eleven.reverse(),
				    },
				    {
				      name: 'INTEREST PAYABLE FIXED DEPOSITS',
				      data: array_twelve.reverse(),
				    },
				    {
				      name: 'INTEREST PAYABLE BORROWED FUNDS',
				      data: array_thirteen.reverse(),
				    },
				    {
				      name: 'NTER BRANCH',
				      data: array_fourteen.reverse(),
				    },
				    {
				      name: 'GRATUITY & PENSIONS',
				      data: array_fifteen.reverse(),
				    },
				    {
				      name: 'GENERAL PROVISIONS BAD DEBTS',
				      data: array_sixteen.reverse(),
				    },
				    {
				      name: 'FREE SAVINGS',
				      data: array_seventeen.reverse(),
				    },
				    {
				      name: 'FIXED DEPOSITS',
				      data: array_eighteen.reverse(),
				    },
				    {
				      name: 'DIVIDEND PAYABLE',
				      data: array_nineteen.reverse(),
				    },
				    {
				      name: 'DESIGNATED FUNDS',
				      data: array_twenty.reverse(),
				    },
				    {
				      name: 'DEFERRED LOAN PROCESSING FEES',
				      data: array_twenty_one.reverse(),
				    },
				    {
				      name: 'DEFERRED LOAN COMMITMENT FEES"',
				      data: array_twenty_two.reverse(),
				    },
				    {
				      name: 'CAPITAL GRANT',
				      data: array_twenty_three.reverse(),
				    },
				    {
				      name: 'ACCUMULATED PROFITS',
				      data: array_twenty_four.reverse(),
				    },
				    {
				      name: 'ACCUMMULATED DEPRECIATION',
				      data: array_twenty_five.reverse(),
				    },
				    {
				      name: 'ACCOUNTS PAYABLE',
				      data: array_twenty_six.reverse(),
				    }]


		      });//End of High chart function

       	});//End of get Json function
	});
});