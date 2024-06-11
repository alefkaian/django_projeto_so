$(document).ready(function () {
	var linkVoltar = document.getElementById("link_botao_voltar");
	if (linkVoltar) {
		var previousPage = sessionStorage.getItem("previousPage");
		if (previousPage) {
			linkVoltar.href = previousPage;
		}
	}
});
