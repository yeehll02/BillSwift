import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

path = resource_path("src/dB")
sys.path.append(path)
path = resource_path("src/images")
sys.path.append(path)
path = resource_path("src/Lib")
sys.path.append(path)

import tkinter as tk
import ctypes
import datetime
from tkinter import ttk
from tkinter.font import Font
from tkinter import messagebox
from factura import Factura
from decimal import Decimal


class Ventana:

    numeroFactura = 1699
    cont = 0
    lista_labels = []
    listaProductos = []

    @classmethod
    def setNumeroFactura(cls, numeroFactura):
        cls.numeroFactura = numeroFactura

    @classmethod
    def getNumeroFactura (cls):
        return cls.numeroFactura

    def __init__(self):

        def seleccionar(event, r, c):
            
            if Ventana.lista_labels[r][c].cget('bg') == 'gray95':    
                Ventana.lista_labels[r][c].config(bg='RoyalBlue2')
            else:
                Ventana.lista_labels[r][c].config(bg="gray95")
             
        def borrar_filas():
            labels_eliminar = [] 
            for idfila, fila in enumerate(Ventana.lista_labels):
                for idlab, lab in enumerate(fila):
                    if lab.cget('bg') == 'RoyalBlue2':
                        labels_eliminar.append((idfila, idlab)) 
                        lab.destroy()               

            for idfila, idlab in reversed(labels_eliminar):
                Ventana.lista_labels[idfila].pop(idlab)
                Ventana.listaProductos[idfila].pop(idlab)

            while [] in Ventana.lista_labels:
                Ventana.lista_labels.remove([])

            while [] in Ventana.listaProductos:
                Ventana.listaProductos.remove([])

            for r in range(len(Ventana.lista_labels)):
                for c in range(len(Ventana.lista_labels[r])):
                    Ventana.lista_labels[r][c].unbind("<Button-1>")
                    Ventana.lista_labels[r][c].bind("<Button-1>", lambda event, row=r, col=c: seleccionar(event, row, col))    


        def agregar_fila(Event=None):

            def corte(label_dt, anchoColumna, texto ):
                fuente = Font(font=label_dt.cget("font"))
                saltos = 0
                palabras = str(texto).split()
                renglon = ''
                textoFinal=""
                copia=palabras.copy()

                for p in palabras:

                    longitudPalabra = fuente.measure(p)
                    copia.pop(0)

                    if (renglon == ''):
                        
                        if ( (longitudPalabra == anchoColumna) and (len(copia) > 0)):
                            
                            saltos += 1
                            textoFinal += p + '\n'

                        elif (longitudPalabra > anchoColumna):
                            cadena = ''
                            for i in range(len(p)):
                                if (fuente.measure((cadena + p[i])) <= anchoColumna):
                                    cadena += p[i]
                                    if (i==len(p)-1):
                                        textoFinal += cadena
                                        renglon += ' '

                                else:
                                    saltos += 1
                                    renglon = p[i:]
                                    textoFinal += cadena + "\n"
                                    cadena = p[i]

                            if (len(copia) > 0):
                                if (fuente.measure(renglon + ' ') >= anchoColumna):
                                    textoFinal += '\n'
                                    renglon = ''
                                    saltos+=1
                                else:
                                    textoFinal += ' '
                                    renglon += ' '

    
                        elif ( (longitudPalabra < anchoColumna) and (len(copia) > 0)):
                            renglon = p + ' '
                            
                            if (fuente.measure(renglon) >= anchoColumna):
                                textoFinal += p + '\n'
                                saltos += 1
                                renglon = ''
                            else:
                                textoFinal += p + ' '

                        elif (len(copia) == 0):
                            textoFinal += p
                        

                    else: 
                       
                        if   ((fuente.measure(renglon + p) == anchoColumna) and (len(copia) > 0)):
                            
                            saltos += 1
                            renglon = ''
                            textoFinal+="\n"

                        elif ( (fuente.measure(renglon + p) < anchoColumna) and (len(copia) > 0)):
                            renglon = renglon + p + ' '
                            if (fuente.measure(renglon) >= anchoColumna):
                                textoFinal += p + '\n'
                                saltos += 1
                                renglon = ''
                            else:
                                textoFinal += p + ' '
                                
                        elif ( (fuente.measure(renglon + p) < anchoColumna) and len(copia) == 0): 
                            textoFinal += p 
                             

                        elif (fuente.measure(renglon + p) > anchoColumna) :
                            saltos += 1
                            textoFinal += '\n'

                            if ( (longitudPalabra == anchoColumna) and (len(copia) > 0)):
                                saltos += 1
                                renglon = ''
                                textoFinal += '\n' + p  

                            elif (longitudPalabra > anchoColumna):
                                
                                cadena = ''
                                for i in range(len(p)):
                                    if (fuente.measure((cadena +  p[i])) <= anchoColumna):
                                        cadena += p[i]
                                        if (i==len(p)-1):
                                            textoFinal += cadena
                                            renglon += ' '
                                    else:
                                        saltos += 1
                                        renglon = p[i:]
                                        textoFinal += cadena + "\n"
                                        cadena = p[i]
                                        
                                if (len(copia) > 0):
                                    if (fuente.measure(renglon + ' ') >= anchoColumna):
                                        textoFinal += '\n'
                                        renglon = ''
                                        saltos+=1
                                    else:
                                        textoFinal += ' '
                                        renglon += ' '


                            elif ( (longitudPalabra < anchoColumna) and (len(copia) > 0)):
                                renglon = p + ' '
                                if (fuente.measure(renglon) >= anchoColumna):
                                    textoFinal += p + '\n'
                                    saltos += 1
                                    renglon=''
                                else:
                                    textoFinal += p + ' '

                            elif (len(copia) == 0):
                                if (fuente.measure(renglon + p) > anchoColumna):
                                    textoFinal += p
                                    renglon=''
                                elif (fuente.measure(renglon + p) <= anchoColumna):
                                    textoFinal += p
                                 
                return textoFinal, saltos

            def ajuste(saltos, saltoMay, colMayorCantSalt, columna, texto ):
                if (colMayorCantSalt == columna) :
                    return texto
                else:
                    if (saltos > 0):
                        return texto + (saltoMay - saltos)*'\n'
                    else:
                        return texto + (saltoMay)*'\n'      


            try:
                
                if (entry2.get("1.0", "end-1c") =="" or entry3.get()=="" or entry5.get()==""):
                    raise ValueError("Por favor completa todos los campos relacionados con el producto.")
                else:
                    try:
                        lista = []
                        serial=entry1.get()
                        lista.append(serial)
                        um=combo1.get()
                        lista.append(um)
                        desc= entry2.get("1.0", "end-1c")
                        desc = desc.replace("\n", " ")
                        lista.append(desc)
                        precio=entry5.get()
                        precio=int(precio)
                        lista.append(str(precio))
                        cantidad=entry3.get()
                        cantidad=int(cantidad)
                        lista.append(str(cantidad))
                        Ventana.listaProductos.append(lista)
                        fila_labels=[]

                        
                        label_st1=tk.Label(self.frame,  borderwidth=1, relief="solid", width=15)
                        label_st1.config(font=("Helvetica", 9))
                        salto_mayor = 0
                        columna_mayor = -1

                        serial, salto1 = corte(label_st1, 103, serial)
                        if (salto1 > salto_mayor):
                            salto_mayor = salto1
                            columna_mayor = 1

                        desc, salto3 = corte(label_st1, 208, desc)
                        if (salto3 > salto_mayor):
                            salto_mayor = salto3
                            columna_mayor = 3

                        precio, salto4 = corte(label_st1, 117, precio)
                        if (salto4 > salto_mayor):
                            salto_mayor = salto4
                            columna_mayor = 4

                        cantidad, salto5 = corte(label_st1, 54, cantidad)
                        if (salto5 > salto_mayor):
                            salto_mayor = salto5
                            columna_mayor = 5

                        entry1.delete(0, tk.END)
                        entry2.delete("1.0", "end")
                        entry3.delete(0, tk.END)
                        entry5.delete(0, tk.END)

                        serial = ajuste(salto1, salto_mayor, columna_mayor, 1, serial) 
                        um = ajuste(0, salto_mayor, columna_mayor, 2, um) 
                        desc = ajuste(salto3, salto_mayor, columna_mayor, 3, desc) 
                        precio = ajuste(salto4, salto_mayor, columna_mayor, 4, precio) 
                        cantidad = ajuste(salto5, salto_mayor, columna_mayor, 5, cantidad) 

                        label_st = tk.Label(self.frame, text=serial, bg="gray95", borderwidth=1, relief="solid", width=15)
                        label_umt = tk.Label(self.frame, text=um, bg="gray95", borderwidth=1, relief="solid", width=12)
                        label_dt = tk.Label(self.frame, text=desc, bg="gray95", borderwidth=1, relief="solid", width=30)
                        label_pt = tk.Label(self.frame, text=precio, bg="gray95", borderwidth=1, relief="solid", width=17)
                        label_ct = tk.Label(self.frame, text=cantidad, bg="gray95", borderwidth=1, relief="solid", width=8)

                        label_st.config(font=("Helvetica", 9))
                        label_umt.config(font=("Helvetica", 9))
                        label_dt.config(font=("Helvetica", 9))
                        label_pt.config(font=("Helvetica", 9))
                        label_ct.config(font=("Helvetica", 9))

                        fila_labels = [label_st, label_umt, label_dt, label_pt, label_ct]
                        Ventana.lista_labels.append(fila_labels)

                        for j in range(len(Ventana.lista_labels)):
                            for col, label in enumerate(fila_labels):
                                label.grid(row=Ventana.cont, column=col+1, padx=3, pady=2)
                                label.bind("<Button-1>", lambda event, row=j, col=col: seleccionar(event, row, col))

                        label_st.grid(row=Ventana.cont, column=1, padx=3, pady=2)
                        label_umt.grid(row=Ventana.cont, column=2, padx=3, pady=3)
                        label_dt.grid(row=Ventana.cont, column=3, padx=3, pady=2)                      
                        label_pt.grid(row=Ventana.cont, column=4, padx=3, pady=3)                       
                        label_ct.grid(row=Ventana.cont, column=5, padx=3, pady=3)
                        Ventana.cont += 1

                        self.frame.update_idletasks()
                        self.canvas.config(scrollregion=self.canvas.bbox("all"))
                                                    
                    except ValueError as i:
                       messagebox.showerror("Error", "Ingresa valores correctos por favor.") 
                
            except ValueError as e:
                messagebox.showerror("Error", str(e))
        
        def generar_factura():

            from serializador import Serializador

            try:

                if(len(Ventana.lista_labels) == 0):
                    raise Exception('No has agregado ningún producto. Por favor agrega al menos uno para generar la factura.')
                else:

                    try:

                        if ( entry6.get() == '' or entry7.get() == '' or  entry8.get() == '' or  entry12.get() == '' ):
                            raise ValueError('Por favor completa todos los campos relacionados con el cliente.')
                        
                        try:

                            int(entry8.get())

                            exCred = False
                            if (combo.get() == 'Crédito'):
                                if (entry10.get() == ''):
                                    exCred = True
                                    raise Exception('Por favor ingresa la cantidad de días de crédito.')
                                else:
                                    int(entry10.get())
                                    dias = entry10.get()
                            else:
                                dias = 'No aplica'

                            nit = 'No aplica'
                            if (entry9.get() != ''):
                                nit = entry9.get() 
                            
                            fechaFatura = datetime.datetime.now()
                            Ventana.numeroFactura += 1

                            facturaActual = Factura(fechaFatura, Ventana.getNumeroFactura(), entry6.get(), entry7.get(), entry8.get(), nit, entry12.get(), combo.get(), dias)

                            try:

                                excBorrar = False
                                for p in Ventana.listaProductos:
                                    if (len(p) != 5):
                                        excBorrar = True
                                        raise Exception('Ha ocurrido un error. Intenta de nuevo. Verifica que si borraste una fila, hayas borrado todas las celdas correspondientes a dicha fila.')

                                for p in range(len(Ventana.listaProductos)):
                                    Ventana.listaProductos[p].append(str(Decimal(Ventana.listaProductos[p][-2])*Decimal(Ventana.listaProductos[p][-1])))
                                    facturaActual.añadirProductos(Ventana.listaProductos[p])

                                facturaActual.generarPDF()

                                Serializador.serializar()

                                for p  in range(len(Ventana.listaProductos)):
                                    Ventana.listaProductos[p].pop(-1)

                            except Exception as ex:

                                if excBorrar :
                                    messagebox.showerror('Error', str(ex))
                                    Ventana.setNumeroFactura(Ventana.getNumeroFactura()-1)
                                

                                else:
                                    messagebox.showerror('Error', 'Ha ocurrido un error.Intenta de nuevo.')

                                    Ventana.setNumeroFactura(Ventana.getNumeroFactura()-1)
                           

                                    for p  in range(len(Ventana.listaProductos)):
                                        Ventana.listaProductos[p].pop(-1)

                        except ValueError as e:
                            messagebox.showerror('Error', 'Ingresa por favor valores numéricos para el campo de teléfono y días de crédito (si el caso aplica).')

                        except Exception as ex:
                            messagebox.showerror('Error', str(ex))
                            
                    except ValueError as e:
                        messagebox.showerror("Error", str(e))

            except Exception as e:
                messagebox.showerror('Error', str(e))

            
        def limpiarTabla():
            for fila in Ventana.lista_labels:
                for lab in fila:    
                    lab.destroy()

            Ventana.listaProductos=[]
            Ventana.lista_labels=[]    

        def cerrar_ventana():

            respuesta = messagebox.askyesno("Confirmar", "¿Estás seguro de que quieres salir?")
            if respuesta:
                
                ventana.destroy() 

        def pago(event):
            if (combo.get()!="Contado"):
                label11.grid(row=5,column=2,padx=20,pady=10,sticky="w")
                entry10.grid(row=5,column=3,padx=0,pady=10)
            else:
                label11.grid_forget()
                entry10.grid_forget()

        def on_configure(event):
            self.canvas_vertical.config(scrollregion=self.canvas_vertical.bbox('all'))



        ventana = tk.Tk()
        ventana.title("Ventana Inicio")
        ventana.state('zoomed')
        ventana.minsize(600, 600)
        ventana.resizable(True, True)
        appId = 'Facturacion.version'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appId) 
        iconPath = resource_path('src/images/icono.ico')
        ventana.iconbitmap(iconPath)
        ventana.rowconfigure(0, weight=1)
        ventana.columnconfigure(0, weight=1)

        mainFrame = tk.Frame(ventana,bg="gray85", height=470,width=770,padx=10, pady=10)
        mainFrame.grid(row = 0, column=0, sticky="nsew",padx=10, pady=10)
        mainFrame.rowconfigure(1, weight=1)
        mainFrame.columnconfigure(1, weight=1)

        self.canvas_vertical = tk.Canvas(mainFrame, bg="gray85", highlightthickness = 0)
        self.canvas_vertical.grid(row = 0, column = 0, sticky = 'nse')

        frameInformacion = tk.Frame(mainFrame, bg="Lavender", height=270, width=670) 
        frameInformacion.grid(row=0, column=0, sticky="nsew",padx=5, pady=20)
        frameInformacion.rowconfigure(2, weight=1)
        frameInformacion.columnconfigure(1, weight=1)

        title_label = tk.Label(frameInformacion, text="Facturación", font=("Helvetica", 20, "bold"), bg="Lavender" )
        title_label.grid(row=1, column=1, padx=10, pady=20)

        frameInterior = tk.Frame(frameInformacion, bg="gray95", height=500, width=800)
        frameInterior.grid(row=2, column=1, padx=40, pady=30, sticky="nsew")

        label1 = tk.Label(frameInterior,text="Serial")
        entry1 = tk.Entry(frameInterior)
        label2 = tk.Label(frameInterior,text="Descripción *")
        entry2 = tk.Text(frameInterior, height=4, width=20)
        label3 = tk.Label(frameInterior,text="Cantidad *")
        entry3 = tk.Entry(frameInterior)
        label4 = tk.Label(frameInterior,text="U/M")
        label5 = tk.Label(frameInterior,text="Precio *")
        entry5 = tk.Entry(frameInterior)
        label6 = tk.Label(frameInterior,text="Cliente *")
        entry6 = tk.Entry(frameInterior)
        label7 = tk.Label(frameInterior,text="Dirección *")
        entry7 = tk.Entry(frameInterior)
        label8 = tk.Label(frameInterior,text="Teléfono *")
        entry8 = tk.Entry(frameInterior)
        label9 = tk.Label(frameInterior,text="NIT")
        entry9 = tk.Entry(frameInterior)
        label12 = tk.Label(frameInterior,text="Asesor *")
        entry12 = tk.Entry(frameInterior)

        v_defecto1 = tk.StringVar(value="Ítem")
        combo1 = ttk.Combobox(frameInterior,values=["Gal","Pimp.", "Lt", "1/2 Lt","Mt","Kg","Man.Ob","Maq.","Accs", "Accs.Esp","Varios","Ítem"], textvariable=v_defecto1,  state="readonly")
        v_defecto = tk.StringVar(value="Contado")
        combo = ttk.Combobox(frameInterior,values=["Contado","Crédito"],textvariable=v_defecto,  state="readonly")
        combo.bind("<<ComboboxSelected>>",pago)
        label10 = tk.Label(frameInterior,text="Forma de pago")
        label11 = tk.Label(frameInterior,text="Días de crédito")
        entry10 = tk.Entry(frameInterior)

        self.canvas = tk.Canvas(frameInterior, bg="gray85",width=623)
        self.canvas.grid(row=0, column=4, rowspan=8, padx=40,pady=70,sticky="w")

        scrollbar = ttk.Scrollbar(frameInterior, orient="vertical",command=self.canvas.yview) 
        self.canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=4, rowspan=7 ,  pady=(40, 0), sticky="e", padx=15, ipady=90)

        scrollbar_vertical = ttk.Scrollbar(mainFrame, orient="vertical",command=self.canvas_vertical.yview) 
        scrollbar_horizontal = ttk.Scrollbar(mainFrame, orient="horizontal",command=self.canvas_vertical.xview) 
        self.canvas_vertical.configure(yscrollcommand=scrollbar_vertical.set, xscrollcommand=scrollbar_horizontal.set)
        scrollbar_vertical.grid(row=0, column=2, sticky = 'nse', rowspan = 2)
        scrollbar_horizontal.grid(row=1, column=0, sticky = 'sew', columnspan = 2)
        self.canvas_vertical.create_window((0, 0), window=frameInformacion,  anchor = 'nw')
        self.canvas_vertical.bind("<Configure>", on_configure)

        self.frame = tk.Frame(self.canvas, bg="gray85")
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
     
        self.frame_tt = tk.Frame(frameInterior, bg="gray95", height=30, width=623)
        self.frame_tt.grid(row=0, column=4, padx=40,pady=30,sticky="w")

        
        self.label_s=tk.Label(self.frame_tt, bg="Lavender", text="Serial", borderwidth=1, relief="solid", width=15)
        self.label_s.grid(row=1, column=1, padx=3, pady=2)
        self.label_um=tk.Label(self.frame_tt, bg="Lavender", text="U/M", borderwidth=1, relief="solid", width=12)
        self.label_um.grid(row=1, column=2, padx=3, pady=3)
        self.label_d=tk.Label(self.frame_tt, bg="Lavender", text="Descripción", borderwidth=1, relief="solid", width=30)
        self.label_d.grid(row=1, column=3, padx=3, pady=2)
        self.label_p=tk.Label(self.frame_tt, bg="Lavender", text="Precio", borderwidth=1, relief="solid", width=17)
        self.label_p.grid(row=1, column=4, padx=3, pady=3)
        self.label_p=tk.Label(self.frame_tt, bg="Lavender", text="Cantidad", borderwidth=1, relief="solid", width=8)
        self.label_p.grid(row=1, column=5, padx=3, pady=3)
        
        boton1=tk.Button(frameInterior,text="Agregar producto", command=agregar_fila)
        boton2=tk.Button(frameInterior,text="Borrar fila(s)", command=borrar_filas)
        boton3=tk.Button(frameInterior,text="Generar Factura", command=generar_factura)
        boton4=tk.Button(frameInterior,text="Limpiar tabla", command=limpiarTabla)

        entry1.config(font=("Helvetica", 9))
        entry2.config(font=("Helvetica", 9))
        entry3.config(font=("Helvetica", 9))
        entry5.config(font=("Helvetica", 9))
        entry6.config(font=("Helvetica", 9))
        entry7.config(font=("Helvetica", 9))
        entry8.config(font=("Helvetica", 9))
        entry9.config(font=("Helvetica", 9))
        entry10.config(font=("Helvetica", 9))
        entry12.config(font=("Helvetica", 9))
        combo.config(font=("Helvetica", 9))
        combo1.config(font=("Helvetica", 9))
       

        label1.grid(row=0,column=0,padx=20,pady=40,sticky="w")
        entry1.grid(row=0,column=1,padx=0,pady=10)
        label2.grid(row=0,column=2,padx=20,pady=10,sticky="w")
        entry2.grid(row=0,column=3,padx=0,pady=10)
        label3.grid(row=1,column=0,padx=20,pady=10,sticky="w")
        entry3.grid(row=1,column=1,padx=0,pady=10)
        label4.grid(row=1,column=2,padx=20,pady=10,sticky="w")
        label5.grid(row=2,column=0,padx=20,pady=10,sticky="w")
        entry5.grid(row=2,column=1,padx=0,pady=10)
        label6.grid(row=2,column=2,padx=20,pady=10,sticky="w")
        entry6.grid(row=2,column=3,padx=0,pady=10)
        label7.grid(row=3,column=0,padx=20,pady=10,sticky="w")
        entry7.grid(row=3,column=1,padx=0,pady=10)
        label8.grid(row=3,column=2,padx=20,pady=10,sticky="w")
        entry8.grid(row=3,column=3,padx=0,pady=10)
        label9.grid(row=4,column=0,padx=20,pady=10,sticky="w")
        entry9.grid(row=4,column=1,padx=0,pady=10)
        label10.grid(row=4,column=2,padx=20,pady=10,sticky="w")
        label12.grid(row=5,column=0,padx=20,pady=10,sticky="w")
        entry12.grid(row=5,column=1,padx=0,pady=10)
        combo.grid(row=4,column=3,padx=0,pady=10)
        combo1.grid(row=1,column=3,padx=0,pady=10)

        boton1.grid(row=7,column=1,pady=10,sticky="se")
        boton2.grid(row=7,column=2,padx=30,pady=10,sticky="sw")
        boton3.grid(row=8, column=1, columnspan=2, padx=10, pady=20, sticky="s")
        boton4.grid(row=7, column=3, padx=30,pady=10,sticky="sw")

        ventana.bind("<Return>", agregar_fila)
        ventana.protocol("WM_DELETE_WINDOW", cerrar_ventana)
        ventana.mainloop()