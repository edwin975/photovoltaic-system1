def P(A,Mostrar):

    import  pylab as pyl
    import numpy as np

    mayor = -1000000
    dias = 365
    pos = 0
    DatosDia = int(len(A)/dias)

    # Identifica el dia con mayor radiacion

    for iter in range(dias):
        hsp = 0
        for i in range(DatosDia):

            hsp += int(A[pos,2])
            pos += 1
        if (hsp> mayor):
            mayor = hsp
            pos1 = iter*DatosDia

    aux = str(A[pos1,0])
    fecha = list(aux)
    fecha = fecha[0:10]
    fecha = ''.join(fecha)

    mayor = mayor/1000

    DiaBase = list(A[pos1:pos1+288,2])
    Horasbase = list(A[pos1:pos1+288,1])

    HorasBase = list()

    for i in Horasbase:
        tiempo = str(i)
        tiempo = tiempo.split(':')

        horas = int(tiempo[0])
        minutos = int(tiempo[1])

        Horas = horas + minutos / 60
        HorasBase.append(Horas)

    if (Mostrar==0):
        print("\n\nEl dia con mayor radiacion solar es %s, con horas solares pico de %s\n" % (fecha, mayor))
        pyl.plot(HorasBase,DiaBase)

        pyl.title('Irradiancia vs tiempo dia pico (%s)'%fecha)
        pyl.xlabel('Hora')
        pyl.ylabel('Irradiancia [W/m^2]')
        pyl.show()
    else:
        return DiaBase



