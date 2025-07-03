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
                            ft.DataCell(ft.Text(f"{v.modelo}")),
                            ft.DataCell(ft.Text(a.tipo_combustivel)),
                            ft.DataCell(ft.Text(f"R$ {a.valor_litro:,.2f}".replace(".", "X").replace(",", ".").replace("X", ","))),
                            ft.DataCell(ft.Text(f"R$ {a.valor_abastecido:,.2f}".replace(".", "X").replace(",", ".").replace("X", ","))),
                            
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
                                ft.DataCell(ft.Text(f"{v.modelo}")),
                                ft.DataCell(ft.Text(a.tipo_combustivel)),
                                ft.DataCell(ft.Text(f"R$ {a.valor_litro:,.2f}".replace(".", "X").replace(",", ".").replace("X", ","))),
                                ft.DataCell(ft.Text(f"R$ {a.valor_abastecido:,.2f}".replace(".", "X").replace(",", ".").replace("X", ","))),
                                
                            ]
                        )
                    )
        tabela.rows = linhas
        tabela.update()

    filtro_tipo.on_change = filtrar_por_tipo

    # substituindo cards por IconButtons
    botao_historico = ft.IconButton(
        icon=ft.Icons.HISTORY,
        icon_size=40,
        tooltip="Histórico",
        on_click=mostrar_historico,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.BLUE_100,
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
    )

    botao_valor = ft.IconButton(
        icon=ft.Icons.ATTACH_MONEY,
        icon_size=40,
        tooltip="Valor",
        on_click=mostrar_valor,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.GREEN_100,
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
    )

    botao_tipo = ft.IconButton(
        icon=ft.Icons.LOCAL_GAS_STATION,
        icon_size=40,
        tooltip="Tipo",
        on_click=mostrar_tipo,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.ORANGE_100,
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
    )


    # mesma lógica do seu código
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[botao_historico, botao_tipo, botao_valor],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Divider(),
                ft.Column(
                    controls=[
                        ft.Container(
                            content=filtro_tipo,
                            alignment=ft.alignment.center,
                            expand=False,
                        ),
                        ft.Container(
                            content=tabela,
                            alignment=ft.alignment.center,
                            expand=False,
                        ),
                        
                        mensagem,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.AUTO,
                ),
            ]
        ),
        expand=True,
        padding=10,
        margin=ft.margin.only(top=20)
    )
