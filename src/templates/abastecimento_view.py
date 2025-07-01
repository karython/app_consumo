import flet as ft
from services.abastecimento_services import criar_abastecimento, buscar_ultimo_km_por_veiculo
from services.veiculos_service import listar_veiculos

def get_abastecimento_view(id_usuario):
    mensagem = ft.Text("", color=ft.Colors.GREEN)

    # Função para formatar moeda (mantida igual)
    def formatar_moeda(e: ft.ControlEvent):
        preco = e.control.value
        numeros = ''.join(filter(str.isdigit, preco))
        if numeros:
            preco_float = int(numeros) / 100
            preco_formatado = f"R$ {preco_float:,.2f}".replace(".", "X").replace(",", ".").replace("X", ",")
            e.control.value = preco_formatado
        else:
            e.control.value = ""
        e.control.update()

    # Campo kilometragem - declare apenas 1 vez!
    kilometragem_atual = ft.TextField(label="Kilometragem Atual", width=250, keyboard_type=ft.KeyboardType.NUMBER)

    # Função para atualizar km ao mudar veículo selecionado
    def atualizar_km(e):
        if dropdown_veiculo.value:
            ultimo_km = buscar_ultimo_km_por_veiculo(int(dropdown_veiculo.value))
            if ultimo_km is not None:
                kilometragem_atual.value = str(ultimo_km)
            else:
                kilometragem_atual.value = ""
            kilometragem_atual.update()

    # Dropdown de veículo (usa atualizar_km no on_change)
    veiculos_usuario = [v for v in listar_veiculos() if v.id_usuario == id_usuario]
    dropdown_veiculo = ft.Dropdown(
        label="Selecione o veículo",
        options=[
            ft.dropdown.Option(str(v.id), f"{v.modelo} - {v.placa}") for v in veiculos_usuario
        ],
        width=250,
        on_change=atualizar_km
    )

    # resto do seu código continua igual, sem redeclarar kilometragem_atual
    tipo_combustivel = ft.Dropdown(
        label="Tipo de Combustível",
        options=[
            ft.dropdown.Option("Alcool"),
            ft.dropdown.Option("Alcool Aditivado"),
            ft.dropdown.Option("Gasolina"),
            ft.dropdown.Option("Gasolina Aditivada"),
            #ft.dropdown.Option("Diesel"),
        ],
        width=250
    )
    valor_litro = ft.TextField(
        label="Valor por Litro (R$)",
        width=250,
        keyboard_type=ft.KeyboardType.NUMBER,
        on_change=formatar_moeda
    )
    valor_abastecido = ft.TextField(
        label="Valor Abastecido (R$)",
        width=250,
        keyboard_type=ft.KeyboardType.NUMBER,
        on_change=formatar_moeda
    )

    def salvar_abastecimento(e):
        if not dropdown_veiculo.value or not tipo_combustivel.value or not valor_litro.value or not valor_abastecido.value or not kilometragem_atual.value:
            mensagem.value = "Preencha todos os campos!"
            mensagem.color = ft.Colors.RED
            mensagem.update()
            return
        try:
            criar_abastecimento(
                id_veiculo=int(dropdown_veiculo.value),
                tipo_combustivel=tipo_combustivel.value,
                valor_litro=float(valor_litro.value.replace("R$", "").replace(".", "").replace(",", ".").strip()),
                valor_abastecido=float(valor_abastecido.value.replace("R$", "").replace(".", "").replace(",", ".").strip()),
                kilometragem_atual=int(kilometragem_atual.value)
            )
            mensagem.value = "Abastecimento registrado com sucesso!"
            mensagem.color = ft.Colors.GREEN
            mensagem.update()
            valor_litro.value = ""
            valor_abastecido.value = ""
            kilometragem_atual.value = ""
            tipo_combustivel.value = None
            dropdown_veiculo.value = None
        except Exception as ex:
            mensagem.value = f"Erro ao registrar: {ex}"
            mensagem.color = ft.Colors.RED
            mensagem.update()

    return ft.Row(
        [
            ft.Container(
                ft.Column(
                    [
                        ft.Text("Registrar Abastecimento", size=22, weight="bold"),
                        dropdown_veiculo,
                        tipo_combustivel,
                        valor_litro,
                        valor_abastecido,
                        kilometragem_atual,
                        ft.ElevatedButton("Registrar", icon=ft.Icons.SAVE, on_click=salvar_abastecimento),
                        mensagem
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15,
                ),
                padding=30,
                bgcolor=ft.Colors.WHITE,
                border_radius=10,
                shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.GREY_200),
                margin=ft.Margin(0, 100, 0, 0)
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True
    )
