from tkinter import ttk
from tkinter import *
import tkinter as tk
import os
from os import *
from tkinter.messagebox import askokcancel, showinfo
from MostrarReceta import MostrarReceta
from Receta import Receta
from PIL import Image,ImageTk 
from PIL import *
from VentanaAgregar import VentanaAgregar
from VentanaEditar import VentanaEditar
from inicio import Inicio

class App(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent=parent
        width=950
        height=700
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        parent.geometry(alignstr)
        parent.title('BiblioRecetas')
        self.parent.iconbitmap('media/icono_recetario.ico')
            
        self.frame=tk.Frame(parent)
        self.frame.pack(expand=1)
        
        self.combo_lista=StringVar()
        self.combo_elementos=StringVar()
        
        carpeta_principal=os.path.dirname(__file__)
        self.carpeta_img=os.path.join(carpeta_principal,'media')
        imagen_logo=Image.open(os.path.join(self.carpeta_img,'imagen recetario final.png'))
        self.img_logo=ImageTk.PhotoImage(imagen_logo)
        imagen_red_logo=imagen_logo.resize((300,250),Image.LANCZOS)
        self.img_logo=ImageTk.PhotoImage(imagen_red_logo)
        self.lb_imagen_recetario=ttk.Label(self.frame,image=self.img_logo).grid(row=0,column=0,columnspan=2,padx=15)
        
        self.frame_filtro=ttk.Frame(self.frame)
        self.frame_filtro=ttk.Labelframe(self.frame,text='Filtrar')
        self.frame_filtro.grid(row=1,column=0,columnspan=2)
        
        self.lb_filtro=ttk.Label(self.frame_filtro,text='Filtrar por: ').grid(row=0,column=0,sticky=E,pady=10,padx=(15,0))
        
        self.lista_filtro=ttk.Combobox(self.frame_filtro,textvariable=self.combo_lista)
        self.lista_filtro["values"] = ('Nombre','Etiqueta','Tiempo de Preparación','Ingrediente','Favorita')
        self.lista_filtro["state"] = "readonly"        
        self.lista_filtro.grid(row=0,column=1,pady=10,padx=(0,15))
        self.lista_filtro.bind('<<ComboboxSelected>>', self.elementos_lista)
        
        self.lb_seleccion=ttk.Label(self.frame_filtro,text='Elegir opción: ').grid(row=1,column=0,sticky=E,pady=10,padx=(15,0))

        self.lista_filtro=ttk.Combobox(self.frame_filtro,textvariable=self.combo_elementos)
        self.lista_filtro["state"] = "readonly"        
        self.lista_filtro.grid(row=1,column=1,pady=10,padx=(0,15))
        
        self.btn_filtrar=ttk.Button(self.frame_filtro,text='Filtrar',command=self.filtrar).grid(row=2,column=0,columnspan=2,pady=10)
        
        self.btn_agregar=ttk.Button(self.frame,text='Agregar Receta',width=20,command=self.ventana_agregar)
        self.btn_agregar.grid(row=3,column=0)
        
        self.btn_editar=ttk.Button(self.frame,text='Editar Receta',width=20,command=self.ventana_editar)
        self.btn_editar.grid(row=3,column=1)
        
        self.btn_eliminar=ttk.Button(self.frame,text='Eliminar Receta',width=20,command=self.eliminar_receta)
        self.btn_eliminar.grid(row=4,column=0)
        
        self.btn_mostrar=ttk.Button(self.frame,text='Ver Receta',width=20,command=self.ver_receta)
        self.btn_mostrar.grid(row=4,column=1)
        
        s = ttk.Style()
        s.configure(
                     "MyButton.TButton",
                     font=('',15,'bold'),                    
                )
        self.btn_receta_aleatoria=ttk.Button(self.frame,text='Ver Receta del Día',style="MyButton.TButton",padding=(60,15),command=self.ver_receta_del_dia)
        self.btn_receta_aleatoria.grid(row=6,column=0,columnspan=2)
        
        frame_lista=ttk.Frame(self.frame)
        frame_lista=LabelFrame(self.frame,text='Recetas')
        frame_lista.grid(row=0, column=3,columnspan=5,rowspan=10,padx=10) 
        cabecera=('Nombre','Tiempo de Preparación','Tiempo de Cocción')
        
        self.btn_mostrar_receta=ttk.Button(frame_lista,text='Actualizar/Mostrar Recetas',command=self.mostrar_recetas)
        self.btn_mostrar_receta.pack()
        
        # configuracion del alto de las filas rowheight
        arbol=ttk.Style()
        arbol.configure('my_style.Treeview', rowheight=80)
        tree_scroll=ttk.Scrollbar(frame_lista)
        tree_scroll.pack(side='right',fill='y')
        self.tabla=ttk.Treeview(frame_lista,columns=tuple(cabecera),style='my_style.Treeview',yscrollcommand=tree_scroll.set,selectmode='browse',show='tree',height=7)
        self.tabla.pack(padx=20,pady=20)
        tree_scroll.config(command=self.tabla.yview)
    
        if not os.path.exists(self.carpeta_img):
            os.makedirs(self.carpeta_img) 
                    
        self.tabla.column('#0',width=120,anchor='center')
        self.tabla.column('Nombre',width=150,anchor='center')
        self.tabla.column('Tiempo de Preparación',width=120,anchor='center')
        self.tabla.column('Tiempo de Cocción',width=120,anchor='center')    
        
    def mostrar_recetas(self):
        for i in self.tabla.get_children():
            self.tabla.delete(i) 
        # imagen=Image.open(os.path.join(self.carpeta_img,"milanesa.png"))
        # imagen_red=imagen.resize((120,80),Image.LANCZOS)
        # self.img_red=ImageTk.PhotoImage(imagen_red)
        for r in Receta.lista_recetas():
            imagen=Image.open(os.path.join(self.carpeta_img,r['Imagen']))
            imagen_red=imagen.resize((120,80),Image.LANCZOS)
            self.img_red=ImageTk.PhotoImage(imagen_red)
            self.tabla.insert("","end",image=self.img_red,values=(r['Nombre'],'Tiempo Preparación:\n'+str(r['Tiempo_preparacion'])+' Minutos','Tiempo de Cocción:\n'+str(r['Tiempo_coccion'])+' Minutos'))        
            #self.tabla.bind("<<TreeviewSelect>>", self.ver_receta)
            
    def ventana_agregar(self):
        toplevel=tk.Toplevel(self.parent)
        VentanaAgregar(toplevel)
        
    def ventana_editar(self):
        seleccion = self.tabla.selection()
        if seleccion:
            item = self.tabla.item(seleccion)
            fila = item['values'][0]
            receta=Receta.buscar_receta_nombre(fila)
            toplevel=tk.Toplevel(self.parent)
            VentanaEditar(toplevel,receta.get('Nombre'),receta.get('Ingredientes'),receta.get('Tiempo_preparacion'),
                        receta.get('Tiempo_coccion'),receta.get('Preparacion'),receta.get('Etiquetas'),receta.get('Imagen'),bool(receta.get('Favorita')))
        else:
            showinfo(message="Debe seleccionar una elemento primero")   
        
    def eliminar_receta(self):
        seleccion = self.tabla.selection()
        if seleccion:
            item = self.tabla.item(seleccion)
            fila = str(item['values'][0]) 
            for item in seleccion:
                res = askokcancel(title="Eliminar fila",
                    message=("Eliminar receta?"
                    "\n" + "".join(fila)))
                if res:
                    self.tabla.delete(item)
                    rec=Receta.buscar_receta_nombre(fila)
                    ruta_img=rec['Imagen']
                    print(ruta_img)
                    if ruta_img != 'sin_imagen.jpg':
                        remove(f'media/{ruta_img}')
                    Receta.eliminar_receta(fila)
                    
        else:
            showinfo(message="Debe seleccionar un elemento primero")  
            
    def ver_receta(self):#si se coloca un event se puede utilizar la funcion de ver solo seleccionando la receta
        seleccion = self.tabla.selection()
        if seleccion:
            item = self.tabla.item(seleccion)
            fila = item['values'][0]
            receta=Receta.buscar_receta_nombre(fila)
            toplevel=tk.Toplevel(self.parent)
            MostrarReceta(toplevel,receta.get('Nombre'),receta.get('Etiquetas'),receta.get('Tiempo_preparacion'),
                        receta.get('Tiempo_coccion'),receta.get('Ingredientes'),receta.get('Imagen'),receta.get('Preparacion'),
                        receta.get('Fecha_creacion'))
        else:
            showinfo(message="Debe seleccionar un elemento primero") 
            
    def ver_receta_del_dia(self):
        receta=Receta.receta_del_dia()
        toplevel=tk.Toplevel(self.parent)
        MostrarReceta(toplevel,receta.get('Nombre'),receta.get('Etiquetas'),receta.get('Tiempo_preparacion'),
                        receta.get('Tiempo_coccion'),receta.get('Ingredientes'),receta.get('Imagen'),receta.get('Preparacion'),
                        receta.get('Fecha_creacion'))     
    
    def elementos_lista(self,evento):
        elemento_a_filtrar=self.combo_lista.get()
        lista=[]
        self.combo_elementos.set('')
        if elemento_a_filtrar=='Nombre':
            for r in Receta.lista_recetas():
                lista.append(r['Nombre'])
        if elemento_a_filtrar=='Etiqueta':
            conj=set()
            for r in Receta.lista_recetas():
                cade=r['Etiquetas']
                l_cade=cade.split(sep=',')
                for eti in l_cade:
                    if eti!='':
                        conj.add(eti)
            lista=list(conj)        
        if elemento_a_filtrar=='Tiempo de Preparación':
            conj=set()
            for r in Receta.lista_recetas():
                conj.add(r['Tiempo_preparacion'])
            lista=list(conj)    
        if elemento_a_filtrar=='Ingrediente':
            conj=set()
            for receta in Receta.lista_recetas():
                for r in receta['Ingredientes']:
                    conj.add(r[2])
            lista=list(conj)            
        if elemento_a_filtrar=='Favorita':                       
            lista = ['Es Favorita','No es Favorita']
        lista.sort()
        self.lista_filtro["values"] = tuple(lista)    
    
    def filtrar(self):
        elemento_a_filtrar=self.combo_lista.get()
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        if elemento_a_filtrar=='Nombre':
            for r in Receta.lista_recetas():
                if r['Nombre']==self.combo_elementos.get():
                    imagen=Image.open(os.path.join(self.carpeta_img,r['Imagen']))
                    imagen_red=imagen.resize((120,80),Image.LANCZOS)
                    self.img_red=ImageTk.PhotoImage(imagen_red)
                    self.tabla.insert("","end",image=self.img_red,values=(r['Nombre'],'Tiempo Preparación:\n'+str(r['Tiempo_preparacion'])+' Minutos','Tiempo de Cocción:\n'+str(r['Tiempo_coccion'])+' Minutos'))        

        if elemento_a_filtrar=='Etiqueta':
            for r in Receta.lista_recetas():
                if self.combo_elementos.get() in r['Etiquetas'].split(sep=','):
                    imagen=Image.open(os.path.join(self.carpeta_img,r['Imagen']))
                    imagen_red=imagen.resize((120,80),Image.LANCZOS)
                    self.img_red=ImageTk.PhotoImage(imagen_red)
                    self.tabla.insert("","end",image=self.img_red,values=(r['Nombre'],'Tiempo Preparación:\n'+str(r['Tiempo_preparacion'])+' Minutos','Tiempo de Cocción:\n'+str(r['Tiempo_coccion'])+' Minutos'))        
      
        if elemento_a_filtrar=='Tiempo de Preparación':
            for r in Receta.lista_recetas():
                if str(r['Tiempo_preparacion'])==self.combo_elementos.get():
                    imagen=Image.open(os.path.join(self.carpeta_img,r['Imagen']))
                    imagen_red=imagen.resize((120,80),Image.LANCZOS)
                    self.img_red=ImageTk.PhotoImage(imagen_red)
                    self.tabla.insert("","end",image=self.img_red,values=(r['Nombre'],'Tiempo Preparación:\n'+str(r['Tiempo_preparacion'])+' Minutos','Tiempo de Cocción:\n'+str(r['Tiempo_coccion'])+' Minutos'))        
   
        if elemento_a_filtrar=='Ingrediente':
            for r in Receta.lista_recetas():
                for ing in r['Ingredientes']:
                    if ing[2]==self.combo_elementos.get():
                        imagen=Image.open(os.path.join(self.carpeta_img,r['Imagen']))
                        imagen_red=imagen.resize((120,80),Image.LANCZOS)
                        self.img_red=ImageTk.PhotoImage(imagen_red)
                        self.tabla.insert("","end",image=self.img_red,values=(r['Nombre'],'Tiempo Preparación:\n'+str(r['Tiempo_preparacion'])+' Minutos','Tiempo de Cocción:\n'+str(r['Tiempo_coccion'])+' Minutos'))        
            
        if elemento_a_filtrar=='Favorita':
            fav=bool
            if self.combo_elementos.get()=='Es Favorita':
                fav=True                       
            else:
                fav=False    
            for r in Receta.lista_recetas():
                if r['Favorita']==fav:
                    imagen=Image.open(os.path.join(self.carpeta_img,r['Imagen']))
                    imagen_red=imagen.resize((120,80),Image.LANCZOS)
                    self.img_red=ImageTk.PhotoImage(imagen_red)
                    self.tabla.insert("","end",image=self.img_red,values=(r['Nombre'],'Tiempo Preparación:\n'+str(r['Tiempo_preparacion'])+' Minutos','Tiempo de Cocción:\n'+str(r['Tiempo_coccion'])+' Minutos'))        
       
            
if __name__=='__main__':
    Inicio(tk.Tk()).mainloop()      
    App(tk.Tk()).mainloop()
            