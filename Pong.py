import pygame
from pygame.locals import *
import time

pygame.init()

# Crear la ventana
size = 1366, 768
ventana = pygame.display.set_mode(size)
pygame.display.set_caption("Pong")
ancho, alto = pygame.display.get_surface().get_size()

# Cargar y escalar la imagen de fondo
fondo = pygame.image.load("imagenes/Sakamoto days fondo.png")
fondo = pygame.transform.scale(fondo, (ancho, alto))

# Colores
colorfondo = 255, 255, 255
colortextoJugador = 255, 255, 255
color_blanco = 255, 255, 255

# Dimensiones de la barra
barra_ancho = 20
barra_alto = alto

# Posición de la barra
barra_x = (ancho - barra_ancho) // 2
barra_y = 0

# Cargar y escalar la imagen de la pelota
pelota = pygame.image.load("imagenes/bola-roja.png")
pelota = pygame.transform.scale(pelota, (40, 40))
pelotaXY = pelota.get_rect()
pelotaXY.move_ip(ancho // 2 - 8, alto // 2 - 8)

# Cargar y escalar las imágenes de los jugadores
jugador1 = pygame.image.load("imagenes/bate.png")
jugador1 = pygame.transform.scale(jugador1, (jugador1.get_width(), jugador1.get_height() * 1.5))
jugador1XY = jugador1.get_rect()
jugador1XY.move_ip(75, alto / 2)

# Cargar y escalar las imágenes de los jugadores
jugador2 = pygame.image.load("imagenes/palazul.png")
jugador2 = pygame.transform.scale(jugador2, (jugador2.get_width(), jugador2.get_height() * 1.5))
jugador2XY = jugador2.get_rect()
jugador2XY.move_ip(ancho - 75, alto / 2)

choqueSonido = pygame.mixer.Sound("sonidos/sfx_zap.ogg")
explosionSonido = pygame.mixer.Sound("sonidos/explosion.mp3")

puntosJugador1 = 0
puntosJugador2 = 0

tipoletra = pygame.font.Font("fuentes/mifuente.ttf", 100)

# Crear el texto de la puntuación
textojugador1 = tipoletra.render(str(puntosJugador1), 0, colortextoJugador)
textojugador2 = tipoletra.render(str(puntosJugador2), 0, colortextoJugador)
textojugador1_rect = textojugador1.get_rect(center=(ancho * 0.25, alto * 0.1))
textojugador2_rect = textojugador2.get_rect(center=(ancho * 0.75, alto * 0.1))

# Velocidad de la pelota
velocidad_pelota = [5, 5]
incremento_velocidad = 0.01

# Contadores de rachas de puntos
rachaJugador1 = 0
rachaJugador2 = 0

# Cargar la animación de la explosión
explosion = pygame.image.load("Animacion/explosion.gif")
explosion = pygame.transform.scale(explosion, (100, 100))

run = True
while run:

    # Mover la pelota
    pelotaXY = pelotaXY.move(velocidad_pelota)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            run = False

    # Puntuación
    if pelotaXY.left < 0 or pelotaXY.right > ancho:
        if pelotaXY.left < 0:
            puntosJugador2 += 1
            rachaJugador2 += 1
            rachaJugador1 = 0
            pelotaXY.center = (ancho // 2, alto // 2)
            velocidad_pelota = [5, 0]

        if pelotaXY.right > ancho:
            puntosJugador1 += 1
            rachaJugador1 += 1
            rachaJugador2 = 0
            pelotaXY.center = (ancho // 2, alto // 2)
            velocidad_pelota = [-5, 0]

        # Crear el texto de la puntuación
        textojugador1 = tipoletra.render(str(puntosJugador1), 0, colortextoJugador)
        textojugador2 = tipoletra.render(str(puntosJugador2), 0, colortextoJugador)
        textojugador1_rect = textojugador1.get_rect(center=(ancho * 0.25, alto * 0.1))
        textojugador2_rect = textojugador2.get_rect(center=(ancho * 0.75, alto * 0.1))

    # Rebotar la pelota
    if pelotaXY.top < 0 or pelotaXY.bottom > alto:
        velocidad_pelota[1] = -velocidad_pelota[1]

    # Jugador 1
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and jugador1XY.top > 0:
        jugador1XY = jugador1XY.move(0, -5)
    if keys[pygame.K_DOWN] and jugador1XY.bottom < alto:
        jugador1XY = jugador1XY.move(0, 5)
    if keys[pygame.K_LEFT] and jugador1XY.left > 0:
        jugador1XY = jugador1XY.move(-5, 0)
    if keys[pygame.K_RIGHT] and jugador1XY.right < ancho * 0.3:
        jugador1XY = jugador1XY.move(5, 0)

    # Jugador 2
    if keys[pygame.K_w] and jugador2XY.top > 0:
        jugador2XY = jugador2XY.move(0, -5)
    if keys[pygame.K_s] and jugador2XY.bottom < alto:
        jugador2XY = jugador2XY.move(0, 5)
    if keys[pygame.K_a] and jugador2XY.left > ancho * 0.7:
        jugador2XY = jugador2XY.move(-5, 0)
    if keys[pygame.K_d] and jugador2XY.right < ancho:
        jugador2XY = jugador2XY.move(5, 0)

    ## Colisiones
    if jugador1XY.colliderect(pelotaXY):
        choqueSonido.play()
        velocidad_pelota[0] = -velocidad_pelota[0]
        pelotaXY.left = jugador1XY.right
        if rachaJugador1 >= 5:
            explosionSonido.play()
            velocidad_pelota[0] *= 5
            rachaJugador1 = 0

    if jugador2XY.colliderect(pelotaXY):
        choqueSonido.play()
        velocidad_pelota[0] = -velocidad_pelota[0]
        pelotaXY.right = jugador2XY.left
        if rachaJugador2 >= 5:
            velocidad_pelota[0] *= 5
            rachaJugador2 = 0

    # Incrementar la velocidad de la pelota
    velocidad_pelota[0] += incremento_velocidad if velocidad_pelota[0] > 0 else -incremento_velocidad
    velocidad_pelota[1] += incremento_velocidad if velocidad_pelota[1] > 0 else -incremento_velocidad

    # Dibujar la ventana
    ventana.blit(fondo, (0, 0))
    ventana.blit(textojugador1, textojugador1_rect)
    ventana.blit(textojugador2, textojugador2_rect)
    ventana.blit(pelota, (pelotaXY))
    ventana.blit(jugador1, (jugador1XY))
    ventana.blit(jugador2, (jugador2XY))

    # Dibujar la barra blanca en el centro
    pygame.draw.rect(ventana, color_blanco, (barra_x, barra_y, barra_ancho, barra_alto))

    pygame.display.update()
    pygame.display.flip()

pygame.quit()