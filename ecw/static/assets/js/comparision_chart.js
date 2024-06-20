$(document).ready(function () {
	$.getJSON('http://192.168.0.29:5000/compare_monthly', function (res_json) {

		const array_one = [];
		const array_two = [];
		const array_three = [];
		const array_four = [];

		const array_month = [];

		const array_final = []

		for (let x of res_json) {
			switch (x.Category) {
				case "Income":
					array_one.push(x.Total)
					break;
				case "Expenses":
					array_two.push(x.Total)
					break;
				case "Liability":
					array_three.push(x.Total)
					break;
				case "Asset":
					array_four.push(x.Total)
					break;
			}
			array_month.push(x.Month)

		}
		
		var chart = new Highcharts.Chart({
			chart: {
				type: 'column',
				renderTo: 'container_compare',
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
					name: 'Income',
					data: array_one.reverse(),
				}, {
					name: 'Expenses',
					data: array_two.reverse(),
				}, {
					name: 'Liability',
					data: array_three.reverse(),
				},
				{
					name: 'Asset',
					data: array_four.reverse(),
				}
			]

		});


	});

});