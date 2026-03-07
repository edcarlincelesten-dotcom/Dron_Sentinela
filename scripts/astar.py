# =========================================================
# NOMBRE: Edcarlin Angeuris Celesten Benitez
# MATRÍCULA: 24-EISN-2-017
# PROYECTO: Dron Sentinela - Algoritmo A* desde Cero
# =========================================================

class NodoAStar:
    """Nodo para el algoritmo A* - Implementación manual"""
    def __init__(self, x, y, g=0, h=0, padre=None):
        self.x = x  # Coordenada x en celdas
        self.y = y  # Coordenada y en celdas
        self.g = g  # Costo desde el inicio
        self.h = h  # Heurística estimada al objetivo
        self.f = g + h  # Costo total
        self.padre = padre

class ListaPrioridad:
    """Cola de prioridad manual para A*"""
    def __init__(self):
        self.elementos = []
    
    def push(self, nodo):
        # Insertar y ordenar por valor f
        self.elementos.append(nodo)
        self.elementos.sort(key=lambda x: x.f)
    
    def pop(self):
        if self.elementos:
            return self.elementos.pop(0)
        return None
    
    def vacia(self):
        return len(self.elementos) == 0
    
    def contiene(self, x, y):
        for nodo in self.elementos:
            if nodo.x == x and nodo.y == y:
                return True
        return False
    
    def obtener(self, x, y):
        for nodo in self.elementos:
            if nodo.x == x and nodo.y == y:
                return nodo
        return None

class AStar:
    """Implementación manual del algoritmo A*"""
    def __init__(self, mapa, ancho_celda, alto_celda, ancho_mapa, alto_mapa):
        self.mapa = mapa
        self.ancho_celda = ancho_celda
        self.alto_celda = alto_celda
        self.ancho_mapa = ancho_mapa
        self.alto_mapa = alto_mapa
        
        # Direcciones: 4 direcciones (sin diagonales)
        self.direcciones = [
            (0, -1),  # Arriba
            (1, 0),   # Derecha
            (0, 1),   # Abajo
            (-1, 0)   # Izquierda
        ]
    
    def coordenadas_a_celda(self, x, y):
        """Convierte coordenadas de píxeles a celdas"""
        col = int(x // self.ancho_celda)
        fila = int(y // self.alto_celda)
        return col, fila
    
    def celda_a_coordenadas(self, col, fila):
        """Convierte celdas a coordenadas de píxeles (centro)"""
        x = col * self.ancho_celda + self.ancho_celda // 2
        y = fila * self.alto_celda + self.alto_celda // 2
        return x, y
    
    def es_transitable(self, col, fila):
        """Verifica si una celda es transitable"""
        if fila < 0 or fila >= self.alto_mapa:
            return False
        if col < 0 or col >= self.ancho_mapa:
            return False
        return self.mapa[fila][col] == 0  # 0 = libre
    
    def heuristica(self, x1, y1, x2, y2):
        """Distancia Manhattan como heurística"""
        return abs(x1 - x2) + abs(y1 - y2)
    
    def buscar_camino(self, inicio_x, inicio_y, objetivo_x, objetivo_y):
        """
        Implementación manual de A*
        Retorna lista de puntos (x, y) en coordenadas de píxeles
        """
        # Convertir a coordenadas de celda
        col_inicio, fila_inicio = self.coordenadas_a_celda(inicio_x, inicio_y)
        col_objetivo, fila_objetivo = self.coordenadas_a_celda(objetivo_x, objetivo_y)
        
        # Verificar que inicio y objetivo sean transitables
        if not self.es_transitable(col_inicio, fila_inicio):
            col_inicio, fila_inicio = self.encontrar_transitable_cercano(col_inicio, fila_inicio)
        
        if not self.es_transitable(col_objetivo, fila_objetivo):
            col_objetivo, fila_objetivo = self.encontrar_transitable_cercano(col_objetivo, fila_objetivo)
        
        # Estructuras de datos
        lista_abierta = ListaPrioridad()
        lista_cerrada = []
        nodos_explorados = {}
        
        # Crear nodo inicial
        h_inicial = self.heuristica(col_inicio, fila_inicio, col_objetivo, fila_objetivo)
        nodo_inicio = NodoAStar(col_inicio, fila_inicio, 0, h_inicial, None)
        lista_abierta.push(nodo_inicio)
        nodos_explorados[(col_inicio, fila_inicio)] = nodo_inicio
        
        while not lista_abierta.vacia():
            nodo_actual = lista_abierta.pop()
            
            # Verificar si llegamos al objetivo
            if nodo_actual.x == col_objetivo and nodo_actual.y == fila_objetivo:
                return self.reconstruir_camino(nodo_actual)
            
            # Agregar a lista cerrada
            lista_cerrada.append((nodo_actual.x, nodo_actual.y))
            
            # Explorar vecinos
            for dx, dy in self.direcciones:
                col_vecino = nodo_actual.x + dx
                fila_vecino = nodo_actual.y + dy
                
                # Verificar si es transitable
                if not self.es_transitable(col_vecino, fila_vecino):
                    continue
                
                # Verificar si ya está en cerrada
                if (col_vecino, fila_vecino) in lista_cerrada:
                    continue
                
                # Calcular nuevos costos
                g_nuevo = nodo_actual.g + 1  # Costo uniforme por movimiento
                
                # Verificar si ya está en abierta
                if (col_vecino, fila_vecino) in nodos_explorados:
                    nodo_vecino = nodos_explorados[(col_vecino, fila_vecino)]
                    if g_nuevo < nodo_vecino.g:
                        # Actualizar con mejor camino
                        nodo_vecino.g = g_nuevo
                        nodo_vecino.f = g_nuevo + nodo_vecino.h
                        nodo_vecino.padre = nodo_actual
                else:
                    # Crear nuevo nodo
                    h_vecino = self.heuristica(col_vecino, fila_vecino, col_objetivo, fila_objetivo)
                    nodo_vecino = NodoAStar(col_vecino, fila_vecino, g_nuevo, h_vecino, nodo_actual)
                    lista_abierta.push(nodo_vecino)
                    nodos_explorados[(col_vecino, fila_vecino)] = nodo_vecino
        
        # No se encontró camino
        return []
    
    def reconstruir_camino(self, nodo_final):
        """Reconstruye el camino desde el nodo final"""
        camino = []
        nodo_actual = nodo_final
        
        while nodo_actual:
            x, y = self.celda_a_coordenadas(nodo_actual.x, nodo_actual.y)
            camino.append((x, y))
            nodo_actual = nodo_actual.padre
        
        camino.reverse()  # De inicio a fin
        return camino
    
    def encontrar_transitable_cercano(self, col, fila, radio_max=5):
        """Encuentra celda transitable más cercana"""
        for radio in range(1, radio_max + 1):
            for dx in range(-radio, radio + 1):
                for dy in range(-radio, radio + 1):
                    nueva_col = col + dx
                    nueva_fila = fila + dy
                    if self.es_transitable(nueva_col, nueva_fila):
                        return nueva_col, nueva_fila
        return col, fila