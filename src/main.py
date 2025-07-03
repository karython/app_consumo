import flet as ft
from templates.perfil_view import get_perfil_view
from templates.usuario_view import get_usuario_cadastro_view
from templates.carros_view import get_veiculo_view
from templates.login_view import get_login_view
from templates.abastecimento_view import get_abastecimento_view
from templates.historico_view import get_historico_view
from services.usuario_service import criar_usuario, buscar_usuario_por_email
from services.veiculos_service import criar_veiculo, listar_veiculos
from services.login_service import autenticar_usuario
from models.usuario import Usuario
from models.veiculos import Veiculo
from models.historico import Historico
from models.troca_oleo import TrocaOleo

def main(page: ft.Page):
    page.title = "Controle de Gastos Automotivo"
    
    page.window.always_on_top = True  
    page.window.width = 500
    page.window.height = 600
    page.theme_mode = ft.ThemeMode.LIGHT   
    page.scroll = ft.ScrollMode.AUTO
    
            
    
    login_feedback = ft.Text("", color=ft.Colors.RED, size=14)
    conteudo = ft.Column(expand=True)
    usuario_logado = {"id": None}
    # FIXME apenas modo desenvolvimento     
    usuario_logado["id"]=1   
 

    def atualizar_layout(): 
        page.controls.clear()
        if usuario_logado["id"]:
            page.add( 
                navbar,  
                ft.Row(  
                    controls=[
                        conteudo, 
                        ft.Row(
                            controls=[ ],
                            alignment="end"),
                    ],   
                    expand=True,
                )
            )         
        else:
            page.add(conteudo)   
        page.update()

    def mostrar_perfil(usuario_id):
        conteudo.controls.clear()
        conteudo.controls.append(get_perfil_view(usuario_id, on_logout=mostrar_login))
        atualizar_layout()
  
    def mostrar_login():
        conteudo.controls.clear()
        conteudo.controls.append(
            get_login_view(on_login=realizar_login, on_cadastro=mostrar_cadastro, feedback_ref=login_feedback)
        )
        usuario_logado["id"] = None
        atualizar_layout()
  
    def mostrar_cadastro():
        conteudo.controls.clear()
        conteudo.controls.append(
            get_usuario_cadastro_view(on_submit=realizar_cadastro, on_voltar=mostrar_login)
        )
        atualizar_layout()  

    def realizar_login(email, senha): 
        usuario = autenticar_usuario(email, senha)
        if usuario:
            usuario_logado["id"] = usuario.id     
            login_feedback.value = ""
            mostrar_perfil(usuario.id)
        else:
            login_feedback.value = "Usuário ou senha inválidos!"
            page.update()  
    
    def realizar_cadastro(nome, email, senha):
        if buscar_usuario_por_email(email):
            return "Email já cadastrado!"
        usuario = criar_usuario(nome, email, senha) 
        usuario_logado["id"] = usuario.id
        mostrar_perfil(usuario.id)
        return None
     
      
    def mudar_tela(e):  
        if usuario_logado["id"]:  
            conteudo.controls.clear()  
            match e.control.selected_index: 
                case 0:
                    conteudo.controls.append(get_abastecimento_view(usuario_logado["id"]))     
                case 1:
                    conteudo.controls.append(get_historico_view(usuario_logado["id" ]))
                case 2:
                    conteudo.controls.append(get_veiculo_view(usuario_logado["id"]))
                case 3:
                    conteudo.controls.append(get_perfil_view(usuario_logado["id"], on_logout=mostrar_login))
                #case 4:
                    #conteudo.controls.append(ft.Text("Troca de oleo"))
            atualizar_layout()
        else: 
            mostrar_login()

    navbar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.LOCAL_GAS_STATION, label="Abastecer"),
            #ft.NavigationBarDestination(icon=ft.Icons.OIL_BARREL_SHARP, label="Troca de óleo"),
            ft.NavigationBarDestination(icon=ft.Icons.HISTORY, label="Histórico"),
            ft.NavigationBarDestination(icon=ft.Icons.CAR_REPAIR, label="Veículos"),
            ft.NavigationBarDestination(icon=ft.Icons.PERSON, label="Perfil"),
        ],
        selected_index=3,
        on_change=mudar_tela        
    )                 
     
    '''abastecer = ft.IconButton(   
        icon=ft.Icons.LOCAL_GAS_STATION,  
        style=ft.ButtonStyle(  
            shape=ft.RoundedRectangleBorder(radius=50),
            padding=10,          
            icon_size=40,            
            bgcolor=ft.Colors.CYAN_50    
        ), 
    )''' 

    #FIXME modo desenvolvimento mostra perfil e define id
    #mostrar_login()
    mostrar_perfil(usuario_logado["id"])
ft.app(target=main, view=ft.WEB_BROWSER, assets_dir="assets")      