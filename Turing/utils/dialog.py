import flet as ft

class Dialog(ft.Column):
    """ esta clase es un alertDialog de flet 
    recibe el TITULO EL CONTENIDO DE TEXTO un ICONO y el COLOR  de este estas dos ultimas variables por defecto ya vienen con el color azul y el icono de informacion

    esta clase se contruye mediante el metodo incorporado build() que instancia la clase AlertDialog

    sus metodos serian 
    - close_d: este cierra el dialog en pantalla
    - show_d: que hace el Callback del metodo build()
    """
    def __init__(self, title, content_text,icon=ft.icons.INFO,color="#80DAEB", *args, **kwargs):
        self.title = title
        self.content_text = content_text
        self.dialog = None
        self.icon = icon
        self.color= color
        super().__init__(*args, **kwargs)

    def build(self):
        # Crear el diálogo
        self.dialog = ft.AlertDialog(
            title=ft.Text(self.title),
            content=ft.Row(
                controls=[
                    ft.Icon(self.icon, size=28,color=self.color),
                    ft.Text(self.content_text)
                ]
            ),
        
        )
        return self.dialog



    def close_d(self):
        # Ocultar el diálogo
        if self.dialog:
            print("cerrando el dialog")
            self.dialog.visible = False
            self.update()
            self.dialog = None
        else:
            print("No hay diálogo para cerrar.")
        self.update()
    def show(self):
        if self.dialog is None:
            self.build()
        # Mostrar el diálogo
        self.dialog.open = True
        self.dialog.visible = True
        self.update()