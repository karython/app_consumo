import flet as ft
import datetime
from services.veiculos_service import criar_veiculo, listar_veiculos,deletar_veiculo

def get_veiculo_view(id_usuario):
     
    form_cadastro = ft.Column(controls=[], visible=False, scroll=ft.ScrollMode.AUTO, expand=True)
    container_veiculos = ft.Column(visible=False,scroll=ft.ScrollMode.AUTO, expand=True)

    # mostrar card de cadastrar veiculo
    bg_padrao = ft.Colors.BLUE_100
    bg_secundaria = ft.Colors.GREEN_100
    bg_houve = ft.Colors.BLUE_200
  

    ano_label = ft.Text("Ano de fabricação não definido")
    # precisa criar uma função para aplicar efeito
    def efeito_houver(e):
        e.control.bgcolor = bg_houve if e.data == "true" else bg_padrao
        e.control.scale = 1.05 if e.data == "true" else 1.0
        


# ---------------------------------------------------------- Formulario de cadastro ------------------------------------------------
    def formulario_cadastro():
        modelo = ft.TextField(label="Modelo",label_style=ft.TextStyle(size=14),height=50)
        tipo_veiculo =ft.Dropdown(
            label="Tipo",
            # se definir um whidth com algum tamanho nao ficará responsivo
            #width=200,
            options=[
                ft.dropdown.Option("Carro"),
                ft.dropdown.Option("Moto")
            ],
            # alem de nao definir uma largura, passe o parametro expand
            expand=True
            

        )

        ano_fabricacao= ft.TextField(label="Ano de Fabricação", value=1990, label_style=ft.TextStyle(size=14),height=50)
        fabricante = ft.TextField(label="Fabricante", label_style=ft.TextStyle(size=14),height=50)
        kilometragem =ft.TextField(label="Kilometragem", label_style=ft.TextStyle(size=14),height=50)
        placa =ft.TextField(label="Placa", label_style=ft.TextStyle(size=14),height=50)
        tipo_combustivel = ft.Dropdown(
            label="Combustível", label_style=ft.TextStyle(size=14),
            options=[
                ft.dropdown.Option("Gasolina"),
                ft.dropdown.Option("Alcool"),
                ft.dropdown.Option("Flex")
            ],
            expand=True,
            
        )
        cap_total_tanque = ft.TextField(label="Cap.max Tanque", value="45")

        # funções para colocar capacidade de tanque sem precisar digitar
        def incrementar(e):
            cap_total_tanque.value = str(int(cap_total_tanque.value)+1)
            form_cadastro.update()

        def decrementar(e):
            if int(cap_total_tanque.value) > 0:
                cap_total_tanque.value = str(int(cap_total_tanque.value)-1)
                form_cadastro.update()
    
        return modelo, tipo_veiculo, ano_fabricacao, fabricante, kilometragem, placa, tipo_combustivel, cap_total_tanque, incrementar, decrementar
    


# -------------------------------------------------- Função cadastrar veiculo ----------------------------------------------------------------------
    
    def mostrar_formulario(e):
        # verifica o estado de visibilidade, se estiver visivel, ao clicar some e limpa a tela
        if form_cadastro.visible:
            container_veiculos.visible = False
            container_veiculos.update()
            form_cadastro.visible = False
            form_cadastro.controls = []
            form_cadastro.update()
            card_cadastro.update()
            return
       
        # passa as variaveis para a função
        modelo, tipo_veiculo, ano_fabricacao, fabricante, kilometragem, placa, tipo_combustivel, cap_total_tanque, incrementar, decrementar = formulario_cadastro()

        # função interna que passa os dados do formulario para a funcao criar veiculo
        def cadastrar_vaiculo(e):
        
            # pega os valores e joga na função
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
            # apos passar os dados para a funcao oculta o formulario e limpa a tela
            form_cadastro.visible = False
            
            form_cadastro.controls = []
            form_cadastro.update()
            card_cadastro.visible = True
            card_cadastro.update()

        form_cadastro.controls = [
            ft.Container(      
                        content=ft.Column(                                                      
                            controls = [
                                ft.Text("Cadastro de Veículo", size=25),
                                
                                # Campos organizados em duas colunas
                                ft.ResponsiveRow(
                                    controls=[
                                        ft.Container(modelo, col=6),
                                        ft.Container(tipo_veiculo, col=6),
                                        ft.Container(ano_fabricacao, col=6),
                                        ft.Container(fabricante, col=6),
                                        ft.Container(tipo_combustivel, col=12),
                                        ft.Container(kilometragem, col=6),
                                        ft.Container(placa, col=6),
                                        
                                    ],
                                    spacing=10
                                ),

                                # Linha com botões de incremento e decremento
                                ft.ResponsiveRow(
                                    controls=[
                                        ft.IconButton(icon=ft.Icons.REMOVE, on_click=decrementar, col=2),
                                        ft.Container(cap_total_tanque, col=4),
                                        ft.IconButton(icon=ft.Icons.ADD, on_click=incrementar, col=2),
                                        ft.IconButton(icon=ft.Icons.CHECK, on_click=cadastrar_vaiculo, col=4, bgcolor=ft.Colors.GREEN_100)

                                    ]
                                
                                    
                                ),
                            ],
                        # defini o espaco entre os componentes filho do container
                        spacing=15,
                        scroll=ft.ScrollMode.AUTO,
                    
                        
                        ), 
                        # alinhamento do container do formulario
                        padding=20,
                        margin=ft.Margin(left=20, top=0, right=30, bottom=20)
                        
                        
                    )
                ]
        form_cadastro.visible = True
        # quando abrir o formulario de cadastro e mudar direto para de meus veiculos ele fecha o mostrar e limpa a tela
        container_veiculos.visible = False
        container_veiculos.update()
        form_cadastro.update()   
        card_cadastro.update()
        
# --------------------------------------------- funcao para mostrar os veiculos --------------------------------------------
    '''def mostrar_veiculos(e):
    # Toggle: se já está visível, esconde; se não, mostra e atualiza
        if container_veiculos.visible:
            container_veiculos.visible = False
            container_veiculos.update()
            return

        # Se não está visível, mostra e atualiza os cards
        form_cadastro.visible = False
        form_cadastro.update()
        container_veiculos.visible = True

        # primeiro busca o veiculo pelo usuario pela função da service
        veiculos = [v for v in listar_veiculos() if v.id_usuario == id_usuario]
        if not veiculos:
            return ft.Text("Nenhum veículo cadastrado.", color=ft.Colors.GREY)
        else:
            cards = []
            # inteira na lista de carros cadastrados e cria um card para cada
            for v in veiculos:
                cards.append(
                    ft.Container(
                        ft.Card(
                        content=ft.Container(
                            content=ft.Column([
                                ft.Text(f"Modelo: {v.modelo}", size=18, weight=ft.FontWeight.BOLD),
                                ft.Text(f"Tipo: {v.tipo_veiculo}"),
                                ft.Text(f"Ano: {v.ano_fabricacao}"),
                                ft.Text(f"Fabricante: {v.fabricante}"),
                                ft.Text(f"Placa: {v.placa}"),
                                ft.Text(f"Combustível: {v.tipo_combustivel}"),
                                ft.Text(f"Cap. Tanque: {v.cap_max_tanque} L"),
                                ft.Text(f"Km: {v.kilometragem}"),
                            ], spacing=1),
                            padding=10,
                        ),
                        margin=ft.margin.only(bottom=10, right=10, left=10)
                    ), 
                    # definir a quandidade de colunas dos cards do container
                    col=6, margin=None
                    )
                )
            # guarda os cards dentro do container que sera redimensionado
            container_veiculos.controls = [
            ft.ResponsiveRow(
                controls=cards,
                spacing=10,
                run_spacing=0,
                

            )]
        container_veiculos.update()'''
    
    def mostrar_veiculos(e):
        if container_veiculos.visible:
            container_veiculos.visible = False
            container_veiculos.update()
            return

        # Se não está visível, mostra e atualiza os cards
        form_cadastro.visible = False
        form_cadastro.update()
        container_veiculos.visible = True

        mensagem_feedback = ft.Text("", color=ft.Colors.BLACK)

        # guarda os veiculos na lista
        lista_veiculos = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("")),
                ft.DataColumn(ft.Text("")),
                ft.DataColumn(ft.Text(""))
                ],
                rows=[],
                visible=False
            )


        lista_visivel = {"value": False}  # Variável de controle

        
        def atualizar_lista(e=None):
            # Toggle: alterna visibilidade
            lista_visivel["value"] = not lista_visivel["value"]
            lista_veiculos.visible = lista_visivel["value"]

            if not lista_visivel["value"]:
                lista_veiculos.update()
                return
            
            # verifica no banco os veiculos e intera sobre eles
            veiculos = [v for v in listar_veiculos() if v.id_usuario == id_usuario]
            # verifica se esta vazio ou nao
            if not veiculos:
                mensagem_feedback.value = "Nenhum veículo cadastrado."
                mensagem_feedback.color = ft.Colors.GREY
                mensagem_feedback.update()
                lista_veiculos.controls.clear()
                lista_veiculos.update()
                return

            mensagem_feedback.value = ""
            mensagem_feedback.update()

            # cria a lista para exibir os veiculos
            # ... dentro da função atualizar_lista ...
            lista_veiculos.rows = [
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(v.modelo)),
                        ft.DataCell(
                            ft.IconButton(
                                icon=ft.Icons.CREATE_OUTLINED,
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
                )
                for v in veiculos
            ]
            lista_veiculos.update()

        # funcao para deletar o veiculo no banco
        def on_delete(veiculo_id):
            if deletar_veiculo(veiculo_id):
                mensagem_feedback.value = "Veículo deletado com sucesso!"
                mensagem_feedback.color = ft.Colors.GREEN
                mensagem_feedback.update()
                atualizar_lista()
            else:
                mensagem_feedback.value = "Erro ao deletar veículo."
                mensagem_feedback.color = ft.Colors.RED
                mensagem_feedback.update()
        
        # função para deletar o veiculo no banco
        def on_editar(veiculo_id):
            mensagem_feedback.value = f"Função de edição do veículo {veiculo_id} ainda não implementada."
            mensagem_feedback.color = ft.Colors.ORANGE
            mensagem_feedback.update()


        card_veiculos = ft.Column(
            controls=[
                ft.ElevatedButton(
                    "Meus veículos",
                    icon=ft.Icons.DIRECTIONS_CAR,
                    on_click=atualizar_lista
                ),
                mensagem_feedback,
                lista_veiculos,
                
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    # ------------------------------------------- CARD Mostrar veiculos  ------------------------------------

    '''        # FIXME: criar card para mostrar os veículos cadastrados
        card_veiculos = ft.Card(
            content=ft.Container(
                content=ft.Column(
                
                [   # coloca todos os componentes que vao dentro do card
                    # icone e texto do card
                    ft.Icon(name=ft.Icons.DIRECTIONS_CAR, size=40, color=ft.Colors.GREEN_400),
                    ft.Text("Veículos", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0
                
            ), 
            on_click=mostrar_veiculos, # abrir formulario de cadastrar veiculo
            # habilita efeito de click
            
            on_hover=efeito_houver,
            padding=10, # borda interna do card
            bgcolor=bg_secundaria,
            border_radius=10,
            alignment=ft.alignment.center,
            # para aplicar animações é preciso do parametro animate
            animate_scale=5,

            ink=True
            
            
        ), visible=True,margin=ft.margin.all(10)) '''


# -------------------------------------- CARD Cadastrar veiculo -----------------------------------------------

    card_cadastro = ft.Card(
        content=ft.Container(
            content=ft.Column(
            
            [   # coloca todos os componentes que vao dentro do card
                # icone e texto do card
                ft.Icon(name=ft.Icons.DIRECTIONS_CAR, size=40, color=ft.Colors.BLUE),
                ft.Text("Novo Veículo", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0
              
        ), 
        on_click=mostrar_formulario, # abrir formulario de cadastrar veiculo
        # habilita efeito de click
        
        on_hover=efeito_houver,
        padding=10, # borda interna do card
        bgcolor=bg_padrao,
        border_radius=10,
        alignment=ft.alignment.center,
        # para aplicar animações é preciso do parametro animate
        animate_scale=5,

        ink=True
        
        
    ), visible=True,margin=ft.margin.all(10)) # margem externa das bordas da tela

    

    return ft.SafeArea(
    content=ft.Container(
        expand=True,
        content=ft.Column(
            expand=True,
            controls=[ft.ResponsiveRow(
                controls=[
                ft.Container(card_cadastro, col={"xs":12, "md":6}), # ajuste para empilhar em telas pequenas
                ft.Container(card_veiculo, col={"xs":12, "md":6}),
                
                ], spacing=5,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ), 
            form_cadastro, container_veiculos, card]

            #controls=[card_cadastro, form_cadastro, card_veiculos]
        )
    )
)
    # associar os cards ao usuario
    # mostrar card de veiculo cadastrado
    # ao clicar no card de cadastro abre formulario
    # ao clicar no card do veiculo mostrar tabela com informações
    # ao clicar fora dos cards sair das modais

