"""
Create by Javier Moyano San Bruno and Jorge Mejias Donoso in dic 2022
Universidad Carlos III de Madrid
"""

import random
import pyxel
import constantes
import explosion
from avion import Avion
import main
import bullets
import mapa
from mapa import Portaaviones, Isla1, Isla2, Isla3
import enemigos
from enemigos import Enemigos_Regular, Enemigos_Caza, Bombardero, Superbombardero



avion = Avion(120, 180)
disparosEnem = bullets.disparosEnem
bullets = bullets.bullets
enemigos = enemigos.enemigos
explosiones = explosion.explosiones
mapa = mapa.mapa
portaaviones = Portaaviones(83, 100)
highscore = [0]
APARICION_ISLA1 = (300, 1200, 2100)
APARICION_ISLA2 = (600, 1500)
APARICION_ISLA3 = (900, 1800, 2400)


class App:

    def __init__(self):
        ''' El método __init__ es un método obligatorio a usar si queremos
                disponer de atributos, puesto que aquí se definen. '''

        pyxel.init(255, 255)
        pyxel.load("assets/example.pyxres")
        self.scene = constantes.SCENE_TITLE
        self.contador = 0
        self.contadorgames = 0

        pyxel.run(self.update, self.draw)

    def update(self):
        ''' En este update actualizamos todos los funciones de los objetos
        asi como las pantallas de inicio, juego y fin.'''

        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btn(pyxel.KEY_R) and self.scene == constantes.SCENE_GAMEOVER:
            self.scene = constantes.SCENE_TITLE

        if pyxel.btn(pyxel.KEY_P) and self.scene == constantes.SCENE_TITLE:
            self.contadorgames += 1
            self.scene = constantes.SCENE_BEGINNING

        if self.scene == constantes.SCENE_BEGINNING:

            if self.contador == 0:
                list.clear(mapa)
                Portaaviones(83, 50)


            avion.firstloop = True
            avion.update()
            update_list(mapa)
            self.contador += 1
            main.portaaviones.alive = True
            avion.alive = True
            avion.lifes = 3
            avion.loopsleft = 3
            avion.score = 0
            main.contador = 0

            list.clear(explosiones)
            list.clear(bullets)
            list.clear(disparosEnem)
            list.clear(enemigos)

            if self.contador == 60:
                self.contador = 0
                self.scene = constantes.SCENE_PLAY



        if self.scene == constantes.SCENE_PLAY:
            drawmap()

            if pyxel.frame_count % 75 == 0 and pyxel.frame_count != 0:
                Enemigos_Regular(pyxel.rndi(0, avion.x - 30), 0, avion)

            if pyxel.frame_count % 70 == 0 and pyxel.frame_count != 0:
                Enemigos_Regular(pyxel.rndi(avion.x + 30, pyxel.width - 15), 0, avion)

            if pyxel.frame_count % 800 == 0 and pyxel.frame_count != 0:
                for j in ([0, 30, 60, 90, 120]):
                    Enemigos_Caza(0 - j, 10, avion)

            if pyxel.frame_count % 500 == 0 and pyxel.frame_count != 0:
                Bombardero(200, 0, avion)

            if pyxel.frame_count % 1500 == 0 and pyxel.frame_count != 0:
                Superbombardero(30, 260, avion)

            update_list(explosiones)
            update_list(bullets)
            update_list(disparosEnem)
            update_list(enemigos)
            update_list(mapa)
            cleanup_list(explosiones)
            cleanup_list(bullets)
            cleanup_list(disparosEnem)
            cleanup_list(enemigos)
            cleanup_list(mapa)

            avion.update()
            main.score = avion.score

            if not avion.alive:
                avion.loopsleft = 3
                # Si muere el avion vuelve a la posicion inicial
                self.contador += 1
                avion.x = 120
                avion.y = 180
                avion.u = 1000

                if self.contador > 30:
                    self.contador = 0
                    list.clear(bullets)
                    list.clear(disparosEnem)
                    list.clear(enemigos)
                    list.clear(mapa)

                    if avion.lifes > 0:
                        avion.alive = True

                    else:
                        highscore.append(avion.score)
                        avion.u = 1000
                        self.scene = constantes.SCENE_GAMEOVER

            if main.contador == constantes.FIN_JUEGO:
                highscore.append(avion.score)
                self.scene = constantes.SCENE_GAMEOVER


    def draw(self):
        ''' Este método imprime en el mapa todos los objetos asi como los
        marcadores. '''

        pyxel.cls(5)
        if self.scene == constantes.SCENE_TITLE:
            if not pyxel.frame_count % 5 == 0:
                pyxel.text(pyxel.width/2 - 27, pyxel.height/2 - 10, "- PRESS P -", 0)
            pyxel.text(pyxel.width/2 - 18, 70," 1942 ", 0)

        elif self.scene == constantes.SCENE_BEGINNING:
            draw_list(mapa)
            avion.draw()
            pyxel.text(pyxel.width / 2 - 10, pyxel.height / 2 - 70,
                       f"GAME {self.contadorgames:2}", 7)

        elif self.scene == constantes.SCENE_PLAY:

            draw_list(mapa)
            draw_list(explosiones)
            draw_list(bullets)
            draw_list(disparosEnem)
            draw_list(enemigos)
            avion.draw()
            pyxel.text(2, 4, f"HIGH SCORE {max(main.highscore):3}", 7)
            pyxel.text(69, 4, f"SCORE {avion.score:3}", 7)
            pyxel.text(155, 4, f"LIFES {avion.lifes:2}", 7)
            pyxel.text(200, 4, f"LOOPS LEFT {avion.loopsleft:2}", 7)

        elif self.scene == constantes.SCENE_GAMEOVER:
            game_over()


contador = 0


def drawmap():
    ''' Este método selecciona una isla cada cierto tiempo (medido con un
    contador) para más tarde generarse en el draw.'''
    main.contador += 1

    for i in APARICION_ISLA1:
        if main.contador == i:
            Isla1(random.randint(-50, 200), -100)

    for i in APARICION_ISLA2:
        if main.contador == i:
            Isla3(random.randint(-50, 200), -100)

    for i in APARICION_ISLA3:
        if main.contador == i:
            Isla2(random.randint(-50, 200), -100)

    if main.contador == 2600:
        main.contador = 0
        Portaaviones(83,-248)


def cleanup_list(list):
    '''La mayoría de objetos se insertan a listas, este método limpia esas
    listas una vez el objeto no vuelva a salir mas por pantalla'''
    i = 0
    while i < len(list):
        elem = list[i]
        if not elem.alive:
            list.pop(i)
        else:
            i += 1


def update_list(list):
    ''' La mayoría de objetos se insertan a listas, este método actualiza
    el objeto al que hacemos referencia en la lista'''
    for elem in list:
        elem.update()


def draw_list(list):
    ''' La mayoria de objetos se insertan a listas, este método imprime en
    el mapa al objeto al que hacemos referencia en la lista'''
    for elem in list:
        elem.draw()

def game_over():
    ''' Este método muestra los marcadores en la pantalla "Game over"'''
    pyxel.text(pyxel.width/2 - 15, pyxel.height/2, "GAME OVER", 0)
    pyxel.text(pyxel.width/2 - 25, pyxel.height/2 - 15, f"HIGH SCORE {max(main.highscore):3}", 0)
    if not pyxel.frame_count % 5 == 0:
        pyxel.text(pyxel.width/2 - 19, pyxel.height/2 + 15, "- PRESS R -", 0)