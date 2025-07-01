import flet as ft

def get_usuario_cadastro_view(on_submit, on_voltar):
    nome = ft.TextField(label="Nome", width=300)
    email = ft.TextField(label="Email", width=300)
    senha = ft.TextField(label="Senha", password=True, can_reveal_password=True, width=300)
    feedback = ft.Text("", color=ft.Colors.RED, size=14)

    def btn_voltar(e):
        if on_voltar:
            on_voltar()

    def handle_submit(e):
        if nome.value and email.value and senha.value:
            # on_submit deve retornar None em caso de sucesso, ou uma mensagem de erro
            erro = on_submit(nome.value, email.value, senha.value)
            if erro:
                feedback.value = erro
            else:
                feedback.value = ""
        else:
            feedback.value = "Preencha todos os campos!"
        e.page.update()

    return ft.Container(
        alignment=ft.alignment.center,
        expand=True,
        content=ft.Column(
            [
                ft.Text("Cadastro de Usuário", size=24, weight="bold"),
                nome,
                email,
                senha,
                feedback,
                ft.ElevatedButton("Cadastrar", icon=ft.Icons.PERSON_ADD, on_click=handle_submit),
                ft.ElevatedButton("Voltar", icon=ft.Icons.ARROW_BACK, on_click=btn_voltar)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
        ),
    )