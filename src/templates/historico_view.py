import flet as ft
from services.abastecimento_services import listar_abastecimentos, listar_abastecimentos_por_veiculo
from services.veiculos_service import listar_veiculos

def get_historico_view(id_usuario):
    mensagem = ft.Text("")

    tabela = ft.DataTable(visible=False, columns=[ft.DataColumn(ft.Text(""))], rows=[])
    # opccoes de filtro por tipo de combustivel
    filtro_tipo = ft.Dropdown(
        label="Tipo de Combustível",
        options=[
            ft.dropdown.Option("Alcool"),
            ft.dropdown.Option("Alcool Aditivado"),
            ft.dropdown.Option("Gasolina"),
            ft.dropdown.Option("Gasolina Aditivada"),
            #ft.dropdown.Option("Diesel"),
        ],
        visible=False
    )

    # Busca todos os veículos do usuário
    veiculos_usuario = [v for v in listar_veiculos() if v.id_usuario == id_usuario]
    veiculo_ids = [v.id for v in veiculos_usuario]

    def mostrar_historico(e):
        tabela.columns = [
            ft.DataColumn(ft.Text("Data")),
            ft.DataColumn(ft.Text("Veículo")),
            ft.DataColumn(ft.Text("Tipo")),
            ft.DataColumn(ft.Text("Valor/Litro")),
            ft.DataColumn(ft.Text("Valor Abastecido")),
            ft.DataColumn(ft.Text("Km")),
        ]
        tabela.visible = True
        filtro_tipo.visible = False
        linhas = []
        for v in veiculos_usuario:
            # intera sobre a lista e chama a função para listar os abastecimentos de cada veiculo
            abastecimentos = listar_abastecimentos_por_veiculo(v.id)
            for a in abastecimentos:
                linhas.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(a.data_abastecimento.strftime("%d/%m/%Y %H:%M") if a.data_abastecimento else "")),
                            ft.DataCell(ft.Text(f"{v.modelo} - {v.placa}")),
                            ft.DataCell(ft.Text(a.tipo_combustivel)),
                            ft.DataCell(ft.Text(f"R$ {a.valor_litro:,.2f}".replace(".", "X").replace(",", ".").replace("X", ","))),
                            ft.DataCell(ft.Text(f"R$ {a.valor_abastecido:,.2f}".replace(".", "X").replace(",", ".").replace("X", ","))),
                            ft.DataCell(ft.Text(str(a.kilometragem_atual))),
                        ]
                    )
                )
        tabela.rows = linhas
        tabela.update()
        filtro_tipo.update()
    # filtro por valor
    def mostrar_valor(e):
        tabela.visible = True
        filtro_tipo.visible = False
        tabela.columns = [
            ft.DataColumn(ft.Text("Mês/Ano")),
            ft.DataColumn(ft.Text("Total Abastecido (R$)")),
        ]
        # Agrupa por mês/ano
        # soma os valores e retorna o tortal por mes/ano
        from collections import defaultdict
        import datetime
        consumo_mensal = defaultdict(float)
        for v in veiculos_usuario:
            abastecimentos = listar_abastecimentos_por_veiculo(v.id)
            for a in abastecimentos:
                if a.data_abastecimento:
                    chave = a.data_abastecimento.strftime("%m/%Y")
                    consumo_mensal[chave] += a.valor_abastecido
        tabela.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(mes)),
                    ft.DataCell(ft.Text(f"R$ {valor:,.2f}".replace(".", "X").replace(",", ".").replace("X", ","))),
                ]
            ) for mes, valor in sorted(consumo_mensal.items())
        ]
        tabela.update()
        filtro_tipo.update()

    def mostrar_tipo(e):
        filtro_tipo.visible = True
        tabela.visible = False
        filtro_tipo.update()
        tabela.update()

    def filtrar_por_tipo(e):
        tipo = filtro_tipo.value
        tabela.visible = True
        tabela.columns = [
            ft.DataColumn(ft.Text("Data")),
            ft.DataColumn(ft.Text("Veículo")),
            ft.DataColumn(ft.Text("Tipo")),
            ft.DataColumn(ft.Text("Valor/Litro")),
            ft.DataColumn(ft.Text("Valor Abastecido")),
            ft.DataColumn(ft.Text("Km")),
        ]
        linhas = []
        for v in veiculos_usuario:
            abastecimentos = listar_abastecimentos_por_veiculo(v.id)
            for a in abastecimentos:
                if a.tipo_combustivel == tipo:
                    linhas.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(a.data_abastecimento.strftime("%d/%m/%Y %H:%M") if a.data_abastecimento else "")),
                                ft.DataCell(ft.Text(f"{v.modelo} - {v.placa}")),
                                ft.DataCell(ft.Text(a.tipo_combustivel)),
                                ft.DataCell(ft.Text(f"R$ {a.valor_litro:,.2f}".replace(".", "X").replace(",", ".").replace("X", ","))),
                                ft.DataCell(ft.Text(f"R$ {a.valor_abastecido:,.2f}".replace(".", "X").replace(",", ".").replace("X", ","))),
                                ft.DataCell(ft.Text(str(a.kilometragem_atual))),
                            ]
                        )
                    )
        tabela.rows = linhas
        tabela.update()

    filtro_tipo.on_change = filtrar_por_tipo

    card_historico = ft.Card(
        content=ft.Container(
            ft.Column([
                ft.Icon(ft.Icons.HISTORY, size=40, color=ft.Colors.BLUE),
                ft.Text("Histórico", size=18, weight="bold")
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            on_click=mostrar_historico,
            padding=10,
            bgcolor=ft.Colors.BLUE_100,
            border_radius=8,
            alignment=ft.alignment.center,
            width=120,   # largura fixa
            height=120   # altura fixa
        ),
        animate_scale=5,
        visible=True,
        margin=ft.margin.all(10)
    )

    card_valor = ft.Card(
        content=ft.Container(
            ft.Column([
                ft.Icon(ft.Icons.ATTACH_MONEY, size=40, color=ft.Colors.GREEN),
                ft.Text("Valor", size=18, weight="bold")
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            on_click=mostrar_valor,
            padding=10,
            bgcolor=ft.Colors.GREEN_100,
            border_radius=8,
            alignment=ft.alignment.center,
            width=120,   # largura fixa
            height=120   # altura fixa
        ),
        animate_scale=5,
        visible=True,
        margin=ft.margin.all(10)
    )

    card_tipo = ft.Card(
        content=ft.Container(
            ft.Column([
                ft.Icon(ft.Icons.LOCAL_GAS_STATION, size=40, color=ft.Colors.ORANGE),
                ft.Text("Tipo", size=18, weight="bold")
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            on_click=mostrar_tipo,
            padding=10,
            bgcolor=ft.Colors.ORANGE_100,
            border_radius=8,
            alignment=ft.alignment.center,
            width=120,   # largura fixa
            height=120   # altura fixa
        ),
        animate_scale=5,
        visible=True,
        margin=ft.margin.all(10)
    )
    return ft.Column(
        [
            ft.ResponsiveRow(
                controls=[
                    ft.Container(card_historico,col={"xs":12, "md":6}), 
                    ft.Container(card_valor, col={"xs":12, "md":6}), 
                    ft.Container(card_tipo, col={"xs":12, "md":6})], alignment=ft.MainAxisAlignment.CENTER),
            filtro_tipo,
            tabela,
            mensagem
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True
    )