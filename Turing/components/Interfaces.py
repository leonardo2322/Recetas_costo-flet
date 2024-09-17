import flet as ft
from screens.form_ingrediente import Form_Ingrediente
from screens.cantidad_ing_x_r import Cantidad_Ing
from data.db import PostgresDatabaseManager
from screens.receta_frame import Receta_Frame

class App(ft.Stack):
    """
    Clase principal de la aplicación que gestiona la navegación entre diferentes pantallas y controla la interfaz de usuario.

    Atributos:
        data (PostgresDatabaseManager): Gestor de la base de datos PostgreSQL.
        frame_container (ft.Column): Contenedor que alberga la pantalla actualmente visible.
        frames (dict): Diccionario que asocia nombres de pantallas con sus respectivas clases.
        current_frame (ft.Page): Instancia de la pantalla actualmente visible.

    """
    def __init__(self, **kwargs):
        """
        Inicializa la clase `App`. Configura el contenedor de pantallas y define las pantallas disponibles en la aplicación.

        Args:
            **kwargs: Argumentos adicionales para la inicialización.
        """
        super().__init__(**kwargs)
        self.data = PostgresDatabaseManager("turing")
        self.data.init_data()
        
        self.frame_container = ft.Column()
        self.frames = {
            "home": Form_Ingrediente,
            "cant": Cantidad_Ing,
            "receta": Receta_Frame
        }
        self.current_frame = None
        
        self.frame_container.controls.append(
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text("Turing-System", size=70, font_family=""),                
                            ],
                        ),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Image(src="C:\\Users\\leonardo\\Desktop\\Recetas\\Turing\\assets\\img\\system\\remove_paper.png", scale=10, width=20, height=20),
                                ],
                            ),
                            margin=ft.margin.all(25),
                            alignment=ft.alignment.center
                        )
                    ]
                )
            )
        )

    def build(self):
        """
        Construye la interfaz principal de la aplicación, incluyendo los botones de navegación y el contenedor de la pantalla actual.

        Returns:
            ft.Column: Contenedor principal que incluye los botones de navegación y el contenedor de la pantalla actual.
        """
        return ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.ElevatedButton(text="Ingredientes", on_click=lambda e: self.show_frame("home")),
                        ft.ElevatedButton(text="Receta", on_click=lambda e: self.show_frame("receta")),
                        ft.ElevatedButton(text="Cantidad_ingredientes", on_click=lambda e: self.show_frame("cant", self.data.selection("ingredientes"))),
                    ]
                ),
                self.frame_container
            ]
        )

    def update_frame(self, frame_class, param=None):
        """
        Actualiza el contenedor de la pantalla con una nueva instancia de la clase de pantalla especificada.

        Args:
            frame_class (type): La clase de pantalla que se mostrará.
            param (optional): Parámetro opcional que se pasará al inicializar la pantalla. Por defecto es None.

        Modifica:
            self.frame_container.controls: Limpia el contenedor de la pantalla actual y añade la nueva pantalla.
            self.current_frame: Actualiza la instancia de la pantalla actual.
        """
        self.frame_container.controls.clear()
        if param is None:
            self.current_frame = frame_class()
        else:
            self.current_frame = frame_class(param)
        self.frame_container.controls.append(self.current_frame.build())
        self.update()

    def show_frame(self, frame_name, param=None):
        """
        Muestra la pantalla correspondiente al nombre proporcionado. Si se proporciona un parámetro, lo pasa al inicializar la pantalla.

        Args:
            frame_name (str): El nombre de la pantalla a mostrar.
            param (optional): Parámetro opcional que se pasará al inicializar la pantalla. Por defecto es None.

        Modifica:
            self.frame_container.controls: Actualiza el contenedor de la pantalla con la pantalla solicitada o muestra un mensaje de error si no se encuentra la pantalla.
        """
        frame_class = self.frames.get(frame_name)
        if frame_class:
            self.update_frame(frame_class, param)
        else:
            self.frame_container.controls.clear()
            self.frame_container.controls.append(ft.Text("frame not found"))
            self.update()
