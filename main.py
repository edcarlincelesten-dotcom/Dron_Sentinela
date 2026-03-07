# =========================================================
# NOMBRE: Edcarlin Angeuris Celesten Benitez
# MATRÍCULA: 24-EISN-2-017
# PROYECTO: Dron Sentinela - Motor Principal
# =========================================================

import pygame
import sys
from scripts.enemigo import Saqueador
# Inicializar Pygame
pygame.init()

# Constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (0, 150, 255)
VERDE = (0, 255, 100)
AMARILLO_CRISTAL = (255, 223, 0)


import random

# 1 = Muro/Obstáculo, 0 = Pasillo Libre
MAPA = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
    [1,0,0,1,1,1,1,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1,1,1,1,0,0,1],
    [1,0,0,1,0,0,1,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,1],
    [1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,1],
    [1,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,1],
    [1,0,0,0,0,0,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,1,1,0,0,1,0,0,0,1,1,1,1,1,1,1,1,0,0,0,1,0,0,1,1,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,1,1,0,0,1,1,1,1,1,0,0,0,0,0,0,1,1,1,1,1,0,0,1,1,0,0,0,0,0,0,0,1],
    [1,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,1],
    [1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,1],
    [1,0,0,1,0,0,1,0,0,1,1,0,0,0,1,1,1,0,0,1,1,0,0,1,1,1,0,0,0,1,1,0,0,0,1,0,0,1,0,0,1],
    [1,0,0,1,1,1,1,0,0,1,1,0,0,0,1,1,1,0,0,0,0,0,0,1,1,1,0,0,0,1,1,0,0,0,1,1,1,1,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

# Configuración pantalla
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Dron Sentinela - Controles")
clock = pygame.time.Clock()

# Configuracion dekl mapa 
TAMANO_CELDA_FIJO = 25  # Antes dependía de la pantalla, ahora es manual
ANCHO_C = TAMANO_CELDA_FIJO
ALTO_C = TAMANO_CELDA_FIJO

# Para centrar el mapa en la pantalla de 800x600
# El mapa tiene 25 columnas y 11 filas
ancho_v, alto_v = screen.get_size()

ANCHO_C = ancho_v / 40
ALTO_C = alto_v / 20

off_x = (800 - ancho_v) // 2
off_y = (600 - alto_v) // 2

def dibujar_mundo(superficie):

    # Pintamos el fondo de un solo golpe (Suelo futurista)

    superficie.fill((10, 10, 15)) 



    for r, fila in enumerate(MAPA):

        for c, celda in enumerate(fila):

            if celda == 1:

                # Dibujamos los muros estirados

                # El +1 es para que no queden rayas milimétricas entre bloques

                rect = (c * ANCHO_C, r * ALTO_C, ANCHO_C + 1, ALTO_C + 1)

                pygame.draw.rect(superficie, (30, 30, 40), rect)

                

                pygame.draw.rect(superficie, (0, 255, 255), rect, 1)    
   
# Clase del Dron

class Dron:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidad = 5
        self.velocidad_boost = 10
        self.radio = 15
        self.boost_activo = False
        self.boost_tiempo = 0
        self.boost_cooldown = 0
        self.boost_duracion = 1000
        self.boost_espera = 3000
        
        # Cargar imagen del dron
        self.imagen_original = self.cargar_imagen()
        self.imagen = self.imagen_original
        self.rect = self.imagen.get_rect(center=(self.x, self.y)) if self.imagen else None
        
        # Animación
        self.angulo = 0
        self.sentido_rotacion = 1
    
    def cargar_imagen(self):
        """Carga la imagen del dron"""
        try:
            import os
            ruta = os.path.join("assets", "dron.png")
            imagen = pygame.image.load(ruta).convert_alpha()
            return pygame.transform.scale(imagen, (70, 70))
        except:
            return None  # Silenciosamente retorna None si no hay imagen

    def colision(self, nueva_x, nueva_y, mapa):
        col = int(nueva_x // ANCHO_C)
        fila = int(nueva_y // ALTO_C)
        if 0 <= fila < len(mapa) and 0 <= col < len(mapa[0]):
            return mapa[fila][col] == 1
        return True

    def mover(self, teclas):
        vel = self.velocidad_boost if self.boost_activo else self.velocidad
        nueva_x, nueva_y = self.x, self.y

        if teclas[pygame.K_w]: nueva_y -= vel
        if teclas[pygame.K_s]: nueva_y += vel
        if teclas[pygame.K_a]: nueva_x -= vel
        if teclas[pygame.K_d]: nueva_x += vel

        if not self.colision(nueva_x, self.y, MAPA):
            self.x = nueva_x
        if not self.colision(self.x, nueva_y, MAPA):
            self.y = nueva_y

        # Límites
        ancho, alto = pygame.display.get_surface().get_size()
        self.x = max(self.radio, min(ancho - self.radio, self.x))
        self.y = max(self.radio, min(alto - self.radio, self.y))
        
        if self.rect:
            self.rect.center = (self.x, self.y)
        
        # Animación
        if any([teclas[pygame.K_w], teclas[pygame.K_s], 
                teclas[pygame.K_a], teclas[pygame.K_d]]):
            self.angulo += 5 * self.sentido_rotacion
            if abs(self.angulo) > 10:
                self.sentido_rotacion *= -1
        else:
            if self.angulo > 0:
                self.angulo = max(0, self.angulo - 2)
            elif self.angulo < 0:
                self.angulo = min(0, self.angulo + 2)

    def activar_boost(self):
        tiempo = pygame.time.get_ticks()
        if not self.boost_activo and tiempo >= self.boost_cooldown:
            self.boost_activo = True
            self.boost_tiempo = tiempo + self.boost_duracion
            self.boost_cooldown = tiempo + self.boost_duracion + self.boost_espera

    def actualizar_boost(self):
        if self.boost_activo and pygame.time.get_ticks() >= self.boost_tiempo:
            self.boost_activo = False

    def dibujar(self, surface):
        # Efecto boost
        if self.boost_activo:
            for i in range(3):
                radio = self.radio + i * 8
                pygame.draw.circle(surface, (0, 255, 100), 
                                 (int(self.x), int(self.y)), radio, 2)

        # Dibujar imagen o fallback
        if self.imagen:
            img_rotada = pygame.transform.rotate(self.imagen_original, self.angulo)
            rect = img_rotada.get_rect(center=(self.x, self.y))
            
            if self.boost_activo:
                img_boost = img_rotada.copy()
                img_boost.fill((100, 255, 100, 50), special_flags=pygame.BLEND_RGBA_ADD)
                surface.blit(img_boost, rect)
            else:
                surface.blit(img_rotada, rect)
        else:
            # Fallback: círculos
            color = VERDE if self.boost_activo else AZUL
            pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.radio)
            pygame.draw.circle(surface, BLANCO, (int(self.x), int(self.y - 5)), 5)

    def get_rect(self):
        return pygame.Rect(self.x - self.radio, self.y - self.radio, 
                          self.radio * 2, self.radio * 2)

# Crear dron en el centro
dron = Dron(ANCHO_C * 1.5, ALTO_C * 1.5)

# --- AQUÍ NACEN LOS ENEMIGOS ---
enemigos = []
# Ponemos a los 3 enemigos en esquinas o puntos lejanos
posiciones_e = [(2, 1), (22, 1), (12, 9)]
for col, fila in posiciones_e:
    # Ajustamos la posición al centro de la celda
    ex = (col * ANCHO_C) + (ANCHO_C // 2)
    ey = (fila * ALTO_C) + (ALTO_C // 2)
    enemigos.append(Saqueador(ex, ey, TAMANO_CELDA_FIJO))

# Lista de posiciones para los cristales [Columna, Fila]

# --- Configuracion de  cristales ---
lista_cristales = []
# Lista de coordenadas (Columna, Fila) donde aparecerán
pos_c = [
    (4, 1), (20, 1),   
    (12, 3),           
    (2, 5), (22, 5),   
    (10, 9), (14, 9),  
    (7, 4)             
]
for col, fila in pos_c:
    cx = col * ANCHO_C
    cy = fila * ALTO_C
    lista_cristales.append([cx, cy])

# Bucle principal
ejecutando = True

while ejecutando:
    # Delta time
    dt = clock.tick(FPS)
    
    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        
        # Teclas presionadas (una sola vez)
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                ejecutando = False
            if evento.key == pygame.K_SPACE:
                dron.activar_boost()
    
    # Teclas mantenidas (movimiento continuo)
    teclas = pygame.key.get_pressed()
    dron.mover(teclas)
    dron.actualizar_boost()

    # --- LÓGICA DEL ENEMIGO ---
    for e in enemigos:
        e.pensar(dron.x, dron.y, MAPA, lista_cristales)     # Cada enemigo decide su objetivo
        e.mover(MAPA)                          # Cada enemigo avanza
        e.verificar_colision(lista_cristales)    # Cada enemigo intenta robar
        

    # Dibujar
    # --- SECCIÓN DE RENDERIZADO (DIBUJO) ---
    # Limpiar la pantalla con el color de fondo
    screen.fill(NEGRO)

    dibujar_mundo(screen)
    
    
    # Dibujar los cristales (Objetivos a proteger)
    for c in lista_cristales:
        pygame.draw.rect(screen, AMARILLO_CRISTAL, (c[0], c[1], 20, 20))

        # --- DIBUJAR AL ENEMIGO ---
    for e in enemigos:
        e.dibujar(screen)

    # Dibujar al jugador (Dron) sobre el mapa
    dron.dibujar(screen)


    # Mostrar instrucciones
    font = pygame.font.SysFont("arial", 20)
    instrucciones = [
        "WASD - Mover",
        "ESPACIO - Impulso (velocidad x2)",
        "ESC - Salir"
    ]
    
    for i, texto in enumerate(instrucciones):
        superficie = font.render(texto, True, BLANCO)
        screen.blit(superficie, (10, 10 + i * 25))
    
    # Mostrar estado del boost
    tiempo_actual = pygame.time.get_ticks()
    if dron.boost_activo:
        estado = "BOOST ACTIVO!"
        color_estado = VERDE
    elif tiempo_actual < dron.boost_cooldown:
        tiempo_restante = (dron.boost_cooldown - tiempo_actual) // 1000 + 1
        estado = f"Cooldown: {tiempo_restante}s"
        color_estado = (255, 100, 100)
    else:
        estado = "Boost listo"
        color_estado = BLANCO
    
    superficie_estado = font.render(estado, True, color_estado)
    screen.blit(superficie_estado, (SCREEN_WIDTH - 200, 10))
    
    pygame.display.flip()

pygame.quit()
sys.exit()
