# =========================================================
# NOMBRE: Edcarlin Angeuris Celesten Benitez
# MATRÍCULA: 24-EISN-2-017
# PROYECTO: Dron Sentinela - Clase Saqueador (IA)
# =========================================================

import pygame

class Saqueador:
    def __init__(self, x, y, tamano_celda):
        """
        Inicializa al enemigo encargado de robar cristales.
        """
        self.x = x
        self.y = y
        self.tamano_celda = tamano_celda
        self.velocidad = 2  # Más lento que el dron
        self.color = (220, 20, 60)  # Rojo Carmesí
        self.radio = 15
        self.objetivo_actual = None

    def dibujar(self, superficie):
        """
        Dibuja el cuerpo del saqueador y su ojo robótico.
        """
        pygame.draw.circle(superficie, self.color, (int(self.x), int(self.y)), self.radio)
        pygame.draw.circle(superficie, (255, 255, 255), (int(self.x), int(self.y)), 5)

    def pensar(self, obj_x, obj_y, mapa_datos, lista_cristales):
        # Si hay cristales, fijar el primero como objetivo
        if lista_cristales:
            self.objetivo_actual = lista_cristales[0]
        else:
            self.objetivo_actual = None # Si no hay cristales, se queda quieto



    def mover(self, mapa_datos):

            if self.objetivo_actual:
             tx, ty = self.objetivo_actual
            nx, ny = self.x, self.y
            
            # Movimiento en X
            if self.x < tx:
                nx += self.velocidad
            elif self.x > tx:
                nx -= self.velocidad
            
            # Movimiento en Y
            if self.y < ty:
                ny += self.velocidad
            elif self.y > ty:
                ny -= self.velocidad

            # CORRECCIÓN: Calcular columna y fila correctamente
            # Usamos el mismo sistema de coordenadas que el mapa principal
            ANCHO_C = 800 / 25  # O pasar esto como parámetro desde el main
            ALTO_C = 600 / 11
            
            col = int(nx // ANCHO_C)
            fila = int(ny // ALTO_C)

            # Verificar límites del mapa ANTES de acceder
            if 0 <= fila < len(mapa_datos) and 0 <= col < len(mapa_datos[0]):
                if mapa_datos[fila][col] == 0:
                    self.x, self.y = nx, ny
                # Si es muro (1), no se mueve (se queda en posición actual)
            else:
                # Fuera de límites, no mover
                pass


    def verificar_colision(self, lista_cristales):
        """
        Revisa si el enemigo está tocando algún cristal.
        """
        for cristal in lista_cristales:
            # Rectángulos para detectar el choque
            rect_cristal = pygame.Rect(cristal[0], cristal[1], 20, 20)
            rect_enemigo = pygame.Rect(self.x - self.radio, self.y - self.radio, self.radio * 2, self.radio * 2)
            
            if rect_enemigo.colliderect(rect_cristal):
                lista_cristales.remove(cristal) # ¡Se roba el cristal!
                self.objetivo_actual = None      # Olvida el objetivo viejo
                print("¡Cristal robado!")        # Aviso en consola
                return True
        return False