import flet as ft
from services.usuario_service import buscar_usuario_por_id
from services.veiculos_service import listar_veiculos, calcular_media_consumo_por_combustivel
from services.abastecimento_services import buscar_ultimo_km_por_veiculo


def get_perfil_view(usuario_id, on_logout=None):
    usuario = buscar_usuario_por_id(usuario_id)
    nome = usuario.nome if usuario else "Usuário não encontrado"

    # busca todos veículos do usuário
    veiculos = [v for v in listar_veiculos() if v.id_usuario == usuario_id]
    

    if not veiculos:
        cards = [
            ft.Card(
                content=ft.Container(
                    ft.Column(
                        [
                            ft.Icon(ft.Icons.DIRECTIONS_CAR, size=80),
                            ft.Text("Nenhum veículo cadastrado", size=18, weight="bold")
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10
                    ),
                    padding=20
                )
            )
        ]
    else:
        # cria uma lista vazia pra ser colocado os cards
        cards = []
        for v in veiculos:
            media_gasolina = calcular_media_consumo_por_combustivel(v.id, "Gasolina") or "--"
            media_alcool = calcular_media_consumo_por_combustivel(v.id, "Alcool") or "--"
            media_alcool_adtv = calcular_media_consumo_por_combustivel(v.id, "Alcool Aditivada") or "--"
            media_gasolina_adtv = calcular_media_consumo_por_combustivel(v.id, "Gasolina Aditivada") or "--"
            #media_diesel = calcular_media_consumo_por_combustivel(v.id, "Diesel") or "--"
            ultimo_km = buscar_ultimo_km_por_veiculo(v.id)
            km_para_mostrar = ultimo_km if ultimo_km else v.kilometragem

            # Escolhe o ícone conforme o tipo de veículo moto/carro
            if v.tipo_veiculo.lower() == "moto":
                icone_veiculo = ft.Icons.SPORTS_MOTORSPORTS
            else:
                icone_veiculo = ft.Icons.DIRECTIONS_CAR

            # intera sobre a lista e a cada veiculo encontrado cria uma linha para as informações
            dados_veiculo = ft.Column(
                [
                    ft.Row([ft.Text("Carro:", weight="bold"), ft.Text(v.modelo)]),
                    ft.Row([ft.Text("Tipo:", weight="bold"), ft.Text(v.tipo_veiculo)]),
                    ft.Row([ft.Text("Modelo:", weight="bold"), ft.Text(v.fabricante)]),
                    ft.Row([ft.Text("Placa:", weight="bold"), ft.Text(v.placa)]),
                    ft.Row([ft.Text("Consumo Gasolina:", weight="bold"), ft.Text(f"{media_gasolina} km/l")]),
                    ft.Row([ft.Text("Consumo Alcool:", weight="bold"), ft.Text(f"{media_alcool} km/l")]),
                    ft.Row([ft.Text("Consumo Gasolina Adtv.:", weight="bold"), ft.Text(f"{media_gasolina_adtv} km/l")]), # gas. aditivada
                    ft.Row([ft.Text("Consumo Alcool Adtv.:", weight="bold"), ft.Text(f"{media_alcool_adtv} km/l")]), # alcool aditivado
                    #ft.Row([ft.Text("Consumo Diesel:", weight="bold"), ft.Text(f"{media_diesel} km/l")]), # diesel
                    ft.Row([ft.Text("Kilometragem:", weight="bold"), ft.Text(f"{km_para_mostrar} km")]),
                    #ft.Row([ft.Text("Data próxima troca de óleo:", weight="bold"), ft.Text("--/--/----")]),  # placeholder
                    #ft.Row([ft.Text("Km próxima troca de óleo:", weight="bold"), ft.Text("--")]),            # placeholder
                ],
                spacing=5
            )
            # depois de criar as linhas, adiciona na lista de cards
            cards.append(
                ft.Card(
                    content=ft.Container(
                        ft.Column(
                            [
                                ft.Icon(icone_veiculo, size=60),
                                ft.Text(v.modelo, weight="bold", size=18),
                                ft.Divider(),
                                dados_veiculo
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=10
                        ),
                        padding=15,
                        width=300,   # largura padrão do card
                    ),
                    elevation=5,
                )
            )

    # horizontal scroll carrossel, coloca a lista de cards dentro de uma linha com scroll habilitado
    carrossel = ft.Row(
        controls=cards,
        scroll=ft.ScrollMode.AUTO,
        spacing=10
    )

    # cria o boneco de perfil
    avatar = ft.Icon(ft.Icons.PERSON, size=60)
    nome_usuario = ft.Text(nome, weight="bold", size=18)

    botao_logout = ft.ElevatedButton("Logout", icon=ft.Icons.LOGOUT, on_click=lambda e: on_logout() if on_logout else None)
    # organiza os componentes que irão na tela
    layout = ft.Column(
        [
            
            ft.Row([avatar, nome_usuario], alignment=ft.MainAxisAlignment.CENTER),
            botao_logout,
            # crie uma linha divisoria
            ft.Divider(),
            carrossel,
            
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return ft.SafeArea(
        content=ft.Container(
            layout,
            padding=20
        )
    )
