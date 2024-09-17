import flet as ft 
from components.base_frame import Base_frame
from hooks.receta import Receta
from data.db import PostgresDatabaseManager
class Receta_Frame(Base_frame):
    """
    esta clase recibe de instancia la clase padre Base_frame

    inicializa la base de datos Nombre, Cantidad, Porcentaje, Precio de Venta, Unidades arrojadas x receta, Cuantas unidades para el paquete 

    que pasa en una por parametro a la clase rece de la carpeta hooks y esta realiza la funcionalidad de mediados con la base de datos
    """
    def __init__(self, ing:list=None,**kwargs):
        super().__init__(**kwargs)
        self.db = PostgresDatabaseManager("turing")
        self.nombre = ft.TextField(label="Nombre",hint_text="Introduzca el Nombre de la Receta")
        self.cantidad = ft.TextField(label="Cantidad",hint_text="Introduzca el cantidad de la Receta elaborada",on_change=lambda e: self.num_validate(e))
        self.porcentaje_venta = ft.TextField(label="Porcentaje",hint_text="Introduzca el porcentaje de  ganancia",on_change=lambda e: self.num_validate(e))
        self.precio_venta = ft.TextField(label="Precio de Venta",hint_text="Introduzca el precio que lo quieres vender",on_change=lambda e: self.num_validate(e))
        self.unidades_x_receta = ft.TextField(label="Unidades arrojadas x receta",hint_text="Introduzca la cantidad que arroja la receta echa",on_change=lambda e: self.num_validate(e))
        self.cant_und_paquete = ft.TextField(label="Cuantas unidades para el paquete",hint_text="Introduzca la cantidad de unidades para el paquete",on_change=lambda e: self.num_validate(e))
        self.submit = ft.ElevatedButton(text="Guardar",on_click=lambda e:self.save())
        self.show_Data = ft.ElevatedButton(text="Mostrar Recetas", on_click=lambda e: self.show_data())
        self.precio_sugerido_venta = ft.Text(size=25,color=ft.colors.GREEN)
        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("id",color=ft.colors.BLACK)),
                ft.DataColumn(label=ft.Text("fecha",color=ft.colors.BLACK)),
                ft.DataColumn(label=ft.Text("nombre",color=ft.colors.BLACK)),
                ft.DataColumn(label=ft.Text("Porcentaje",color=ft.colors.BLACK)),
                ft.DataColumn(label=ft.Text("Precio_venta_ingresado",color=ft.colors.BLACK)),
                ft.DataColumn(label=ft.Text("Und_x_Receta",color=ft.colors.BLACK)),
                ft.DataColumn(label=ft.Text("cantidad_elaborada",color=ft.colors.BLACK)),
                ft.DataColumn(label=ft.Text("Cant_x_paquete",color=ft.colors.BLACK)),
                ft.DataColumn(label=ft.Text("costo_receta por paquete",color=ft.colors.BLACK)),
                ft.DataColumn(label=ft.Text("Opciones",color=ft.colors.BLACK)),
            ],
            border=ft.border.all(0.7,"black"),
            border_radius=10,
            vertical_lines=ft.BorderSide(0.7,"black"),
            horizontal_lines=ft.BorderSide(0.7,"black"),
            bgcolor="#F5EDED",
            data_row_color="#CAF4FF",
            heading_row_color="#E2DAD6",
        )
        self.form = ft.Container(
            content=
                 ft.Column(
                controls=[
                    self.nombre,
                    self.cantidad,
                    self.porcentaje_venta,
                    self.precio_venta,
                    self.unidades_x_receta,
                    self.cant_und_paquete,
                    ft.Row(
                        controls=[
                            self.submit,
                            self.show_Data,
                        ]
                    ),ft.Column(
                        controls=[
                            self.precio_sugerido_venta
                        ],
                        
                    ),
                    ft.Container(
                    content=ft.Row(
                    controls=[
                        self.table
                    ],
                    scroll=ft.ScrollMode.ALWAYS,
                    spacing=25,
                    
                ),
                margin=ft.margin.all(20),
                padding=ft.padding.all(40),
                )
                ]
            )
        )
           
       
        self.content.controls.append(self.form)

   
    def save(self):
        if (self.porcentaje_venta.value not in (None, "") and
            self.nombre.value not in (None, "") and
            self.cantidad.value not in (None, "") and
            self.precio_venta.value not in (None, "") and
            self.unidades_x_receta.value not in (None,"") and
            self.cant_und_paquete.value not in (None,"")
            ):
            r = Receta(self.porcentaje_venta.value,self.nombre.value,self.cantidad.value,self.precio_venta.value,self.unidades_x_receta.value,self.cant_und_paquete.value)
        else:
            print("aca")
            self.show_dialog("Error Guardando", "Verifica que has rellenado todos los valores",ft.icons.DANGEROUS, "red")
        if r.save_receta():
            self.show_dialog("Insercion Exitosa!", "la data se ha insertado en la base de datos con exito",ft.icons.CHECK,"#90EE90")
        else:
            self.show_dialog("Error insertando", "Verifica la data que has ingresado e intentalo de nuevo",ft.icons.DANGEROUS, "red")

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


    def num_validate(self,event):
        """
            Valida y filtra la entrada del usuario en un campo de texto para permitir solo números y caracteres especiales 
            como punto y coma.

            Args:
                event: El evento que contiene el control y su valor. Se espera que 'event.control.value' sea una cadena.
            
            Modifica:
                event.control.value: El valor del control se actualiza para contener solo dígitos, punto o coma.
        """
        n_value = event.control.value

        filtered_value = "".join(c for c in n_value if c.isdigit() or c in ".,")
        event.control.value = filtered_value
        event.control.update()
    def edit(self):
        """
                Función placeholder para la edición de datos. Actualmente no realiza ninguna acción.

        """
        pass

    def delete(self,r):
        """
            Elimina una entrada de datos basada en la información proporcionada en el parámetro.

            Args:
                r (tuple): Una tupla que contiene datos de la entrada a eliminar. Se espera que 'r' contenga al menos un identificador
                        y un nombre para la búsqueda de la entrada a eliminar.
            
            Modifica:
                Muestra un diálogo de éxito si la eliminación es satisfactoria, o un diálogo de error si ocurre un problema.

        """
        data = Receta.from_data(r)
        result = data.delete(id=r[0],name=r[2])
        if result:
                self.show_data()
                self.call_dialog("Eliminación", "La eliminación ha sido satisfactoria", ft.icons.CHECK, "green")
                return True
        elif isinstance(result, dict) and "Error" in result:
            self.call_dialog("Error", result["Error"], ft.icons.WARNING, "red")
        else:
            self.call_dialog("Error", "Falló la eliminación sin un error específico", ft.icons.WARNING, "red")
    def show_data(self):
        """
            Muestra y actualiza los datos en una tabla y muestra un resumen del costo sugerido de venta de cada ítem.

            Modifica:
                self.table.rows: Actualiza las filas de la tabla con los nuevos datos.
                self.precio_sugerido_venta.value: Actualiza el texto del costo sugerido de venta.
                self.content.update(): Actualiza el contenido para reflejar los cambios en la interfaz de usuario.

        """
        self.table.rows.clear()
        data = self.db.selection("receta")
        new_data = [(i,f_u,n,p_v,p,und,c_r,c_p,c) for (i,f,f_u,n,p_v,p,und,c_r,c_p,c) in data ]
        nombre_precio = {}
        for datos in new_data:
            costo = ((float(datos[3]) /100 )* float(datos[-1]))+ float(datos[-1])
            if datos[2] not in nombre_precio:
                nombre_precio[datos[2]]= (costo,)
        
        self.precio_sugerido_venta.value = "\n".join([f"{key.capitalize()} tiene un costo de: {v[0]:.3f}"for key,v in nombre_precio.items()]) +"\n el costo se le ha sumado el porcentaje de ganancia que haz ingresado"
        
        self.table.rows = [ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(cell,width=150,color=ft.colors.BLACK))for cell in row] + [ft.DataCell(ft.Row(controls=[ft.IconButton(icon="create",on_click=lambda e, r=row:self.edit(r)),ft.IconButton(icon=ft.icons.DELETE,icon_color="red",on_click=lambda e, r=row:self.delete(r))],spacing=15))] 
                )for row in new_data] 
        self.content.update()

