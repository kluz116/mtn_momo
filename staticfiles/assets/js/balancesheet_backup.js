$("button").click(function (e) {
	e.preventDefault();

	var table = $('#data-table-default').DataTable({
		"serverSide": false,
		destroy: true,

		ajax: {
			url: 'http://192.168.0.29:5000/balancesheet',
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
		"displayLength": 25,
		"drawCallback": function (settings) {
			var api = this.api();
			var rows = api.rows({
				page: 'current'
			}).nodes();
			var last = null;
			var subTotal = new Array();
			var groupID = -1;
			var aData = new Array();
			var index = 0;


			api.column(1, {
				page: 'current'
			}).data().each(function (group, i) {

				var vals = api.row(api.row($(rows).eq(i)).index()).data();

				var bal = vals.Amount

				if (typeof aData[group] == 'undefined') {
					aData[group] = new Array();
					aData[group].rows = [];
					aData[group].bal = [];
				}

				aData[group].rows.push(i);
				aData[group].bal.push(bal);

			});


			var idx = 0;


			for (var x in aData) {

				idx = Math.max.apply(Math, aData[x].rows);

				var sum = 0;
				$.each(aData[x].bal, function (k, v) {
					sum = sum + v;
				});
				console.log(`The total is :${aData[x].bal}`);
				$(rows).eq(idx).after(
					'<tr><td colspan="2" class="text-primary">' + x + '</td>' + '<td class="text-danger"><strong>' + numeral(sum).format('0,0') + '</strong></td></tr>'

				);

			};


		}
	});


});