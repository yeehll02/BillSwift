import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
path = resource_path("src/Lib")
sys.path.append(path)

import copy
from tkinter import filedialog
from fpdf import FPDF
from datetime import datetime, timedelta
from math import ceil
from decimal import Decimal

class Factura:

    def __init__(self, fecha, numeroFactura, cliente, direccion, telefono, nit, asesor, formaPago, credito):

        self.fecha = fecha
        self.productos = []
        self.numeroFactura = numeroFactura
        self.cliente = cliente
        self.direccion = direccion
        self.telefono = telefono
        self.nit = nit
        self.asesor = asesor
        self.formaPago = formaPago
        self.credito = credito

    def añadirProductos(self, producto):

        self.productos.append(producto)

    def calcularTotal(self):

        total = 0

        for i in range(0, len(self.productos)):
            total += Decimal(self.productos[i][-1])

        return total
    
    def ajustar(self, ejeX, ejeY, w, numeroDato, valorAjuste, datoAjuste, datosAjusteMenor, documento, texto):

        documento.set_xy(ejeX, ejeY)

        if (numeroDato in datoAjuste):
            documento.multi_cell(w = w, h = 5, txt = texto, border = 1, align = 'C', fill = 1)
        elif (numeroDato in datosAjusteMenor):
            ajusteColumna = self.calcularRenglones(texto, w - 2, documento)
            h1 = (5*valorAjuste)/ajusteColumna
            documento.multi_cell(w = w, h = h1, txt = texto, border = 1, align = 'C', fill = 1)
        else:
            documento.multi_cell(w = w, h = 5*valorAjuste, txt = texto, border = 1, align = 'C', fill = 1)
            

    def encabezadoPágina(self, documento, diasCredito, diasValidez):

        #Agregar logo 
        documento.image(resource_path('src/images/logo.jpg'), x = 7, y = 15, w = 65, h = 55 )

        #Encabezado - Info empresa
        documento.set_font('Arial', 'B', 9)
        documento.text(x= 75, y= 11, txt='EMPRESA -----')

        documento.set_font('Arial', '', 7)
        documento.text(x= 75, y= 15, txt='SECTOR --------')
        documento.text(x= 75, y= 19, txt='Dirección --------')
        documento.text(x= 75, y= 23, txt='Tel -------- Cel -------')
        # documento.text(x= 75, y= 27, txt='Nit: 1036964096-5')
        documento.text(x= 120, y= 27, txt=f'Página {documento.page_no()}')

        #Encabezado - Figuras
        documento.line(70, 31, 140, 31)

        documento.set_xy(145, 8)
        documento.cell(w = 57, h = 23, txt = '', border = 1, ln=1, align = 'R', fill = 0)

        documento.set_xy(145, 8)
        documento.set_fill_color(170, 172, 173)
        documento.cell(w = 57, h = 5, txt = '', border = 1, ln=1, align = 'R', fill = 1)
            
        documento.set_font('Arial', 'B', 9)
        documento.text(x = 165, y = 12, txt = 'VEN - VENTA')

        #Encabezado - datos factura
        documento.set_font('Arial', '', 8)
        documento.text(x= 147, y= 17, txt='Número: ')
        documento.text(x= 147, y= 21, txt='Fecha: ')
        documento.text(x= 147, y= 25, txt='Vencimiento: ')
        documento.text(x= 147, y= 29, txt='Días de validez: ')

        documento.set_font('Arial', 'B', 8)
        documento.text(x= 168, y= 17, txt=f'{self.numeroFactura}')
        documento.text(x= 168, y= 21, txt=self.fecha.strftime("%d - %m - %Y"))
        if (diasCredito == 0): diasCredito = 1
        fechaVencimiento = self.fecha + timedelta(days=diasCredito)
        documento.text(x= 168, y= 25, txt=fechaVencimiento.strftime("%d - %m - %Y"))
        documento.text(x= 168, y= 29, txt=str(diasValidez))

        # Info del cliente
        documento.set_xy(70, 40)
        documento.cell(w = 80, h = 40, txt = '', border = 1, ln=1, align = 'L', fill = 0)

        documento.set_font('Arial', '', 9)
        documento.text(x= 72, y= 50, txt='Señores:')
        documento.text(x= 72, y= 56, txt='Dirección:')
        documento.text(x= 72, y= 62, txt='Teléfono:')
        documento.text(x= 72, y= 68, txt='NIT:')
        documento.text(x= 72, y= 74, txt='Asesor:')

        documento.set_font('Arial', 'B', 9)
        documento.text(x= 87, y= 50, txt=self.cliente)
        documento.text(x= 87, y= 56, txt=self.direccion)
        documento.text(x= 87, y= 62, txt=self.telefono)
        documento.text(x= 87, y= 68, txt=self.nit)
        documento.text(x= 87, y= 74, txt=self.asesor)

        # Forma de pago
        documento.set_xy(152, 40)
        documento.cell(w = 50, h = 40, txt = '', border = 1, ln=1, align = 'R', fill = 0)

        documento.line(177, 40, 177, 80)

        documento.set_font('Arial', '', 9)
        documento.text(x= 153, y= 68, txt='Forma de pago:')
        documento.text(x= 180, y= 68, txt=self.formaPago)

        #Credito
        documento.text(x= 153, y= 74, txt='Días de crédito:')
        documento.text(x= 180, y= 74, txt=self.credito)

    def encabezadoTabla(self, documento, y):

        # Encabezado 
        documento.set_font('Arial', 'B', 9)
        documento.set_fill_color(42, 127, 169)
        documento.set_text_color(255, 255, 255)

        documento.set_xy(15, y)
        documento.cell(w = 20, h = 5, txt = 'Serial', border = 1, ln=1, align = 'C', fill = 1)

        documento.set_xy(35, y)
        documento.cell(w = 20, h = 5, txt = 'U/M', border = 1, ln=1, align = 'C', fill = 1)

        documento.set_xy(55, y)
        documento.cell(w = 80, h = 5, txt = 'Descripción', border = 1, ln=1, align = 'C', fill = 1)

        documento.set_xy(135, y)
        documento.cell(w = 20, h = 5, txt = 'Valor UND', border = 1, ln=1, align = 'C', fill = 1)

        documento.set_xy(155, y)
        documento.cell(w = 20, h = 5, txt = 'Cantidad', border = 1, ln=1, align = 'C', fill = 1)

        documento.set_xy(175, y)
        documento.cell(w = 27, h = 5, txt = 'Valor total', border = 1, ln=1, align = 'C', fill = 1)
        
    def calcularRenglones(self, texto, anchoColumna, documento):

        saltos = 0
        palabras = texto.split()
        renglon = ''
        copia = copy.deepcopy(palabras)
        
        for p in palabras:
            longitudPalabra = documento.get_string_width(p)
            copia.pop(0)

            if (renglon == ''):
            
                if ( (longitudPalabra == anchoColumna) and (len(copia) > 0)):
                    saltos += 1

                elif (longitudPalabra > anchoColumna):

                    cadena = ''
                    for i in range(len(p)):
                        if (documento.get_string_width((cadena +  p[i])) <= anchoColumna):
                            cadena += p[i]
                        else:
                            saltos += 1
                            renglon = p[i:]
                            cadena = p[i]
                    
                    if (len(copia) > 0):
                        
                        if (documento.get_string_width(renglon + ' ') >= anchoColumna):
                            # print('entro 5')
                            saltos += 1
                            renglon = ''
                        else:
                            
                            renglon += ' '

                elif ( (longitudPalabra < anchoColumna) and (len(copia) > 0)):
                    
                    renglon = p + ' '

            else: 
                
                if   ((documento.get_string_width(renglon + p) == anchoColumna) and (len(copia) > 0)):
                    
                    saltos += 1
                    renglon = ''

                elif ((documento.get_string_width(renglon + p) < anchoColumna) and (len(copia) > 0)):
                    
                    renglon = renglon + p + ' '

                elif (documento.get_string_width(renglon + p) > anchoColumna):
                    
                    
                    saltos += 1

                    if ( (longitudPalabra == anchoColumna) and (len(copia) > 0)):
                        
                        saltos += 1
                        renglon = ''

                    elif (longitudPalabra > anchoColumna):
                        
                        
                        cadena = ''
                        for i in range(len(p)):
                            if (documento.get_string_width((cadena +  p[i])) <= anchoColumna):
                                cadena += p[i]
                            else:
                                saltos += 1
                                renglon = p[i:]
                                cadena = p[i]
                        
                        if (len(copia) > 0):
                            
                            
                            if (documento.get_string_width(renglon + ' ') >= anchoColumna):
                                
                                saltos += 1
                                renglon = ''
                            else:
                                
                                renglon += ' '

                    elif ( (longitudPalabra < anchoColumna) and (len(copia) > 0)):
                       
                        renglon = p + ' '
        
        
        return saltos + 1
    
    def generarPDF(self):

        from ventana import Ventana

        file_path = filedialog.asksaveasfilename(defaultextension = ".pdf",
         filetypes = [("PDF files", "*.pdf")], initialfile = f"Factura{self.numeroFactura}.pdf" )


        if file_path:

            documento = FPDF(orientation = 'P', unit = 'mm', format = 'Letter')
            
            #Agregar hojaaaaa
            documento.add_page()

            #Encabezado con info de la empresa
            diasCredito = -1
            diasValidez = 1
            if (self.credito != 'No aplica'):
                diasCredito = int(self.credito)
                diasValidez = diasCredito
            else:
                diasCredito = 0

            # Encabezado 
            self.encabezadoPágina(documento, diasCredito, diasValidez)

            # Listado de productos
            self.encabezadoTabla(documento, 85)
        
            # Registro de productos
            documento.set_font('Arial', '', 9)
            documento.set_text_color(0, 0, 0)
            cambioColor = 1 #Cambiar color por cada fila
            ejeY = 90 #Para ir añadiendo las celdas

            for p in self.productos:

                # Ajuste
                ajuste = 1 # Mayor cantidad Renglones
                datoAjuste = [] #Columnas con la mayor cantidad de renglones (indices)
                datosAjusteMenor = [] #Columnas con un más un renglon pero con menos del ajuste (indices)

                r1 = self.calcularRenglones(p[0], 18, documento)
                if (r1 > 1):
                    datosAjusteMenor.append(0)
                    if (r1 > ajuste):
                        ajuste = r1
                        datoAjuste = [0]

                    elif (r1 == ajuste):
                        datoAjuste.append(0)

                r2 = self.calcularRenglones(p[1], 18, documento)
                if (r2 > 1):
                    datosAjusteMenor.append(1)
                    if (r2 > ajuste):
                        ajuste = r2
                        datoAjuste = [1]
                            
                    elif (r2 == ajuste):
                        datoAjuste.append(1)

                r3 = self.calcularRenglones(p[2], 78, documento)
                if (r3 > 1):
                    datosAjusteMenor.append(2)
                    if (r3 > ajuste):
                        ajuste = r3
                        datoAjuste = [2]
                        
                    elif (r3 == ajuste):
                        datoAjuste.append(2)

                t4 = '$ {:,.2f}'.format(Decimal(p[3])).replace(",", "@").replace(".", ",").replace("@", ".")
                r4 = self.calcularRenglones(t4, 18, documento)
                if (r4 > 1):
                    datosAjusteMenor.append(3)
                    if (r4 > ajuste):
                        ajuste = r4
                        datoAjuste = [3]
                        
                    elif (r4 == ajuste):
                        datoAjuste.append(3)

                r5 = self.calcularRenglones(p[4], 18, documento)
                if (r5 > 1):
                    datosAjusteMenor.append(4)
                    if (r5 > ajuste):
                        ajuste = r5
                        datoAjuste = [4]
                        
                    elif (r5 == ajuste):
                        datoAjuste.append(4)

                t6 = '$ {:,.2f}'.format(Decimal(p[5])).replace(",", "@").replace(".", ",").replace("@", ".")
                r6 = self.calcularRenglones(t6, 25, documento)
                if (r6 > 1):
                    datosAjusteMenor.append(5)
                    if (r6 > ajuste):
                        ajuste = r6
                        datoAjuste = [5]
                        
                    elif (r6 == ajuste):
                        datoAjuste.append(5)

                
                if (len(datoAjuste) > 0 ):
                    for e in datoAjuste:
                        datosAjusteMenor.remove(e)
                
                if ( cambioColor == 1 ):
                    documento.set_fill_color(203, 209, 241)
                    cambioColor = 0
                else:
                    documento.set_fill_color(227, 241, 247)
                    cambioColor = 1

                # Crear la fila

                # Verificar espacio antes de crear la fila 

                posicionActual = documento.get_y()
                alturaFila = 5*ajuste

                if ((posicionActual + alturaFila) >=  (documento.h - documento.b_margin - documento.t_margin)): # No hay espacio suficiente

                    documento.add_page()
                    self.encabezadoPágina(documento, diasCredito, diasValidez)
                    self.encabezadoTabla(documento, 90)

                    # Filas
                    ejeY = 95
                    documento.set_font('Arial', '', 9)
                    documento.set_text_color(0, 0, 0)
                    
                    # Intercalar color de filas 
                    if ( cambioColor == 1 ):
                        documento.set_fill_color(227, 241, 247)  
                    else:
                        documento.set_fill_color(203, 209, 241)


                    self.ajustar(15, ejeY, 20, 0, ajuste, datoAjuste, datosAjusteMenor, documento, p[0])
                    self.ajustar(35, ejeY, 20, 1, ajuste, datoAjuste, datosAjusteMenor, documento, p[1])
                    self.ajustar(55, ejeY, 80, 2, ajuste, datoAjuste, datosAjusteMenor, documento, p[2])
                    self.ajustar(135, ejeY, 20, 3, ajuste, datoAjuste, datosAjusteMenor, documento, t4)
                    self.ajustar(155, ejeY, 20, 4, ajuste, datoAjuste, datosAjusteMenor, documento, p[4])
                    self.ajustar(175, ejeY, 27, 5, ajuste, datoAjuste, datosAjusteMenor, documento, t6)

                else:
                    
                    self.ajustar(15, ejeY, 20, 0, ajuste, datoAjuste, datosAjusteMenor, documento, p[0])
                    self.ajustar(35, ejeY, 20, 1, ajuste, datoAjuste, datosAjusteMenor, documento, p[1])
                    self.ajustar(55, ejeY, 80, 2, ajuste, datoAjuste, datosAjusteMenor, documento, p[2])
                    self.ajustar(135, ejeY, 20, 3, ajuste, datoAjuste, datosAjusteMenor, documento, t4)
                    self.ajustar(155, ejeY, 20, 4, ajuste, datoAjuste, datosAjusteMenor, documento, p[4])
                    self.ajustar(175, ejeY, 27, 5, ajuste, datoAjuste, datosAjusteMenor, documento, t6)

                
                ejeY += (5*ajuste)

            #Pie página 
            Total  = self.calcularTotal()
            Total = '$ {:,.2f} COP'.format(Total).replace(",", "@").replace(".", ",").replace("@", ".")
           
            #Ajuste del valor total
            ajusteTotal = 1
            recuadro = []
            if (self.calcularRenglones(Total,40,documento) > 1): # Necesita ajuste
                ajusteTotal = self.calcularRenglones(Total,40,documento)
                recuadro = [1] 

            # Verificar espacio
            posicionActual = documento.get_y()
            espacioRequerido = max((ajusteTotal*5), 30) + 10 # 30: Caja de las transferencias, lo otro es el tamaño del valor total y 10 de espacio

            if ((posicionActual + espacioRequerido) >= (documento.h - documento.b_margin - documento.t_margin)): #No hay espacio
                
                documento.add_page()
                self.encabezadoPágina(documento, diasCredito, diasValidez)
                documento.set_xy(135, 90)
                documento.set_fill_color(164, 173, 178)
                documento.set_font('Arial', 'B', 9)

                #Recuadros

                # Valor del total
                self.ajustar(160, 90, 42, 1, ajusteTotal, recuadro, [], documento, Total)

                #Texto
                self.ajustar(135,90, 25, 0, ajusteTotal, recuadro, [], documento, 'Total a pagar:')

                # Transferencias 
                documento.set_xy(15, 90)
                documento.cell(w = 110, h = 30, txt = '', border = 1, ln=1, align = 'L', fill = 0)
                documento.text(x = 17, y = 90  + 12, txt = 'CONSIGNAR O HACER TRANSFERENCIAS SOLO EN LAS CUENTAS')
                documento.text(x = 17, y = 90  + 16, txt = 'ENTIDAD BANCARIA ')
                documento.text(x = 17, y = 90  + 20, txt = 'AHORROS No. -----')

            else:

                documento.set_xy(135, posicionActual + 10)
                documento.set_fill_color(164, 173, 178)
                documento.set_font('Arial', 'B', 9)

                #Recuadros
                # Valor del total
                self.ajustar(160, posicionActual + 10, 42, 1, ajusteTotal, recuadro, [], documento, Total)

                #Texto
                self.ajustar(135,posicionActual + 10, 25, 0, ajusteTotal, recuadro, [], documento, 'Total a pagar:')

                # Transferencias 
                documento.set_xy(15, posicionActual + 10)
                documento.cell(w = 110, h = 30, txt = '', border = 1,  align = 'L', fill = 0)
                documento.text(x = 17, y = posicionActual +  10 + 12, txt = 'CONSIGNAR O HACER TRANSFERENCIAS SOLO EN LAS CUENTAS')
                documento.text(x = 17, y = posicionActual +  10 + 16, txt = 'ENTIDAD BANCARIA ')
                documento.text(x = 17, y = posicionActual +  10 + 20, txt = 'AHORROS No. -----')

            #Guardar pdf
            documento.output(file_path)
            
            #Abrir automáticamente el pdf
            os.system(file_path)
        
        else:

            Ventana.setNumeroFactura(Ventana.getNumeroFactura() - 1)