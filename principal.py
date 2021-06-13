#! /usr/bin/env python
import os, random, sys, math, time

import pygame
from pygame.locals import *

from configuracion import *
from extras import *
from funcionesSeparador import *
from funcionesRESUELTO import *

#Funcion principal
def main():
    #Centrar la ventana y despues inicializar pygame
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()
    #pygame.mixer.init()

    #Preparar la ventana
    pygame.display.set_caption("Rapido...")
    screen = pygame.display.set_mode((ANCHO, ALTO))

    #tiempo total del juego
    gameClock = pygame.time.Clock()
    totaltime = 0
    timer = time.time()
    segundos = TIEMPO_MAX
    fps = FPS_inicial

    puntos = 0
    candidata = ""
    silabasEnPantalla = []
    posiciones = []
    listaDeSilabas = []
    lemario = []

    pantallas = ["menu", "juego", "puntajes", "jugador"]
    pantallaSeleccionada = "menu"

    opcionesMenu = ["JUGAR", "PUNTAJES", "CAMBIAR JUGADOR", "SALIR"]
    opcionMenuSeleccionada = 0

    jugador = ""
    nombre = ""
    mejoresPuntajes = []

    lastUpgrade = 0

    archivo= open("silabas.txt","r")
    lectura(archivo, listaDeSilabas)
    """ print(listaDeSilabas) """

    archivo2= open("lemario.txt","r")
    lectura(archivo2, lemario)
    """ print(lemario) """

    while True:
        gameClock.tick(fps)

        while jugador == "" or pantallaSeleccionada == "jugador":
            gameClock.tick(fps)
            pygame.display.flip()
            screen.fill(COLOR_FONDO)
            dibujarIngresaNombre(screen, nombre)

            for e in pygame.event.get():
                if e.type == KEYDOWN:
                        letra = dameLetraApretada(e.key)
                        nombre += letra
                        if e.key == K_BACKSPACE:
                            nombre = nombre[0:len(nombre)-1]
                        if e.key == K_RETURN:
                            procesarUsuario(nombre)
                            jugador = nombre
                            pantallaSeleccionada = "menu"
        
        while pantallaSeleccionada == "puntajes":
            gameClock.tick(fps)
            pygame.display.flip()
            screen.fill(COLOR_FONDO)
            dibujarPuntajes(screen, jugador, mejoresPuntajes)

            for e in pygame.event.get():
                if e.type == KEYDOWN:
                    letra = dameLetraApretada(e.key)
                    if e.key == K_RETURN:
                        pantallaSeleccionada = "menu"

        while segundos > fps/1000 and pantallaSeleccionada == "juego":
            # 1 frame cada 1/fps segundos
            gameClock.tick(fps)
            totaltime += gameClock.get_time()

            if True:
                fps = FPS_inicial

            #Buscar la tecla apretada del modulo de eventos de pygame
            for e in pygame.event.get():
                
                #QUIT es apretar la X en la ventana
                if e.type == QUIT:
                    pygame.quit()
                    return()

                #Ver si fue apretada alguna tecla
                if e.type == KEYDOWN:
                    letra = dameLetraApretada(e.key)
                    candidata += letra
                    if e.key == K_BACKSPACE:
                        candidata = candidata[0:len(candidata)-1]
                    if e.key == K_RETURN:
                        puntos += procesar(candidata, silabasEnPantalla, posiciones, lemario)
                        candidata = ""

            segundos = TIEMPO_MAX - (time.time() - timer)

            #Limpiar pantalla anterior
            screen.fill(COLOR_FONDO)

            #Dibujar de nuevo todo
            dibujar(screen, candidata, silabasEnPantalla, posiciones, puntos, segundos)

            pygame.display.flip()

            actualizar(silabasEnPantalla, posiciones, listaDeSilabas, totaltime/1000, lastUpgrade)

            lastUpgrade = totaltime/1000
        
        if segundos <= fps/1000 and pantallaSeleccionada == "juego":
            screen.fill(COLOR_FONDO)
            dibujarPuntajeJuego(screen, puntos)
            guardarPuntaje(jugador, puntos)
            pygame.display.flip()
            time.sleep(4)
            pantallaSeleccionada = "menu"
    
        while pantallaSeleccionada == "menu":
            gameClock.tick(fps)

            screen.fill(COLOR_FONDO)

            dibujarInicio(screen, opcionesMenu, opcionesMenu[opcionMenuSeleccionada], jugador)
            pygame.display.flip()

            #Esperar el QUIT del usuario
            for e in pygame.event.get():
                if e.type == QUIT:
                    pygame.quit()
                    return
                if e.type == KEYDOWN:
                    if e.key == TECLA_ARRIBA:
                        opcionMenuSeleccionada = moverMenu(opcionesMenu, opcionMenuSeleccionada, -1)
                    if e.key == TECLA_ABAJO:
                        opcionMenuSeleccionada = moverMenu(opcionesMenu, opcionMenuSeleccionada, 1)
                    if e.key == K_RETURN:
                        seleccionada = opcionesMenu[opcionMenuSeleccionada]
                        if seleccionada == "JUGAR":
                            timer = time.time()
                            pantallaSeleccionada = "juego"
                        if seleccionada == "PUNTAJES":
                            mejoresPuntajes = buscarMejoresPuntajes(jugador)
                            pantallaSeleccionada = "puntajes"
                        if seleccionada == "CAMBIAR JUGADOR":
                            nombre = ""
                            jugador = ""
                            pantallaSeleccionada = "jugador"
                        if seleccionada == "SALIR":
                            pygame.quit()

#Programa Principal ejecuta Main
if __name__ == "__main__":
    main()
