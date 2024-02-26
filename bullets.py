"""
Create by Javier Moyano San Bruno and Jorge Mejias Donoso in dic 2022
Universidad Carlos III de Madrid
"""

import pyxel

import constantes
from explosion import Explosion
bullets = []
disparosEnem = []

class Bullet:

    def __init__(self, x, y):
        ''' El método __init__ es un método obligatorio a usar si queremos
            disponer de atributos, puesto que aquí se definen. '''

        self.x = x
        self.y = y
        self.w = constantes.ANCHO_BALA
        self.h = constantes.ALTO_BALA
        bullets.append(self)
        self.alive = True

    def update(self):
        ''' Este método actualiza el movimiento de las balas una vez son
        disparadas y las incluye en una lista para cuando salgan del mapa
        sean eliminadas'''

        if self.alive:
            self.y -= constantes.VELOCIDAD_BALA
        if self.y < 0:
            self.alive = False

    def draw(self):
        ''' Este método imprime a las balas en el mapa. '''

        pyxel.blt(self.x, self.y, 0, 102, 83, constantes.ANCHO_BALA,
                  constantes.ALTO_BALA, colkey=7)

class DisparosEnem():

    def __init__(self, x, y, avion, enemy, bomber_dir):
        ''' El método __init__ es un método obligatorio a usar si queremos
            disponer de atributos, puesto que aquí se definen. '''

        self.x = x
        self.y = y
        self.w = constantes.ANCHO_BALA
        self.h = constantes.ALTO_BALA
        self.alive = True
        self.avion = avion
        self.enemy = enemy
        disparosEnem.append(self)
        #Creamos aquí xa y ya para que el disparo no vaya siguiendo al avion
        self.xa = avion.x
        self.ya = avion.y
        self.distx = self.xa - self.x
        self.disty = self.ya - self.y
        self.disthipotenusa = (self.distx ** 2 + self.disty ** 2)**(1/2)
        self.bomber_dir = bomber_dir



    def update(self):
        ''' Este método actualiza el movimiento de las balas una vez son
            disparadas y las incluye en una lista para cuando salgan del mapa
            sean eliminadas'''

        if self.enemy.clase() == 'clase4':
            self.shoot_bomber(self.bomber_dir)
        else:
            self.shoot_plane()

        if self.hitbox_plane() and self.avion.alive and not self.avion.isloop:
            self.alive = False
            self.avion.alive = False
            Explosion(self.avion.x, self.avion.y, True, None, self.avion, None)
            self.avion.lifes -= 1

        if self.y > pyxel.height or self.y < 0 or self.x > pyxel.width or self.x < 0:
            self.alive = False

    def hitbox_plane(self):
        ''' Este método detecta si las balas enemigas entran en contacto
            con el avión. '''

        if (
                self.avion.x + 15 > self.x
                and self.x + 5 > self.avion.x
                and self.avion.y + 15 > self.y
                and self.y + 5 > self.avion.y
        ):
            return True
        else:
            return False

    def shoot_bomber(self, dir_shoot):
        '''Este método actualiza el movimiento de las balas del
        superbombardero'''

        self.x += constantes.VELOCIDAD_BALAENEM * dir_shoot[0]
        self.y += constantes.VELOCIDAD_BALAENEM * dir_shoot[1]


    def shoot_plane(self):
        ''' Este método actualiza el movimiento de las balas del resto de
            enemigos'''

        self.x += self.distx / self.disthipotenusa * constantes.VELOCIDAD_BALAENEM
        self.y += self.disty / self.disthipotenusa * constantes.VELOCIDAD_BALAENEM

    def draw(self):
        ''' Este método imprime a las balas enemigas en el mapa. '''

        pyxel.blt(self.x, self.y, 0, 122, 89, constantes.ANCHO_BALAENEM,
                  constantes.ALTO_BALAENEM, colkey=7)