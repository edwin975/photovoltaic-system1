
def P3(Excel,A,Mostrar,Diabase):

    import numpy as np
    import cvxopt.modeling as cv
    import pylab as py
    import Punto1

    def RadHoras(DiaBase):
        pos = suma = 0
        DiaH = list()

        for i in range(24): #Horas del dia
            cont = pos
            for j in range(12):
                suma += DiaBase[j+ cont]
                if j==11:
                  DiaH.append(suma/12)
                  suma = 0
                pos +=1

        return DiaH

    if (Diabase==1):
        DiaBase = Punto1.P(Excel,1) # Dia Base punto 1
    else:
        DiaBase = Excel # Todos  los dias del año incluido el dia base

    DiaBaseH = RadHoras(DiaBase)

    """
    DiaBaseH = [0.0, 0.0, 0.0, 1000, 0.0, 0.0, 211.33333333333334, 583.1666666666666, 771.25, 850.8333333333334, 861.3333333333334,
     850.75, 794.3333333333334, 870.3333333333334, 895.5833333333334, 882.0, 750.0833333333334, 516.0833333333334,
     99.41666666666667, 0.0, 0.0, 0.0, 0.0, 0.0]
    """
    DiaBaseH = list(np.array(DiaBaseH)*(1/1000)) #kw/m^2

    Pde = list(A[:,1])

    # Valores de POTENCIA maximos y minimos en kW
        #Bateria
    PBmax = 5  # capacidad maxima de la bateria 13.5 kw, pero solo puede cargarse o descargarse por hora 5 kw
    PBmin = 0
    Befi = 0.9
    Vmax = 13.5
    Vmin = 0
    Vinicial = 0
        # Generador Diesel
    PDMax = 2.8
    PDmin = 0
    capacidadDiesel = 12.5  # Litros
    PrecioGalon = 8151.994  # FALTA DEFINIR PRECIO
        # Paneles
    PsMax = 0.255
    Psmin = 0
    numPanel = 40
        # STN
    PrecioSTN = 609.57  # $/kWh
    PstnMin = 0
    PstnMax = 25

    # Variables

    horas = len(Pde)  # 24 horas

    Pstn = cv.variable()
    PD = cv.variable()
    PB = cv.variable()
    PS = cv.variable()
    V = cv.variable()
    S = cv.variable()
    R = cv.variable()

    Vant = list()
    STN = list()
    Pdiesel = list()
    Psol = list()
    Pbateria = list()
    PnoServida = list()
    Vertimiento = list()
    VolumenAux = list()
    Costo = list()
    Todo = list()

    for h in range(horas):

        Res = []
        Res.append(PD<=PDMax)
        Res.append(PD>=PDmin)

        hsp = DiaBaseH[h]  #Horas solares
        Pmax = hsp*PsMax
        Pmaxtotal = Pmax*numPanel

        Res.append(PS<=float(Pmaxtotal))
        Res.append(PS>=Psmin)

        Res.append(V<=Vmax)
        Res.append(V>=Vmin)

        Res.append(PB<=PBmax)
        Res.append(PB>=PBmin)

        Res.append(S >= 0)
        Res.append(R>=0)
        Res.append(Pstn >= PstnMin)
        Res.append(Pstn <= PstnMax)

        if h>0:

                if ((Pmaxtotal + PDMax) >= Pde[h]):
                    Res.append(PB == 0)
                else:
                    if (Pa==0):
                        if (Vant[h - 1] != 0):
                            Res.append(PB <= Pbaux)
                    else:
                        Res.append(PB <= Pbaux)

                Res.append(Pa - S <= PBmax)
                Res.append(Vant[h - 1] + Pa - PB - S == V)


        else:
            Res.append(PB==0)
            Pa = 0
            Res.append(S==0)
            Res.append(V == Vinicial + Pa - PB - S)

        Res.append((Pstn + PD + PS + Befi * PB + R) == float(Pde[h]))

        LITROS = (capacidadDiesel / PDMax) * PD
        galones = LITROS * (1 / 3.785412)  # Conversion de litros a galones

        costo = galones * PrecioGalon + PrecioSTN*Pstn + 5 * PrecioGalon * R + 1000 * S  # Funcion Objetivo

        fo = cv.op(costo, Res)

        fo.solve()

        fo.status

        costo1 = fo.objective.value()
        aux = np.array(costo1)
        aux = round(float(aux[0, 0]), 4)
        Costo.append(aux)

        vol = np.array(V.value)
        vol = round(float(vol[0, 0]), 4)
        Vant.append(vol)

        aux = np.array(Pstn.value)
        aux = round(float(aux[0, 0]), 4)
        STN.append(aux)

        aux = np.array(PD.value)
        aux = round(float(aux[0, 0]), 4)
        Pdiesel.append(aux)

        aux = np.array(PS.value)
        aux = round(float(aux[0, 0]), 4)
        Psol.append(aux)

        if (h > 0):

            Pa = abs(round(float(round(Pmaxtotal,4) - Psol[h]),3))

            if (vol>=Vmax):
                Saux = Pa
            else:
                if (Pa>PBmax):
                    Saux = Pa-PBmax
                else:
                    if (vol<=(Vmax-PBmax)):
                        Saux = 0
                    else:
                        if(Pa>(Vmax-vol)):
                            Saux = Pa-Vmax+vol
                        else:
                            Saux = 0
            if ((Pa-Saux+vol)>=PBmax):
                Pbaux = PBmax
            else:
                Pbaux = Pa-Saux+vol

            VolumenAux.append(vol+Pa-Saux)

        aux = np.array(PB.value)
        aux = round(float(aux[0, 0]), 4)
        Pbateria.append(Befi*aux)

        aux = np.array(R.value)
        a1 = float(aux[0, 0])
        aux = round(float(aux[0, 0]), 4)
        PnoServida.append(aux)

        aux = np.array(S.value)
        a2 = float(aux[0, 0])
        aux = round(float(aux[0, 0]), 4)
        Vertimiento.append(aux)

        Costo[h] = round((Costo[h]-(5*PrecioGalon*a1+1000*a2)),4)

        if (Mostrar==0):
            print("\n\nITERACION: ", h)
            print("STN: ", STN[h])
            print("Diesel: ", Pdiesel[h])
            print("SOL: ", Psol[h])
            if(h==0):
                Saux = 0
            print("Volumen al Final Iter = ", vol + Pa - Saux)
            print("BATERIA: ", Befi * Pbateria[h])
            print("R: ", PnoServida[h])
            print("S: ", Vertimiento[h])
            print("COSTO: ", Costo[h])
            print("Valor Pa: ",Pa)

    cont = 0
    for i in VolumenAux:
        Vant[cont + 1] = round(i, 3)
        Pbateria[cont] = round(Pbateria[cont], 3)
        cont += 1
    cont = 0
    Costo1 = horas*[0]
    for i in Costo:
        Costo1[cont] = round(i, 4)
        cont += 1

    if (Mostrar==0):

        print("\nIrradiacion por Horas: ", DiaBaseH)
        print("Costo: ",Costo1)
        print("\nPotencia Diesel: ", Pdiesel)
        print("\nPotencia sol: ",  Psol)
        print("\nPotencia bateria: ", Pbateria)
        print("\nvolumen: ", Vant)
        print("\nPotencia NS: ", PnoServida)
        print("\nS: ", Vertimiento)

        py.figure(1)
        py.plot(range(24), Costo1)
        py.title('Costo vs tiempo')
        py.xlabel('Hora')
        py.ylabel('costo [$COP]')



        py.figure(2)
        py.plot(range(24),Psol)
        py.title('Potencia Paneles vs tiempo')
        py.xlabel('Hora')
        py.ylabel('Potencia [kW]')


        py.figure(3)
        py.plot(range(24), Pdiesel)
        py.title('Potencia Diesel vs tiempo')
        py.xlabel('Hora')
        py.ylabel('Potencia [kW]')


        py.figure(4)
        py.plot(range(24), Pbateria)
        py.title('Potencia Bateria vs tiempo')
        py.xlabel('Hora')
        py.ylabel('Potencia [kW]')


        py.figure(5)
        py.plot(range(24), Vant)
        py.title('Almacenamiento Bateria vs tiempo')
        py.xlabel('Hora')
        py.ylabel('Potencia [kW]')


        PnsTotal = sum(PnoServida)

        py.figure(6)
        py.plot(range(24), PnoServida)
        py.title('Potencia No servida vs tiempo\nEnergia acumulada (%s kWh/dia)'% PnsTotal)
        py.xlabel('Hora')
        py.ylabel('Potencia [kW]')


        py.figure(7)
        py.plot(range(24), STN)
        py.title('Potencia STN vs tiempo')
        py.xlabel('Hora')
        py.ylabel('Potencia [kW]')

        py.show()

    else:
        if (Diabase==0):
            Todo.append(STN)
            Todo.append(Pdiesel)
            Todo.append(Psol)
            Todo.append(Pbateria)
            Todo.append(PnoServida)
            Todo.append(Vant)
            Todo.append(Costo1)
            return Todo
        else:
            return Costo



