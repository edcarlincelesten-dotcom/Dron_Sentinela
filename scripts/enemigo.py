# =========================================================
# NOMBRE: Edcarlin Angeuris Celesten Benitez
# MATRÍCULA: 24-EISN-2-017
# PROYECTO: Dron Sentinela - Clase Saqueador con IA Completa
# =========================================================

import pygame
import math
import random
from scripts.astar import AStar
from scripts.comportamiento import *

class Saqueador:
    def __init__(self, x, y, tamano_celda, ancho_mapa=40, alto_mapa=20):
        """
        Inicializa al enemigo con IA completa
        """
        self.x = x
        self.y = y
        self.tamano_celda = tamano_celda
        self.ancho_mapa = ancho_mapa
        self.alto_mapa = alto_mapa
        
        # Estadísticas
        self.salud = 100
        self.velocidad = 2
        self.radio = 15
        self.cristal_cargado = False
        
        # Referencia a A* (se inicializa después con el mapa)
        self.astar = None
        
        # Estado y camino
        self.estado = "patrullando"
        self.camino_actual = []
        self.objetivo_actual = None
        
        # Colores
        self.color_patrulla = (220, 20, 60)    # Rojo Carmesí
        self.color_huida = (100, 100, 255)      # Azul
        self.color_combate = (255, 100, 0)      # Naranja
        self.color_robo = (255, 255, 0)         # Amarillo
        self.color_escape = (0, 255, 0)         # Verde
        self.color_actual = self.color_patrulla
        
        # Construir árbol de comportamiento
        self.arbol = self.construir_arbol()
    
    def construir_arbol(self):
        """Construye el árbol de comportamiento"""
        # PRIORIDAD ALTA: Huir si vida baja
        huir_alta = Secuencia("HuirAlta", [
            CondicionVidaBaja(20),
            Selector("EstrategiaHuida", [
                AccionHuir(),
                AccionCombatir()
            ])
        ])
        
        # PRIORIDAD MEDIA: Combatir si acorralado
        combatir_media = Secuencia("CombatirMedia", [
            CondicionAcorralado(),
            AccionCombatir()
        ])
        
        # PRIORIDAD BAJA: Misión de robo
        robo_baja = Selector("MisionRobo", [
            # Si tiene cristal, escapar
            Secuencia("EscapeConCristal", [
                CondicionTieneCristal(),
                Selector("EstrategiaEscape", [
                    Secuencia("EscaparPortal", [
                        AccionEscaparConCristal(),
                        AccionSeguirCamino()
                    ]),
                    AccionHuir()
                ])
            ]),
            
            # Si no tiene cristal, robar
            Secuencia("RobarCristal", [
                CondicionHayCristales(),
                Selector("EstrategiaRobo", [
                    Secuencia("RobarYSeguir", [
                        AccionRobarCristal(),
                        AccionSeguirCamino()
                    ]),
                    AccionPatrullar()
                ])
            ])
        ])
        
        # Comportamiento por defecto
        patrullar = AccionPatrullar()
        
        # Raíz del árbol
        return Selector("Raiz", [huir_alta, combatir_media, robo_baja, patrullar])
    
    def inicializar_astar(self, mapa):
        """Inicializa A* con el mapa"""
        ANCHO_C = 800 / self.ancho_mapa
        ALTO_C = 600 / self.alto_mapa
        self.astar = AStar(mapa, ANCHO_C, ALTO_C, self.ancho_mapa, self.alto_mapa)
    
    def colisiona_con_mapa(self, x, y, mapa_datos):
        """Verifica si una posición colisiona con el mapa"""
        ANCHO_C = 800 / self.ancho_mapa
        ALTO_C = 600 / self.alto_mapa
        
        col = int(x // ANCHO_C)
        fila = int(y // ALTO_C)
        
        if fila < 0 or fila >= self.alto_mapa:
            return True
        if col < 0 or col >= self.ancho_mapa:
            return True
            
        return mapa_datos[fila][col] == 1
    
    def pensar(self, mundo):
        """Ejecuta el árbol de comportamiento"""
        if not self.astar:
            self.inicializar_astar(mundo.mapa)
        
        # Ejecutar árbol
        resultado = self.arbol.ejecutar(self, mundo)
    
    def mover(self, mapa_datos):
        """El movimiento se maneja en las acciones del árbol"""
        pass
    
    def verificar_colision(self, lista_cristales):
        """Revisa si el enemigo está tocando algún cristal"""
        for i, cristal in enumerate(lista_cristales[:]):
            dx = cristal[0] - self.x
            dy = cristal[1] - self.y
            distancia = math.sqrt(dx*dx + dy*dy)
            
            if distancia < self.radio + 10:
                lista_cristales.pop(i)
                self.cristal_cargado = True
                self.objetivo_actual = None
                print("¡Cristal robado!")
                return True
        return False
    
    def recibir_danio(self, cantidad):
        """Recibe daño"""
        self.salud -= cantidad
        if self.salud < 0:
            self.salud = 0
    
    def dibujar(self, superficie):
        """Dibuja el cuerpo del saqueador"""
        # Cuerpo principal
        pygame.draw.circle(superficie, self.color_actual, (int(self.x), int(self.y)), self.radio)
        
        # Ojos
        pygame.draw.circle(superficie, (255, 255, 255), (int(self.x - 5), int(self.y - 5)), 4)
        pygame.draw.circle(superficie, (255, 255, 255), (int(self.x + 5), int(self.y - 5)), 4)
        
        # Pupilas
        if self.objetivo_actual:
            if self.objetivo_actual[0] > self.x:
                pygame.draw.circle(superficie, (0, 0, 0), (int(self.x - 3), int(self.y - 6)), 2)
                pygame.draw.circle(superficie, (0, 0, 0), (int(self.x + 7), int(self.y - 6)), 2)
            else:
                pygame.draw.circle(superficie, (0, 0, 0), (int(self.x - 7), int(self.y - 6)), 2)
                pygame.draw.circle(superficie, (0, 0, 0), (int(self.x + 3), int(self.y - 6)), 2)
        else:
            pygame.draw.circle(superficie, (0, 0, 0), (int(self.x - 5), int(self.y - 5)), 2)
            pygame.draw.circle(superficie, (0, 0, 0), (int(self.x + 5), int(self.y - 5)), 2)
        
        # Barra de salud
        ancho_barra = 30
        alto_barra = 4
        x_barra = self.x - ancho_barra // 2
        y_barra = self.y - self.radio - 10
        
        pygame.draw.rect(superficie, (100, 100, 100), (x_barra, y_barra, ancho_barra, alto_barra))
        
        ancho_salud = (self.salud / 100) * ancho_barra
        if self.salud > 50:
            color_salud = (0, 255, 0)
        elif self.salud > 20:
            color_salud = (255, 255, 0)
        else:
            color_salud = (255, 0, 0)
        pygame.draw.rect(superficie, color_salud, (x_barra, y_barra, ancho_salud, alto_barra))
        
        # Indicador de cristal
        if self.cristal_cargado:
            pygame.draw.circle(superficie, (255, 255, 0), (int(self.x), int(self.y - self.radio - 15)), 5)
        
        # Indicador de estado (letra)
        fuente = pygame.font.Font(None, 16)
        if self.estado == "huyendo":
            texto = "H"
        elif self.estado == "combatiendo":
            texto = "C"
        elif self.estado == "robando":
            texto = "R"
        elif self.estado == "escapando":
            texto = "E"
        else:
            texto = "P"
        
        render = fuente.render(texto, True, (255, 255, 255))
        superficie.blit(render, (self.x - 5, self.y - 30))