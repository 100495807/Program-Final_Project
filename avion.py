"""
Create by Javier Moyano San Bruno and Jorge Mejias Donoso in dic 2022
Universidad Carlos III de Madrid
"""

import pyxel

import constantes
from bullets import Bullet


class Avion:

    def __init__(self, x, y):
        ''' El método __init__ es un método obligatorio a usar si queremos
                disponer de atributos, puesto que aquí se definen. '''

        self.x = x
        self.y = y
        self.u = 5
        self.v = 5
        self.w = 25
        self.h = 18
        self.contador = 0
        self.alive = True
        self.frameaspas = 4
        self.score = 0
        self.lifes = 3
        self.contadorloop = 0
        self.isloop = False
        self.firstloop = False
        self.loopsleft = 3

    def update(self):
        ''' Este método crea el movimiento de él avion y se cambia el contador
            para el cambio de aspecto en los giros'''

        if self.alive and not self.isloop:
            #Mover y cambiar de aspecto
            self.mover()
            self.aspectogiro()
            #Disparar las balas

            if pyxel.btnp(pyxel.KEY_SPACE):
                Bullet(self.x + (constantes.ANCHO_PLANE - constantes.ANCHO_BALA) / 2,
                       self.y - constantes.ALTO_BALA)

        if self.isloop or self.firstloop:
            self.loop()

    def mover(self):
        ''' Este método detecta hacia que lugar quiere mover el usuario el
            avión y también ejecuta el movimiento de las helices.'''

        if pyxel.btn(pyxel.KEY_A) and self.x > 0 and not self.firstloop:
            self.x -= constantes.PLANE_SPEED
            self.frameaspas = 4
            if self.contador > -15:
                self.contador += -1

        elif pyxel.btn(pyxel.KEY_D) and self.x < 232 and not self.firstloop:
            self.x += constantes.PLANE_SPEED
            self.frameaspas = 4
            if self.contador < 15:
                self.contador += 1

        elif pyxel.btn(pyxel.KEY_W) and self.y > 70 and not self.firstloop:
            self.y -= constantes.PLANE_SPEED
            self.frameaspas = 3
            self.u = 5
            if self.contador > 0:
                self.contador -= 1
            elif self.contador < 0:
                self.contador += 1

        elif pyxel.btn(pyxel.KEY_S) and self.y < 210 and not self.firstloop:
            self.y += constantes.PLANE_SPEED
            self.frameaspas = 3
            self.u = 5
            if self.contador > 0:
                self.contador -= 1
            elif self.contador < 0:
                self.contador += 1

        else:
            self.frameaspas = 4
            if self.contador > 0:
                self.contador -= 1
            elif self.contador < 0:
                self.contador += 1

        if pyxel.btn(pyxel.KEY_X) and self.loopsleft != 0:
            self.loopsleft -= 1
            self.isloop = True

    def aspectogiro(self):
        ''' Este metodo actualiza el sprite del avion si está girando hacia
            la izquierda o derecha, simulado como si se tumbase.'''

        if self.contador == 0:
            self.u = 5

        elif self.contador >= 5:
            self.u = 37
            if self.contador >= 10:
                self.u = 101
                if self.contador == 15:
                    self.u = 165

        elif self.contador <= -5:
            self.u = 69
            if self.contador <= -10:
                self.u = 133
                if self.contador == -15:
                    self.u = 197

    def loop(self):
        ''' Este método se inicia cuando se solicita ejecutar el loop,
            siendo como una corografía'''

        if pyxel.btn(pyxel.KEY_A) and self.x > 0 and not self.firstloop:
            self.x -= constantes.PLANE_SPEED

        elif pyxel.btn(pyxel.KEY_D) and self.x < 232 and not self.firstloop:
            self.x += constantes.PLANE_SPEED

        self.contadorloop += 1
        self.w = 32
        self.h = 24

        if self.contadorloop < 35:
            self.v = 25
            if self.contadorloop < 5:
                self.u = 1
                self.y -= 1.5
            elif self.contadorloop < 10:
                self.u = 32
                self.y -= 1.5
            elif self.contadorloop < 15:
                self.u = 65
            elif self.contadorloop < 20:
                self.u = 99
                self.y += 1.5
            elif self.contadorloop < 25:
                self.u = 130
                self.y += 1.5
            elif self.contadorloop < 30:
                self.u = 161
                self.y += 1.5
            elif self.contadorloop < 35:
                self.u = 199
                self.y += 1.5

        else:
            self.v = 59
            if self.contadorloop < 40:
                self.u = 1
                self.y += 1.5
            elif self.contadorloop < 45:
                self.u = 33
                self.y += 1.5
            elif self.contadorloop < 50:
                self.u = 65
            elif self.contadorloop < 55:
                self.u = 99
                self.y -= 1.5
            elif self.contadorloop < 60:
                self.u = 130
                self.y -= 1.5
            elif self.contadorloop < 65:
                self.u = 165
                self.y -= 1.5
            else:
                self.contadorloop = 0
                self.isloop = False
                self.firstloop = False
                self.u = 5
                self.v = 5
                self.w = 25
                self.h = 18




    def draw(self):
        ''' Este método imprime el sprite del avion y el de las helices en el
            mapa. '''

        pyxel.blt(self.x, self.y, 0, self.u, self.v, self.w, self.h, colkey=7)
        if pyxel.frame_count % self.frameaspas == 0 and not self.isloop:
            pyxel.blt(self.x, self.y + 2, 0, self.u, 1, 25, 1, colkey=7)