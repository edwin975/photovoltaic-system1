
def P5(A,De):

    import Punto2
    import Punto3
    import pylab as py

    TodoP2 = 365*[0]
    TodoP3 = 365*[0]
    pos = 0

    for i in range(365):

        DiaRef = list(A[pos:pos + 288, 2])
        TodoP2[i] = Punto2.P2(DiaRef, De, 1, 0)
        TodoP3[i] = Punto3.P3(DiaRef, De, 1, 0)

        pos += 288

    Titulo = ['Potencia STN vs tiempo','Potencia Diesel vs tiempo','Potencia Paneles vs tiempo','Potencia Bateria vs tiempo','Potencia No servida vs tiempo', 'Almacenamiento Bateria vs tiempo','Costo vs tiempo']
    Etiqueta = ['Potencia [kW]','Precio ($ COP)']


    for i in range(2):
        if (i==0):
            num = 6
            num1 = num
            for fig in range(num):
                prom2 = 24*[0]
                py.figure(fig+1)
                py.title(Titulo[fig+1]+'\n(Sistema Aislado)')
                py.xlabel('Hora')

                if (fig!=num-1):
                    py.ylabel(Etiqueta[0])
                else:
                    py.ylabel(Etiqueta[1])

                cont = 0
                b3 = 365*[0]

                for j in TodoP2:
                    aux4 = TodoP2[cont]
                    b4 = aux4[fig]
                    b3[cont] = b4

                    if (cont < len(TodoP2)-1):
                        py.plot(range(24), b4, color='black', alpha=0.5, linewidth=0.5)
                    else:
                        py.plot(range(24), b4, color='black', alpha=0.5, linewidth=0.5, linestyle="-", label="Diario")

                    cont+=1

                for j in range(24):
                    sum = 0
                    for k in range(len(TodoP2)):
                        aux3 = b3[k]
                        sum += aux3[j]

                    prom2[j] = float(sum/len(TodoP2))

                py.plot(range(24),prom2,color='blue', alpha=1.0, linewidth=2.5, linestyle="-", label="Promedio")
                py.legend(loc='upper left')

        else:

            num = 7
            for fig in range(num):
                prom1 = 24*[0]
                py.figure(fig+num1+1)
                py.title(Titulo[fig]+'\n(Sistema conectado al STN)')
                py.xlabel('Hora')
                if (fig != num-1):
                    py.ylabel(Etiqueta[0])
                else:
                    py.ylabel(Etiqueta[1])

                cont = 0
                b2 = 365 * [0]

                for j in TodoP3:
                    aux2 = TodoP3[cont]
                    b1 = aux2[fig]
                    b2[cont] = b1

                    if (cont<len(TodoP3)-1):
                        py.plot(range(24),b1, color='black', alpha=0.5, linewidth=0.5)
                    else:
                        py.plot(range(24), b1, color='black', alpha=0.5, linewidth=0.5, linestyle="-", label="Diario")

                    cont += 1

                for j in range(24):
                    sum = 0
                    for k1 in range(len(TodoP3)):
                        aux1 = b2[k1]
                        sum += aux1[j]

                    prom1[j] = float(sum / len(TodoP3))

                py.plot(range(24), prom1,color='blue', alpha=1.0, linewidth=2.5, linestyle="-", label="Promedio")
                py.legend(loc='upper left')


    py.show() # Mostrar todas las figuras




