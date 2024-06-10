$(document).ready(function () {
	let weekOffset = 0;

	function loadContent() {
		$.ajax({
			url: loadContentUrl, // Use a URL correta para sua view
			type: "GET",
			data: {
				week_offset: weekOffset,
			},
			dataType: "json",
			success: function (data) {
				$("#cabecalhoContainer").html(data.cabecalho_html);
				$("#conteudoContainer").html(data.agendamentos_html);
			},
			error: function (xhr, status, error) {
				console.error(xhr.responseText);
			},
		});
	}

	$("#chevron-right").click(function (event) {
		event.preventDefault(); // Evita o comportamento padrão do link
		weekOffset++;
		loadContent();
	});

	$("#chevron-left").click(function (event) {
		event.preventDefault(); // Evita o comportamento padrão do link
		weekOffset--;
		loadContent();
	});

	// Carrega o conteúdo inicial
	loadContent("current");
});
