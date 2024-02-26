"""
Create by Javier Moyano San Bruno and Jorge Mejias Donoso in dic 2022
Universidad Carlos III de Madrid
"""

import pyxel
explosiones = []


class Explosion:

    def __init__(self, x, y, isplayer, bullet, avion, enemy):
        ''' El método __init__ es un método obligatorio a usar si queremos
                disponer de atributos, puesto que aquí se definen. '''

        self.x = x
        self.y = y
        self.i = 0
        self.isplayer = isplayer
        self.alive = True
        self.enemy = enemy
        self.bank = 0

        if isplayer:
            self.u = 0
            self.v = 152
            self.w = 30
            self.h = 31
            self.avion = avion
            self.planeboom = [3, 33, 69, 108, 145, 184]

        else:
            self.u = 0
            self.v = 0
            self.w = 0
            self.h = 0
            self.bullet = bullet
            self.enemy = enemy      #en este caso enemigo
            self.explosion1 = [4, 21, 41, 64, 87, 107]
            self.explosion2 = [3, 33, 69, 108, 145, 184]
            self.explosion3u = [7, 74, 141, 7, 74, 141, 7, 74, 141, 211, 211,
                               211]
            self.explosion3v = [105, 105, 105, 162, 162, 162, 216, 216, 216,
                                109, 170, 226]
            self.explosion3h = [50, 50, 50, 50, 50, 50, 50, 50, 30,
                                30, 30, 22]

        explosiones.append(self)

    def update(self):
        ''' Este método actualiza los distintos sprites que se usan para
        simular la explosion dependiendo del avion que sea. '''

        if self.isplayer and self.alive:
            self.bank = 2

            if self.i < len(self.planeboom) - 1:
                self.u = self.planeboom[self.i]
                self.i += 1
            else:

                self.avion.alive = False
                self.avion.u = 1000
                self.alive = False

        else:

            if self.enemy.clase() == 'clase1' or self.enemy.clase() == 'clase2':
                self.u = 0
                self.v = 129
                self.w = 18
                self.h = 16
                self.bank = 2

                if self.i < len(self.explosion1) - 1:
                    self.u = self.explosion1[self.i]
                    self.i += 1

                else:
                    self.alive = False

            if self.enemy.clase() == 'clase3':
                self.v = 186
                self.w = 30
                self.h = 31
                self.bank = 2

                if self.i < len(self.explosion2) - 1:
                    self.u = self.explosion2[self.i]
                    self.i += 1

                else:
                    self.alive = False

            if self.enemy.clase() == 'clase4':
                self.w = 65
                self.h = 50
                self.bank = 0

                if self.i < len(self.explosion3u) - 1:
                    self.u = self.explosion3u[self.i]
                    self.v = self.explosion3v[self.i]
                    self.h = self.explosion3h[self.i]
                    self.i += 1
                    if self.i >=9:
                        self.x += 3
                        self.y += 3

                else:
                    self.alive = False


    def draw(self):
        ''' Este método imprime a las animaciones de las explosiones en el
            mapa.'''
        pyxel.blt(self.x, self.y, self.bank, self.u, self.v, self.w, self.h,
                  colkey=7)