import mysql.connector 
from mysql.connector import errors
import config

def conectar():
    try:
        conn = mysql.connector.connect(user=config.credenciales["user"],
                                    password=config.credenciales["password"],
                                    host=config.credenciales["host"])
    except errors.DatabaseError as err:
        print("Error al conectar.", err)
    else:
        return conn

def create_if_not_exists():
    crear_database = "CREATE DATABASE IF NOT EXISTS %s" %config.credenciales["database"]
    tabla_recetas='''CREATE TABLE IF NOT EXISTS recetas(
                id INT NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR (50) UNIQUE NOT NULL,
                preparacion TEXT NOT NULL,
                imagen VARCHAR(255) NOT NULL,
                tiempo_preparacion INT NOT NULL,
                tiempo_coccion INT NOT NULL,
                fecha_creacion TIMESTAMP DEFAULT NOW(),
                favorita TINYINT NOT NULL
                )'''
    tabla_ingredientes='''CREATE TABLE IF NOT EXISTS ingredientes(
                id INT NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) UNIQUE NOT NULL)'''
    tabla_etiqueta='''CREATE TABLE IF NOT EXISTS etiquetas(
                id INT NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) UNIQUE NOT NULL)'''
    tabla_receta_etiqueta='''CREATE TABLE IF NOT EXISTS receta_etiqueta(
                id INT NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
                id_receta INT NOT NULL,
                id_etiqueta INT NOT NULL,
                FOREIGN KEY (id_receta) REFERENCES recetas(id),
                FOREIGN KEY (id_etiqueta) REFERENCES etiquetas(id))'''            
    tabla_receta_ingrediente='''CREATE TABLE IF NOT EXISTS receta_ingrediente(
                id INT NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
                id_receta INT NOT NULL,
                id_ingrediente INT NOT NULL,
                cantidad FLOAT NOT NULL,
                medida VARCHAR (20) NOT NULL,
                FOREIGN KEY (id_receta) REFERENCES recetas(id),
                FOREIGN KEY(id_ingrediente) REFERENCES ingredientes(id))'''
    tabla_receta_del_dia='''CREATE TABLE IF NOT EXISTS receta_del_dia(
                id INT NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
                id_receta INT NOT NULL,
                fecha DATE,
                FOREIGN KEY (id_receta) REFERENCES recetas(id))'''
                           
    try:
        conn=conectar()
        cur = conn.cursor()
        cur.execute(crear_database)
        cur.execute("USE %s" %config.credenciales["database"])
        cur.execute(tabla_recetas)
        cur.execute(tabla_ingredientes)
        cur.execute(tabla_etiqueta)
        cur.execute(tabla_receta_etiqueta)
        cur.execute(tabla_receta_ingrediente)
        cur.execute(tabla_receta_del_dia)
        conn.close()
    except errors.DatabaseError as err:
        print("Error al conectar o crear la base de datos.", err)
        raise
   