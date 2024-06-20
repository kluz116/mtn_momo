$(document).ready(function () {
	$("button").click(function (e) {
		e.preventDefault();

		var table = $('#data-table-default').DataTable({
			"serverSide": false,
			destroy: true,
			"ordering": false,


			ajax: {
				url: 'http://192.168.0.29:5000/bs_list',
				'data': {
					'position_date': $('#datepicker-autoClose').val()
				},
				dataSrc: ""
			},
			columns: [{
					data: 'Description'
				},
				{
					data: 'CategoryID'
				},
				{
					data: 'Amount'
				},
				{
					data: 'Position_date'
				}
			],

			"columnDefs": [{
				"visible": false,
				"targets": 1
			}],
			"order": [
				[1, 'desc']
			],
			"displayLength": 25
		});


	}); //End of balance sheet list table

	$("button").click(function (e) {
		e.preventDefault();
		var getdate = $('#datepicker-autoClose').val();
		$.getJSON('http://192.168.0.29:5000/bs_daily?position_date=' + getdate, function (dat) {

			const asset_list = [];
			const array_final = []

			for (let i of dat) {

				asset_list.push(i.Name);
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
					text: 'Balance Sheet Totals'
				},
				xAxis: {
					categories: asset_list
				},
				yAxis: {
					title: {
						text: 'Total  (millions)'
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
					name: 'Balance Sheet',
					colorByPoint: true,
					data: array_final
				}]
			});


		});


	}); // End of balancesheet Graph

	$.getJSON('http://192.168.0.29:5000/balancesheet_monthly', function (res_json) {

		const array_one = [];
		const array_two = [];
		const array_three = [];
		const array_month = [];

		const array_final = []

		for (let x of res_json) {
			switch (x.Name) {
				case "Total Assets":
					array_one.push(x.Total)
					break;
				case "Total Liabilities":
					array_two.push(x.Total)
					break;
				case "Total Liabilities And ShareFunds":
					array_three.push(x.Total)
					break;

			}
			array_month.push(x.Month)

		}

		var chart = new Highcharts.Chart({
			chart: {
				type: 'column',
				renderTo: 'container3',
				borderColor: '#EBBA95',
				borderWidth: 1
			},
			title: {
				text: 'Monthly BalaneSheet Total Breakdown '
			},
			xAxis: {
				categories: [...new Set(array_month)].reverse()
			},
			yAxis: {
				title: {
					text: 'Total (millions)'
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
				name: 'Total Assets',
				data: array_one.reverse(),
			}, {
				name: 'Total Liabilities',
				data: array_two.reverse(),
			}, {
				name: 'Total Liabilities And Share Funds',
				data: array_three.reverse(),
			}]


		});

	});
});