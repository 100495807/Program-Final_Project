"""
Create by Javier Moyano San Bruno and Jorge Mejias Donoso in dic 2022
Universidad Carlos III de Madrid
"""

import constantes
import pyxel

mapa = []


class Mapa:
    ''' Creamos una clase Madre (Mapa), ya que todas las islas tienen las
    mismas funciones y lo unico que cambia es su sprite'''

    def __init__(self, x, y):
        ''' El método __init__ es un método obligatorio a usar si queremos
        disponer de atributos, puesto que aquí se definen. '''

        self.y = y
        self.x = x
        self.u = 0
        self.v = 0
        self.w = 0
        self.h = 0
        mapa.append(self)
        self.bank = 1
        self.alive = True

    def update(self):
        ''' Este metodo actualiza la posición de los objetos del mapa en el
        lienzo, simulando un movimiento en -y. '''
        self.y += constantes.MOVIMINETO_MAPA
        if pyxel.height < self.y:
            self.alive = False


    def draw(self):
        ''' Este método imprime a las islas en el mapa. '''
        pyxel.blt(self.x, self.y, self.bank, self.u, self.v, self.w, self.h,
                  colkey=8)


class Isla1(Mapa):
    def __init__(self, x, y):
        ''' El método __init__ es un método obligatorio a usar si queremos
                disponer de atributos, puesto que aquí se definen. '''

        super().__init__(x, y)
        ''' Invocamos a la clase madre con el método super()'''
        self.u = 144
        self.v = 0
        self.w = 110
        self.h = 79


class Isla2(Mapa):
    def __init__(self, x, y):
        ''' El método __init__ es un método obligatorio a usar si queremos
                disponer de atributos, puesto que aquí se definen. '''

        super().__init__(x, y)
        ''' Invocamos a la clase madre con el método super()'''
        self.u = 152
        self.v = 88
        self.w = 102
        self.h = 71


class Isla3(Mapa):
    def __init__(self, x, y):
        ''' El método __init__ es un método obligatorio a usar si queremos
                disponer de atributos, puesto que aquí se definen. '''

        super().__init__(x, y)
        ''' Invocamos a la clase madre con el método super()'''
        self.u = 128
        self.v = 160
        self.w = 112
        self.h = 88


class Portaaviones(Mapa):
    def __init__(self, x, y):
        ''' El método __init__ es un método obligatorio a usar si queremos
                disponer de atributos, puesto que aquí se definen. '''

        super().__init__(x, y)
        ''' Invocamos a la clase madre con el método super()'''
        self.u = 0
        self.v = 0
        self.w = 120
        self.h = 250
        self.alive = True