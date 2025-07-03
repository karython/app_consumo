'''import flet as ft
from services.usuario_service import buscar_usuario_por_id
from services.veiculos_service import listar_veiculos, deletar_veiculo, atualizar_veiculo

def get_perfil_view(usuario_id, on_logout=None):
    usuario = buscar_usuario_por_id(usuario_id)
    nome = usuario.nome if usuario else "Usuário não encontrado"

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
        veiculos = [v for v in listar_veiculos() if v.id_usuario == usuario_id]
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

    def fazer_logout(e):
        if on_logout:
            on_logout()

    informacoes = ft.Column(
        controls=[
            ft.Icon(ft.Icons.PERSON, size=80),
            ft.Text(f"Usuário: {nome}", size=20, weight="bold"),
            ft.ElevatedButton("Logout", icon=ft.Icons.LOGOUT, on_click=fazer_logout),
            
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

    return ft.SafeArea(
        content=ft.Container(
            ft.Column([informacoes]),
            alignment=ft.alignment.center,
            margin=ft.Margin(0,100,0,0)
        )
    )
'''