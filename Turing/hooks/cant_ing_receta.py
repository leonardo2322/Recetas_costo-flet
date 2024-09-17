from data.db import PostgresDatabaseManager

class Cant_ing_x_receta:
    def __init__(self,ing:list):
        self.ing = ing 
        self.db = PostgresDatabaseManager("turing")
    @property
    def total_ing_costo(self):
        receta_ing = {}
        data = []
        for items in self.ing:
                if items["nombre"] == "panela":
                    items["precio"] = (float(items["precio"]) * 2450) / 3300

                receta_ing["id_ingrediente"] = items["id"]
                receta_ing["id_receta"] = items["id_receta"]
                receta_ing["precio"] = round((float(items["precio"])* float(items['cantidad'])+0.20),3)
                receta_ing["cantidad"] = items["cantidad"]
                if receta_ing not in data:
                    data.append(receta_ing)
                receta_ing = {}
        total = sum(round(float(i["precio"]),3)for i in data)
        return data, total


    def save(self,ingre):
        try:
            self.db.insert("cant_ing",ingre)
            return True

        except Exception as e:
            print("error: este" ,e)
            return False
                

#  for _ in items:
 #               precio = items['precio']
 #               cant = items['cantidad']
  #              nombre = items['nombre']
   #             cantida[nombre] =                    

              
    def __str__(self):
        return f"ingredientes {self.ing}"
    
