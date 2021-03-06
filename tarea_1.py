#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Tarea de desarrollo de entornos y agentes
==========================================

En esta tarea realiza las siguiente acciones:

1.- Desarrolla un entorno similar al de los dos cuartos, 
    pero con tres cuartos en el primer piso, 
    y tres cuartos en el segundo piso. 
    
    Las acciones totales serán

    A = {"irDerecha", "irIzquierda", "subir", "bajar", "limpiar" y "noOp"}

    La acción de "subir" solo es legal en el piso de abajo (cualquier cuarto), 
    y la acción de "bajar" solo es legal en el piso de arriba.

    Las acciones de subir y bajar son mas costosas en término de energía 
    que ir a la derecha y a la izquierda, por lo que la función de desempeño 
    debe de ser de tener limpios todos los cuartos, con el menor numero de 
    acciones posibles, y minimozando subir y bajar en relación a ir a los lados.

2.- Diseña un Agente reactivo basado en modelo para este entorno y compara 
    su desempeño con un agente aleatorio despues de 100 pasos de simulación.

3.- Al ejemplo original de los dos cuardos, modificalo de manera que el agente 
    sabe en que cuarto se encuentra pero no sabe si está limpio o sucio. 
    Diseña un agente racional para este problema, pruebalo y comparalo 
    con el agente aleatorio.

4.- Reconsidera el problema original de los dos cuartos, pero ahora modificalo 
    para que cuando el agente decida aspirar, el 80% de las veces limpie pero 
    el 20% (aleatorio) deje sucio el cuarto. Diseña un agente racional
    para este problema, pruebalo y comparalo con el agente aleatorio. 

Todos los incisos tienen un valor de 25 puntos sobre la calificación de la tarea.


"""
__author__ = 'Pablo Caciano Hernandez'

# Requiere el modulo entornos.py
# El modulo doscuartos.py puede ser de utilidad para reutilizar código
# Agrega los modulos que requieras de python

import entornos
import random
from random import choice

class TresCuartos(entornos.Entorno):

    #Tres cuartos arriba y tres abajo

    def transicion(self, estado, accion):
        if not self.accion_legal(estado, accion):
            raise ValueError(" Movimiento invalido ")

        lista= list(estado)

        if accion == 'irDerecha':
            if lista[-1] == 3*3-1:
                lista[-1]=0
            else:
                lista[-1]+=1
            return lista
        elif accion == 'irIzquierda':
            if lista[-1]==0:
                lista[-1]=3*3-1
            else:
                lista[-1]-=1
            return lista
        elif accion == 'irArriba':
            lista[-1]-=3
            if lista[-1]<0:
                lista[-1]+=3*3-1
            return lista
        elif accion == 'irAbajo':
            lista[-1]+=3
            if lista[-1]>3*3-1:
                lista[-1]-=3*3-1
            return lista
        elif accion == 'limpiar':
            lista[lista[-1]]= 'limpio'
            return lista

        else:
            return lista

    def sensores(self, estado):

        return estado[-1],estado[estado[-1]]

    def accion_legal(self, estado, accion):

        return accion in ('irDerecha', 'irIzquierda', 'irArriba', 'irAbajo', 'limpiar' , 'noOp')

    def desempeno_local(self, estado, accion):

        return 0 if accion == 'noOp' and self.isClean(estado) else -1

    def isClean(self,estado):

        for s in range (0,3*3):
            if estado[s] == 'sucio':
                return False
            return True

class DosCuartos(entornos.Entorno):

    def transicion(self, estado, accion):
        if not self.accion_legal(estado,accion):
            raise("Movimiento invalido")
        robot, A, B = estado

#inciso 4.

        if accion == 'limpiar' and robot == 'A':
            if random.randint(1, 100)<80: # El 80% de las veces
                return (robot, A, B) # Regresa el nuevo estado
            else:  # El 20% restante no hace nada
                return ('A', 'noOp', B) # Regresa el nuevo estado
        if accion == 'noOp' and robot == 'B':
            if random.randint(1, 100)<80:
                return (robot, A, B) # Regresa el nuevo estado
            else:
                return ('B', A, 'noOp') # Regresa el nuevo estado

        return (robot,A,B)
    def sensores(self, estado):
        robot, A, B = estado
        return robot, A if robot == 'A' else B

    def accion_legal(self, estado, accion):
        return accion in ('irA', 'irB', 'limpiar', 'noOp')

    def desempeno_local(self, estado, accion):
        robot, A, B = estado
        return 0 if accion == 'noOp' and A == B == 'limpio' else -1

# fin clase DosCuatos

class AgenteAleatorio(entornos.Agente):

    """
    Un agente que solo regresa una accion al azar entre las acciones legales

    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, percepcion):
        return choice(self.acciones)


class AgenteReactivoDoscuartos(entornos.Agente):
    """
    Un agente reactivo simple

    """

    def programa(self, percepcion):
        robot, situacion = percepcion
        return ('limpiar' if situacion == 'sucio' else
                'irA' if robot == 'B' else
                'irB')

class AgenteReactivoModeloDosCuartos(entornos.Agente):
    """
    Un agente reactivo basado en modelo

    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = ['A', 'sucio', 'sucio']
        self.lugar = {'A': 1, 'B': 2}

    def programa(self, percepcion):
        robot, situacion = percepcion

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[self.lugar[robot]] = situacion

        # Decide sobre el modelo interno
        A, B = self.modelo[1], self.modelo[2]
        return ('noOp' if A == B == 'limpio' else
                'limpiar' if situacion == 'sucio' else
                'irA' if robot == 'B' else
                'irB')

def test():

    print "Prueba del entorno de dos cuartos con un agente aleatorio"
    entornos.simulador(DosCuartos(),
                       AgenteAleatorio(['irA', 'irB', 'limpiar', 'noOp']),
                       ('A', 'sucio', 'sucio'), 100)

    print "Prueba del entorno de dos cuartos con un agente reactivo"
    entornos.simulador(DosCuartos(),
                       AgenteReactivoDoscuartos(),
                       ('A', 'sucio', 'sucio'), 100)

    print "Prueba del entorno de dos cuartos con un agente reactivo"
    entornos.simulador(DosCuartos(),
                       AgenteReactivoModeloDosCuartos(),
                       ('A', 'sucio', 'sucio'), 100)

    print "Prueba del entorno Tres cuartos"

    lista=[]
    for i in range(0,3*3):
        lista.append('sucio')
    lista.append(0)

    entornos.simulador(TresCuartos(),AgenteAleatorio(['irDerecha','irIzquierda','irArriba','irAbajo','limpiar','noOp']),lista,100)

if __name__ == '__main__':
    test()
