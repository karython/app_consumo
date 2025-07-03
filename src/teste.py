import flet as ft

def main(page: ft.Page):
    page.title = "Exemplo de Alinhamentos"
    page.bgcolor = ft.Colors.GREY_200
    page.window_width = 600
    page.window_height = 600

    # exemplo de container
    container = ft.Container(
        content=ft.Text("Sou um Container centralizado"),
        bgcolor=ft.Colors.BLUE_100,
        padding=20,
        border_radius=10,
        alignment=ft.alignment.center   # alinha o texto dentro do container
    )

    # exemplo de row
    row = ft.Row(
        controls=[
            ft.Container(ft.Text("Item 1"), bgcolor=ft.Colors.RED_100, padding=10),
            ft.Container(ft.Text("Item 2"), bgcolor=ft.Colors.GREEN_100, padding=10),
            ft.Container(ft.Text("Item 3"), bgcolor=ft.Colors.YELLOW_100, padding=10),
        ],
        alignment=ft.MainAxisAlignment.SPACE_AROUND,   # espaço ao redor
        vertical_alignment=ft.CrossAxisAlignment.CENTER
    )

    # exemplo de column
    column = ft.Column(
        controls=[
            ft.Text("Exemplo de Column", weight="bold"),
            ft.Container(ft.Text("Conteúdo 1"), bgcolor=ft.Colors.PURPLE_100, padding=10),
            ft.Container(ft.Text("Conteúdo 2"), bgcolor=ft.Colors.PURPLE_200, padding=10),
            ft.Container(ft.Text("Conteúdo 3"), bgcolor=ft.Colors.PURPLE_300, padding=10),
        ],
        alignment=ft.MainAxisAlignment.START,  # alinha no topo da coluna
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # centraliza horizontalmente os filhos
        expand=True,
        scroll=ft.ScrollMode.AUTO  # permite rolar caso falte espaço
    )

    btn = ft.ElevatedButton(text="botao 1", bgcolor="blue", color=ft.Colors.WHITE)
    btn2 = ft.ElevatedButton(text="botao 2", bgcolor="blue", color=ft.Colors.WHITE)
    btn3 = ft.ElevatedButton(text="botao 3", bgcolor="blue", color=ft.Colors.WHITE)
    
    page.add(ft.Row(controls=[btn, btn2, btn3],alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.END, expand=True))

    
    

ft.app(main)
