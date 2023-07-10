from tkinter import *
import tkinter as tk
from tkinter import ttk
from PIL import Image,ImageTk 
from PIL import *
import time

class Inicio(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent=parent
        width=300
        height=350
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        parent.geometry(alignstr) 
        parent.title('BiblioRecetas')
        parent.iconbitmap('media/icono_recetario.ico')
        parent.overrideredirect(True)
        
        imagen=Image.open('media/imagen recetario final.png')
        imagen_red=imagen.resize((300,300),Image.LANCZOS)
        self.img=ImageTk.PhotoImage(imagen_red)
        self.label_img=ttk.Label(parent,image=self.img).grid(row=0,column=0)
        
        self.bar=ttk.Progressbar(parent,orient='horizontal',length=305)
        self.bar.grid(row=1,column=0)
        self.texto=StringVar()
        self.texto.set('Inicializando...')
        self.lb_inicio=ttk.Label(parent,textvariable=self.texto,justify='center').grid(row=2,column=0,sticky=EW)
    
        self.cargar_barra()
    def cargar_barra(self):
        task=100
        x=0
        while x<task:
            time.sleep(0.02)
            self.bar['value']+=1  
            x+=1  
            self.parent.update_idletasks()
            if x==50:
                self.texto.set('Cargando y leyendo fichero...')
        if x==100:
            self.parent.destroy()    


      
    
        
        