from tkinter import ttk
from tkinter import *
import tkinter as tk
import os
from os import *
from PIL import Image,ImageTk 
from PIL import *
import tkinter.font as tkFont


class MostrarReceta(ttk.Frame):
    def __init__(self,parent,nombre,etiquetas,tiempo_preparacion,tiempo_coccion,ingredientes,imagen,preparacion,fecha_creacion):
        super().__init__(parent)
        self.parent=parent
        width=920
        height=600
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        parent.geometry(alignstr) 
        parent.title('BiblioRecetas')
        parent.iconbitmap('media/icono_recetario.ico')
        
        carpeta_principal=os.path.dirname(__file__)
        self.carpeta_img=os.path.join(carpeta_principal,'media')
        imagen=Image.open(os.path.join(self.carpeta_img,imagen))
        self.img=ImageTk.PhotoImage(imagen)
        imagen_red=imagen.resize((400,300),Image.LANCZOS)
        self.img_red=ImageTk.PhotoImage(imagen_red)
        
        titulo=tkFont.Font(family='Arial',size=30,weight='bold')
        sub_titulo=tkFont.Font(family='Arial',size=20,weight='bold')
        font_italica=tkFont.Font(family='Arial',size=9,slant='italic')
        font_normal=tkFont.Font(family='Arial',size=10)
        
        self.label_nombre=ttk.Label(parent,text=nombre,font=titulo).grid(row=0,column=1,columnspan=3,pady=(20,0))
        self.label_fecha=ttk.Label(parent,text=f'Creación: {fecha_creacion}',font=font_italica).grid(row=1,column=1,padx=5,pady=5,sticky=W)
        self.label_etiqueta=ttk.Label(parent,text=f'Etiquetas: {etiquetas}',font=font_italica).grid(row=1,column=2,columnspan=2,pady=5,sticky=W)
        self.label_tp=ttk.Label(parent,text=f'Tiempo preparación: {tiempo_preparacion}min',font=font_italica).grid(row=2,column=1,padx=5,pady=5,sticky=W)
        self.label_tc=ttk.Label(parent,text=f'Tiempo Cocción: {tiempo_coccion}min',font=font_italica).grid(row=2,column=2,padx=5,sticky=W)
        self.label_tit_ing=ttk.Label(parent,text='Ingredientes:',font=sub_titulo).grid(row=3,column=1,pady=(20,5),sticky=W)

        i=0 
        colum=1
        for ing in ingredientes:
                self.label_ing=ttk.Label(parent,text=f'{ing[0]} {ing[1]} {ing[2]}',font=font_normal).grid(row=4+i,column=colum,sticky=W)
                i+=1
                if i==5:
                    colum+=1
                    i=0
        self.label_img=ttk.Label(parent,image=self.img_red).grid(row=0,column=0,rowspan=20,padx=(0,10))
        self.label_tit_prep=ttk.Label(parent,text='Preparación:',font=sub_titulo).grid(row=21,column=0,columnspan=4)
        self.label_prep=ttk.Label(parent,text=preparacion,width=120,wraplength=700)
        self.label_prep.grid(row=22,column=0,columnspan=4)
         