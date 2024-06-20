	$(function () {
  
  $(document).ready(function(){

	$.getJSON('http://192.168.0.29:5000/liability_graph', function(resp_dat) {
		  
		      const income_list = [];
		      const  array_final = []

		      for (let i of resp_dat){
		  
		      	 income_list.push(i.Month);
		      	 array_final.push(i.Total)
		      }


		      var chart = new Highcharts.Chart({
		        chart: {
		          type: 'column',
		          renderTo: 'container3',
		           borderColor: '#EBBA95',
				      borderWidth: 1
		        },
		        title: {
		          text: 'Monthly Total Liability Breakdown'
		        },
		        subtitle: {
		          text: 'Source: Finace Trust Bank'
		        },
		        xAxis: {
		          categories: income_list.reverse()
		        },
		        yAxis: {
		        title: {
		            text: 'Total Expenses (millions)'
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
		          name: 'Expenses',
		          colorByPoint: true,
		          data: array_final.reverse()
		        }]
		      });

		  
		  });
		
  });





});