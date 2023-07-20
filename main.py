import VentanaPrincipal
import inicio
import tkinter as tk
import conector

if __name__=='__main__':
    conector.create_if_not_exists()
    inicio.Inicio(tk.Tk()).mainloop()      
    VentanaPrincipal.App(tk.Tk()).mainloop()
            
