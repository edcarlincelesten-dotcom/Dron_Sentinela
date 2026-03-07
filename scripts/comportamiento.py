# =========================================================
# NOMBRE: Edcarlin Angeuris Celesten Benitez
# MATRÍCULA: 24-EISN-2-017
# PROYECTO: Dron Sentinela - Árbol de Comportamiento 
# =========================================================

import math
import random

class EstadoBT:
    """Estados posibles para los nodos del árbol"""
    EXITO = 1
    FALLO = 2
    EJECUTANDO = 3

class NodoBT:
    """Clase base para todos los nodos del árbol"""
    def __init__(self, nombre=""):
        self.nombre = nombre
    
    def ejecutar(self, enemigo, mundo):
        """Método a implementar por cada nodo"""
        pass

class Secuencia(NodoBT):
    """Ejecuta hijos en orden. FALLO si alguno falla."""
    def __init__(self, nombre="Secuencia", hijos=None):
        super().__init__(nombre)
        self.hijos = hijos if hijos else []
    
    def ejecutar(self, enemigo, mundo):
        for hijo in self.hijos:
            resultado = hijo.ejecutar(enemigo, mundo)
            if resultado == EstadoBT.FALLO:
                return EstadoBT.FALLO
            elif resultado == EstadoBT.EJECUTANDO:
                return EstadoBT.EJECUTANDO
        return EstadoBT.EXITO

class Selector(NodoBT):
    """Ejecuta hijos en orden. EXITO si alguno tiene éxito."""
    def __init__(self, nombre="Selector", hijos=None):
        super().__init__(nombre)
        self.hijos = hijos if hijos else []
    
    def ejecutar(self, enemigo, mundo):
        for hijo in self.hijos:
            resultado = hijo.ejecutar(enemigo, mundo)
            if resultado == EstadoBT.EXITO:
                return EstadoBT.EXITO
            elif resultado == EstadoBT.EJECUTANDO:
                return EstadoBT.EJECUTANDO
        return EstadoBT.FALLO

# =========================================================
# CONDICIONES (Verifican el estado)
# =========================================================

class CondicionVidaBaja(NodoBT):
    def __init__(self, umbral=20):
        super().__init__("VidaBaja")
        self.umbral = umbral
    
    def ejecutar(self, enemigo, mundo):
        return EstadoBT.EXITO if enemigo.salud < self.umbral else EstadoBT.FALLO

class CondicionAcorralado(NodoBT):
    def ejecutar(self, enemigo, mundo):
        """Verifica si no hay rutas de escape"""
        if not mundo.portales:
            return EstadoBT.FALLO
        
        # Verificar si hay al menos un portal alcanzable
        for portal in mundo.portales:
            camino = enemigo.astar.buscar_camino(
                enemigo.x, enemigo.y, portal[0], portal[1]
            )
            if camino:
                return EstadoBT.FALLO  # Hay escape
        
        return EstadoBT.EXITO  # No hay escape

class CondicionHayCristales(NodoBT):
    def ejecutar(self, enemigo, mundo):
        return EstadoBT.EXITO if mundo.cristales else EstadoBT.FALLO

class CondicionTieneCristal(NodoBT):
    def ejecutar(self, enemigo, mundo):
        return EstadoBT.EXITO if enemigo.cristal_cargado else EstadoBT.FALLO

class CondicionPortalCercano(NodoBT):
    def ejecutar(self, enemigo, mundo):
        if not mundo.portales:
            return EstadoBT.FALLO
        
        for portal in mundo.portales:
            dx = portal[0] - enemigo.x
            dy = portal[1] - enemigo.y
            distancia = math.sqrt(dx*dx + dy*dy)
            if distancia < 100:
                return EstadoBT.EXITO
        return EstadoBT.FALLO

# =========================================================
# ACCIONES (Realizan tareas)
# =========================================================

class AccionHuir(NodoBT):
    def ejecutar(self, enemigo, mundo):
        # Prioridad 1: Buscar refugio más alejado del jugador
        if mundo.refugios:
            refugio_mas_alejado = None
            distancia_max = -1
            
            for refugio in mundo.refugios:
                dx = refugio[0] - mundo.jugador_x
                dy = refugio[1] - mundo.jugador_y
                dist = dx*dx + dy*dy
                
                if dist > distancia_max:
                    distancia_max = dist
                    refugio_mas_alejado = refugio
            
            if refugio_mas_alejado:
                enemigo.camino_actual = enemigo.astar.buscar_camino(
                    enemigo.x, enemigo.y, refugio_mas_alejado[0], refugio_mas_alejado[1]
                )
                enemigo.estado = "huyendo"
                enemigo.color_actual = (100, 100, 255)
                return EstadoBT.EJECUTANDO
        
        # Prioridad 2: Buscar portal más alejado
        if mundo.portales:
            portal_mas_alejado = None
            distancia_max = -1
            
            for portal in mundo.portales:
                dx = portal[0] - mundo.jugador_x
                dy = portal[1] - mundo.jugador_y
                dist = dx*dx + dy*dy
                
                if dist > distancia_max:
                    distancia_max = dist
                    portal_mas_alejado = portal
            
            if portal_mas_alejado:
                enemigo.camino_actual = enemigo.astar.buscar_camino(
                    enemigo.x, enemigo.y, portal_mas_alejado[0], portal_mas_alejado[1]
                )
                enemigo.estado = "huyendo"
                enemigo.color_actual = (100, 100, 255)
                return EstadoBT.EJECUTANDO
        
        return EstadoBT.FALLO

class AccionCombatir(NodoBT):
    def ejecutar(self, enemigo, mundo):
        enemigo.estado = "combatiendo"
        enemigo.color_actual = (255, 100, 0)
        
        # Movimiento evasivo
        dx = mundo.jugador_x - enemigo.x
        dy = mundo.jugador_y - enemigo.y
        distancia = math.sqrt(dx*dx + dy*dy)
        
        if distancia > 100:
            # Acercarse al jugador con patrón aleatorio
            angulo = random.uniform(0, 2 * 3.14159)
            radio = 80
            destino_x = mundo.jugador_x + math.cos(angulo) * radio
            destino_y = mundo.jugador_y + math.sin(angulo) * radio
            
            enemigo.camino_actual = enemigo.astar.buscar_camino(
                enemigo.x, enemigo.y, destino_x, destino_y
            )
        
        return EstadoBT.EJECUTANDO

class AccionRobarCristal(NodoBT):
    def ejecutar(self, enemigo, mundo):
        if not mundo.cristales:
            return EstadoBT.FALLO
        
        # Encontrar cristal más cercano
        cristal_cercano = None
        distancia_min = float('inf')
        
        for cristal in mundo.cristales:
            dx = cristal[0] - enemigo.x
            dy = cristal[1] - enemigo.y
            dist = dx*dx + dy*dy
            
            if dist < distancia_min:
                distancia_min = dist
                cristal_cercano = cristal
        
        if cristal_cercano:
            enemigo.camino_actual = enemigo.astar.buscar_camino(
                enemigo.x, enemigo.y, cristal_cercano[0], cristal_cercano[1]
            )
            enemigo.estado = "robando"
            enemigo.objetivo_actual = cristal_cercano
            enemigo.color_actual = (255, 255, 0)
            return EstadoBT.EJECUTANDO
        
        return EstadoBT.FALLO

class AccionEscaparConCristal(NodoBT):
    def ejecutar(self, enemigo, mundo):
        if not mundo.portales or not enemigo.cristal_cargado:
            return EstadoBT.FALLO
        
        # Encontrar portal más cercano
        portal_cercano = None
        distancia_min = float('inf')
        
        for portal in mundo.portales:
            dx = portal[0] - enemigo.x
            dy = portal[1] - enemigo.y
            dist = dx*dx + dy*dy
            
            if dist < distancia_min:
                distancia_min = dist
                portal_cercano = portal
        
        if portal_cercano:
            enemigo.camino_actual = enemigo.astar.buscar_camino(
                enemigo.x, enemigo.y, portal_cercano[0], portal_cercano[1]
            )
            enemigo.estado = "escapando"
            enemigo.color_actual = (0, 255, 0)
            return EstadoBT.EJECUTANDO
        
        return EstadoBT.FALLO

class AccionSeguirCamino(NodoBT):
    def ejecutar(self, enemigo, mundo):
        if not enemigo.camino_actual:
            return EstadoBT.FALLO
        
        # Obtener siguiente punto
        siguiente = enemigo.camino_actual[0]
        dx = siguiente[0] - enemigo.x
        dy = siguiente[1] - enemigo.y
        distancia = math.sqrt(dx*dx + dy*dy)
        
        if distancia < 5:
            # Llegó al punto
            enemigo.camino_actual.pop(0)
            
            if not enemigo.camino_actual:
                # Camino completado
                if enemigo.estado == "robando" and enemigo.objetivo_actual:
                    # Verificar si puede robar
                    for i, cristal in enumerate(mundo.cristales):
                        if cristal == enemigo.objetivo_actual:
                            mundo.cristales.pop(i)
                            enemigo.cristal_cargado = True
                            enemigo.objetivo_actual = None
                            print("¡Cristal robado!")
                            break
                return EstadoBT.EXITO
        else:
            # Moverse hacia el punto
            if distancia > 0:
                dx = (dx / distancia) * enemigo.velocidad
                dy = (dy / distancia) * enemigo.velocidad
                
                # Intentar mover en X
                nueva_x = enemigo.x + dx
                if not enemigo.colisiona_con_mapa(nueva_x, enemigo.y, mundo.mapa):
                    enemigo.x = nueva_x
                
                # Intentar mover en Y
                nueva_y = enemigo.y + dy
                if not enemigo.colisiona_con_mapa(enemigo.x, nueva_y, mundo.mapa):
                    enemigo.y = nueva_y
        
        return EstadoBT.EJECUTANDO

class AccionPatrullar(NodoBT):
    def ejecutar(self, enemigo, mundo):
        enemigo.estado = "patrullando"
        enemigo.color_actual = (220, 20, 60)
        
        # Si no tiene camino, generar destino aleatorio
        if not enemigo.camino_actual:
            for _ in range(50):
                col = random.randint(1, enemigo.ancho_mapa - 2)
                fila = random.randint(1, enemigo.alto_mapa - 2)
                
                if mundo.mapa[fila][col] == 0:
                    ANCHO_C = 800 / enemigo.ancho_mapa
                    ALTO_C = 600 / enemigo.alto_mapa
                    dest_x = col * ANCHO_C + ANCHO_C // 2
                    dest_y = fila * ALTO_C + ALTO_C // 2
                    
                    enemigo.camino_actual = enemigo.astar.buscar_camino(
                        enemigo.x, enemigo.y, dest_x, dest_y
                    )
                    break
        
        # Seguir el camino
        if enemigo.camino_actual:
            siguiente = enemigo.camino_actual[0]
            dx = siguiente[0] - enemigo.x
            dy = siguiente[1] - enemigo.y
            distancia = math.sqrt(dx*dx + dy*dy)
            
            if distancia < 5:
                enemigo.camino_actual.pop(0)
            else:
                if distancia > 0:
                    dx = (dx / distancia) * enemigo.velocidad
                    dy = (dy / distancia) * enemigo.velocidad
                    
                    nueva_x = enemigo.x + dx
                    if not enemigo.colisiona_con_mapa(nueva_x, enemigo.y, mundo.mapa):
                        enemigo.x = nueva_x
                    
                    nueva_y = enemigo.y + dy
                    if not enemigo.colisiona_con_mapa(enemigo.x, nueva_y, mundo.mapa):
                        enemigo.y = nueva_y
        
        return EstadoBT.EJECUTANDO

# =========================================================
# CLASE MUNDO (Estado global)
# =========================================================

class Mundo:
    """Contiene toda la información del entorno"""
    def __init__(self, mapa, cristales, portales, refugios, jugador_x, jugador_y):
        self.mapa = mapa
        self.cristales = cristales
        self.portales = portales
        self.refugios = refugios
        self.jugador_x = jugador_x
        self.jugador_y = jugador_y
    
    def actualizar_jugador(self, x, y):
        self.jugador_x = x
        self.jugador_y = y