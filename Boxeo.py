#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
import sys
import time
from pygame.locals import *
from random import randint

pixel = 650

class player1(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self) #Clase base para mostrar objetos
		self.ImagenJugador = pygame.image.load("Image/BoxerP1A.png") #Cargar imagenes jugador
		self.rect = self.ImagenJugador.get_rect()
		self.rect.centerx = pixel/3
		self.rect.centery = pixel - 300

		self.Vida = 100
		self.Energia = 2
		self.Fuerza = 10
		self.Velocidad = 20

	def obtenerpos(self):
		return self.rect.centerx, self.rect.centery

	def dibujar(self, superficie):
		superficie.blit(self.ImagenJugador, self.rect) #Posicionamiento de jugador en pantalla
		
	def movimientoH(self): #Movimiento horizontal jugador
			if self.rect.left <= 0:
				self.rect.left = 0
			elif self.rect.right >= 2*pixel:
				self.rect.right = 2*pixel

class player2(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self) #Clase base para mostrar objetos
		self.ImagenJugador = pygame.image.load("Image/BoxerP2A.png") #Cargar imagenes jugador
		self.rect = self.ImagenJugador.get_rect()
		self.rect.centerx = 2*pixel - 200 
		self.rect.centery = pixel - 300

		self.Vida = 100
		self.Energia = 2
		self.Fuerza = 10
		self.Velocidad = 20

	def obtenerpos(self):
		return self.rect.centerx, self.rect.centery

	def movimientoH(self): #Movimiento horizontal jugador
			if self.rect.left <= 0:
				self.rect.left = 0
			elif self.rect.right >= 2*pixel:
				self.rect.right = 2*pixel

	def dibujar(self, superficie):
		superficie.blit(self.ImagenJugador, self.rect) #Posicionamiento de jugador en pantalla

def pelea(jugador, enemigo):
	aux = randint(1,3)

	if aux < 3:
		if (enemigo.rect.left + enemigo.Velocidad - 30) > jugador.rect.right:
			enemigo.rect.left -= enemigo.Velocidad
	else:
		enemigo.rect.right += enemigo.Velocidad

	if (jugador.rect.right + 30) >= enemigo.rect.left:
		return True
	else:
		return False

def boxing():
	pygame.init()
	ventana = pygame.display.set_mode((2*pixel,pixel)) #Creacion ventana
	pygame.display.set_caption("Boxing Game")
	fondo = pygame.image.load("Image/fondo.jpg")
	color = (255,255,255)
	jugador = player1()
	enemigo =  player2()

	pygame.mixer.music.load("Sounds/musica.mp3")
	pygame.mixer.music.play(2)

	energiaP1 = pygame.image.load("Image/P1/bar1.png")
	energiaP2 = pygame.image.load("Image/P2/bar1.png")

	fuente = pygame.font.Font(None, 50)
	P11 = fuente.render("Player 1",0,color)
	P22 = fuente.render("Player 2",0,color)
 
	SonidoGolpe = pygame.mixer.Sound("Sounds/golpe.wav")
	KO = pygame.mixer.Sound("Sounds/KO.wav")

	while True:

		jugador.movimientoH()
		enemigo.movimientoH()

		for evento in pygame.event.get():
			if evento.type == QUIT:
				pygame.quit()
				sys.exit()

			elif jugador.Vida > 0 and enemigo.Vida > 0:

				aux = pelea(jugador, enemigo)

				if aux == True:
					enemigo.ImagenJugador = pygame.image.load("Image/BoxerP2B.png")
					enemigo.dibujar(ventana)
					Ltiempo = time.time()

					SonidoGolpe.play()
					jugador.Vida -= enemigo.Fuerza
					cadena = "Image/P2/bar" + str(jugador.Energia) + ".png"
					energiaP1 = pygame.image.load(cadena)
					jugador.Energia += 1
					enemigo.rect.right += 3*enemigo.Velocidad

					if (time.time() - Ltiempo) > 1:
						enemigo.ImagenJugador = pygame.image.load("Image/BoxerP2A.png")
						enemigo.dibujar(ventana)

				if evento.type == pygame.KEYDOWN:

					if evento.key == K_LEFT:
						jugador.rect.left -= jugador.Velocidad # disminuye la coordenanda de la esquina izquierda del rectangulo
					
					elif evento.key == K_RIGHT:
						if (jugador.rect.right + jugador.Velocidad) < (enemigo.rect.left + 30):
							jugador.rect.right += jugador.Velocidad  # disminuye la coordenanda de la esquina derecha del rectangulo
							
					elif evento.key == K_SPACE:
						x,y= jugador.obtenerpos()
						jugador.ImagenJugador = pygame.image.load("Image/BoxerP1B.png")
						jugador.dibujar(ventana)

						SonidoGolpe.play()
										
				elif evento.type == pygame.KEYUP:
					if evento.key == K_SPACE:
						jugador.ImagenJugador = pygame.image.load("Image/BoxerP1A.png")
						jugador.dibujar(ventana)

						if (jugador.rect.right + 60) >= enemigo.rect.left: # Si P1 esta muy cerca de P2 y golpea le hace daño
							enemigo.Vida -= jugador.Fuerza
							cadena = "Image/P1/bar" + str(enemigo.Energia) + ".png"
							energiaP2 = pygame.image.load(cadena)
							enemigo.Energia += 1

			elif jugador.Vida == 0 or enemigo.Vida == 0:
				pygame.mixer.music.stop()

				KO.play()

				GameOver = pygame.image.load("Image/Gover.png")

				ventana.blit(GameOver,(100,0))
				pygame.display.update()
				time.sleep(5)
				sys.exit()

		ventana.blit(fondo,(0,0))
		ventana.blit(P11,(30,0))
		ventana.blit(P22,(2*pixel-250,0))
		ventana.blit(energiaP1,(20,30))
		ventana.blit(energiaP2,(2*pixel-260,30))
		jugador.dibujar(ventana)
		enemigo.dibujar(ventana)
		pygame.display.update()

boxing()