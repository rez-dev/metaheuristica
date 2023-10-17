import math

def calcular_distancia(puntos):
    n = len(puntos)
    matriz_distancias = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            if i == j:
                matriz_distancias[i][j] = 0.0
            else:
                x1, y1 = puntos[i][1], puntos[i][2]
                x2, y2 = puntos[j][1], puntos[j][2]
                distancia = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                matriz_distancias[i][j] = distancia
                matriz_distancias[j][i] = distancia
    return matriz_distancias

def leer_archivo_de_coordenadas(nombre_archivo):
    puntos = []
    try:
        with open(nombre_archivo, 'r') as archivo:
            for linea in archivo:
                partes = linea.strip().split()
                if len(partes) == 3:
                    punto_id = int(partes[0])
                    x = float(partes[1])
                    y = float(partes[2])
                    puntos.append((punto_id, x, y))
    except FileNotFoundError:
        print(f"El archivo {nombre_archivo} no se encontró.")
    return puntos
nombre_archivo = 'dj38.tsp'  # Reemplaza esto con el nombre de tu archivo
puntos = leer_archivo_de_coordenadas(nombre_archivo)
# Calcular la matriz de distancias
matriz_distancias = calcular_distancia(puntos)

