import datetime
import json
import random
import conector
import config
from datetime import date
from mysql.connector import errors
class Receta:
    def __init__(self, nombre, ingredientes, preparacion, tiempo_preparacion, 
                 tiempo_coccion, etiquetas,
                 imagen=None, favorita=False):
        self.nombre=nombre
        self.ingredientes=ingredientes
        self.preparacion=preparacion
        self.imagen=imagen
        self.tiempo_preparacion=tiempo_preparacion
        self.tiempo_coccion=tiempo_coccion
        self.fecha_creacion=(str) (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.etiquetas=etiquetas
        self.favorita=favorita 
        
    def crear_receta(self):
        receta={
            'Nombre':self.nombre,
            'Ingredientes':self.ingredientes,
            'Preparacion':self.preparacion,
            'Imagen':self.imagen,
            'Tiempo_preparacion':self.tiempo_preparacion,
            'Tiempo_coccion':self.tiempo_coccion,
            'Fecha_creacion':self.fecha_creacion,
            'Etiquetas':self.etiquetas,
            'Favorita':self.favorita
        }  
        conn=conector.conectar()
        cursor=conn.cursor()
        try:
            query_receta='''INSERT INTO recetario.recetas (nombre,preparacion,imagen,tiempo_preparacion,tiempo_coccion,favorita)
                        values(%s,%s,%s,%s,%s,%s)'''        
            cursor.execute(query_receta,(receta['Nombre'],receta['Preparacion'],receta['Imagen'],receta['Tiempo_preparacion'],
                                        receta['Tiempo_coccion'],receta['Favorita']))  
            conn.commit()  
            ultimo_id = cursor.lastrowid    
            
            cursor.execute('SELECT nombre FROM recetario.ingredientes')
            ingredientes=[elemento[0] for elemento in cursor.fetchall()]
            for ingrediente in receta['Ingredientes']:
                if ingrediente[2] not in ingredientes:
                    query_ing='INSERT INTO recetario.ingredientes (nombre) values(%s)'
                    cursor.execute(query_ing,(ingrediente[2],))
                    conn.commit()
                cursor.execute('SELECT id FROM recetario.ingredientes WHERE ingredientes.nombre=%s',(ingrediente[2],))
                id_ing=cursor.fetchone()[0]
                cursor.execute('''INSERT INTO recetario.receta_ingrediente(id_receta,id_ingrediente,cantidad,medida)
                               values(%s,%s,%s,%s)''',(ultimo_id,id_ing,ingrediente[0],ingrediente[1],))
                conn.commit()
                
            cursor.execute('SELECT nombre FROM recetario.etiquetas')
            etiquetas=[elemento[0] for elemento in cursor.fetchall()]
            lista_etiquetas = receta['Etiquetas'].split(",")
            for etiqueta in lista_etiquetas:
                if etiqueta not in etiquetas:
                    query_etiq='INSERT INTO recetario.etiquetas (nombre) values(%s)'
                    cursor.execute(query_etiq,(etiqueta,))
                    conn.commit()
                cursor.execute('SELECT id FROM recetario.etiquetas WHERE etiquetas.nombre=%s',(etiqueta,))
                id_etiq=cursor.fetchone()[0]
                cursor.execute('''INSERT INTO recetario.receta_etiqueta(id_receta,id_etiqueta)
                               values(%s,%s)''',(ultimo_id,id_etiq,))
                conn.commit()    
            conn.close()   
             
        except errors.DatabaseError as err:
            print("Error al conectar.", err)
            conn.close()          
    
    def modificar_receta(self):  
        receta={
        'Nombre':self.nombre,
        'Ingredientes':self.ingredientes,
        'Preparacion':self.preparacion,
        'Imagen':self.imagen,
        'Tiempo_preparacion':self.tiempo_preparacion,
        'Tiempo_coccion':self.tiempo_coccion,
        'Fecha_creacion':self.fecha_creacion,
        'Etiquetas':self.etiquetas,
        'Favorita':self.favorita
        }      
        conn=conector.conectar()
        cursor=conn.cursor()
        try:
            obtener_id_receta='SELECT id FROM recetario.recetas WHERE recetas.nombre=%s'
            cursor.execute(obtener_id_receta,(receta['Nombre'],))
            id_receta=cursor.fetchone()[0]
            query_receta='''UPDATE recetario.recetas set preparacion=%s,imagen=%s,tiempo_preparacion=%s,tiempo_coccion=%s,favorita=%s WHERE recetas.nombre=%s'''                    
            cursor.execute(query_receta,(receta['Preparacion'],receta['Imagen'],receta['Tiempo_preparacion'],
                                        receta['Tiempo_coccion'],receta['Favorita'],receta['Nombre'],))  
            conn.commit()  
            query_elim_ing='''DELETE FROM recetario.receta_ingrediente WHERE receta_ingrediente.id_receta=%s'''
            cursor.execute(query_elim_ing,(id_receta,)) 
            conn.commit()
            query_elim_etiq='''DELETE FROM recetario.receta_etiqueta WHERE receta_etiqueta.id_receta=%s'''
            cursor.execute(query_elim_etiq,(id_receta,)) 
            conn.commit()
                
            cursor.execute('SELECT nombre FROM recetario.ingredientes')
            ingredientes=[elemento[0] for elemento in cursor.fetchall()]
            for ingrediente in receta['Ingredientes']:
                if ingrediente[2] not in ingredientes:
                    query_ing='INSERT INTO recetario.ingredientes (nombre) values(%s)'
                    cursor.execute(query_ing,(ingrediente[2],))
                    conn.commit()
                cursor.execute('SELECT id FROM recetario.ingredientes WHERE ingredientes.nombre=%s',(ingrediente[2],))
                id_ing=cursor.fetchone()[0]
                cursor.execute('''INSERT INTO recetario.receta_ingrediente(id_receta,id_ingrediente,cantidad,medida)
                               values(%s,%s,%s,%s)''',(id_receta,id_ing,ingrediente[0],ingrediente[1],))
                conn.commit()
            cursor.execute('SELECT nombre FROM recetario.etiquetas')
            etiquetas=[elemento[0] for elemento in cursor.fetchall()]
            lista_etiquetas = receta['Etiquetas'].split(",")
            for etiqueta in lista_etiquetas:
                if etiqueta not in etiquetas:
                    query_etiq='INSERT INTO recetario.etiquetas (nombre) values(%s)'
                    cursor.execute(query_etiq,(etiqueta,))
                    conn.commit()
                cursor.execute('SELECT id FROM recetario.etiquetas WHERE etiquetas.nombre=%s',(etiqueta,))
                id_etiq=cursor.fetchone()[0]
                cursor.execute('''INSERT INTO recetario.receta_etiqueta(id_receta,id_etiqueta)
                               values(%s,%s)''',(id_receta  ,id_etiq,))
                conn.commit()    
            conn.close()   
        except errors.DatabaseError as err:
            print("Error al conectar.", err)
            conn.close()        
    
    def eliminar_receta(nombre):
        conn=conector.conectar()
        cursor=conn.cursor()
        try:
            query_receta='''SELECT id FROM recetario.recetas WHERE recetas.nombre=%s'''  
            cursor.execute(query_receta,(nombre,))  
            id_receta=cursor.fetchone()[0]
            query_elim_ing='''DELETE FROM recetario.receta_ingrediente WHERE receta_ingrediente.id_receta=%s'''
            cursor.execute(query_elim_ing,(id_receta,)) 
            conn.commit()
            query_elim_etiq='''DELETE FROM recetario.receta_etiqueta WHERE receta_etiqueta.id_receta=%s'''
            cursor.execute(query_elim_etiq,(id_receta,)) 
            conn.commit()      
            query_elim_receta='''DELETE FROM recetario.recetas WHERE recetas.id=%s'''     
            cursor.execute(query_elim_receta,(id_receta,))          
            conn.commit()     
            conn.close()   
             
        except errors.DatabaseError as err:
            print("Error al conectar.", err)
            conn.close()                       
                  
    def receta_del_dia():
        conn=conector.conectar()
        cursor=conn.cursor()
        try:
            fecha=''
            try:
                query_fecha='SELECT fecha FROM recetario.receta_del_dia'
                cursor.execute(query_fecha)
                fecha=cursor.fetchone()[0]
            except:
                None    
            if fecha != date.today() or fecha=='':
                eliminar_datos='DELETE FROM recetario.receta_del_dia'
                cursor.execute(eliminar_datos)
                conn.commit()
                cursor.execute('SELECT id FROM recetario.recetas')
                id_recetas=cursor.fetchall()
                lista = tuple(zip(*id_recetas))[0]
                id_receta_random=random.choice(lista)
                agregar_receta='''INSERT INTO recetario.receta_del_dia(id_receta,fecha) values(%s,%s)'''
                cursor.execute(agregar_receta,(id_receta_random,date.today(),))
                conn.commit()
            id_receta_dia_query='''SELECT id_receta FROM recetario.receta_del_dia'''
            cursor.execute(id_receta_dia_query)
            id_receta_dia=cursor.fetchone()[0] 
            query_receta='''SELECT A.nombre, GROUP_CONCAT(DISTINCT CONCAT(B.cantidad, ' ', B.medida, ' ', C.nombre) SEPARATOR ',') AS ingredientes, A.tiempo_preparacion, A.tiempo_coccion, A.preparacion, GROUP_CONCAT(DISTINCT E.nombre), A.imagen, A.favorita,A.id
                        FROM recetario.recetas A
                        INNER JOIN recetario.receta_ingrediente B ON A.id = B.id_receta
                        INNER JOIN recetario.ingredientes C ON B.id_ingrediente = C.id
                        INNER JOIN recetario.receta_etiqueta D ON A.id = D.id_receta
                        INNER JOIN recetario.etiquetas E ON D.id_etiqueta = E.id
                        WHERE A.id=%s
                        GROUP BY A.nombre
                        '''  
            cursor.execute(query_receta,(id_receta_dia,))  
            receta=cursor.fetchone()
            ings=receta[1].split(',')
            ingredientes=[]
            for ing in ings:
                palabras = ing.split()
                valor = int(palabras[0])
                unidad = palabras[1]
                nombre = ' '.join(palabras[2:])
                ingredientes.append((valor, unidad, nombre))
            receta_datos={
            'Nombre':receta[0],
            'Ingredientes':ingredientes,
            'Tiempo_preparacion':receta[2],
            'Tiempo_coccion':receta[3],
            'Preparacion':receta[4],
            'Etiquetas':receta[5],
            'Imagen':receta[6],
            'Favorita':receta[7]
            }   
            return receta_datos    
        except errors.DatabaseError as err:
            print("Error al conectar.", err)
            conn.close()             
    
    def buscar_receta_nombre(nombre):
        conn=conector.conectar()
        cursor=conn.cursor()
        try:
            query_receta='''SELECT A.nombre, GROUP_CONCAT(DISTINCT CONCAT(B.cantidad, ' ', B.medida, ' ', C.nombre) SEPARATOR ',') AS ingredientes, A.tiempo_preparacion, A.tiempo_coccion, A.preparacion, GROUP_CONCAT(DISTINCT E.nombre), A.imagen, A.favorita,A.fecha_creacion
                        FROM recetario.recetas A
                        INNER JOIN recetario.receta_ingrediente B ON A.id = B.id_receta
                        INNER JOIN recetario.ingredientes C ON B.id_ingrediente = C.id
                        INNER JOIN recetario.receta_etiqueta D ON A.id = D.id_receta
                        INNER JOIN recetario.etiquetas E ON D.id_etiqueta = E.id
                        WHERE A.nombre=%s
                        GROUP BY A.nombre
                        '''  
            cursor.execute(query_receta,(nombre,)) 
            receta=cursor.fetchone()
            ings=receta[1].split(',')
            ingredientes=[]
            for ing in ings:
                palabras = ing.split()
                valor = int(palabras[0])
                unidad = palabras[1]
                nombre = ' '.join(palabras[2:])
                ingredientes.append((valor, unidad, nombre))
            receta_datos={
            'Nombre':receta[0],
            'Ingredientes':ingredientes,
            'Tiempo_preparacion':receta[2],
            'Tiempo_coccion':receta[3],
            'Preparacion':receta[4],
            'Etiquetas':receta[5],
            'Imagen':receta[6],
            'Favorita':receta[7],
            'Fecha_creacion':receta[8]
            }   
            return receta_datos    
        except errors.DatabaseError as err:
            print("Error al conectar.", err)
            conn.close()  
            
    @staticmethod
    def lista_recetas():        
        conn=conector.conectar()
        cursor=conn.cursor()
        try:
            query_receta='''SELECT A.nombre, GROUP_CONCAT(DISTINCT CONCAT(B.cantidad, ' ', B.medida, ' ', C.nombre) SEPARATOR ',') AS ingredientes, A.tiempo_preparacion, A.tiempo_coccion, A.preparacion, GROUP_CONCAT(DISTINCT E.nombre), A.imagen, A.favorita
                        FROM recetario.recetas A
                        INNER JOIN recetario.receta_ingrediente B ON A.id = B.id_receta
                        INNER JOIN recetario.ingredientes C ON B.id_ingrediente = C.id
                        INNER JOIN recetario.receta_etiqueta D ON A.id = D.id_receta
                        INNER JOIN recetario.etiquetas E ON D.id_etiqueta = E.id
                        GROUP BY A.nombre
                        '''  
            cursor.execute(query_receta) 
            recetas=cursor.fetchall()
            lista_recetas=[]
            for receta in recetas:
                ings=receta[1].split(',')
                ingredientes=[]
                for ing in ings:
                    palabras = ing.split()
                    valor = int(palabras[0])
                    unidad = palabras[1]
                    nombre = ' '.join(palabras[2:])
                    ingredientes.append((valor, unidad, nombre))
                receta_datos={
                'Nombre':receta[0],
                'Ingredientes':ingredientes,
                'Tiempo_preparacion':receta[2],
                'Tiempo_coccion':receta[3],
                'Preparacion':receta[4],
                'Etiquetas':receta[5],
                'Imagen':receta[6],
                'Favorita':receta[7]
                } 
                lista_recetas.append(receta_datos)  
            return lista_recetas    
        except errors.DatabaseError as err:
            print("Error al conectar.", err)
            conn.close()
