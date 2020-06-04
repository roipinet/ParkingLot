import subprocess

import os
import time
import datetime
import MySQLdb
import RPi.GPIO as GPIO
from picamera import PiCamera

camera = PiCamera()
banderaPlaca = 0

global crsr
global db
global banderaPluma

def SetAngle(angle):
    duty = angle / 18 + 2
    return duty


def moverPluma():
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
                p.ChangeDutyCycle(SetAngle(90))
                time.sleep(1)
                GPIO.output(servoPIN, False)
                p.ChangeDutyCycle(0)
            except KeyboardInterrupt:
                p.stop()
            p.stop()
            GPIO.cleanup()
            ##Cambiar bandera
            banderaPluma = 1
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
                p.ChangeDutyCycle(SetAngle(0))
                time.sleep(1)
                GPIO.output(servoPIN, False)
                p.ChangeDutyCycle(0)
            except KeyboardInterrupt:
                p.stop()
            p.stop()
            GPIO.cleanup()
            ##Cambiar bandera
            banderaPluma = 0

def calculateDistance():
    try:
        GPIO.setmode(GPIO.BOARD)
        PIN_TRIGGER = 7
        PIN_ECHO = 13

        GPIO.setup(PIN_TRIGGER, GPIO.OUT)
        GPIO.setup(PIN_ECHO, GPIO.IN)
        GPIO.output(PIN_TRIGGER, GPIO.LOW)
        time.sleep(2)
        GPIO.output(PIN_TRIGGER, GPIO.HIGH)

        time.sleep(0.00001)

        GPIO.output(PIN_TRIGGER, GPIO.LOW)

        while GPIO.input(PIN_ECHO) == 0:
            pulse_start_time = time.time()
        while GPIO.input(PIN_ECHO) == 1:
            pulse_end_time = time.time()

        pulse_duration = pulse_end_time - pulse_start_time

        distance = round(pulse_duration * 17150, 2)
        lectura = str(distance) + ' cm'
        return distance
    finally:
        GPIO.cleanup()


def generarTicket(placa):
    time_now = (datetime.datetime.fromtimestamp(time.time()).strftime("%H:%M:%S"))
    date_now = (datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d"))
    date_time = str(date_now) + " " + str(time_now)
    comandoSQL = "INSERT INTO ticket(matricula, entrada, costo, status) VALUES (%s,%s, '3','1')"
    crsr.execute(comandoSQL, [str(placa), str(date_time)])
    db.commit()
        
def checarPlaca(placa):
    comandoSQL = "SELECT * FROM vehiculo WHERE matricula=%s"
    crsr.execute(comandoSQL, [str(placa)])
    if crsr.rowcount == 0:
        #No está registrada
        return False
    elif crsr.rowcount != 0:
        #ya está registrada
        return True

def ingresarPlaca(nuevaPlaca):
        #Buscar si ya existe la placa
        if checarPlaca(nuevaPlaca):
        #Ya existe la placa
            print("El auto ya se encuentra registrado, generando ticket")
            generarTicket(nuevaPlaca)
        else:
        #No existe la placa, se agrega
            comandoSQL = "INSERT INTO vehiculo(matricula) VALUES (%s)"
            print("Se ha registrado el auto, generando ticket")
            crsr.execute(comandoSQL, [str(nuevaPlaca)])
            db.commit()

        #Se genera el ticket
            generarTicket(nuevaPlaca)


##Ingresar placa en el sistema



#connect to db
while(True):
    if __name__ == "__main__":
        
        try:
            banderaPluma = 0
            db = MySQLdb.connect("localhost","root","12345","estacionamiento")
            crsr= db.cursor()
            GPIO.setwarnings(False)
            ##Disparar el analizador de imágenes.
            if(calculateDistance() <= 15 and banderaPlaca == 0):
                print("Nuevo auto detectado")
#                 camera.start_preview()
#                 sleep(5)
                camera.capture('/home/pi/Desktop/GUI_Perfect_Form/placa.jpeg')
#                 camera.stop()
                ruta = "alpr /home/pi/Desktop/GUI_Perfect_Form/placa.jpeg -c eu -n 1"
                resultado = subprocess.run(ruta, shell=True, stdout=subprocess.PIPE)
                banderaPlaca = 1
                print (resultado.stdout)
                ##Aislar la placa

                cadena = str(resultado.stdout)
                inicio = cadena.find('-')
                placa = cadena[inicio+2:inicio+9]
                
                print(placa)
                
                if placa[0:6]=="'No li":
                    print("Placa no reconocible")
                else:
                    placa = placa[:3] + '-' + placa[3:5] + '-' + placa[5:]
                    
                    ingresarPlaca(placa)
                    print(placa)
                    print("Abriendo pluma...")
                    moverPluma()
                    print("Pluma abierta")
                    time.sleep(5)
                    print("Cerrando pluma...")
                    moverPluma()
                    print("Pluma cerrada")
            elif(calculateDistance() > 15):
                banderaPlaca = 0
        except:
            print ("ERROR: No se puede conectar a la base de datos")
             

