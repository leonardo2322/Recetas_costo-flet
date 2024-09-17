import flet as ft
from components.base_frame import Base_frame
from hooks.ingrediente import Ingredientes 
from data.db import PostgresDatabaseManager
class Form_Ingrediente(Base_frame):
    """
        Clase que define un formulario para gestionar ingredientes. Hereda de `Base_frame` y proporciona 
        funcionalidades para agregar, editar, eliminar y mostrar datos de ingredientes en una tabla.

        Atributos:
            db (PostgresDatabaseManager): Gestor de la base de datos PostgreSQL.
            name (ft.TextField): Campo de texto para introducir el nombre del ingrediente.
            quantity (ft.TextField): Campo de texto para introducir la cantidad del ingrediente.
            price (ft.TextField): Campo de texto para introducir el precio del ingrediente.
            mostrar_data (ft.ElevatedButton): Botón para mostrar los datos de los ingredientes.
            _id_and_time (str): Almacena el ID y la fecha del ingrediente actual para editar.
            radio_gr_kg (ft.RadioGroup): Grupo de botones de radio para seleccionar la unidad de medida (kg o gr).
            submit_button (ft.ElevatedButton): Botón para guardar un nuevo ingrediente.
            btn_update (ft.ElevatedButton): Botón para actualizar un ingrediente existente.
            table (ft.DataTable): Tabla para mostrar los datos de los ingredientes.
            form (ft.Column): Contenedor de todos los controles del formulario.

    """
    def __init__(self, **kwargs):
        """
            Inicializa la clase `Form_Ingrediente`, configura los campos del formulario, botones y tabla.

            Args:
                **kwargs: Argumentos adicionales para la inicialización.
        """
        super().__init__(**kwargs)
        self.db = PostgresDatabaseManager("turing")
        self.name = ft.TextField(label="Nombre",hint_text="Introduzca el Nombre de la receta",on_change=lambda e: self.num_validate(e))
        self.quantity = ft.TextField(label="Cantidad",hint_text="Introduzca la cantidad de la receta",on_change=lambda e: self.num_validate(e))
        self.price = ft.TextField(label="Precio",hint_text="Introduzca el precio de la receta",on_change=lambda e: self.num_validate(e))
        self.mostrar_data = ft.ElevatedButton(text="Mostrar datos",on_click=lambda e:self.show_data())
        self._id_and_time = ""
        self.radio_gr_kg = ft.RadioGroup(content=ft.Column(
            [
                ft.Radio(value="Kg",label="kilogramos"),
                ft.Radio(value="gr",label="Gramos")
            ]
        ))
        self.submit_button = ft.ElevatedButton(text="Guardar",on_click=lambda e:self.submit())
        self.btn_update = ft.ElevatedButton(text="Actualizar",on_click=lambda e:self.updated(),visible=False)
        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("id",color=ft.colors.BLACK)),
                ft.DataColumn(label=ft.Text("fecha",color=ft.colors.BLACK)),
                ft.DataColumn(label=ft.Text("nombre",color=ft.colors.BLACK)),
                ft.DataColumn(label=ft.Text("cantidad",color=ft.colors.BLACK)),
                ft.DataColumn(label=ft.Text("kg_gr",color=ft.colors.BLACK)),
                ft.DataColumn(label=ft.Text("precio",color=ft.colors.BLACK)),
                ft.DataColumn(label=ft.Text("opciones",color=ft.colors.BLACK))

            ],
            border=ft.border.all(0.7,"black"),
            border_radius=10,
            vertical_lines=ft.BorderSide(0.7,"black"),
            horizontal_lines=ft.BorderSide(0.7,"black"),
            bgcolor="#F5EDED",
            data_row_color="#CAF4FF",
            heading_row_color="#E2DAD6",
        )
        self.form = ft.Column(
            controls=[
                self.name,
                self.quantity,
                self.price,
                self.radio_gr_kg,
                ft.Row(
                    controls=[
                    self.submit_button,
                    self.mostrar_data,
                    self.btn_update,

                    ]
                ),
                ft.Container(
                    content=ft.Row(
                    controls=[
                        self.table
                    ],
                    scroll="always",
                    spacing=15
                ),
                margin=ft.margin.all(16)
                )
            ],
            scroll=ft.ScrollMode.ALWAYS,
            spacing=20
        )
        
      
        self.content.controls.append(self.form)
    def updated(self):
        """
            Actualiza un ingrediente existente con los valores actuales del formulario. Muestra un diálogo 
            de éxito o error según el resultado de la actualización.

            Modifica:
                self.submit_button.disabled: Deshabilita el botón de guardar al editar.
                self.btn_update.visible: Hace visible el botón de actualización durante la edición.
                self._id_and_time: Almacena el ID y la fecha del ingrediente actual para la actualización.
        """
        if (self.quantity.value not in (None, "") and
            self.name.value not in (None, "") and
            self.price not in (None, "") and
            self.radio_gr_kg.value not in (None, "")):
            print("aca")
            data = Ingredientes(
                self.name.value,
                float(self.quantity.value),
                float(self.price.value),
                self.radio_gr_kg.value,
                id=self._id_and_time[0],
                fecha=self._id_and_time[1]
            )
            result = data.updated_data(tabla_name="ingredientes",id=data.id,data=data.to_dict_update())
            if 200 in result:
                self.name.value = ""
                self.quantity.value = ""
                self.price.value = ""
                self.radio_gr_kg.value = ""
                self.submit_button.disabled =False 
                self.btn_update.visible = False
                self.show_data()
                self.call_dialog("Actualizacion", "ha sido satisfactoria", ft.icons.CHECK, "green")
            elif "Error" in result:
                self.call_dialog("Actualizacion fallida", "No se pudo actualizar el valor", ft.icons.WARNING, "green")
        self.btn_update.visible = False
        
    def edit(self,r):
        """
        Rellena los campos del formulario con los datos del ingrediente seleccionado para su edición.

        Args:
            r (tuple): Una tupla que contiene los datos del ingrediente seleccionado para editar.
        
        Modifica:
            self.submit_button.disabled: Deshabilita el botón de guardar al editar.
            self.btn_update.visible: Hace visible el botón de actualización durante la edición.
            self._id_and_time: Almacena el ID y la fecha del ingrediente para su actualización.
        """
        self.submit_button.disabled = True
        self.btn_update.visible = True
        self.name.value = r[2]
        self.quantity.value = r[3]
        self.price.value = r[5]
        self.radio_gr_kg.value = r[4]

        self._id_and_time = (r[0],r[1])
        self.name.focus()
        self.content.update()
    def delete(self,r):
        """
        Elimina un ingrediente basado en los datos proporcionados. Muestra un diálogo de éxito o error 
        según el resultado de la eliminación.

        Args:
            r (tuple): Una tupla que contiene los datos del ingrediente a eliminar.

        Modifica:
            Muestra un diálogo de éxito si la eliminación es satisfactoria o un diálogo de error si ocurre un problema.
        """
        ing = Ingredientes("",0,0.0,"")
        try:
            id = r[0]
            name = r[2]
            result = ing.delete(id=id,name=name)
            if isinstance(result, bool) and result:
                self.show_data()
                self.call_dialog("Eliminación", "La eliminación ha sido satisfactoria", ft.icons.CHECK, "green")
                return True
            elif isinstance(result, dict) and "Error" in result:
                self.call_dialog("Error", result["Error"], ft.icons.WARNING, "red")
            else:
                self.call_dialog("Error", "Falló la eliminación sin un error específico", ft.icons.WARNING, "red")
        except Exception as e:
            print("error")
            self.call_dialog("Error",str(e),ft.icons.WARNING,"red")

    def show_data(self):
        """
        Muestra los datos de los ingredientes en la tabla. Obtiene los datos de la base de datos y actualiza 
        las filas de la tabla.

        Modifica:
            self.table.rows: Actualiza las filas de la tabla con los nuevos datos.
        """
        self.table.rows.clear()
        ing = self.db.selection("ingredientes")
        data = [(i,f_u,n,c,p,kg) for (i,f,f_u,n,c,p,kg) in ing ]
        self.table.rows = [ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(cell,width=150,color=ft.colors.BLACK))for cell in row] + [ft.DataCell(ft.Row(controls=[ft.IconButton(icon="create",on_click=lambda e, r=row:self.edit(r)),ft.IconButton(icon=ft.icons.DELETE,icon_color="red",on_click=lambda e, r=row:self.delete(r))],spacing=15))]
                )for row in data] 
        self.content.update()

    def num_validate(self,event):
        """
        Valida y filtra la entrada del usuario en los campos de texto para permitir solo números y caracteres 
        especiales según el campo. Para 'Cantidad' y 'Precio', permite solo dígitos y puntos. Para otros campos, 
        permite cualquier valor.

        Args:
            event: El evento que contiene el control y su valor. Se espera que 'event.control.value' sea una cadena.

        Modifica:
            event.control.value: El valor del control se actualiza según el filtro aplicado.
        """
        n_value = event.control.value
        filtered_value = ""
        if event.control.label == "Cantidad" or event.control.label == "Precio":
            filtered_value = "".join(c for c in n_value if c.isdigit() or c in ".")
        else:
            filtered_value = n_value
        event.control.value = filtered_value
        event.control.update()
    def call_dialog(self,title,content,icon=None, color=None):
        """
        Muestra un diálogo con un título, contenido, y opciones opcionales de icono y color.

        Args:
            title (str): El título del diálogo.
            content (str): El contenido del diálogo.
            icon (str, optional): El icono que se mostrará en el diálogo. Por defecto es None.
            color (str, optional): El color del icono o del fondo del diálogo. Por defecto es None.
        """
        self.show_dialog(title,content,icon,color)
    def submit(self):
        """
        Inserta un nuevo ingrediente en la base de datos con los valores actuales del formulario. Muestra un 
        diálogo de éxito o error según el resultado de la inserción.

        Modifica:
            self.name.value: Limpia el campo de nombre.
            self.quantity.value: Limpia el campo de cantidad.
            self.price.value: Limpia el campo de precio.
            self.radio_gr_kg.value: Limpia la selección de unidad de medida.
        """
        if (self.quantity.value not in (None, "") and
            self.name.value not in (None, "") and
            self.price not in (None, "") and
            self.radio_gr_kg.value not in (None, "")):

            data = Ingredientes(
                self.name.value,
                float(self.quantity.value),
                float(self.price.value),
                self.radio_gr_kg.value
            )
        
            query = data.insert("ingredientes")
            if query:
                self.show_dialog("Insercion Exitosa!", "la data se ha insertado en la base de datos con exito",ft.icons.CHECK,"#90EE90")
            else:
                self.show_dialog("Error ", "Verifica que has rellenado y seleccionado todos los campos",ft.icons.DANGEROUS, "red")
            self.name.value = ""
            self.quantity.value = ""
            self.price.value = ""
            self.radio_gr_kg.value = ""
            self.show_data()
        else:
            self.show_dialog("Error ", "Verifica que has rellenado y seleccionado todos los campos",ft.icons.DANGEROUS, "red")
        
            

