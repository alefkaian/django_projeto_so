$(document).ready(function () {
	var form = document.getElementById("formulario");
	if (form) {
		form.setAttribute("novalidate", true);
	}
	var selectHorario = document.getElementById("id_horario");

	document.addEventListener("submit", function (event) {
		event.preventDefault();
		confirmacaoExtra();
	});

	function confirmacaoExtra() {
		if ($("#id_tipo_de_agendamento").val() === "Cirurgia") {
			atualizarModalAgendamentosDia();
		} else if (selectHorario[selectHorario.selectedIndex].classList.contains("data_indisponivel")) {
			atualizarModalAgendamentoHorario();
		} else {
			form.submit();
		}
	}

	$("#modalConfirmButton").on("click", function () {
		$("#confirmModal").modal("hide");
		form.submit();
	});

	if (!previousUrl.includes("/agendar/") && !previousUrl.includes("/sucesso/") && previousUrl !== "None") {
		sessionStorage.setItem("previousPage", previousUrl);
	}

	function atualizarModalAgendamentosDia() {
		$.ajax({
			url: "/api/req_agendamentos_dia",
			method: "GET",
			data: {
				dia: $("#id_data").val(),
			},
			success: function (data) {
				// Limpa o conteúdo atual do modal
				$(".modal-body").empty();

				// Adiciona o conteúdo recebido da requisição ao modal
				$(".modal-body").append("A cirurgia irá cancelar todos os atendimentos do dia. Deseja continuar?");
				if (data.length > 0) {
					$(".modal-body").append("<br/><br/> <span style='font-weight: bold; display: block'>Agendamentos afetados:</span>");
					for (let i = 0; i < data.length; i++) {
						if (data[i].horario !== null) {
							$(".modal-body").append(data[i].horario.split(":")[0] + ":" + data[i].horario.split(":")[1] + " - ");
						}
						$(".modal-body").append(data[i].nome_do_tutor);
						if (data[i].tipo_de_agendamento.length > 1) {
							$(".modal-body").append(" / " + data[i].tipo_de_agendamento);
						}
						$(".modal-body").append("<br/>");
					}
				}

				$("#confirmModal").modal("show");
			},
			error: function (jqXHR, textStatus, errorThrown) {
				// Trata erros de requisição
				console.error("Erro ao fazer requisição:", errorThrown);
			},
		});
	}

	function atualizarModalAgendamentoHorario() {
		$.ajax({
			url: "/api/req_agendamento_horario",
			method: "GET",
			data: {
				dia: $("#id_data").val(),
				hora: $("#id_horario").val(),
			},
			success: function (data) {
				// Limpa o conteúdo atual do modal
				$(".modal-body").empty();

				// Adiciona o conteúdo recebido da requisição ao modal
				$(".modal-body").append("Este agendamento irá substituir o agendamento a seguir. Deseja continuar?");
				if (data.length > 0) {
					$(".modal-body").append("<br/><br/> <span style='font-weight: bold; display: block'>Agendamento afetado:</span>");
					for (let i = 0; i < data.length; i++) {
						$(".modal-body").append(data[i].horario.split(":")[0] + ":" + data[i].horario.split(":")[1] + " - ");
						$(".modal-body").append(data[i].nome_do_tutor);
						if (data[i].tipo_de_agendamento.length > 1) {
							$(".modal-body").append(" / " + data[i].tipo_de_agendamento);
						}
					}
				}

				$("#confirmModal").modal("show");
			},
			error: function (jqXHR, textStatus, errorThrown) {
				// Trata erros de requisição
				console.error("Erro ao fazer requisição:", errorThrown);
			},
		});
	}

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

	/**
	 * Este evento é acionado quando a caixa de confirmação é alterada.
	 * Desabilita o botão "Cadastrar" se a caixa não estiver marcada.
	 */
	document.getElementById("confirmacao").addEventListener("change", function () {
		// Obter o botão "Cadastrar"
		var botao = document.querySelector(".botao_cadastrar");
		// Desabilitar o botão se a caixa não estiver marcada
		botao.disabled = !this.checked;
	});

	// Definir a configuração do datepicker para Português (Brasil)
	$.datepicker.setDefaults($.datepicker.regional["pt-BR"]);

	/**
	 * Esta função gera um array de datas que não estão disponíveis para agendamento.
	 * @returns {Array} Um array de datas que não estão disponíveis para agendamento
	 */
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

	// Gerar o array de datas indisponíveis
	var disabledDates = gerar_dias_indisponiveis();

	let selectedDate;

	/**
	 * Esta função desabilita certas datas no datepicker.
	 * @param {Date} date - A data a ser verificada
	 * @returns {Array} - Um array com o primeiro elemento indicando se a data está habilitada ou não, e o segundo elemento sendo uma string vazia.
	 */
	function disableDates(date) {
		const noWeekends = $.datepicker.noWeekends(date);
		if (!noWeekends[0]) {
			return noWeekends; // Se for um fim de semana, retorne falso.
		}

		const formattedDate = $.datepicker.formatDate("yy-mm-dd", date);
		if (disabledDates.includes(formattedDate)) {
			if (isUserAuthenticated) return [true, "data_indisponivel", "Indisponível"];
			else return [false, "", "Indisponível"];
		}
		return [true, ""];
	}

	// Configurar o datepicker
	$("#datePicker").datepicker({
		dateFormat: "DD, d 'de' M 'de' yy",
		minDate: 0,
		beforeShowDay: disableDates,
		onSelect: function (dateText, inst) {
			selectedDate = $(this).datepicker("getDate");
			selectedDateDjangoFomat = $.datepicker.formatDate("yy-mm-dd", selectedDate);
			// Carregar as opções disponíveis para a data selecionada
			carregarOpcoesHorario(converterSelectedDateEmHorario(selectedDateDjangoFomat));
			$("#id_data").val(selectedDateDjangoFomat);
			$(this).removeClass("input_invalido");
			$("#id_data").next(".error").text("").hide();
		},
	});

	// Definir a data inicial se especificada no formulário
	var dataInicial = $("#id_data").val();
	if (dataInicial) {
		if (dataInicial.substr(2, 1) === "/") {
			dateF = $.datepicker.parseDate("dd/mm/yy", dataInicial);
			$("#datePicker").datepicker("setDate", dateF);
			document.querySelector("#id_data").value = dataInicial.split("/")[2] + "-" + dataInicial.split("/")[1] + "-" + dataInicial.split("/")[0];
		} else if (dataInicial.substr(4, 1) === "-") {
			dateF = $.datepicker.parseDate("yy-mm-dd", dataInicial);
			$("#datePicker").datepicker("setDate", dateF);
		}
	}

	/**
	 * Esta função converte a data selecionada para um array indicando quais opções estão disponíveis para essa data.
	 * @param {string} date - A data selecionada no formato "yyyy-mm-dd"
	 * @returns {Array} - Um array com cinco elementos indicando se cada opção está disponível ou não.
	 */
	function converterSelectedDateEmHorario(date) {
		let objectDate = horariosIndisponiveis.filter((obj) => obj.data === date);
		if (objectDate[0]) {
			return [false, objectDate[0].horario_14, objectDate[0].horario_15, objectDate[0].horario_16, objectDate[0].horario_17];
		} else {
			return [false, false, false, false, false];
		}
	}

	/**
	 * Esta função carrega as opções disponíveis para a data selecionada.
	 * @param {Array} estadoHorarios - Um array indicando quais opções estão disponíveis para a data selecionada
	 */
	function carregarOpcoesHorario(estadoHorarios) {
		// Primeiro, redefinir todas as opções para habilitadas
		for (let i = 0; i < selectHorario.options.length; i++) {
			selectHorario.options[i].disabled = false;
		}

		// Desabilitar as opções com base no estado de horarios
		for (let i = 0; i < estadoHorarios.length; i++) {
			if (estadoHorarios[i]) {
				if (isUserAuthenticated) {
					selectHorario.options[i].classList.add("data_indisponivel");
				} else {
					selectHorario.options[i].disabled = true;
				}
			} else {
				selectHorario.options[i].classList.remove("data_indisponivel");
			}
		}

		// Limpar a opção selecionada se ela agora estiver desabilitada
		if (selectHorario.selectedIndex >= 0 && selectHorario.options[selectHorario.selectedIndex].disabled) {
			selectHorario.selectedIndex = 0;
		}
	}

	// Carregar as opções disponíveis para a data inicial se especificada no formulário
	if ($("#datePicker").val()) {
		selectedDate = $("#datePicker").datepicker("getDate");
		selectedDateDjangoFomat = $.datepicker.formatDate("yy-mm-dd", selectedDate);
		carregarOpcoesHorario(converterSelectedDateEmHorario(selectedDateDjangoFomat));
	} else carregarOpcoesHorario[(false, true, true, true, true)];
});
