$(document).ready(function () {
	if (thisPage === "Futuros") var ajax_url = "/api/req_agendamentos_futuros";
	else if (thisPage === "Antigos") var ajax_url = "/api/req_agendamentos_antigos";
	else if (thisPage === "Sem Data") var ajax_url = "/api/req_agendamentos_semdata";

	var tabela = $("#tabela-dados").DataTable({
		order: [
			[2, "asc"],
			[3, "asc"],
		],
		paging: true,
		pageLength: 10, // Número de registros por página
		ajax: {
			url: ajax_url,
			type: "GET",
			dataSrc: "", // Indica que os dados estão diretamente no array de objetos retornado
		},
		columns: [
			{
				data: "nome_do_tutor",
				render: function (data, type, row) {
					// Supondo que 'id' seja o id do tutor que você deseja usar na URL
					var url = urlAgendar + row.id + "/";
					return '<a href="' + url + '">' + data + "</a>";
				},
			},
			{ data: "tipo_de_agendamento", className: "campo_centralizado" },
			{
				data: "data",
				className: "campo_centralizado",
			},

			{ data: "horario", render: converterHorario, className: "campo_centralizado" },
		],
		language: {
			url: urlTranslation,
		},
	});

	function converterHorario(horario) {
		if (horario !== null) {
			return horario.split(":")[0] + ":" + horario.split(":")[1];
		} else {
			return "";
		}
	}

	function converterData(data) {
		if (data !== null) {
			return data.split("-")[2] + "/" + data.split("-")[1] + "/" + data.split("-")[0];
		} else {
			return "";
		}
	}
});
