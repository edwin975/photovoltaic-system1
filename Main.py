
import pandas as pd
import numpy as np
import  os

import Punto1
import Punto2
import Punto3
import Punto4
import Punto5

nom = 'datos_sol.xlsx'
columna = {"columna":str}
archivo = pd.ExcelFile(nom)
hoja1 = archivo.sheet_names

recibido = pd.read_excel(nom,hoja1[0])
df = pd.DataFrame(recibido)
A = np.array(recibido)

nom = 'Demanda.xlsx'
archivo = pd.ExcelFile(nom)
hoja1 = archivo.sheet_names

recibido = pd.read_excel(nom, hoja1[0])
Demanda = np.array(recibido)

print("Vector Demanda:\n",Demanda)

intento=0

while (intento==0):

    os.system('cls')

    print("Por favor seleccione una opcion: \n")
    print("1. Punto 1\n2.Punto 2\n3.Punto 3\n4.Punto 4\n5. Punto 5\n")

    opcion = int(input())

    if (opcion==1):
        Punto1.P(A,0)
        des = int(input("\n\nPara volver al menu precione 1:  "))
        if (des==1):
            intento = 0
        else:
            intento = 1
    elif (opcion==2):
        Punto2.P2(A,Demanda,0,1)
        des = int(input("\n\nPara volver al menu precione 1:  "))
        if (des == 1):
            intento = 0
        else:
            intento = 1
    elif (opcion==3):
        Punto3.P3(A,Demanda,0,1)
        des = int(input("\n\nPara volver al menu precione 1:  "))
        if (des == 1):
            intento = 0
        else:
            intento = 1
    elif (opcion == 4):
        Punto4.P4(A,Demanda)
        des = int(input("\n\nPara volver al menu precione 1:  "))
        if (des == 1):
            intento = 0
        else:
            intento = 1
    elif (opcion==5):
        Punto5.P5(A,Demanda)
        des = int(input("\n\nPara volver al menu precione 1:  "))
        if (des == 1):
            intento = 0
        else:
            intento = 1
    else:
        print("\nIntentar nuevamente (opcion invalida)")
        intento = 0

print("\nPROGRAMA FINALIZADO")