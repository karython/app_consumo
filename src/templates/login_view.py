import flet as ft

def get_login_view(on_login, on_cadastro, feedback_ref=None):
    email = ft.TextField(label="Email", width=300)
    senha = ft.TextField(label="Senha", password=True, can_reveal_password=True, width=300)
    feedback = feedback_ref if feedback_ref else ft.Text("", color=ft.Colors.RED, size=14)
    def handle_login(e):
        if not email.value or not senha.value:
            feedback.value = "Preencha todos os campos!"
            
        else:
            feedback.value = ""
            on_login(email.value, senha.value)
        e.page.update()
        
    return ft.Container(
        
        alignment=ft.alignment.center,
        expand=True,
        content=ft.Column(
            [
                ft.Text("Login", size=24, weight="bold"),
                email,
                senha,
                feedback,
                ft.ElevatedButton("Entrar", icon=ft.Icons.LOGIN, on_click=handle_login),
                ft.TextButton("Não tem cadastro? Cadastre-se", on_click=lambda e: on_cadastro())
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            
        ),
        margin=ft.Margin(0,200,0,0)
        
    )