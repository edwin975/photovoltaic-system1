
def P4(Excel,Demanda):

    import Punto2
    import Punto3
    import math as m

    PrecioSTN = 609.57  # $/kWh
    CostoInversion = 75000000
    DTF = 4.49 # % DTF promedio vigente hasta Abril 2020

    CostoAislado,PnoServidaTotal = Punto2.P2(Excel,Demanda,1,1)
    CostoSTN = Punto3.P3(Excel,Demanda,1,1)

    CostoPnoServida = PnoServidaTotal*PrecioSTN

    CostoAisladoDia = round(sum(CostoAislado)+CostoPnoServida,4)
    CostoSTNDia = sum(CostoSTN)

    Ahorro = CostoAisladoDia - CostoSTNDia

    print("\nAhorro por Dia: Sistema acoplado al STN con respecto al sistema aislado: ",Ahorro)

    Dias = CostoInversion/Ahorro

    suma = 0

    if ((Dias-int(Dias))!=0):
        Dias = int(Dias+1)

    DTFdia = m.pow((1+DTF/100),(1/360))-1 # Tasa DTF anual a diaria, y el año comercial es de 360 dias

    for i in range(Dias):

        suma += Ahorro/(m.pow((1+DTFdia),i+1))

    VAN = suma-CostoInversion

    if (VAN>0):
        print("\nSi se justifica la inversion, ya que el VAN es positivo ($ %s), para\nuna tasa de inflacion o tasa de retorno esperado al invertir en banco de %s porciento (DTF)"%(VAN,DTF))
    else:
        print(
            "\nNo se justifica la inversion, ya que el VAN es negativo ($ %s), para una tasa de inflacion o tasa de retorno esperado al invertir en banco de %s porciento (DTF)"%(VAN,DTF))





