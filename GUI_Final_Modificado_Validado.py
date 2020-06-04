# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI_Final.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!

import os
import time
import datetime
import MySQLdb
import RPi.GPIO as GPIO
#from datetime import datetime

global crsr
global db
global banderaPluma

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AdministracionLogIn(object):
    def RegistroDeAutos(self):
        self.stackedWidget.setCurrentIndex(4)
        self.statusbar.showMessage('Registro de autos')

    def HistorialDeIngresos(self):
        self.stackedWidget.setCurrentIndex(3)
        self.statusbar.showMessage('Historial de ingresos')

    def SalidaVehiculosEstacionamiento(self):
        self.stackedWidget.setCurrentIndex(0)
        self.statusbar.showMessage('Salida de autos')

    def AdministracionScreen(self):
        self.stackedWidget.setCurrentIndex(1)
        self.statusbar.showMessage('Administración Log-In')

    def AdministracionLoggedInScreen(self):
        self.stackedWidget.setCurrentIndex(2)
        self.statusbar.showMessage('Administración')

    def Salir(self):
        self.statusbar.showMessage('Saliendo...')
        AdministracionLogIn.close()
        
    def verificarUsuario(self):
        usuario = self.UsuarioInput.toPlainText()
        contraseña = self.ContrasenaInput.toPlainText()
        
        comandoSQL = "SELECT username, password, tipo FROM administradores WHERE username = %s AND password = %s"
        crsr.execute(comandoSQL, [usuario, contraseña])
        
        try:
            resultado = crsr.fetchall()[0][2]
            print (resultado)
        
            if resultado == 1:
                self.AdministracionLoggedInScreen()
                self.UsuarioInput.setText('')
                self.ContrasenaInput.setText('')
            elif resultado == 0:
                self.UsuarioInput.setText("Incorrecto")
                self.ContrasenaInput.setText("Incorrecto")
        except:
            self.UsuarioInput.setText("Incorrecto")
            self.ContrasenaInput.setText("Incorrecto")
            
            
    def sacarCoche(self, tipoVehiculo):
        global crsr
        #Preguntar or la placa
        matriculaSacar = self.MatriculaLeidaInput.toPlainText()
        
        #VErificar que sea un auto válido
        
        try:
            comandoSQL = "SELECT status FROM ticket WHERE matricula = %s"
            crsr.execute(comandoSQL, [matriculaSacar])
            resultado = crsr.fetchall()[0][0]
            if resultado==0:
                #El auto no es válido.
                self.TotalACobrarInput.setText("Error, el auto no se encuentra adentro")
            elif resultado==1:
                
                #Buscar la hora de entrada del auto
                comandoSQL = "SELECT entrada from ticket WHERE matricula = %s"
                crsr.execute(comandoSQL, [matriculaSacar])
                resultado = crsr.fetchall()
                horaEntrada = resultado[0][0]
                print(horaEntrada)
                #Calcular hora actual
                ##time_now = (datetime.datetime.fromtimestamp(time.time()).strftime("%H:%M:%S"))
                ##date_now = (datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d"))
                horaActual = datetime.datetime.now()
                self.CheckOutInput.setText((datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")))
                total = horaActual - horaEntrada
                horaTotal = total.days*24 + total.seconds//3600
                print(total)
                #print the data in the GUI
                
                self.CheckInInput.setText(str(horaEntrada))
                
                
                #obtener numero de horas:
                #revisar tolerancia
            
                if (total.seconds//60)%60 >= 1:
                    #agregar una hora
                    horaTotal += 1
                
                if tipoVehiculo ==1:
                    comandoSQL= "SELECT precio FROM costo WHERE id=1"
                    crsr.execute(comandoSQL)
                elif tipoVehiculo ==2:
                    comandoSQL= "SELECT precio FROM costo WHERE id=2"
                    crsr.execute(comandoSQL)
                elif tipoVehiculo ==3:
                    comandoSQL= "SELECT precio FROM costo WHERE id=3"
                    crsr.execute(comandoSQL)
                    
                    
                resultado= crsr.fetchall()
                precio= resultado[0][0]
                
                totalApagar= precio* horaTotal
                
                #print the total on the GUI
                
                self.TotalACobrarInput.setText(str(totalApagar))
                
                print("Total: " + str(horaTotal) + " horas.")
                print("Costo por hora: " + str(precio) + ", total a pagar: " + str(totalApagar))
            

                # UPDATE ticket SET costo = "Tipo de cochce", salida = "timestamp actual",
                # status = '0', pago = "variable pago" WHERE matricula = "variable mat",
                
                comandoSQL= "UPDATE ticket SET costo = %s, salida = %s , status=0 , pago= %s, costoActual = %s WHERE matricula= %s"
                crsr.execute(comandoSQL, [int(tipoVehiculo), str(horaActual), int(totalApagar), int(precio), str(matriculaSacar)])
                db.commit()
        except:
            self.statusbar.showMessage('Error: Verifique que la matrícula sea correcta.')

    def checarPlaca(self, placa):
        comandoSQL = "SELECT * FROM vehiculo WHERE matricula=%s"
        crsr.execute(comandoSQL, [str(placa)])
        if crsr.rowcount == 0:
            #No está registrada
            return False
        elif crsr.rowcount != 0:
            #ya está registrada
            return True

    def generarTicket(self, placa):
        time_now = (datetime.datetime.fromtimestamp(time.time()).strftime("%H:%M:%S"))
        date_now = (datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d"))
        date_time = str(date_now) + " " + str(time_now)
        comandoSQL = "INSERT INTO ticket(matricula, entrada, costo, status) VALUES (%s,%s, '3','1')"
        crsr.execute(comandoSQL, [str(placa), str(date_time)])
        db.commit()
        
        
    def ingresarPlaca(self):
        #Pedir la placa
        nuevaPlaca = self.MatriculaLeidaInput.toPlainText()
        #Buscar si ya existe la placa
        if self.checarPlaca(nuevaPlaca):
        #Ya existe la placa
            print("El auto ya se encuentra registrado, generando ticket")
            self.generarTicket(nuevaPlaca)
        else:
        #No existe la placa, se agrega
            comandoSQL = "INSERT INTO vehiculo(matricula) VALUES (%s)"
            print("Se ha registrado el auto, generando ticket")
            crsr.execute(comandoSQL, [str(nuevaPlaca)])
            db.commit()

        #Se genera el ticket
            self.generarTicket(nuevaPlaca)
            
            
    def SetAngle(self, angle):
        duty = angle / 18 + 2
        return duty

    def moverPluma(self):
        if self.TotalACobrarInput.toPlainText() == "":
            self.statusbar.showMessage('Error: Debes asignar primero un precio al vehículo.')
        else:
            global banderaPluma
            if banderaPluma == 0:
                ##Levantar pluma
                #GPIO setup
                servoPIN = 17
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(servoPIN, GPIO.OUT)
                p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz 
                p.start(0) # Initialization
                try:
                    GPIO.output(servoPIN, True)
                    p.ChangeDutyCycle(self.SetAngle(90))
                    time.sleep(1)
                    GPIO.output(servoPIN, False)
                    p.ChangeDutyCycle(0)
                except KeyboardInterrupt:
                    p.stop()
                p.stop()
                GPIO.cleanup()
                ##Cambiar bandera
                banderaPluma = 1
                ##Cambiar texto
                self.LevantarPlumaBoton.setText("Bajar Pluma")
            elif banderaPluma == 1:
                ##Bajar pluma
                #GPIO setup
                servoPIN = 17
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(servoPIN, GPIO.OUT)
                p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz 
                p.start(0) # Initialization
                try:
                    GPIO.output(servoPIN, True)
                    p.ChangeDutyCycle(self.SetAngle(0))
                    time.sleep(1)
                    GPIO.output(servoPIN, False)
                    p.ChangeDutyCycle(0)
                except KeyboardInterrupt:
                    p.stop()
                p.stop()
                GPIO.cleanup()
                self.MatriculaLeidaInput.setText("")
                self.CheckInInput.setText("")
                self.CheckOutInput.setText("")
                self.TotalACobrarInput.setText("")
                ##Cambiar bandera
                banderaPluma = 0
                ##Cambiar texto
                self.LevantarPlumaBoton.setText("Levantar Pluma")

    def estatusEstacionamiento(self): 
        #Obtener listal
        comandoSQL = "SELECT precio FROM costo WHERE ID=3"
        crsr.execute(comandoSQL)
        precioCoches = crsr.fetchall()
        iteracion = 0
        comandoSQL = "SELECT * FROM ticket WHERE status='1'"
        crsr.execute(comandoSQL)
        resultado = crsr.fetchall()
        if resultado is not None:
            for i in resultado:
                self.TablaAutos.setItem(iteracion, 0, QtWidgets.QTableWidgetItem(str(i[1])))
                self.TablaAutos.setItem(iteracion, 1, QtWidgets.QTableWidgetItem(str(i[2])))
                horaActual = datetime.datetime.now()
                tiempoTramscurrido= horaActual-i[2]
                self.TablaAutos.setItem(iteracion, 2, QtWidgets.QTableWidgetItem(str(tiempoTramscurrido)))
                #Calcular precio estimado.
                #pasar todo a horas.
                horasTotales = tiempoTramscurrido.days*24 + tiempoTramscurrido.seconds//3600
                #print("Dias: " + str(tiempoTramscurrido.days " Horas: " + tiempoTramscurrido.seconds//3600)
                #Calcular precio
                precioEstimado = horasTotales*precioCoches[0][0]
                print(precioEstimado)
                self.TablaAutos.setItem(iteracion, 3, QtWidgets.QTableWidgetItem("$" + str(precioEstimado)))
                header = self.TablaAutos.horizontalHeader()
                header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
                header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
                header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
                header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
                iteracion = iteracion + 1
                
        
                
    def verHistorial(self):
        #Obtener listal
        iteracion = 0
        comandoSQL = "SELECT * FROM ticket WHERE status='0'"
        crsr.execute(comandoSQL)
        resultado = crsr.fetchall()
        if resultado is not None:
            for i in resultado:
                self.TablaAutosIngresados.setItem(iteracion, 0, QtWidgets.QTableWidgetItem(str(i[1])))
                self.TablaAutosIngresados.setItem(iteracion, 1, QtWidgets.QTableWidgetItem(str(i[2])))
                self.TablaAutosIngresados.setItem(iteracion, 2, QtWidgets.QTableWidgetItem(str(i[3])))
                self.TablaAutosIngresados.setItem(iteracion, 3, QtWidgets.QTableWidgetItem(str(i[5])))
                header = self.TablaAutosIngresados.horizontalHeader()
                header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
                header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
                header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
                header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
                iteracion = iteracion + 1
            
        

    def cambiarPrecios(self, tipoCambiar):
        if self.MontoPrimerasHorasInput.toPlainText() == "":
            self.statusbar.showMessage('Error: Ingresa el nuevo monto.')
        else:
            
            if tipoCambiar==1:
                nuevoPrecio = self.MontoPrimerasHorasInput.toPlainText()
                if (nuevoPrecio.isdecimal()):
                    comandoSQL= "UPDATE costo SET precio = %s WHERE ID = 1"
                    crsr.execute(comandoSQL, [int(nuevoPrecio)])
                    db.commit()
                    self.statusbar.showMessage('Precio cambiado.')
                    self.MontoPrimerasHorasInput.setText('')
                else:
                    self.statusbar.showMessage('Error: Monto no valido, ingresa un monto numérico.')
            elif tipoCambiar==2:
                nuevoPrecio = self.MontoPrimerasHorasInput.toPlainText()
                if (nuevoPrecio.isdecimal()):
                    comandoSQL= "UPDATE costo SET precio = %s WHERE ID = 2"
                    crsr.execute(comandoSQL, [int(nuevoPrecio)])
                    db.commit()
                    self.statusbar.showMessage('Precio cambiado.')
                    self.MontoPrimerasHorasInput.setText('')
                else:
                    self.statusbar.showMessage('Error: Monto no valido, ingresa un monto numérico.')
            elif tipoCambiar==3:
                nuevoPrecio = self.MontoPrimerasHorasInput.toPlainText()
                if (nuevoPrecio.isdecimal()):
                    comandoSQL= "UPDATE costo SET precio = %s WHERE ID = 3"
                    crsr.execute(comandoSQL, [int(nuevoPrecio)])
                    db.commit()
                    self.statusbar.showMessage('Precio cambiado.')
                    self.MontoPrimerasHorasInput.setText('')
                else:
                    self.statusbar.showMessage('Error: Monto no valido, ingresa un monto numérico.')
        
    def setupUi(self, AdministracionLogIn):
        AdministracionLogIn.setObjectName("AdministracionLogIn")
        AdministracionLogIn.resize(480, 320)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Logos/ParkingLotLogo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        AdministracionLogIn.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(AdministracionLogIn)
        self.centralwidget.setObjectName("centralwidget")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 0, 481, 261))
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.CarroBoton = QtWidgets.QPushButton(self.page)
        self.CarroBoton.setGeometry(QtCore.QRect(55, 40, 50, 50))
        self.CarroBoton.setStyleSheet("")
        self.CarroBoton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/Logos/Car.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.CarroBoton.setIcon(icon1)
        self.CarroBoton.setIconSize(QtCore.QSize(46, 50))
        self.CarroBoton.setObjectName("CarroBoton")
        self.CamionBoton = QtWidgets.QPushButton(self.page)
        self.CamionBoton.setGeometry(QtCore.QRect(55, 100, 50, 50))
        self.CamionBoton.setStyleSheet("")
        self.CamionBoton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/Logos/Truck.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.CamionBoton.setIcon(icon2)
        self.CamionBoton.setIconSize(QtCore.QSize(46, 50))
        self.CamionBoton.setObjectName("CamionBoton")
        self.CamionetaBoton = QtWidgets.QPushButton(self.page)
        self.CamionetaBoton.setGeometry(QtCore.QRect(55, 160, 50, 50))
        self.CamionetaBoton.setStyleSheet("")
        self.CamionetaBoton.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/Logos/Van.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.CamionetaBoton.setIcon(icon3)
        self.CamionetaBoton.setIconSize(QtCore.QSize(46, 50))
        self.CamionetaBoton.setObjectName("CamionetaBoton")
        self.EntradaManualBoton = QtWidgets.QPushButton(self.page)
        self.EntradaManualBoton.setGeometry(QtCore.QRect(185, 210, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.EntradaManualBoton.setFont(font)
        self.EntradaManualBoton.setDefault(False)
        self.EntradaManualBoton.setObjectName("EntradaManualBoton")
        self.LevantarPlumaBoton = QtWidgets.QPushButton(self.page)
        self.LevantarPlumaBoton.setGeometry(QtCore.QRect(340, 210, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.LevantarPlumaBoton.setFont(font)
        self.LevantarPlumaBoton.setDefault(False)
        self.LevantarPlumaBoton.setObjectName("LevantarPlumaBoton")
        self.SalidaVehiculo = QtWidgets.QLabel(self.page)
        self.SalidaVehiculo.setGeometry(QtCore.QRect(148, 10, 351, 31))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.SalidaVehiculo.setFont(font)
        self.SalidaVehiculo.setObjectName("SalidaVehiculo")
        self.MatriculaLeida = QtWidgets.QLabel(self.page)
        self.MatriculaLeida.setGeometry(QtCore.QRect(160, 45, 141, 31))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.MatriculaLeida.setFont(font)
        self.MatriculaLeida.setObjectName("MatriculaLeida")
        self.MatriculaLeidaInput = QtWidgets.QTextEdit(self.page)
        self.MatriculaLeidaInput.setGeometry(QtCore.QRect(280, 50, 171, 23))
        self.MatriculaLeidaInput.setObjectName("MatriculaLeidaInput")
        self.CheckIn = QtWidgets.QLabel(self.page)
        self.CheckIn.setGeometry(QtCore.QRect(160, 85, 111, 31))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.CheckIn.setFont(font)
        self.CheckIn.setObjectName("CheckIn")
        self.CheckOut = QtWidgets.QLabel(self.page)
        self.CheckOut.setGeometry(QtCore.QRect(160, 125, 121, 31))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.CheckOut.setFont(font)
        self.CheckOut.setObjectName("CheckOut")
        self.TotalCobrar = QtWidgets.QLabel(self.page)
        self.TotalCobrar.setGeometry(QtCore.QRect(160, 165, 141, 31))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.TotalCobrar.setFont(font)
        self.TotalCobrar.setObjectName("TotalCobrar")
        self.CheckInInput = QtWidgets.QTextEdit(self.page)
        self.CheckInInput.setGeometry(QtCore.QRect(280, 90, 171, 23))
        self.CheckInInput.setObjectName("CheckInInput")
        self.CheckOutInput = QtWidgets.QTextEdit(self.page)
        self.CheckOutInput.setGeometry(QtCore.QRect(280, 130, 171, 23))
        self.CheckOutInput.setObjectName("CheckOutInput")
        self.TotalACobrarInput = QtWidgets.QTextEdit(self.page)
        self.TotalACobrarInput.setGeometry(QtCore.QRect(280, 170, 171, 23))
        self.TotalACobrarInput.setObjectName("TotalACobrarInput")
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.Logo_2 = QtWidgets.QLabel(self.page_2)
        self.Logo_2.setGeometry(QtCore.QRect(20, 40, 151, 181))
        self.Logo_2.setStyleSheet("image: url(:/Logos/ParkingLotLogo.png);")
        self.Logo_2.setText("")
        self.Logo_2.setScaledContents(True)
        self.Logo_2.setObjectName("Logo_2")
        self.LogIn = QtWidgets.QLabel(self.page_2)
        self.LogIn.setGeometry(QtCore.QRect(305, 10, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.LogIn.setFont(font)
        self.LogIn.setObjectName("LogIn")
        self.UsuarioInput = QtWidgets.QTextEdit(self.page_2)
        self.UsuarioInput.setGeometry(QtCore.QRect(250, 90, 161, 23))
        self.UsuarioInput.setObjectName("UsuarioInput")
        self.Usuario = QtWidgets.QLabel(self.page_2)
        self.Usuario.setGeometry(QtCore.QRect(303, 60, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Usuario.setFont(font)
        self.Usuario.setObjectName("Usuario")
        self.Contrasea = QtWidgets.QLabel(self.page_2)
        self.Contrasea.setGeometry(QtCore.QRect(290, 130, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Contrasea.setFont(font)
        self.Contrasea.setObjectName("Contrasea")
        self.ContrasenaInput = QtWidgets.QTextEdit(self.page_2)
        self.ContrasenaInput.setGeometry(QtCore.QRect(250, 160, 161, 23))
        self.ContrasenaInput.setObjectName("ContrasenaInput")
        self.Entrar = QtWidgets.QPushButton(self.page_2)
        self.Entrar.setGeometry(QtCore.QRect(340, 210, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Entrar.setFont(font)
        self.Entrar.setObjectName("Entrar")
        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.Logo = QtWidgets.QLabel(self.page_3)
        self.Logo.setGeometry(QtCore.QRect(20, 40, 151, 181))
        self.Logo.setStyleSheet("image: url(:/Logos/ParkingLotLogo.png);")
        self.Logo.setText("")
        self.Logo.setPixmap(QtGui.QPixmap(":/newPrefix/Logos/ParkingLotLogo.png"))
        self.Logo.setScaledContents(True)
        self.Logo.setObjectName("Logo")
        self.Administracion = QtWidgets.QLabel(self.page_3)
        self.Administracion.setGeometry(QtCore.QRect(280, 10, 171, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Administracion.setFont(font)
        self.Administracion.setObjectName("Administracion")
        self.MontoPrimerasHoras = QtWidgets.QLabel(self.page_3)
        self.MontoPrimerasHoras.setGeometry(QtCore.QRect(241, 45, 221, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.MontoPrimerasHoras.setFont(font)
        self.MontoPrimerasHoras.setObjectName("MontoPrimerasHoras")
        self.MontoPrimerasHorasInput = QtWidgets.QTextEdit(self.page_3)
        self.MontoPrimerasHorasInput.setGeometry(QtCore.QRect(263, 85, 131, 23))
        self.MontoPrimerasHorasInput.setObjectName("MontoPrimerasHorasInput")
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.CamionBotonModificarMonto = QtWidgets.QPushButton(self.page_3)
        self.CamionBotonModificarMonto.setGeometry(QtCore.QRect(300, 150, 50, 50))
        self.CamionBotonModificarMonto.setStyleSheet("")
        self.CamionBotonModificarMonto.setText("")
        self.CamionBotonModificarMonto.setIcon(icon2)
        self.CamionBotonModificarMonto.setIconSize(QtCore.QSize(46, 50))
        self.CamionBotonModificarMonto.setObjectName("CamionBotonModificarMonto")
        self.CamionetaBotonModificarMonto = QtWidgets.QPushButton(self.page_3)
        self.CamionetaBotonModificarMonto.setGeometry(QtCore.QRect(390, 150, 50, 50))
        self.CamionetaBotonModificarMonto.setStyleSheet("")
        self.CamionetaBotonModificarMonto.setText("")
        self.CamionetaBotonModificarMonto.setIcon(icon3)
        self.CamionetaBotonModificarMonto.setIconSize(QtCore.QSize(46, 50))
        self.CamionetaBotonModificarMonto.setObjectName("CamionetaBotonModificarMonto")
        self.CarroBotonModificarMonto = QtWidgets.QPushButton(self.page_3)
        self.CarroBotonModificarMonto.setGeometry(QtCore.QRect(210, 150, 50, 50))
        self.CarroBotonModificarMonto.setStyleSheet("")
        self.CarroBotonModificarMonto.setText("")
        self.CarroBotonModificarMonto.setIcon(icon1)
        self.CarroBotonModificarMonto.setIconSize(QtCore.QSize(46, 50))
        self.CarroBotonModificarMonto.setObjectName("CarroBotonModificarMonto")
        self.MontoPrimerasHoras_2 = QtWidgets.QLabel(self.page_3)
        self.MontoPrimerasHoras_2.setGeometry(QtCore.QRect(200, 120, 321, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.MontoPrimerasHoras_2.setFont(font)
        self.MontoPrimerasHoras_2.setObjectName("MontoPrimerasHoras_2")
        self.stackedWidget.addWidget(self.page_3)
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setObjectName("page_4")
        self.HistorialIngresos = QtWidgets.QLabel(self.page_4)
        self.HistorialIngresos.setGeometry(QtCore.QRect(110, 10, 371, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.HistorialIngresos.setFont(font)
        self.HistorialIngresos.setObjectName("HistorialIngresos")
        self.TablaAutosIngresados = QtWidgets.QTableWidget(self.page_4)
        self.TablaAutosIngresados.setGeometry(QtCore.QRect(30, 60, 417, 175))
        self.TablaAutosIngresados.setObjectName("TablaAutosIngresados")
        self.TablaAutosIngresados.setColumnCount(4)
        self.TablaAutosIngresados.setRowCount(5)
        item = QtWidgets.QTableWidgetItem()
        self.TablaAutosIngresados.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.TablaAutosIngresados.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.TablaAutosIngresados.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.TablaAutosIngresados.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.TablaAutosIngresados.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.TablaAutosIngresados.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.TablaAutosIngresados.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.TablaAutosIngresados.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.TablaAutosIngresados.setHorizontalHeaderItem(3, item)
        self.stackedWidget.addWidget(self.page_4)
        self.page_5 = QtWidgets.QWidget()
        self.page_5.setObjectName("page_5")
        self.AutosDentro = QtWidgets.QLabel(self.page_5)
        self.AutosDentro.setGeometry(QtCore.QRect(130, 10, 351, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.AutosDentro.setFont(font)
        self.AutosDentro.setObjectName("AutosDentro")
        self.TablaAutos = QtWidgets.QTableWidget(self.page_5)
        self.TablaAutos.setGeometry(QtCore.QRect(30, 60, 417, 173))
        self.TablaAutos.setObjectName("TablaAutos")
        self.TablaAutos.setColumnCount(4)
        self.TablaAutos.setRowCount(5)
        item = QtWidgets.QTableWidgetItem()
        self.TablaAutos.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.TablaAutos.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.TablaAutos.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.TablaAutos.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.TablaAutos.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.TablaAutos.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.TablaAutos.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(7)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.TablaAutos.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(6)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.TablaAutos.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.TablaAutos.setItem(0, 0, item)
        self.stackedWidget.addWidget(self.page_5)
        AdministracionLogIn.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(AdministracionLogIn)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 480, 21))
        self.menubar.setObjectName("menubar")
        self.menuMen = QtWidgets.QMenu(self.menubar)
        self.menuMen.setObjectName("menuMen")
        self.menuAcerca_de = QtWidgets.QMenu(self.menubar)
        self.menuAcerca_de.setObjectName("menuAcerca_de")
        AdministracionLogIn.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(AdministracionLogIn)
        self.statusbar.setObjectName("statusbar")
        AdministracionLogIn.setStatusBar(self.statusbar)
        self.actionRegistro_de_autos = QtWidgets.QAction(AdministracionLogIn)
        self.actionRegistro_de_autos.setObjectName("actionRegistro_de_autos")
        self.actionHistorial_de_ingresos = QtWidgets.QAction(AdministracionLogIn)
        self.actionHistorial_de_ingresos.setObjectName("actionHistorial_de_ingresos")
        self.actionSalida_de_autos = QtWidgets.QAction(AdministracionLogIn)
        self.actionSalida_de_autos.setObjectName("actionSalida_de_autos")
        self.actionAdministraci_n = QtWidgets.QAction(AdministracionLogIn)
        self.actionAdministraci_n.setEnabled(True)
        self.actionAdministraci_n.setObjectName("actionAdministraci_n")
        self.actionSalir_Ctrl_Q = QtWidgets.QAction(AdministracionLogIn)
        self.actionSalir_Ctrl_Q.setObjectName("actionSalir_Ctrl_Q")
        self.actionEstacionamiento_v_1_0 = QtWidgets.QAction(AdministracionLogIn)
        self.actionEstacionamiento_v_1_0.setObjectName("actionEstacionamiento_v_1_0")
        self.actionLab_Sistemas_Embebidos = QtWidgets.QAction(AdministracionLogIn)
        self.actionLab_Sistemas_Embebidos.setObjectName("actionLab_Sistemas_Embebidos")
        self.menuMen.addAction(self.actionRegistro_de_autos)
        self.menuMen.addAction(self.actionHistorial_de_ingresos)
        self.menuMen.addAction(self.actionSalida_de_autos)
        self.menuMen.addAction(self.actionAdministraci_n)
        self.menuMen.addAction(self.actionSalir_Ctrl_Q)
        self.menuAcerca_de.addAction(self.actionEstacionamiento_v_1_0)
        self.menuAcerca_de.addAction(self.actionLab_Sistemas_Embebidos)
        self.menubar.addAction(self.menuMen.menuAction())
        self.menubar.addAction(self.menuAcerca_de.menuAction())

        self.retranslateUi(AdministracionLogIn)
        self.stackedWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(AdministracionLogIn)

        self.statusbar.showMessage('Administración Log-In')

        self.actionRegistro_de_autos.triggered.connect(self.RegistroDeAutos)
        self.actionRegistro_de_autos.triggered.connect(self.estatusEstacionamiento)
        
        self.actionHistorial_de_ingresos.triggered.connect(self.HistorialDeIngresos)
        self.actionHistorial_de_ingresos.triggered.connect(self.verHistorial)
        
        self.actionSalida_de_autos.triggered.connect(self.SalidaVehiculosEstacionamiento)
        self.actionAdministraci_n.triggered.connect(self.AdministracionScreen)
        self.actionSalir_Ctrl_Q.triggered.connect(self.Salir)
        self.actionSalir_Ctrl_Q.setShortcut('Ctrl+Q')
        
        self.Entrar.clicked.connect(self.verificarUsuario)
        
        self.EntradaManualBoton.clicked.connect(self.ingresarPlaca)
        #self.SalidaManualBoton.clicked.connect(self.sacarCoche)
        self.CarroBoton.clicked.connect(lambda: self.sacarCoche(int(3)))
        self.CamionetaBoton.clicked.connect(lambda: self.sacarCoche(int(2)))
        self.CamionBoton.clicked.connect(lambda: self.sacarCoche(int(1)))
        self.LevantarPlumaBoton.clicked.connect(self.moverPluma)
        
        self.CarroBotonModificarMonto.clicked.connect(lambda: self.cambiarPrecios(int(3)))
        self.CamionetaBotonModificarMonto.clicked.connect(lambda: self.cambiarPrecios(int(2)))
        self.CamionBotonModificarMonto.clicked.connect(lambda: self.cambiarPrecios(int(1)))
        
        #self.YourTableName.item(row, column).setText("Put here whatever you want!")

    def retranslateUi(self, AdministracionLogIn):
        _translate = QtCore.QCoreApplication.translate
        AdministracionLogIn.setWindowTitle(_translate("AdministracionLogIn", "Proyecto de estacionamiento"))
        self.EntradaManualBoton.setText(_translate("AdministracionLogIn", "Entrada Manual"))
        self.LevantarPlumaBoton.setText(_translate("AdministracionLogIn", "Levantar Pluma"))
        self.SalidaVehiculo.setText(_translate("AdministracionLogIn", "Entrada y salida de vehículo del estacionamineto"))
        self.MatriculaLeida.setText(_translate("AdministracionLogIn", "Matrícula leída"))
        self.CheckIn.setText(_translate("AdministracionLogIn", "Check-in"))
        self.CheckOut.setText(_translate("AdministracionLogIn", "Check-out"))
        self.TotalCobrar.setText(_translate("AdministracionLogIn", "Total a cobrar"))
        self.LogIn.setText(_translate("AdministracionLogIn", "Log-In"))
        self.Usuario.setText(_translate("AdministracionLogIn", "Usuario"))
        self.Contrasea.setText(_translate("AdministracionLogIn", "Contraseña"))
        self.Entrar.setText(_translate("AdministracionLogIn", "Entrar"))
        self.Administracion.setText(_translate("AdministracionLogIn", "Administración"))
        self.MontoPrimerasHoras.setText(_translate("AdministracionLogIn", "Monto por hora o fracción"))
        self.MontoPrimerasHoras_2.setText(_translate("AdministracionLogIn", "Selecciona el tipo de vehículo a modificar"))
        self.HistorialIngresos.setText(_translate("AdministracionLogIn", "Historial de ingresos al estacionamiento"))
        item = self.TablaAutosIngresados.verticalHeaderItem(0)
        item.setText(_translate("AdministracionLogIn", "1"))
        item = self.TablaAutosIngresados.verticalHeaderItem(1)
        item.setText(_translate("AdministracionLogIn", "2"))
        item = self.TablaAutosIngresados.verticalHeaderItem(2)
        item.setText(_translate("AdministracionLogIn", "3"))
        item = self.TablaAutosIngresados.verticalHeaderItem(3)
        item.setText(_translate("AdministracionLogIn", "4"))
        item = self.TablaAutosIngresados.verticalHeaderItem(4)
        item.setText(_translate("AdministracionLogIn", "6"))
        item = self.TablaAutosIngresados.horizontalHeaderItem(0)
        item.setText(_translate("AdministracionLogIn", "Matrícula"))
        item = self.TablaAutosIngresados.horizontalHeaderItem(1)
        item.setText(_translate("AdministracionLogIn", "Check-in"))
        item = self.TablaAutosIngresados.horizontalHeaderItem(2)
        item.setText(_translate("AdministracionLogIn", "Check-out"))
        item = self.TablaAutosIngresados.horizontalHeaderItem(3)
        item.setText(_translate("AdministracionLogIn", "Monto cobrado"))
        self.AutosDentro.setText(_translate("AdministracionLogIn", "Autos dentro del estacionamiento"))
        item = self.TablaAutos.verticalHeaderItem(0)
        item.setText(_translate("AdministracionLogIn", "1"))
        item = self.TablaAutos.verticalHeaderItem(1)
        item.setText(_translate("AdministracionLogIn", "2"))
        item = self.TablaAutos.verticalHeaderItem(2)
        item.setText(_translate("AdministracionLogIn", "3"))
        item = self.TablaAutos.verticalHeaderItem(3)
        item.setText(_translate("AdministracionLogIn", "4"))
        item = self.TablaAutos.verticalHeaderItem(4)
        item.setText(_translate("AdministracionLogIn", "6"))
        item = self.TablaAutos.horizontalHeaderItem(0)
        item.setText(_translate("AdministracionLogIn", "Matrícula"))
        item = self.TablaAutos.horizontalHeaderItem(1)
        item.setText(_translate("AdministracionLogIn", "Check-in"))
        item = self.TablaAutos.horizontalHeaderItem(2)
        item.setText(_translate("AdministracionLogIn", "Tiempo Transcurrido"))
        item = self.TablaAutos.horizontalHeaderItem(3)
        item.setText(_translate("AdministracionLogIn", "Monto hasta el momento"))
        __sortingEnabled = self.TablaAutos.isSortingEnabled()
        self.TablaAutos.setSortingEnabled(False)
        self.TablaAutos.setSortingEnabled(__sortingEnabled)
        self.menuMen.setTitle(_translate("AdministracionLogIn", "Menú"))
        self.menuAcerca_de.setTitle(_translate("AdministracionLogIn", "Acerca de"))
        self.actionRegistro_de_autos.setText(_translate("AdministracionLogIn", "Registro de autos"))
        self.actionHistorial_de_ingresos.setText(_translate("AdministracionLogIn", "Historial de ingresos"))
        self.actionSalida_de_autos.setText(_translate("AdministracionLogIn", "Salida de autos"))
        self.actionAdministraci_n.setText(_translate("AdministracionLogIn", "Administración"))
        self.actionSalir_Ctrl_Q.setText(_translate("AdministracionLogIn", "Salir (Ctrl + Q)"))
        self.actionEstacionamiento_v_1_0.setText(_translate("AdministracionLogIn", "Estacionamiento v 1.0"))
        self.actionLab_Sistemas_Embebidos.setText(_translate("AdministracionLogIn", "Lab. Sistemas Embebidos"))
import Logos

if __name__ == "__main__":
    
    try:
        banderaPluma = 0
        db = MySQLdb.connect("localhost","root","12345","estacionamiento")
        crsr= db.cursor()
    except:
        print ("ERROR: No se puede conectar a la base de datos")
             
    try:
        import sys
        app = QtWidgets.QApplication(sys.argv)
        AdministracionLogIn = QtWidgets.QMainWindow()
        ui = Ui_AdministracionLogIn()
        ui.setupUi(AdministracionLogIn)
        AdministracionLogIn.show()
        sys.exit(app.exec_())
    except KeyboardInterrupt:
      print ("Saliendo")
      pass
