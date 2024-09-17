import flet as ft 
from components.base_frame import Base_frame
from data.db import PostgresDatabaseManager
from hooks.cant_ing_receta import Cant_ing_x_receta
from hooks.receta import Receta

class Cantidad_Ing(Base_frame):
    """
    Clase que define un formulario para gestionar las cantidades de ingredientes en una receta. Hereda de `Base_frame` 
    y proporciona funcionalidades para agregar, mostrar y guardar cantidades de ingredientes en una receta.

    Atributos:
        select_option (list): Lista de ingredientes disponibles para seleccionar.
        select_option_updated_date (list): Lista de ingredientes actualizada para mostrar en el formulario.
        data_dict (dict): Diccionario que almacena las cantidades de ingredientes seleccionados.
        data_list (list): Lista que almacena los datos formateados para insertar en la base de datos.
        db (PostgresDatabaseManager): Gestor de la base de datos PostgreSQL.
        ingredientes (ft.RadioGroup): Grupo de botones de radio para seleccionar un ingrediente.
        receta (list): Lista de recetas obtenidas de la base de datos.
        receta_not_date (list): Lista de recetas sin la fecha.
        name_receta (ft.RadioGroup): Grupo de botones de radio para seleccionar una receta.
        quantity (ft.TextField): Campo de texto para introducir la cantidad del ingrediente.
        button_add (ft.ElevatedButton): Botón para agregar la cantidad del ingrediente seleccionado.
        button_save (ft.ElevatedButton): Botón para guardar las cantidades de ingredientes en la base de datos.
        table (ft.DataTable): Tabla para mostrar los ingredientes y sus cantidades.
        contain (ft.Column): Contenedor que organiza los controles del formulario.

    """
    def __init__(self, ing: list = [], **kwargs):
        """
        Inicializa la clase `Cantidad_Ing`, configura los campos del formulario, botones y tabla.

        Args:
            ing (list, optional): Lista de ingredientes disponibles para seleccionar. Por defecto es una lista vacía.
            **kwargs: Argumentos adicionales para la inicialización.
        """
        super().__init__(**kwargs)
        self.select_option = ing
        self.select_option_updated_date = [(i, f_u, n, c, p, kg) for (i, f, f_u, n, c, p, kg) in ing]
        self.data_dict = {}
        self.data_list = []
        self.db = PostgresDatabaseManager("turing")
        
        self.ingredientes = ft.RadioGroup(
            content=ft.Column(
                controls=[
                    ft.Radio(value=key[2], label=key[2])
                    for key in self.select_option_updated_date
                ]
            )
        )
        self.receta = self.db.selection("receta")
        self.receta_not_date = [(i, f_u, n, p_v, p, und, c_r, c_p, c) for (i, f, f_u, n, p_v, p, und, c_r, c_p, c) in self.receta]
        self.name_receta = ft.RadioGroup(
            content=ft.Row(
                controls=[
                    ft.Radio(value=key[0], label=key[2])
                    for key in self.receta_not_date
                ]
            )
        )
        self.quantity = ft.TextField(label="Cantidad", hint_text="Introduzca la cantidad solo numeros", on_change=self.num_validate)
        self.button_add = ft.ElevatedButton(text="agg", on_click=lambda e: self.add_quantity(), icon=ft.icons.ADD)
        self.button_save = ft.ElevatedButton(text="Guardar", disabled=True, icon=ft.icons.SAVE, on_click=lambda e: self.save_quantity())
        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("Ingrediente", color=ft.colors.BLACK)),
                ft.DataColumn(label=ft.Text("Cantidad", color=ft.colors.BLACK)),
                ft.DataColumn(label=ft.Text("Options", color=ft.colors.BLACK)),
            ],
            border=ft.border.all(0.7, "black"),
            border_radius=10,
            vertical_lines=ft.BorderSide(0.7, "black"),
            horizontal_lines=ft.BorderSide(0.7, "black"),
            width=700,
            bgcolor="#F5EDED",
            data_row_color="#CAF4FF",
            heading_row_color="#E2DAD6",
        )
        self.contain = ft.Column(
            controls=[
                ft.ListView(
                    controls=[self.ingredientes],
                    auto_scroll=True, padding=20, spacing=10
                ),
                self.quantity,
                ft.Divider(height=9, color="white", thickness=3),
                self.name_receta,
                ft.Divider(height=9, color="white", thickness=3),
                ft.Row(
                    controls=[
                        self.button_add,
                        self.button_save
                    ]
                ),
                ft.Row(
                    controls=[self.table],
                    scroll=ft.ScrollMode.ALWAYS,
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.ALWAYS,
        )
        self.content.controls.append(self.contain)

    def delete(self, r):
        """
        Método para eliminar un registro basado en los datos proporcionados. Actualmente solo imprime los datos.

        Args:
            r (tuple): Datos del ingrediente a eliminar.
        """
        print(r)
        
    def edit(self, r):
        """
        Método para editar un registro basado en los datos proporcionados. Actualmente solo imprime los datos.

        Args:
            r (tuple): Datos del ingrediente a editar.
        """
        print(r)
        
    def show_data(self):
        """
        Muestra los datos de ingredientes y cantidades en la tabla. Actualiza las filas de la tabla con los datos 
        almacenados en `data_dict`.

        Modifica:
            self.table.rows: Actualiza las filas de la tabla con los datos de `data_dict`.
        """
        self.table.rows.clear()
        
        self.table.rows = [ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(cell, width=150, color=ft.colors.BLACK)) for cell in row
            ] + [ft.DataCell(ft.Row(controls=[
                ft.IconButton(icon="create", on_click=lambda e, r=row: self.edit(r)),
                ft.IconButton(icon=ft.icons.DELETE, icon_color="red", on_click=lambda e, r=row: self.delete(r))
            ], spacing=15))]
        ) for row in self.data_dict.items()]
        self.content.update()
    
    def call_dialog(self, title, content, icon=None, color=None):
        """
        Muestra un diálogo con un título, contenido, y opciones opcionales de icono y color.

        Args:
            title (str): El título del diálogo.
            content (str): El contenido del diálogo.
            icon (str, optional): El icono que se mostrará en el diálogo. Por defecto es None.
            color (str, optional): El color del icono o del fondo del diálogo. Por defecto es None.
        """
        self.show_dialog(title, content, icon, color)

    def add_quantity(self):
        """
        Agrega la cantidad del ingrediente seleccionado al diccionario `data_dict`. Habilita el botón de guardar 
        si se han agregado al menos 3 cantidades. Muestra los datos actualizados en la tabla.

        Modifica:
            self.data_dict: Agrega la cantidad del ingrediente seleccionado.
            self.button_save.disabled: Habilita o deshabilita el botón de guardar según la cantidad de datos.
            self.quantity.value: Limpia el campo de cantidad.
            self.ingredientes.value: Limpia la selección de ingrediente.
        """
        if self.quantity.value not in (None, ""):
            self.data_dict[self.ingredientes.value] = self.quantity.value
        else:
            self.show_dialog("Error", "Verifica que has rellenado y seleccionado todos los campos", ft.icons.DANGEROUS, "red")
        
        if len(self.data_dict) >= 3:
            self.button_save.disabled = False
        else:
            self.button_save.disabled = True
        
        self.quantity.value = ""
        self.ingredientes.value = ""
        self.show_data()
        self.content.update()
     
    def num_validate(self, event):
        """
        Valida y filtra la entrada del usuario en el campo de texto de cantidad para permitir solo números.

        Args:
            event: El evento que contiene el control y su valor. Se espera que 'event.control.value' sea una cadena.

        Modifica:
            event.control.value: El valor del control se actualiza para permitir solo números.
        """
        n_value = event.control.value
        filtered_value = "".join(c for c in n_value if c.isdigit())
        event.control.value = filtered_value
        event.control.update()
    
    def save_quantity(self):
        """
        Guarda las cantidades de ingredientes en la base de datos. Actualiza el costo de la receta y muestra un 
        diálogo de éxito o error según el resultado de la inserción.

        Modifica:
            self.data_dict: Limpia el diccionario de datos.
            self.name_receta.value: Limpia la selección de receta.
            self.quantity.value: Limpia el campo de cantidad.
            self.data_list: Actualiza la lista de datos para insertar en la base de datos.
        """
        for _ in range(len(self.data_dict)):
            for item in self.select_option_updated_date:
                if item[2] in self.data_dict:
                    self.data_list.append({
                        "id": item[0],
                        "fecha": item[1],
                        "id_receta": self.name_receta.value,
                        "nombre": item[2],
                        "precio": item[-1],
                        "cantidad": self.data_dict[item[2]]
                    })
        
        cant = Cant_ing_x_receta(self.data_list)
        datos = cant.total_ing_costo
        
        if cant.save(datos[0]):
            self.show_dialog("Insercion Exitosa!", "La data se ha insertado en la base de datos con éxito", ft.icons.CHECK, "#90EE90")
            receta = self.db.selection("receta", f"WHERE ID= {self.name_receta.value}")
            (i, _, f_u, n, p_v, p, und, c_r, c_p, c) = receta
            receta_not_date = (i, _, f_u, n, p_v, p, und, c_r, c_p, c)
            instancia_receta = Receta.from_data(receta_not_date)
            result = self.db.update("receta", receta[0], instancia_receta.costo_empaquetado(instancia_receta.costo_total_p_receta[0]))
            if "success" in result:
                self.show_dialog("Actualizacion Exitosa!", "La receta se ha actualizado correctamente", ft.icons.CHECK, "#90EE90")
                self.data_dict = {}
                self.name_receta.value = ""
                self.quantity.value = ""
                self.show_data()
            else:
                self.show_dialog("Error interno", "Comuníquese con el técnico", ft.icons.DANGEROUS, "red")
        else:
            self.show_dialog("Error", "Verifica que has rellenado y seleccionado todos los campos", ft.icons.DANGEROUS, "red")
