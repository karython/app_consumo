import flet as ft
import datetime
from services.veiculos_service import criar_veiculo, listar_veiculos, deletar_veiculo, buscar_veiculo_por_id, atualizar_veiculo

def get_veiculo_view(id_usuario):
    # controle de formulário
    form_cadastro = ft.Column(visible=False, scroll=ft.ScrollMode.AUTO, expand=True)
    container_veiculos = ft.Column(visible=False, scroll=ft.ScrollMode.AUTO)
    form_edicao = ft.Column(visible=False)

    # cores
    bg_padrao = ft.Colors.BLUE_100
    bg_secundaria = ft.Colors.GREEN_100
    bg_hover = ft.Colors.BLUE_200

    # efeito hover
    def efeito_hover(e):
        e.control.bgcolor = bg_hover if e.data == "true" else bg_padrao
        e.control.scale = 1.05 if e.data == "true" else 1.0

    # ------------------------------------------------------------- FORMULÁRIO CADASTRO ------------------------------------------------
    def formulario_cadastro():
        modelo = ft.TextField(label="Modelo", label_style=ft.TextStyle(size=14), height=50)
        tipo_veiculo = ft.Dropdown(
            label="Tipo",
            options=[ft.dropdown.Option("Carro"), ft.dropdown.Option("Moto")],
            expand=True
        )
        ano_fabricacao = ft.TextField(label="Ano de Fabricação", value="1990", height=50)
        fabricante = ft.TextField(label="Fabricante", height=50)
        kilometragem = ft.TextField(label="Kilometragem", height=50)
        placa = ft.TextField(label="Placa", height=50)
        tipo_combustivel = ft.Dropdown(
            label="Combustível",
            options=[
                ft.dropdown.Option("Gasolina"),
                ft.dropdown.Option("Alcool"),
                ft.dropdown.Option("Flex")
            ],
            expand=True
        )

        def incrementar(e):
            cap_total_tanque.value = str(int(cap_total_tanque.value) + 1)
            form_cadastro.update()

        def decrementar(e):
            if int(cap_total_tanque.value) > 0:
                cap_total_tanque.value = str(int(cap_total_tanque.value) - 1)
                form_cadastro.update()

        botao_menos = ft.IconButton(
            icon=ft.Icons.REMOVE, 
            on_click=decrementar
        )

        botao_mais = ft.IconButton(
            icon=ft.Icons.ADD, 
            on_click=incrementar
)
        cap_total_tanque = ft.TextField(
            label="Cap. Tanque (L)", 
            value="45", 
            prefix_icon=botao_menos, 
            suffix_icon=botao_mais)



        return modelo, tipo_veiculo, ano_fabricacao, fabricante, kilometragem, placa, tipo_combustivel, cap_total_tanque, incrementar, decrementar

    # ------------------------------------------------------------- MOSTRAR FORM CADASTRO ------------------------------------------------
    def mostrar_formulario(e):
        if form_cadastro.visible:
                form_cadastro.visible = False
                form_cadastro.controls.clear()
                form_cadastro.update()
                return

        modelo, tipo_veiculo, ano_fabricacao, fabricante, kilometragem, placa, tipo_combustivel, cap_total_tanque, incrementar, decrementar = formulario_cadastro()

        def cadastrar_veiculo(e):
            criar_veiculo(
                modelo.value,
                tipo_veiculo.value,
                int(ano_fabricacao.value),
                fabricante.value,
                int(kilometragem.value),
                placa.value,
                tipo_combustivel.value,
                int(cap_total_tanque.value),
                id_usuario
            )
            form_cadastro.visible = False
            form_cadastro.controls.clear()
            form_cadastro.update()
            atualizar_lista_veiculos()

        form_cadastro.controls = [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Cadastro de Veículo", size=22, weight=ft.FontWeight.BOLD),

                        ft.ResponsiveRow(
                            controls=[
                                ft.Container(modelo, col=6, padding=5),
                                ft.Container(tipo_veiculo, col=6, padding=5),
                            ]
                        ),

                        ft.ResponsiveRow(
                            controls=[
                                ft.Container(ano_fabricacao, col=6, padding=5),
                                ft.Container(fabricante, col=6, padding=5),
                            ]
                        ),

                        ft.ResponsiveRow(
                            controls=[
                                ft.Container(kilometragem, col=6, padding=5),
                                ft.Container(placa, col=6, padding=5),
                            ]
                        ),
                       

                        ft.ResponsiveRow(
                            controls=[
                                ft.Container(tipo_combustivel, col=12, padding=5),
                            ]
                        ),

                        ft.Row(
                            controls=[
                                
                                ft.Container(cap_total_tanque, width=120),  # controla a largura
                                ft.IconButton(icon=ft.Icons.CHECK, bgcolor=ft.Colors.BLUE_100, on_click=cadastrar_veiculo)
                            ], alignment=ft.MainAxisAlignment.END
                            
                        )
                    ],
                    spacing=10
                ),
                padding=20,
                border_radius=10,
                bgcolor=ft.Colors.GREY_100,
                margin=ft.Margin(left=10, top=10, right=10, bottom=10)
            )
        ]
        container_veiculos.visible = False   # fecha o outro card
        container_veiculos.update()
        form_cadastro.visible = True
        form_cadastro.update()
        # ------------------------------------------------------------- MOSTRAR VEICULOS (TABELA) ------------------------------------------------
    mensagem_feedback = ft.Text("", color=ft.Colors.BLACK)

    lista_veiculos = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Modelo")),
            ft.DataColumn(ft.Text("Editar")),
            ft.DataColumn(ft.Text("Excluir"))
        ],
        rows=[]
    )

    def atualizar_lista_veiculos():
        veiculos = [v for v in listar_veiculos() if v.id_usuario == id_usuario]
        if not veiculos:
            mensagem_feedback.value = "Nenhum veículo cadastrado."
            mensagem_feedback.color = ft.Colors.GREY
            mensagem_feedback.update()
            lista_veiculos.rows = []
            lista_veiculos.update()
            return
        mensagem_feedback.value = ""
        mensagem_feedback.update()

        lista_veiculos.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(v.modelo)),
                    ft.DataCell(
                        ft.IconButton(
                            icon=ft.Icons.CREATE,
                            tooltip="Editar veículo",
                            on_click=lambda e, vid=v.id: on_editar(vid)
                        )
                    ),
                    ft.DataCell(
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            tooltip="Deletar veículo",
                            on_click=lambda e, vid=v.id: on_delete(vid)
                        )
                    ),
                ]
            ) for v in veiculos
        ]
        lista_veiculos.update()

    def mostrar_veiculos(e):
        if container_veiculos.visible:
                container_veiculos.visible = False
        else:
            form_cadastro.visible = False
            form_cadastro.controls.clear()   # esvazia se estava aberto
            form_cadastro.update()
            atualizar_lista_veiculos()
            container_veiculos.visible = True
        container_veiculos.update()

    def on_delete(veiculo_id):
        if deletar_veiculo(veiculo_id):
            mensagem_feedback.value = "Veículo deletado com sucesso!"
            mensagem_feedback.color = ft.Colors.GREEN
            mensagem_feedback.update()
            atualizar_lista_veiculos()
        else:
            mensagem_feedback.value = "Erro ao deletar veículo."
            mensagem_feedback.color = ft.Colors.RED
            mensagem_feedback.update()
        
        
    def on_editar(veiculo_id):
        # buscar o veículo pelo id
        veiculo = buscar_veiculo_por_id(veiculo_id)

        if not veiculo:
            mensagem_feedback.value = f"Veículo {veiculo_id} não encontrado!"
            mensagem_feedback.color = ft.Colors.RED
            mensagem_feedback.update()
            return
        
        # cria campos de edição preenchidos com valores do banco
        modelo_input = ft.TextField(label="Modelo", value=veiculo.modelo)
        placa_input = ft.TextField(label="Placa", value=veiculo.placa)
        fabricante_input = ft.TextField(label="Fabricante", value=veiculo.fabricante)
        
        def editar_veiculo(e):
            atualizar_veiculo(
                veiculo.id,
                modelo_input.value,
                fabricante_input.value,
                placa_input.value
            )

            # ao salvar, fecha form edicao e reabre a lista
            form_edicao.visible = False
            form_edicao.controls.clear()
            form_edicao.update()
            lista_veiculos.visible = True
            lista_veiculos.update()
            atualizar_lista_veiculos()
        
        def fechar_edicao(e):
            # ao cancelar, volta a exibir a lista de veículos
            form_edicao.controls.clear()
            form_edicao.visible = False
            form_edicao.update()
            lista_veiculos.visible = True
            lista_veiculos.update()

        # monta o formulário de edição
        form_edicao.controls = [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Edição de Veículo", size=22, weight=ft.FontWeight.BOLD),
                        ft.ResponsiveRow(
                            controls=[
                                ft.Container(modelo_input, col=6, padding=5),
                                ft.Container(placa_input, col=6, padding=5),
                            ]
                        ),
                        ft.ResponsiveRow(
                            controls=[
                                ft.Container(fabricante_input, padding=5),
                            ]
                        ),
                        ft.Row(
                            controls=[
                                ft.IconButton(
                                    icon=ft.Icons.CHECK,
                                    bgcolor=ft.Colors.GREEN_300,
                                    on_click=editar_veiculo
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.CLOSE,
                                    bgcolor=ft.Colors.RED_300,
                                    on_click=fechar_edicao
                                )
                            ],
                            alignment=ft.MainAxisAlignment.END
                        )
                    ],
                    spacing=10
                ),
                padding=20,
                border_radius=10,
                bgcolor=ft.Colors.GREY_100,
                margin=ft.Margin(left=10, top=10, right=10, bottom=10)
            )
        ]
        form_edicao.visible = True
        form_edicao.update()
        lista_veiculos.visible = False
        lista_veiculos.update()



        '''mensagem_feedback.value = f"Função de edição para {veiculo_id} ainda não implementada."
        mensagem_feedback.color = ft.Colors.ORANGE
        mensagem_feedback.update()'''

    container_veiculos.controls = [
        mensagem_feedback,
        lista_veiculos
    ]

    # ------------------------------------------------------------- CARDS DE ACESSO ------------------------------------------------
    card_cadastro = ft.Card(
        content=ft.Container(
            ft.Column([
                ft.Icon(name=ft.Icons.DIRECTIONS_CAR, size=40, color=ft.Colors.BLUE),
                ft.Text("Novo Veículo", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            on_click=mostrar_formulario,  # <<< coloque aqui
            on_hover=efeito_hover,
            padding=10,
            bgcolor=bg_padrao,
            border_radius=8,
            alignment=ft.alignment.center
        ),
        animate_scale=5,
        
        visible=True,
        margin=ft.margin.all(10)
    )


    card_veiculos = ft.Card(
        content=ft.Container(
            ft.Column([
                ft.Icon(name=ft.Icons.DIRECTIONS_CAR, size=40, color=ft.Colors.GREEN_400),
                ft.Text("Veículos", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            on_click=mostrar_veiculos,  # <<< aqui também
            on_hover=efeito_hover,
            padding=10,
            bgcolor=bg_secundaria,
            border_radius=8,
            alignment=ft.alignment.center
        ),
        animate_scale=5,
        
        visible=True,
        margin=ft.margin.all(10)
    )


    # ------------------------------------------------------------- RETORNO ------------------------------------------------
    return ft.SafeArea(
        content=ft.Container(
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.ResponsiveRow(
                        controls=[
                            ft.Container(card_cadastro, col={"xs":12, "md":6}),
                            ft.Container(card_veiculos, col={"xs":12, "md":6}),
                        ],
                        spacing=5
                    ),
                    form_cadastro,
                    form_edicao,

                        ft.Row(
                            [container_veiculos],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        # centralizando o container dos veiculos a partir de seu container, porem nao pode ter o expand=true
                   
                ]
            )
        )
    )
