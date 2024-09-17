import psycopg2
from psycopg2 import sql
from data.data_injection import tables
from dotenv import load_dotenv
import os

load_dotenv()

class PostgresDatabaseManager:
    """
    Clase para gestionar la conexión y operaciones con una base de datos PostgreSQL.

    Atributos:
        db_name (str): Nombre de la base de datos.
        user (str): Usuario de la base de datos.
        password (str): Contraseña del usuario de la base de datos.
        host (str): Host del servidor de la base de datos.
        port (str): Puerto del servidor de la base de datos.
        conn (psycopg2.connection): Conexión a la base de datos.
        cursor (psycopg2.cursor): Cursor para ejecutar consultas en la base de datos.
    """
    def __init__(self, db_name):
        """
        Inicializa la conexión a la base de datos con las credenciales y parámetros proporcionados.

        Args:
            db_name (str): Nombre de la base de datos.
        """
        self.db_name = db_name
        self.user = os.getenv("USER")
        self.password = os.getenv("PASSWORD")
        self.host = os.getenv("HOST")
        self.port = os.getenv("PORT")
        self.conn = psycopg2.connect(
            dbname=self.db_name,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        self.cursor = self.conn.cursor()

    def connection(self):
        """
        Establece una nueva conexión y cursor a la base de datos. 

        Returns:
            psycopg2.cursor: Un nuevo cursor para ejecutar consultas.
        """
        self.conn = psycopg2.connect(
            dbname=self.db_name,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        self.cursor = self.conn.cursor()
        return self.cursor

    def create_table(self, table_name, columns: dict):
        """
        Crea una nueva tabla en la base de datos si no existe.

        Args:
            table_name (str): Nombre de la tabla.
            columns (dict): Diccionario con nombres de columnas y sus tipos de datos.
        """
        self.connection()
        columns_with_types = ", ".join([f"{col} {typ}" for col, typ in columns.items()])
        create_table_sql = sql.SQL("CREATE TABLE IF NOT EXISTS {} ({})").format(
            sql.Identifier(table_name),
            sql.SQL(columns_with_types)
        )
        self.cursor.execute(create_table_sql)
        self.conn.commit()
        self.conn.close()

    def insert(self, table_name, values: list):
        """
        Inserta registros en una tabla. Verifica si el registro ya existe antes de insertar.

        Args:
            table_name (str): Nombre de la tabla.
            values (list): Lista de diccionarios con los valores a insertar.
        """
        self.connection()
        keys = ", ".join(values[0].keys())
        placeholders = ", ".join(["%s"] * len(values[0]))
        
        # Verificar si el registro ya existe
        if table_name in ["ingredientes", "receta"]:
            self.cursor.execute(
                sql.SQL("SELECT COUNT(*) FROM {} WHERE nombre = %s").format(sql.Identifier(table_name)),
                (values[0]["nombre"],)
            )
            exists = self.cursor.fetchone()[0] > 0
        else:
            exists = False
        
        if not exists:
            query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                sql.Identifier(table_name),
                sql.SQL(keys),
                sql.SQL(placeholders)
            )
            data = [tuple(record.values()) for record in values]
            self.cursor.executemany(query, data)
            self.conn.commit()
        
        self.conn.close()

    def delete(self, table_name, id_value, condition=None):
        """
        Elimina un registro de la tabla especificada basado en el ID y una condición opcional.

        Args:
            table_name (str): Nombre de la tabla.
            id_value (int): ID del registro a eliminar.
            condition (str or None): Condición adicional para la eliminación.

        Returns:
            bool: True si el registro fue eliminado, False en caso contrario.
            dict: {'Error': str} en caso de error.
        """
        try:
            self.connection()

            if condition is None:
                query = sql.SQL("DELETE FROM {} WHERE ID = %s").format(sql.Identifier(table_name))
                self.cursor.execute(query, (id_value,))
            else:
                query = sql.SQL("DELETE FROM {} WHERE ID = %s AND {}").format(
                    sql.Identifier(table_name),
                    sql.SQL(condition)
                )
                self.cursor.execute(query, (id_value,))
            
            self.conn.commit()
            rows_deleted = self.cursor.rowcount
            return rows_deleted > 0

        except Exception as e:
            return {"Error": str(e)}

        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()

    def update(self, table_name, id_tabla, condition, data=None):
        """
        Actualiza registros en la tabla especificada.

        Args:
            table_name (str): Nombre de la tabla.
            id_tabla (int): ID del registro a actualizar.
            condition (str): Nuevo valor para actualizar (solo para la tabla "receta").
            data (dict or None): Diccionario con columnas y valores para actualizar (para otras tablas).

        Returns:
            dict: {'success': int} con el número de filas afectadas, o {'error': str} en caso de error.
        """
        self.connection()
        if table_name == "receta":
            query = sql.SQL("""
                UPDATE receta
                SET costo_receta = %s
                WHERE id = %s;
            """)
            try:
                self.cursor.execute(query, (condition, id_tabla))
                self.conn.commit()
                return {"success": self.cursor.rowcount}
            except Exception as e:
                return {"error": str(e)}
        elif table_name == "ingredientes":
            set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
            query = sql.SQL("""
                UPDATE {table}
                SET {set_clause}
                WHERE id = %s;
            """).format(
                table=sql.Identifier(table_name),
                set_clause=sql.SQL(set_clause)
            )
            self.cursor.execute(query, list(data.values()) + [id_tabla])
            self.conn.commit()
        self.conn.close()

    def selection(self, table_name, condition=None, boll=False, param: list = []):
        """
        Selecciona datos de la tabla especificada. Puede incluir condiciones y filtros adicionales.

        Args:
            table_name (str): Nombre de la tabla.
            condition (str or None): Condición para la selección de datos.
            boll (bool): Si True, se realiza una consulta con un CTE para seleccionar datos únicos.
            param (list): Parámetros adicionales para la consulta.

        Returns:
            list: Resultados de la consulta.
            dict: {'404': 'no hay valores'} si no hay resultados.
        """
        self.connection()
        if condition is None:
            query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name))
            self.cursor.execute(query)
            return self.cursor.fetchall()
        elif condition and not boll:
            query = sql.SQL("SELECT * FROM {} {}").format(
                sql.Identifier(table_name),
                sql.SQL(condition)
            )
            self.cursor.execute(query, param)
            return self.cursor.fetchone()
        elif condition and boll:
            query = sql.SQL("""
            WITH RankedIngredients AS (
                SELECT
                    id,
                    id_ingrediente,
                    id_receta,
                    cantidad,
                    precio,
                    ROW_NUMBER() OVER (PARTITION BY id_ingrediente ORDER BY created_at DESC) AS rn
                FROM
                    {}
                WHERE
                    id_receta = %s
            )
            SELECT
                id,
                id_ingrediente,
                id_receta,
                cantidad,
                precio
            FROM
                RankedIngredients
            WHERE
                rn = 1;
            """).format(sql.Identifier(table_name))
            self.cursor.execute(query, (condition,))
            return self.cursor.fetchall()
        else:
            return {"404": "no hay valores"}

    def init_data(self):
        """
        Inicializa las tablas en la base de datos usando los esquemas proporcionados en `tables`.
        """
        for t in tables[0]:
            self.create_table(t, tables[0][t])




# import sqlite3
# from data.data_injection import tables

# class Database_manager:
#     def __init__(self,db_name):
#         self.db_name = db_name
#         self.conn = sqlite3.connect(db_name)
#         self.cursor = self.conn.cursor()
#     def connection(self):
#         self.conn = sqlite3.connect(self.db_name)
#         self.cursor = self.conn.cursor()
#         return self.cursor

#     def create_table(self, table_name,columns:dict):
#         self.connection()
#         columns_with_types = ", ".join([f"{col} {typ}"for col, typ in columns.items()])
#         create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_with_types})"
#         self.cursor.execute(create_table_sql)
#         self.conn.commit()
#         self.conn.close()
#     def insert(self,table_name, values:list):
#         self.connection()
#         keys = ", ".join(values[0].keys())
#         placeholders = ", ".join("?" * len(values[0]))
#         global exists
#         if table_name == "ingredientes":
#             self.cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE nombre = ?",(values[0]["nombre"],))
#             exists = self.cursor.fetchone()[0] > 0
#         elif table_name == "cant_ing":
#             query = f"INSERT INTO {table_name} ({keys})VALUES ({placeholders})"
#             datos = [tuple(record.values())for record in values]
#             self.cursor.executemany(query,datos)
#             self.conn.commit()
#         if not exists:
#             query = f"INSERT INTO {table_name} ({keys})VALUES ({placeholders})"
#             datos = [tuple(record.values())for record in values]
#             self.cursor.executemany(query,datos)
#             self.conn.commit()
#         self.conn.close()
#     def delete(self,table_name,id_value,condition=None):
#         self.connection()
#         if condition == None:
#             query = f"DELETE FROM {table_name} WHERE ID = ?"
#             self.cursor.execute(query,(id_value,))

#             self.conn.commit()
#         self.conn.close()
#     def update(self,table_name,values,condition):
#         pass
#     def selection(self,table_name,condition=None,param:list=[]):
#         self.connection()
#         if condition == None:
#             query = f"SELECT * FROM {table_name}"
#             self.cursor.execute(query)
#             return self.cursor.fetchall()
#         elif condition:
#             query = f"SELECT * FROM {table_name} {condition}"
#             self.cursor.execute(query,(param[0],param[1]))
#             return self.cursor.fetchone()

#         else:
#             return {"404":"no hay valores"}
        


#     def init_data(self):
#         for t in tables[0]:
#             self.create_table(t,tables[0][t])
