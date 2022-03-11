# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 09:35:51 2018

@author: Justin Acuña. Luis Vega
"""
#se importan las librerias
import numpy as np
from scipy import misc 
import time
import sys

"""
funcion que recibe los parametros ingersados por consola
@param listaDatos, lista que contiene los parametros ingresados por consola
@param nombreEntrada, nombre de la imagen a manipular
@param nombreSalida, nombre con que se guardara la imagen tratada
@param anchoVentana, dimensiones del estructurante
@param accion, accion a realizar, erosion o dilatacion
@param return nombreSalida,nombreEntrada,anchoVentana,accion
retornan los datos validados
"""
def recibirParametros(listaDatos,nombreEntrada,nombreSalida,anchoVentana,accion):
    #se ejecutara hasta que la lista que contiene los parametros este vacia
    if (listaDatos == [ ]):
        #cuando la lista este vacia llamara a la funcion encargada de validar la entrada
       return validarParametros(nombreSalida,nombreEntrada,anchoVentana,accion);
   #si la posicion concuerda con el identificador
    elif (listaDatos[0] == "-i"):
        #se guarda el dato en la variable respectiva
        nombreEntrada = listaDatos[1];
        #se descartan las posicones que contien el identificador y el dato guardado
        listaDatos = listaDatos[2:];
        #se retorna el llamdo recursivo para continuar la comparacion
        return recibirParametros(listaDatos, nombreEntrada, nombreSalida, anchoVentana, accion);
    elif (listaDatos[0] == "-o"):
        nombreSalida = listaDatos[1];
        listaDatos = listaDatos[2:];
        return recibirParametros(listaDatos, nombreEntrada, nombreSalida,anchoVentana, accion);
    elif (listaDatos[0] == "-v"):
        anchoVentana = listaDatos[1];
        listaDatos = listaDatos[2:];
        return recibirParametros(listaDatos, nombreEntrada, nombreSalida, anchoVentana, accion);
    elif (listaDatos[0] == "-e"):
        accion = listaDatos[1];
        listaDatos = listaDatos[2:];
        return recibirParametros(listaDatos, nombreEntrada, nombreSalida, anchoVentana, accion);
    else:
        recibirParametros(listaDatos[1:], nombreSalida, nombreEntrada, anchoVentana, accion);
        

"""
funcion que valida los paramentros recibidos por consola
@param nombreEntrada,nombreSalida, anchoVentana, accion
@return nombreEntrada,nombreSalida, anchoVentana, accion
retornan los datos validados
"""
def validarParametros(nombreSalida,nombreEntrada, anchoVentana, accion,):
    #se prueba que los datos sean del tipo correcto
    try: 
        nombreEntrada = str(nombreEntrada);
        nombreSalida = str(nombreSalida);
        anchoVentana = int(anchoVentana);
        #retorna las valores recibidos por consola
        return nombreEntrada,nombreSalida, anchoVentana, accion;     
    except:
        #si no son del tipo correcto de dato se muestra un mensaje de error
        raise ValueError("El tipo de dato ingresado es incorrecto");
"""
funcion que recorre las filas de la imagen a procesar
@param imagenAProcesar, imagenAProcesar que sera evaluada
@param filaActual, guarda la pocision actual en las fila
@param numeroFilas, cantidad de filas de la imagenAProcesar
@return imagenProcesada, imagen ya procesada
"""
def recorrerFila(imagenAProcesar,filaActual,numeroFilas,desplazador,dimensiones,imagenProcesada,accion):
    sys.setrecursionlimit(10**6)
    #condicion de parada, se repetira mientras la fila actual sea menor a el numero de filas
    if (filaActual < numeroFilas):
        #se descarta la porcion de la imagenAProcesar por la que el extructurante no puede pasar
        columnaActual= dimensiones // 2;
        #se toma el largo de las columnas, se descarta la porcion por la que el extructurante no puede pasar
        numeroColumnas = len(imagenAProcesar[0,:])- dimensiones // 2;
        #se hace el llamdo de la funcion que recorre las columnas
        #retorna la imagen modificada
        imagenProcesada = recorrerColumna(imagenAProcesar,columnaActual,numeroColumnas,filaActual,desplazador,dimensiones,imagenProcesada,accion);
        #se retorna el llamado recursivo la funcion recorrerFila, se aumenta la fila
        return recorrerFila (imagenAProcesar,filaActual+1,numeroFilas,desplazador,dimensiones,imagenProcesada,accion);
    else:
        #retorna la imagenAProcesar erosionada o dilatada
        return imagenProcesada;
        

"""
funcion que recorre las columnas de la imagen a procesar
@param imagenAProcesar, imagen que sera procesada
@param columnaActual,posicion actual en las columnas
@param filaActual, posicion actual en las filas
@return imagenProcesada, imagen ya  procesada
"""
def recorrerColumna(imagenAProcesar,columnaActual,numeroColumnas,filaActual,desplazador,dimensiones,imagenProcesada,accion):
    #condicion de parada, mientras la columna actual sea menor al numero de columnas
    if (columnaActual < numeroColumnas):
        #se asigna a porcionAComparar el resultado de la funcion encargada de extraer lo porcion a comparar de la imagen
        porcionAComparar = extraerPorcion(imagenAProcesar,filaActual,columnaActual,desplazador);
        #condicion que decide que accion tomar
        #si la accion es erosicionar 
        if (accion == "t"):
            #se asigna a productoPunto el resultado del produto punto para erosion
            productoPunto = erosionar(porcionAComparar,dimensiones);
        else:
            #si no, se asigna a productoPunto el producto punto para dilatacion
            productoPunto = dilatar(porcionAComparar,dimensiones);
        #si el resultado del producto punto es True
        if productoPunto == True:
            #se coloca en un uno en las coordenadas de la posicion actual
            imagenProcesada[filaActual,columnaActual]= 1;
        else:
            #si no, se coloco un cero en las coordenadas de la posicion Acutual
            imagenProcesada[filaActual,columnaActual]= 0;
        #se hace el llamado recursivo, aumentando en uno la columna actual
        return recorrerColumna(imagenAProcesar,columnaActual+1,numeroColumnas,filaActual,desplazador,dimensiones,imagenProcesada,accion);

    else:
        #se retorna la imagen procesada
        return imagenProcesada;
    
"""
funcion encarda de extraer una porcion de la imagen a procesar, para se comparada con el estructurante
@param imagenAprocesar, imagen a a procesar
@param filaAcutal, posicion actual en las filas
@param columnaActual, poscion actual en la columnas
@param desplazador, valor de acuerdo a las dimensiones del estructurante
se utliza para extraer la porcion de la imange a procesar
@return porcionAComparar, porcion extraida de la imagen a procesar
"""
def extraerPorcion(imagenAProcesar,filaActual,columnaActual,desplazador):
    #para extraer la porcion de la imagen se indexa un intervalo de filas y columnas
    #se calcula la fila superior
    fila1 = filaActual - desplazador  
    #se calcula la fila inferior
    fila2 = (filaActual+desplazador)
    #se aumenta en uno la fila inferior, pues esta no es tomada en la indexacion 
    fila2 +=1   
    #se calcula la columna izquierda
    columna1 = columnaActual - desplazador
    #se calcula la columna derecha
    columna2 = (columnaActual + desplazador)
    #se aumenta en uno la columan derecha, pues la ultima columna no es tomada en cuenta
    columna2 +=1
    #se extraer la porcion a comparar
    porcionAcomparar = imagenAProcesar[fila1:fila2,columna1:columna2] 
    #se retorna la porcion a comparar
    return porcionAcomparar
 

"""
funcion encargada de crear el estructurante
@param dimensiones, dimensiones del estructurante
@return estructurante, retorna el estructurante
"""       
def crearEstructurante(dimensiones):
    #crea el estructurante de acuerdo con las dimensiones especificadas por el usuario
    estructurante = np.ones([dimensiones,dimensiones])
    #retorna el estructurante creado
    return estructurante


"""
funcion encargada de hacer la erosion
@param porcionAComparar, porcion extraida de la imagen a procesar
@param dimensiones, dimensiones del estructurante
@return True, si el producto punto es igual
False, de lo contrario
"""
def erosionar(porcionAcomparar,dimensiones):
    #se llama la funcion que crea el estructurante
    estructurante = crearEstructurante(dimensiones)
    #se inicializa en cero el resultado del producto punto
    resultado =0
    #se inicializan en cero la columna y la fila actual
    filaActual =0
    columnaActual =0
    #se llama la funcion encargada de realizar el producto punto
    #se mandan como parametros la porcion a comparar y el estructurante
    productoPunto = calcularProductoPunto(porcionAcomparar,estructurante, resultado, filaActual,columnaActual)
    #se calucula producto punto del estructurante
    producto = calcularProductoPunto(estructurante,estructurante, resultado, filaActual,columnaActual)
    #si el producto punto del la porcion a comparar es igual al producto punto del estructurante
    if productoPunto == producto:
        #retorna True
        return True
    else: 
        #si no, retorna False
        return False
    
    
"""
funcion encargada de realizar la dilatacion
@param porcionAcomparar, porcion extraida de la imagen a procesar
@param dimensiones, dimensiones del estructurante dadas por el usuario
@return True si el resultado del producto punto es mayor a cero
False de lo contrario 
""" 
def dilatar(porcionAcomparar,dimensiones):
    #se llama la funcion que crea el estructurante
    estructurante = crearEstructurante(dimensiones)
    #se inicializa el resultado, la fila y columna Actual
    resultado =0
    filaActual =0
    columnaActual =0   
    #se hace el calculo del producto punto
    productoPunto = calcularProductoPunto(porcionAcomparar,estructurante, resultado, filaActual,columnaActual);
    #si el resultado es mayor que cero
    if productoPunto > 0:
        return True#retorna True
    else:#si no, retorna False 
        return False
    
    
"""
funcion encargda de calcular el producto punto
@param porcionImagen, porcion extraida de la imagen
@param estructurante, estructurante
@param resultado, resultado del producto punto
@param filaActual, posicion actual en las filas
@param columnaActual posicion actual en la columnas
@return resultado, resultado del producto punto
"""
def calcularProductoPunto(porcionImagen,estructurante,resultado,filaActual,columnaActual):
    #condicion de parada, mientras la fila actual sea menor a el largo de las filas
    if (filaActual<len(porcionImagen[:,0])):
        #mientras columna actual sea menor al largo de las columnas
        if (columnaActual< len(porcionImagen[:,0])):
            #se construye el resultado al sumar el producto del los valores de las matrices
            resultado += (porcionImagen[filaActual,columnaActual] * estructurante[filaActual,columnaActual])
            #se hace el llamado recursivo aumentando la columna
            return calcularProductoPunto(porcionImagen,estructurante,resultado,filaActual,columnaActual+1)
        else:
            #se restablece la columna actual
            columnaActual = 0
            #se hace el llamado recursivo aumnetando la fila
            return calcularProductoPunto(porcionImagen,estructurante,resultado,filaActual+1,columnaActual)
    else:
        #se retorna el resultado del producto punto
        return resultado 


def principal():
    #se asigna los parametros ingresados por consola
    #se inicializa las variables que alamcenara los datos ingresados por consola
    listaDatos = sys.argv    
    nombreSalida = time.strftime(time.strftime("%d-%m-%y")+"_"+time.strftime("%I-%M-%S")+".bmp")
    nombreEntrada = ' '
    anchoVentana = 3
    accion = "t"
    #se retorna los datos ingresados por el usuario
    nombreEntrada, nombreSalida, anchoVentana, accion,  = recibirParametros(listaDatos[1:],nombreEntrada, nombreSalida, anchoVentana, accion, )
    nombreEntrada = str(nombreEntrada)
    #se carga la imagen a procesar
    imagenAProcesar = misc.imread(nombreEntrada,1)
    #se combierte a binario la imagen
    imagenAProcesar = imagenAProcesar // 255
    #se asigan las dimensiones del estructurante
    dimensiones = anchoVentana
    #se asigna el numero de filas y se desacarta porcion por la que el estructurante no puede pasar
    numeroFilas=len(imagenAProcesar[:,0])-dimensiones // 2
    filaActual = dimensiones //2
    desplazador = dimensiones // 2
    #se carga la imangen que se modificara al realizar el filtro morfologico
    imagenProcesada = misc.imread(nombreEntrada,1)
    imagenProcesada = imagenProcesada // 255
    imagenResultado = recorrerFila(imagenAProcesar,filaActual,numeroFilas,desplazador,dimensiones,imagenProcesada,accion)
    #se retorna la imagen procesada en el formato original
    imagenResultado =imagenResultado*255
    #se guarda la imagen procesada
    misc.imsave(nombreSalida,imagenResultado)   
    
#para ver el tiempo de ejecucion     
def tiempoEjecucion():
    #se toma el tiempo acutal en que comienza la ejecucion
    inicio = time.time()
    ret = principal()
    #se toma el final de la ejecucion
    fin = time.time()
    #se calcula el tiempo restando el al final el incial
    tiempoTotal = (fin - inicio)*1000
    return tiempoTotal
print("Tarda: ",round(tiempoEjecucion(),2),"ms")
    
    
    
    
    
    
    
    
    

