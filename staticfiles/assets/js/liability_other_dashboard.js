	$(function () {
  
  $(document).ready(function(){
   

   	  $("button").click(function(e) {
		    e.preventDefault();
		   var getdate = $('#datepicker-autoClose').val();
		    $.getJSON('http://192.168.0.29:5000/liability_graph_data?position_date='+ getdate, function(dat) {
		   
		      const income_list = [];
		      const  array_final = []

		      for (let i of dat){
		  
		      	 income_list.push(i.asset_name);
		      	 array_final.push(i.Total)
		      }


		      var chart = new Highcharts.Chart({
		        chart: {
		          type: 'column',
		          renderTo: 'container',
		           borderColor: '#EBBA95',
				      borderWidth: 1
		        },
		        title: {
		          text: 'Total Liability Breakdown'
		        },
		        subtitle: {
		          text: 'Source: Finace Trust Bank'
		        },
		        xAxis: {
		          categories: income_list 
		        },
		        yAxis: {
		        title: {
		            text: 'Total Expense (millions)'
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
		          name: 'Income',
		          colorByPoint: true,
		          data: array_final
		        }]
		      });

		    

		  });


		});




     $("button").click(function(e) {
		    e.preventDefault();

		   var getdate = $('#datepicker-autoClose').val();
		    $.getJSON('http://192.168.0.29:5000/liability_graph_data?position_date='+ getdate, function(dat) {
		   
		      const income_list = [];
		      const  array_final = []

		      for (let i of dat){
		  
		      	 income_list.push(i.asset_name);
		      	 array_final.push(i.Total)
		      }


		      var chart = new Highcharts.Chart({
		        chart: {
		          type: 'line',
		          renderTo: 'container4',
		           borderColor: '#EBBA95',
				      borderWidth: 1
		        },
		        title: {
		          text: 'Total Liability Breakdown'
		        },
		        subtitle: {
		          text: 'Source: Finace Trust Bank'
		        },
		        xAxis: {
		          categories: income_list 
		        },
		        yAxis: {
		        title: {
		            text: 'Total Expense (millions)'
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
		          name: 'Income',
		          colorByPoint: true,
		          data: array_final
		        }]
		      });

		    

		  });


		});



     $('button').on('click', function(e){
        e.preventDefault();
        var getdate = $('#datepicker-autoClose').val();
        $.getJSON('http://192.168.0.29:5000/liability_graph_data?position_date='+ getdate, function(datas) {
        
              // Build the chart
	      const income_list = [];
	      const  array_final = []

	      for (let i of datas){
	  
	      	 income_list.push(i.asset_name);
	      	 array_final.push(i.Total)
	      }
          var chart = new Highcharts.Chart({
              chart: {
		      type: 'pie',
		      renderTo: 'container2',
		      borderColor: '#EBBA95',
		      borderWidth: 1
		    },
            title: {
                text: 'Total Liability Breakdown'
            },
            tooltip: {
				  formatter: function() {
				    var sliceIndex = this.point.index;
				    var sliceName = this.series.chart.axes[0].categories[sliceIndex];
				    return 'Total For <b>' + sliceName + '</b> is <b>' + this.y + '</b>';
				  }
				},
			legend: {
			  enabled: true,
			  labelFormatter: function() {
			    var legendIndex = this.index;
			    var legendName = this.series.chart.axes[0].categories[legendIndex];

			    return legendName;
			  }
			},
			 plotOptions: {
			      pie: {
			        allowPointSelect: true,
			        cursor: 'pointer',
			        showInLegend: true,
			        dataLabels: {
			          enabled: true,
			          format: '{point.y:,.0f}'
			        }
			      }
			    },
             xAxis: {                                                                
            categories: income_list                                    
              },
            series: [{                                                    
            name: 'Directors',                                        
            data: array_final
        }]  
        });

        });
    

  });

		
  });
});