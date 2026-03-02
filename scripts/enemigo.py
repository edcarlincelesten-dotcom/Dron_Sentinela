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

    def pensar(self, lista_cristales):
        """
        Lógica básica: fijar como objetivo el primer cristal disponible.
        """
        if lista_cristales:
            self.objetivo_actual = lista_cristales[0]

    def mover(self):
        """
        Mueve al enemigo paso a paso hacia la posición del cristal objetivo.
        """
        if self.objetivo_actual:
            tx, ty = self.objetivo_actual
            
            if self.x < tx:
                self.x += self.velocidad
            elif self.x > tx:
                self.x -= self.velocidad
                
            if self.y < ty:
                self.y += self.velocidad
            elif self.y > ty:
                self.y -= self.velocidad

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