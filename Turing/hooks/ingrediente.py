from data.db import PostgresDatabaseManager

class Ingredientes:
    def __init__(self,nombre:str,cant:int,precio:float,kg_gr:str,id= None, fecha= None):
        self.bd = PostgresDatabaseManager("turing")
        self.id = id 
        self.fecha = fecha
        self.nombre_i = nombre
        self.cantid = cant
        self.precio = precio
        self.kg_gr = kg_gr
    @property
    def valor_x_gramo(self):
        peso = self.kg_gr.lower()
        if peso == "kg":
            costo = (self.precio / self.cantid) / 1000
            return costo 
        elif peso == "gr":
            costo = self.precio / self.cantid
            return costo
        return f"{self.kg_gr} opcion no definida"
    @classmethod
    def from_data(cls,data):
        (id,fecha, nombre,cant, precio, kg_gr)= data
        return cls(
            nombre = nombre,
            cant = cant,
            precio = precio,
            kg_gr = kg_gr

        )
    def to_dict_update(self):
        return {
            "nombre":str(self.nombre_i),
            "cantidad":float(self.cantid),
            "kg_gr":str(self.kg_gr),
            "precio":self.precio,
            
        }

    def to_dict(self):
        return {
            "nombre":self.nombre_i,
            "cantidad":self.cantid,
            "kg_gr":self.kg_gr,
            "precio":self.valor_x_gramo,
            
        }

    def __str__(self):
        return f"{self.nombre_i}->{self.cantid}->{self.precio}->{self.kg_gr}"

    def insert(self,tabla):
        try:
            self.bd.insert(tabla,[self.to_dict()])
            return True
        except Exception as e:
            print(("error",e))
            return False
    def delete(self,id,name):
        data = self.bd.selection("ingredientes",f"WHERE ID = {id} AND nombre = '{name}'",param=[id,name])
        if data:
            self.bd.delete("ingredientes",data[0])
            return True
        else:
            return {"Error": "No se encontró el registro para eliminar."}
    def updated_data(self,tabla_name, id,data, condition=None):
        try:
            self.bd.update(table_name=tabla_name,id_tabla=str(id),data=data,condition=condition)
            return {200:"success"}
        except Exception as e:
            return {"Error":str(e)}
