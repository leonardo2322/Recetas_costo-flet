import flet as ft
from utils.dialog import Dialog

class Base_frame(ft.Container):
    """
    Clase base para todos los marcos de la aplicación. Gestiona la interfaz de usuario básica y el diálogo de notificación.

    Atributos:
        content (ft.Column): Contenedor principal para los controles y componentes del marco.
        dialog (Dialog or None): Instancia del diálogo de notificación actual o None si no hay ninguno.

    """
    def __init__(self, **kwargs):
        """
        Inicializa la clase `Base_frame`. Configura el contenedor principal y el diálogo.

        Args:
            **kwargs: Argumentos adicionales para la inicialización del contenedor.
        """
        super().__init__(**kwargs)
        self.content = ft.Column()
        self.dialog = None

    def build(self):
        """
        Construye el contenido del marco. Esta función debe ser sobrescrita en subclases para definir el contenido específico.

        Returns:
            ft.Column: El contenedor de la interfaz de usuario del marco.
        """
        return self.content

    def show_dialog(self, titulo, content, icon=None, color=None):
        """
        Muestra un diálogo de notificación con el título, contenido, icono y color especificados. Si ya existe un diálogo abierto, lo cierra antes de mostrar el nuevo.

        Args:
            titulo (str): El título del diálogo.
            content (str): El contenido del diálogo.
            icon (str or None): Icono opcional que se mostrará en el diálogo.
            color (str or None): Color opcional del diálogo.
        
        Modifica:
            self.dialog: Cierra el diálogo actual (si existe) y crea uno nuevo con los parámetros proporcionados.
            self.content.page: Añade el nuevo diálogo a la página actual.
        """
        if self.dialog:
            self.dialog.close_d()  # Cierra el diálogo actual si existe
        self.dialog = Dialog(
            title=titulo,
            content_text=content,
            icon=icon,
            color=color
        )
        self.content.page.add(self.dialog)  # Añade el nuevo diálogo a la página
        self.dialog.show()  # Muestra el nuevo diálogo
