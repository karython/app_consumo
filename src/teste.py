import flet as ft

def main(page: ft.Page):
    
    def formatar_moeda(e: ft.ControlEvent):
        texto = e.control.value
        # remove tudo que não é número
        numeros = ''.join(filter(str.isdigit, texto))
        
        if numeros:
            # converte para float considerando centavos
            valor_float = int(numeros) / 100
            valor_formatado = f"R$ {valor_float:,.2f}".replace(".", "X").replace(",", ".").replace("X", ",")
            e.control.value = valor_formatado
        else:
            e.control.value = ""
        e.control.update()
    
    campo = ft.TextField(
        label="Valor",
        on_change=formatar_moeda,
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    
    page.add(campo)

ft.app(main)
