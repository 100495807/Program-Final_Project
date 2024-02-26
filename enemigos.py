"""
Create by Javier Moyano San Bruno and Jorge Mejias Donoso in dic 2022
Universidad Carlos III de Madrid
"""

import random

import pyxel
import constantes
import bullets
import explosion
from bullets import DisparosEnem
from explosion import Explosion

bullets = bullets.bullets
enemigos = []
explosiones = explosion.explosiones


class Enemigos:
    ''' Creamos una clase madre (Enemigos), ya que todos los enemigos
    disponen de los mismos métodos y solo cambia en método de "coreografía"
    y el de "clase".'''

    def __init__(self, x, y, avion, sumx, sumy):
        ''' El método __init__ es un método obligatorio a usar si queremos
                disponer de atributos, puesto que aquí se definen. '''

        self.x = x
        self.y = y
        enemigos.append(self)
        self.avion = avion
        self.alive = True
        self.u = 0
        self.v = 0
        self.w = 0
        self.h = 0
        self.bank = 0
        self.lifes = 1
        self.sumx = sumx
        self.sumy = sumy
        self.centerx = None
        self.centery = None
        self.randomnum = 0
        self.has_shot = False

    def clase(self):
        ''' Este método devuelve el tipo de enemigo que es, lo debemos saber
         para otorgar una cierta cantidad de puntos o conocer cuantos
         disparos debe recibir para ser eliminado, como eso se declara en la
         clase hija insertamos un pass para que lo ignore cuando no tiene
         info'''

        pass

    def update(self):
        ''' Este método actualiza los movimientos de los enemigos,
        las colisiones y SIN_TERMINAR '''

        self.centerx = (self.x + (self.x + self.sumx)) / 2
        self.centery = (self.y + (self.y + self.sumy)) / 2
        if self.alive:
            self.coreografia()
            self.colisiones()

    def move(self, dir, u, v, w, h):
        ''' Este método actualiza el movimiento y el sprite mientras un
        avion gira. '''

        self.x += constantes.ENEMY_SPEED * dir[0]
        self.y += constantes.ENEMY_SPEED * dir[1]
        if u or v or w or h:
            self.u = u
            self.v = v
            self.w = w
            self.h = h

    def coreografia(self):
        ''' Cada enemigo tiene su propia coreografía, pero como dentro de la
        clase madre usamos coreografía en otros métodos debemos crearlo.
        Además, dentro de él establecemos Pass para que lo ignore cuando
        tiene no info'''

        pass

    def colisiones(self):
        ''' Metodo que usamos para detectar las colisiones de las balas del
        avion con los enemigos o el avión con el enemigo.
        Además de seleccionar el tipo de enemigo para otorgar
        cierta puntuación. '''

        for bullet in bullets:
            if (
                    self.x + self.w > bullet.x
                    and bullet.x + bullet.w > self.x
                    and self.y + self.h > bullet.y
                    and bullet.y + bullet.h > self.y
            ):


                bullet.alive = False
                self.lifes -= 1
                if self.lifes == 0:
                    self.alive = False
                    Explosion(self.x, self.y, False, bullet, self.avion,
                              self)
                    if self.clase() == 'clase1' or self.clase() == 'clase2':
                        self.avion.score += 10
                    if self.clase() == 'clase3':
                        self.avion.score += 50
                    if self.clase() == 'clase4':
                        self.avion.score += 100

        #colisiones de el avion con los enemigos
        if (
                self.avion.x + self.avion.w > self.x
                and self.x + self.w > self.avion.x
                and self.avion.y + self.avion.h > self.y
                and self.y + self.h > self.avion.y
                and self.avion.alive
                and not self.avion.isloop
        ):
            Explosion(self.avion.x, self.avion.y, True, None, self.avion,
                      None)
            Explosion(self.x, self.y, False, None, self.avion,
                      self)
            self.avion.lifes -= 1
            self.alive = False
            self.avion.alive = False

    #colisiones de las balas de los enemigos con el avion
    def hitbox_bullet(self, bullet):
        ''' Método para detectar el impacto de las balas enemigas con el
            avión.'''

        if (
                self.x + self.sumx > bullet.x
                and bullet.x + 15 > self.x
                and self.y + self.sumy > bullet.y
                and bullet.y + 15 > self.y
                and self.alive
                and bullet.alive
        ):
            return True
        else:
            return False

    def draw(self):
        pyxel.blt(self.x, self.y, self.bank, self.u, self.v, self.w, self.h,
                  colkey=7)


class Enemigos_Regular(Enemigos):

    def __init__(self, x, y, avion):
        ''' El método __init__ es un método obligatorio a usar si queremos
                disponer de atributos, puesto que aquí se definen. '''

        super().__init__(x, y, avion, 10, 10)
        self.down = True
        self.side = None
        self.bank = 2

    def clase(self):
        ''' Metodo que devuelve el tipo de avión'''

        return ('clase1')

    def coreografia(self):
        ''' Método que realiza la coreografía del avion enemigo cuando
            aparece por pantalla. Asimismo ejecuta los disparos del
            enemigo. '''

        if self.x <= self.avion.x and self.down:
            self.move(constantes.DIR_SSE, 4, 45, 18, 16)
            self.side = False
            if self.avion.x - 3 < round(self.x) < self.avion.x + 3 or self.y >= \
                    self.avion.y:
                self.down = False

        if self.x >= self.avion.x and self.down:
            self.move(constantes.DIR_SSW, 4, 45, 18, 16)
            self.side = True
            if self.avion.x - 3 < round(self.x) < self.avion.x + 3 or self.y >= \
                    self.avion.y:
                self.down = False

        if not self.down and self.side:
            self.move(constantes.DIR_NNW, 122, 45, 18, 16)

        if not self.down and not self.side:
            self.move(constantes.DIR_NNE, 122, 45, 18, 16)


        randomnum = pyxel.rndi(0, 20)
        if randomnum == 1 and not self.has_shot:
            DisparosEnem(self.x + (constantes.ANCHO_BALAENEM + 16)/2,
                         self.y + 16, self.avion, self, None)
            self.has_shot = True


class Enemigos_Caza(Enemigos):

    def __init__(self, x, y, avion):
        ''' El método __init__ es un método obligatorio a usar si queremos
                disponer de atributos, puesto que aquí se definen. '''

        super().__init__(x, y, avion, 10, 10)
        self.contador = 0
        self.giro = False
        self.giro1 = False
        self.giro2 = False
        self.bank = 2

    def clase(self):
        ''' Método que devuelve el tipo de avión'''

        return ('clase2')


    def coreografia(self):
        ''' Método que realiza la coreografía del avion enemigo cuando
            aparece por pantalla. Asimismo ejecuta los disparos del enemigo. '''

        if not self.giro:
            self.move(constantes.DIR_E, 4, 4, 19, 17)
            if self.x == 50 and not self.giro1:
                self.giro = True
                self.giro1 = True
            elif self.x == 200 and not self.giro2:
                self.giro = True
                self.giro2 = True

        if self.giro:
            self.contador += 1
            if self.contador < 10:
                self.move(constantes.DIR_SEE, 22, 4, 17, 17)
            elif self.contador < 20:
                self.move(constantes.DIR_SSE, 38, 4, 17, 17)
            elif self.contador < 30:
                self.move(constantes.DIR_S, 60, 4, 17, 17)
            elif self.contador < 40:
                self.move(constantes.DIR_SSW, 83, 4, 17, 17)
            elif self.contador < 50:
                self.move(constantes.DIR_SWW, 101, 4, 17, 17)
            elif self.contador < 60:
                self.move(constantes.DIR_W, 117, 4, 17, 17)
            elif self.contador < 70:
                self.move(constantes.DIR_NWW, 4, 25, 17, 18)
            elif self.contador < 80:
                self.move(constantes.DIR_NNW, 23, 25, 17, 18)
            elif self.contador < 90:
                self.move(constantes.DIR_N, 44, 25, 17, 18)
            elif self.contador < 100:
                self.move(constantes.DIR_NNE, 64, 25, 17, 18)
            elif self.contador < 110:
                self.move(constantes.DIR_NEE, 84, 25, 17, 18)
            elif 110 < self.contador:
                self.giro = False
                self.contador = 0


        randomnum = pyxel.rndi(0, 20)
        if randomnum == 1 and not self.has_shot:
            DisparosEnem(self.x + (constantes.ANCHO_BALAENEM + 17)/2,
                         self.y + 18, self.avion, self, None)
            self.has_shot = True


class Bombardero(Enemigos):

    def __init__(self, x, y, avion):
        ''' El método __init__ es un método obligatorio a usar si queremos
                disponer de atributos, puesto que aquí se definen. '''

        super().__init__(x, y, avion, 10, 10)
        self.giro = False
        self.contador = 0
        self.giro1 = False
        self.bank = 2
        self.lifes = 5

    def clase(self):
        ''' Metodo que devuelve el tipo de avión'''

        return ('clase3')

    def coreografia(self):
        ''' Método que realiza la coreografía del avion enemigo cuando
            aparece por pantalla. Asimismo ejecuta los disparos del enemigo. '''

        if not self.giro:
            self.move(constantes.DIR_S, 2, 66, 30, 24)
            if self.y == 80 and not self.giro1:
                self.giro = True
                self.giro1 = True

        if self.giro:
            self.contador += 1
            if self.contador < 10:
                self.move(constantes.DIR_SSW, 38, 66, 30, 24)
            elif self.contador < 20:
                self.move(constantes.DIR_SWW, 71, 66, 30, 24)
            elif self.contador < 80:
                self.move(constantes.DIR_W, 105, 66, 30, 24)
            elif self.contador < 84:
                self.move(constantes.DIR_NWW, 138, 66, 30, 24)
            elif self.contador < 88:
                self.move(constantes.DIR_NNW, 166, 66, 30, 24)
            elif self.contador < 92:
                self.move(constantes.DIR_N, 201, 66, 30, 24)
            elif self.contador < 96:
                self.move(constantes.DIR_NNE, 2, 94, 30, 24)
            elif self.contador < 100:
                self.move(constantes.DIR_NEE, 39, 94, 30, 24)
            elif self.contador < 160:
                self.move(constantes.DIR_E, 71, 94, 30, 24)
            elif self.contador < 170:
                self.move(constantes.DIR_SEE, 102, 94, 30, 24)
            elif self.contador < 180:
                self.move(constantes.DIR_SSE, 134, 94, 30, 24)
            elif 180 < self.contador:
                self.giro = False
                self.contador = 0

        randomnum = pyxel.rndi(0, 30)
        if randomnum == 1:
            DisparosEnem(self.x + (constantes.ANCHO_BALAENEM + 30)/2,
                         self.y + 24, self.avion, self, None)


class Superbombardero(Enemigos):

    def __init__(self, x, y, avion):
        ''' El método __init__ es un método obligatorio a usar si queremos
                disponer de atributos, puesto que aquí se definen. '''

        super().__init__(x, y, avion, 10, 10)
        self.giro = False
        self.contador = 0
        self.giro1 = False
        self.giro2 = False
        self.bank = 0
        self.lifes = 10

    def clase(self):
        ''' Método que devuelve el tipo de avión'''

        return ('clase4')

    def coreografia(self):
        ''' Método que realiza la coreografía del avion enemigo cuando
            aparece por pantalla. Asimismo ejecuta los disparos del enemigo. '''

        if not self.giro:

            self.move(constantes.DIR_N, 7, 105, 65, 47)
            if self.y == 80 and not self.giro1:
                self.giro = True
                self.giro1 = True
            elif self.giro1 and not self.giro2:
                self.giro = True
                self.giro2 = True

        if self.giro:
            self.contador += 1
            if self.contador < 10:
                self.move(constantes.DIR_NNE, 7, 105, 65, 47)
            elif self.contador < 20:
                self.move(constantes.DIR_NEE, 7, 105, 65, 47)
            elif self.contador < 80:
                self.move(constantes.DIR_E, 7, 105, 65, 47)
            elif self.contador < 84:
                self.move(constantes.DIR_SEE, 7, 105, 65, 47)
            elif self.contador < 88:
                self.move(constantes.DIR_SSE, 7, 105, 65, 47)
            elif self.contador < 92:
                self.move(constantes.DIR_S, 7, 105, 65, 47)
            elif self.contador < 96:
                self.move(constantes.DIR_SSW, 7, 105, 65, 47)
            elif self.contador < 100:
                self.move(constantes.DIR_SWW, 7, 105, 65, 47)
            elif self.contador < 160:
                self.move(constantes.DIR_W, 7, 105, 65, 47)
            elif self.contador < 170:
                self.move(constantes.DIR_NWW, 7, 105, 65, 47)
            elif self.contador < 180:
                self.move(constantes.DIR_NNW, 7, 105, 65, 47)
            elif 180 < self.contador:
                self.giro = False
                self.contador = 0


        self.randomnum = random.randint(0, 100)
        if self.randomnum == 1:
            DisparosEnem(self.x + 47 / 2, self.y + 50,
                         self.avion, self, constantes.DIR_S)
            DisparosEnem(self.x + 47 / 2, self.y + 50,
                         self.avion, self, constantes.DIR_SEE)
            DisparosEnem(self.x + 47 / 2, self.y + 50,
                         self.avion, self, constantes.DIR_SSW)