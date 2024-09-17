tables =[
        {   
     "ingredientes" :{
    "id":"SERIAL PRIMARY KEY",
    "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
    "updated_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
    "nombre":"TEXT NOT NULL",
    "cantidad":"REAL",
    "kg_gr":"TEXT NOT NULL",
    "precio":"REAL",
    
    },
     "receta":{
        "id":"SERIAL PRIMARY KEY",
        "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        "updated_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        "nombre":"TEXT NOT NULL UNIQUE",
        "porcentaje_venta":"REAL",
        "precio_venta":"REAL",
        "unidades_x_receta":"INTEGER",
        "cantidad_Receta":"REAL",
        "cant_x_paquete":"REAL",
        "costo_receta":"REAL"

    },
    "cant_ing":{
        "id":"SERIAL PRIMARY KEY",
        "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        "updated_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        "id_ingrediente":"INTEGER",
        "id_receta":"INTEGER",
        "cantidad":"REAL",
        "precio":"REAL",
        "FOREIGN KEY (id_ingrediente)": "REFERENCES ingredientes (id) ON DELETE CASCADE",
        "FOREIGN KEY (id_receta)": "REFERENCES receta (id) ON DELETE CASCADE"
    },
   
  }
]
