$(document).ready(function () {
	var form = document.getElementById("formulario");
	if (form) {
		form.setAttribute("novalidate", true);
	}
	var nomeDoTutorInput = document.getElementById("id_nome_do_tutor");
	var dateInput = document.getElementById("id_data_nascimento");
	var phoneInput = document.getElementById("id_whatsapp");
	var emailInput = document.getElementById("id_email");
	var nomeDoAnimalInput = document.getElementById("id_nome_do_animal");
	var tipoDeAnimalInput = document.getElementById("id_tipo_de_animal");
	var idadeDoAnimalInput = document.getElementById("id_idade_do_animal");
	var pesoDoAnimalInput = document.getElementById("id_peso_do_animal");

	var enterKeydownListener = function (event) {
		if (event.key === "Enter") {
			event.preventDefault();
			const currentElement = document.activeElement;
			const formElements = Array.from(document.querySelectorAll("#formulario input, #formulario textarea"));
			const currentIndex = formElements.indexOf(currentElement);
			if (currentIndex !== -1) {
				if (currentIndex < formElements.length - 2) {
					formElements[currentIndex + 1].focus();
				} else {
					const submitButton = document.querySelector(".botao_cadastrar");
					if (submitButton) {
						submitButton.click();
					}
				}
			}
		}
	};

	document.addEventListener("keydown", enterKeydownListener);

	// Iterar sobre todos os campos do formulário
	document.querySelectorAll(".form-group").forEach(function (element) {
		// Verificar se o campo tem erros
		if (element.querySelector(".error")) {
			// Adicionar a classe de erro ao campo
			if (element.querySelector("input")) {
				element.querySelector("input").classList.add("input_invalido");
			} else {
				element.querySelector("select").classList.add("input_invalido");
			}
		}
	});

	$("#id_nome_do_tutor").on("input", function () {
		var errorMessage = $(this).attr("data-error-msg");
		var inputValue = $(this).val();
		// Lógica para validar o valor do campo e exibir/ocultar a mensagem de erro
		if (inputValue.length > 1) {
			$(this).removeClass("input_invalido");
			$(this).next(".error").text("").hide(); // ou $(this).next('.error').hide();
		}
	});

	$("#id_data_nascimento").on("input", function () {
		var inputValue = $(this).val();
		inputValue = inputValue.replace(/\D/g, "");
		if (inputValue.length > 2 && inputValue.length <= 4) {
			inputValue = `${inputValue.slice(0, 2)}/${inputValue.slice(2)}`;
		} else if (inputValue.length > 4 && inputValue.length <= 6) {
			inputValue = `${inputValue.slice(0, 2)}/${inputValue.slice(2, 4)}/${inputValue.slice(4)}`;
		} else if (inputValue.length > 6) {
			inputValue = `${inputValue.slice(0, 2)}/${inputValue.slice(2, 4)}/${inputValue.slice(4, 8)}`;
		}
		inputValue = inputValue.slice(0, 10);
		$(this).val(inputValue);
		if (inputValue.length == 10) {
			$(this).removeClass("input_invalido");
			$(this).next(".error").text("").hide();
		}
	});

	$("#id_whatsapp").on("input", function () {
		var inputValue = $(this).val();
		inputValue = inputValue.replace(/\D/g, "");
		if (inputValue.length > 2 && inputValue.length <= 7) {
			inputValue = `(${inputValue.slice(0, 2)}) ${inputValue.slice(2)}`;
		} else if (inputValue.length > 7 && inputValue.length <= 11) {
			inputValue = `(${inputValue.slice(0, 2)}) ${inputValue.slice(2, 7)}-${inputValue.slice(7)}`;
		}
		inputValue = inputValue.slice(0, 15);
		$(this).val(inputValue);
		if (inputValue.length == 15) {
			$(this).removeClass("input_invalido");
			$(this).next(".error").text("").hide();
		}
	});

	$("#id_email").on("input", function () {
		var inputValue = $(this).val();
		if (validar_email(inputValue)) {
			$(this).removeClass("input_invalido");
			$(this).next(".error").text("").hide();
		}
	});

	function validar_email(email) {
		if (email.length < 3) return false;
		else {
			var count_at = 0;
			for (var i = 0; i < email.length; i++) {
				if (email[i] == "@") count_at++;
			}
			if (count_at == 1) return true;
			else return false;
		}
	}

	$("#id_nome_do_animal").on("input", function () {
		var inputValue = $(this).val();
		inputValue = inputValue.replace(/[^a-zA-Z\s]/g, "");
		if (inputValue.length > 1) {
			$(this).removeClass("input_invalido");
			$(this).next(".error").text("").hide();
		}
		$(this).val(inputValue);
	});

	$("#id_tipo_de_animal").on("input", function () {
		var inputValue = $(this).val();
		if (inputValue !== "Selecione") {
			$(this).removeClass("input_invalido");
			$(this).next(".error").text("").hide();
		}
	});

	$("#id_idade_do_animal, #id_peso_do_animal").on("input", function () {
		var inputValue = $(this).val();
		if (validar_numero(inputValue)) {
			$(this).removeClass("input_invalido");
			$(this).next(".error").text("").hide();
		}
		$(this).val(inputValue);
	});

	function validar_numero(entrada) {
		if (entrada.length < 3) return false;
		else {
			if (/\d/.test(entrada)) {
				return true;
			} else {
				return false;
			}
		}
	}

	document.getElementById("confirmacao").addEventListener("change", function () {
		var botao = document.querySelector(".botao_cadastrar");
		botao.disabled = !this.checked;
	});
	$.datepicker.setDefaults($.datepicker.regional["pt-BR"]);
	var selectHorario = document.getElementById("id_horario");

	function gerar_dias_indisponiveis() {
		let dias_indisponiveis = [];
		if (horariosIndisponiveis !== undefined) {
			for (var i = 0; i < horariosIndisponiveis.length; i++) {
				let dia = horariosIndisponiveis[i];
				if (
					horariosIndisponiveis[i].horario_14 &&
					horariosIndisponiveis[i].horario_15 &&
					horariosIndisponiveis[i].horario_16 &&
					horariosIndisponiveis[i].horario_17
				) {
					dias_indisponiveis.push(dia.data);
				}
			}
		}
		return dias_indisponiveis;
	}

	var disabledDates = gerar_dias_indisponiveis();

	let selectedDate;

	function disableDates(date) {
		const noWeekends = $.datepicker.noWeekends(date);
		if (!noWeekends[0]) {
			return noWeekends; // If it's a weekend, return false.
		}

		const formattedDate = $.datepicker.formatDate("yy-mm-dd", date);
		if (disabledDates.includes(formattedDate)) {
			return [false, "", "Indisponível"];
		}
		return [true, ""];
	}

	$("#datePicker").datepicker({
		dateFormat: "DD, d 'de' M 'de' yy",
		minDate: 0,
		beforeShowDay: disableDates,
		onSelect: function (dateText, inst) {
			selectedDate = $(this).datepicker("getDate");
			selectedDateDjangoFomat = $.datepicker.formatDate("yy-mm-dd", selectedDate);
			carregarOpcoesHorario(converterSelectedDateEmHorario(selectedDateDjangoFomat));
			$("#id_data").val(selectedDateDjangoFomat);
			$(this).removeClass("input_invalido");
			$("#id_data").next(".error").text("").hide();
		},
	});

	const dataInicial = $("#id_data").val();
	if (dataInicial) {
		if (dataInicial.substr(2, 1) === "/") {
			dateF = $.datepicker.parseDate("dd/mm/yy", dataInicial);
			$("#datePicker").datepicker("setDate", dateF);
			
		} else if (dataInicial.substr(4, 1) === "-") {
			dateF = $.datepicker.parseDate("yy-mm-dd", dataInicial);
			$("#datePicker").datepicker("setDate", dateF);
		}
	}

	function converterSelectedDateEmHorario(date) {
		let objectDate = horariosIndisponiveis.filter((obj) => obj.data === date);
		if (objectDate[0]) {
			return [false, objectDate[0].horario_14, objectDate[0].horario_15, objectDate[0].horario_16, objectDate[0].horario_17];
		} else {
			return [false, false, false, false, false];
		}
	}

	function carregarOpcoesHorario(estadoHorarios) {
		// Reset all options to enabled first
		for (let i = 0; i < selectHorario.options.length; i++) {
			selectHorario.options[i].disabled = false;
		}
		// Disable options based on the state of horarios
		for (let i = 0; i < estadoHorarios.length; i++) {
			if (estadoHorarios[i]) {
				selectHorario.options[i].disabled = true;
			}
		}
		// Clear the selected option if it is now disabled
		if (selectHorario.selectedIndex >= 0 && selectHorario.options[selectHorario.selectedIndex].disabled) {
			selectHorario.selectedIndex = 0;
		}
	}

	if ($("#datePicker").val()) {
		selectedDate = $("#datePicker").datepicker("getDate");
		selectedDateDjangoFomat = $.datepicker.formatDate("yy-mm-dd", selectedDate);
		carregarOpcoesHorario(converterSelectedDateEmHorario(selectedDateDjangoFomat));
	} else carregarOpcoesHorario[(false, true, true, true, true)];
});
