# =========================================================
# NOMBRE: Edcarlin Angeuris Celesten Benitez
# MATRÍCULA: 24-EISN-2-017
# PROYECTO: Dron Sentinela - Motor Principal
# =========================================================

import pygame
import sys

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

# Configuracion dekl mapa 
TAMANO_CELDA = 40  # Tamaño de cada cuadrito
GRIS_OSCURO = (40, 40, 40) # Color para las líneas
AMARILLO_CRISTAL = (255, 223, 0) # Color de los cristales

def dibujar_cuadricula(superficie):

    """
    Dibuja una red de líneas (nodos) sobre el mapa para facilitar 
    la navegación del algoritmo de IA A*.
    """
    ancho_ventana, alto_ventana = superficie.get_size()
    # Dibuja líneas verticales
    for x in range(0, ancho_ventana, TAMANO_CELDA):
        pygame.draw.line(superficie, GRIS_OSCURO, (x, 0), (x, alto_ventana))
    # Dibuja líneas horizontales
    for y in range(0, alto_ventana, TAMANO_CELDA):
        pygame.draw.line(superficie, GRIS_OSCURO, (0, y), (ancho_ventana, y))
                    
# Configuración pantalla
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Dron Sentinela - Controles")
clock = pygame.time.Clock()

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
        self.boost_duracion = 1000  # 1 segundo en ms
        self.boost_espera = 3000    # 3 segundos en ms
    
    def mover(self, teclas):
        # Determinar velocidad actual
        vel = self.velocidad_boost if self.boost_activo else self.velocidad
        
        # Movimiento WASD
        if teclas[pygame.K_w]:
            self.y -= vel
        if teclas[pygame.K_s]:
            self.y += vel
        if teclas[pygame.K_a]:
            self.x -= vel
        if teclas[pygame.K_d]:
            self.x += vel
        
        # Limitar a la pantalla
        ancho_ventana, alto_ventana = pygame.display.get_surface().get_size()
        self.x = max(self.radio, min(ancho_ventana - self.radio, self.x))
        self.y = max(self.radio, min(alto_ventana - self.radio, self.y))
        
    def activar_boost(self):
        tiempo_actual = pygame.time.get_ticks()
        
        # Solo activar si no está en cooldown
        if not self.boost_activo and tiempo_actual >= self.boost_cooldown:
            self.boost_activo = True
            self.boost_tiempo = tiempo_actual + self.boost_duracion
            self.boost_cooldown = tiempo_actual + self.boost_duracion + self.boost_espera
    
    def actualizar_boost(self):
        tiempo_actual = pygame.time.get_ticks()
        
        # Desactivar boost cuando se acaba el tiempo
        if self.boost_activo and tiempo_actual >= self.boost_tiempo:
            self.boost_activo = False
    
    def dibujar(self, surface):
        # Color cambia cuando boost está activo
        color = VERDE if self.boost_activo else AZUL
        
        # Cuerpo del dron
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.radio)
        
        # Indicador de dirección (pequeño círculo blanco)
        pygame.draw.circle(surface, BLANCO, (int(self.x), int(self.y - 5)), 5)
    
    def get_rect(self):
        return pygame.Rect(
            self.x - self.radio,
            self.y - self.radio,
            self.radio * 2,
            self.radio * 2
        )

# Crear dron en el centro
dron = Dron(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Lista de posiciones para los cristales [Columna, Fila]
# Multiplicamos por TAMANO_CELDA para que queden centrados en la rejilla
cristales = [
    [5 * TAMANO_CELDA + 10, 5 * TAMANO_CELDA + 10],
    [15 * TAMANO_CELDA + 10, 3 * TAMANO_CELDA + 10],
    [10 * TAMANO_CELDA + 10, 12 * TAMANO_CELDA + 10]
]
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
    
    # Dibujar
    # --- SECCIÓN DE RENDERIZADO (DIBUJO) ---
    # Limpiar la pantalla con el color de fondo
    screen.fill(NEGRO)
    
    # Dibujar la cuadrícula de fondo para el sistema de coordenadas de la IA
    dibujar_cuadricula(screen)
    

    # Dibujar los cristales (Objetivos a proteger)
    for c in cristales:
        pygame.draw.rect(screen, AMARILLO_CRISTAL, (c[0], c[1], 20, 20))


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
