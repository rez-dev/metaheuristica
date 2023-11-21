import random

def generar_arreglos(arr, m, longitud_maxima):
    nuevos_arreglos = []
    
    for _ in range(m):
        inicio = random.randint(0, len(arr) - 1)
        longitud_seccion = round(random.uniform(2, longitud_maxima))
        fin = min(inicio + longitud_seccion, len(arr))
        
        seccion_reversa = arr[inicio:fin]
        seccion_reversa.reverse()
        
        nuevo_arreglo = arr[:inicio] + seccion_reversa + arr[fin:]
        nuevos_arreglos.append(nuevo_arreglo)
    
    return nuevos_arreglos

# Ejemplo de uso
arreglo = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
cantidad_nuevos_arreglos = 3
longitud_maxima_seccion = 5
print(arreglo)

nuevos_arreglos = generar_arreglos(arreglo, cantidad_nuevos_arreglos, longitud_maxima_seccion)
for arreglo in nuevos_arreglos:
    print(arreglo)
