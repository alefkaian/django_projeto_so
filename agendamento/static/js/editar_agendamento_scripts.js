$(document).ready(function () {
	var colunas = [
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
			render: function (data, type, row) {
				if (type === "display" || type === "filter") {
					return converterData(data);
				}
				return data; // Para a ordenação usar o formato original
			},
		},
		{ data: "horario", render: converterHorario, className: "campo_centralizado" },
	];

	if (thisPage === "Futuros") {
		var ajax_url = "/api/req_agendamentos_futuros";
		ordenacao = [
			[2, "asc"],
			[3, "asc"],
		];
	} else if (thisPage === "Antigos") {
		var ajax_url = "/api/req_agendamentos_antigos";
		ordenacao = [
			[2, "desc"],
			[3, "asc"],
		];
	} else if (thisPage === "Sem Data") {
		var ajax_url = "/api/req_agendamentos_semdata";
		ordenacao = [[4, "asc"]];
		colunas.push({
			data: "data_de_criacao",
			className: "campo_centralizado",
			render: function (data, type, row) {
				if (type === "display" || type === "filter") {
					return formatarDataISO(data);
				}
				return data; // Para a ordenação usar o formato original
			},
		});
	}

	var tabela = $("#tabela-dados").DataTable({
		order: ordenacao,
		paging: true,
		pageLength: 10, // Número de registros por página
		ajax: {
			url: ajax_url,
			type: "GET",
			dataSrc: "", // Indica que os dados estão diretamente no array de objetos retornado
		},
		columns: colunas,
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

	function formatarDataISO(dataHoraOriginal) {
		if (dataHoraOriginal) {
			const data = new Date(dataHoraOriginal);
			const dia = String(data.getDate()).padStart(2, "0");
			const mes = String(data.getMonth() + 1).padStart(2, "0"); // Mês começa em 0
			const ano = String(data.getFullYear()).slice(-2);
			const horas = String(data.getHours()).padStart(2, "0");
			const minutos = String(data.getMinutes()).padStart(2, "0");
			const segundos = String(data.getSeconds()).padStart(2, "0");

			return `${dia}/${mes}/${ano} - ${horas}:${minutos}:${segundos}`;
		}
	}
});
