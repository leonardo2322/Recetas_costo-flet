from data.db import PostgresDatabaseManager

class Receta:
    def __init__(self, porcentaje,receta, cantidad_receta,precio,unidades,cant_x_paquete,costo_receta=None,stikers=0.03, empaque=0.01):
        self.db = PostgresDatabaseManager("turing")
        self.nombre = receta
        self.cantidad_producida = cantidad_receta
        self.porcentaje_venta = porcentaje
        self.precio = precio
        self.unidades = unidades
        self.cant_x_paquete = cant_x_paquete
        self.costo_receta = costo_receta
        self.empaque = empaque
        self.stiker = stikers
    @classmethod
    def from_data(cls, data):
        # Asumiendo que 'data' es una tupla en el formato dado
        (id, fecha, f_updated,nombre, porcentaje_venta, precio_venta, unidades_x_receta, cantidad_receta, cant_x_paquete, costo_receta) = data
        return cls(
            porcentaje=porcentaje_venta,
            receta=nombre,
            cantidad_receta = cantidad_receta,
            precio=precio_venta,
            unidades=unidades_x_receta,
            cant_x_paquete=cant_x_paquete,
            costo_receta = costo_receta,
            # Opcionales, con valores por defecto
            stikers=0.03,
            empaque=0.01
        )
    @property
    def costo_total_p_receta(self):
        seleccion = self.db.selection("receta",f"WHERE nombre ='{self.nombre}'")
        valores = self.db.selection("cant_ing",int(seleccion[0]),True)
        price = 0
        print(valores)
        for precio in valores:
           price  += precio[-1]
        porcentaje = (int(self.porcentaje_venta)  / 100) * float(price)
        return price,porcentaje
    
    def costo_empaquetado(self, costo):
        costo_total_receta = float(costo)

        costo_unitario = costo_total_receta / float(self.unidades)
        costo_paquete =((costo_unitario * float(self.cant_x_paquete)) + self.empaque) + self.stiker
        con_porcentaje_extras = ((costo_paquete * 15) /100 )+ costo_paquete
        return con_porcentaje_extras
    def to_dict(self):
        return {
            "nombre":self.nombre,
            "porcentaje_venta":self.porcentaje_venta ,
            "precio_venta": self.precio,
            "unidades_x_receta":self.unidades,
            "cantidad_Receta":self.cantidad_producida,
            "cant_x_paquete":self.cant_x_paquete,
            "costo_receta":self.costo_receta
        }
    def save_receta(self):
        try:
            self.db.insert("receta",[self.to_dict()])
            return True
        except Exception as e:
            print(("error",e))
            return False
            
    def delete(self,id,name):
        try:
            data = self.db.selection("receta",f"WHERE ID = {id} AND nombre = '{name}'",param=[id,name])
            if data:
                result = self.db.delete("receta",data[0])
                return result
        except Exception as e:
            return {"Error":str(e)}
    def __str__(self):
        return f"Reseta: {self.nombre} costos de la receta: 0 Cantidad receta elavorada: {self.cantidad_producida}"

