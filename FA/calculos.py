# def calcular_medias_mejores_valores(archivo):
#     resultados = {}
#     with open(archivo, 'r') as file:
#         lineas = file.readlines()
#         nombre_archivo = ''
#         mejores_valores = []

#         for linea in lineas:
#             if linea.startswith('###'):
#                 nombre_archivo = linea.strip()
#             elif '-' in linea:
#                 mejor_valor = float(linea.split('-')[-1].strip())
#                 mejores_valores.append(mejor_valor)
#                 if nombre_archivo in resultados:
#                     resultados[nombre_archivo].append(mejor_valor)
#                 else:
#                     resultados[nombre_archivo] = [mejor_valor]

#     medias = {}
#     for archivo, valores in resultados.items():
#         medias[archivo] = sum(valores) / len(valores)

#     return medias

# # Utilizar la función con tu archivo
# archivo_resultados = 'salida nbs con parametros random 5 poblacion.txt'  # Reemplaza con la ruta correcta de tu archivo
# medias_mejores_valores = calcular_medias_mejores_valores(archivo_resultados)

# # Imprimir las medias de los mejores valores para cada archivo
# for archivo, media in medias_mejores_valores.items():
#     print(f"Archivo: {archivo.strip()} - Media de los mejores valores: {media}")

# def procesar_archivo(file_path):
#     with open(file_path, 'r') as file:
#         lines = file.readlines()

#     ejecuciones = []
#     for line in lines:
#         if line.startswith('###'):
#             ejecuciones.append([])  # Iniciar una nueva lista para las ejecuciones
#         elif line.strip() != '':  # Saltar líneas vacías
#             parts = line.split(' - ')
#             valores = list(map(float, parts[0][1:-1].split(', ')))  # Extraer valores y convertir a float
#             min_max = float(parts[1])
#             ejecuciones[-1].append((valores, min_max))  # Agregar los valores a la última ejecución

#     resultados = []
#     for i, ejecucion in enumerate(ejecuciones):
#         valores = [ej[1] for ej in ejecucion]
#         min_valor = min(valores)
#         max_valor = max(valores)
#         idx_min = valores.index(min_valor)
#         idx_max = valores.index(max_valor)
#         resultado = {
#             'Archivo': file_path,
#             'Ejecucion': i + 1,
#             'Minimo': min_valor,
#             'Maximo': max_valor,
#             'Indice_Min': idx_min,
#             'Indice_Max': idx_max
#         }
#         resultados.append(resultado)

#     return resultados

# # Ejemplo de uso para un archivo específico
# archivo = 'salida nbs con parametros random optuna.txt'  # Cambiar por la ruta del archivo deseado
# resultados = procesar_archivo(archivo)
# for resultado in resultados:
#     print(resultado)

# import matplotlib.pyplot as plt

# titulos = ['Variación ejecuciones wi29', 'Variación ejecuciones dj38', 'Variación ejecuciones uy734', 'Variación ejecuciones zi929', 'Variación ejecuciones lu980']
# nombres = ['wi29', 'dj38', 'uy734', 'zi929', 'lu980']
# def generar_boxplot(datos):
#     archivos = datos.split("\n\n")
#     for archivo in archivos:
#         lines = archivo.split("\n")
#         if len(lines) > 1:
#             nombre_archivo = lines[0]
#             valores = []
#             for line in lines[1:]:
#                 # Verificar si la línea tiene valores numéricos
#                 if "-" in line and "[" in line and "]" in line:
#                     valor = float(line.split(" - ")[0].split(", ")[0][1:])
#                     valores.append(valor)
#             if valores:
#                 print(len(valores))
#                 print(valores)
#                 plt.figure(figsize=(8, 6))
#                 plt.boxplot(valores, patch_artist = True,
#                     boxprops = dict(facecolor = "lightblue"))
#                 plt.title(titulos[archivos.index(archivo)])
#                 plt.xlabel("Mejores soluciones")
#                 plt.ylabel('Costo de recorrido')
#                 plt.xticks([1], [nombres[archivos.index(archivo)]])
#                 plt.grid()
#                 plt.show()

# # Lectura del archivo
# nombre_archivo = 'salida nbs con parametros random 5 poblacion.txt'  # Nombre de tu archivo
# with open(nombre_archivo, 'r') as file:
#     datos = file.read()

# # Generar boxplots
# generar_boxplot(datos)

# Valores teóricos
wi29 = 27603
dj38 = 6656
uy734 = 79114
zi929 = 95345
lu980 = 11340

# Datos proporcionados
datos_proporcionados = [
{'Ejecucion': 1, 'Minimo': 27603.0, 'Maximo': 29260.0},
{'Ejecucion': 2, 'Minimo': 6656.0, 'Maximo': 7156.0},
{'Ejecucion': 3, 'Minimo': 94852.0, 'Maximo': 98713.0},
{'Ejecucion': 4, 'Minimo': 109779.0, 'Maximo': 116755.0},
{'Ejecucion': 5, 'Minimo': 13447.0, 'Maximo': 14003.0}
]

# Función para calcular el gap en porcentaje
def calcular_gap_porcentaje(datos, valores_teoricos):
    gaps = []
    for dato in datos:
        valor_teorico = valores_teoricos[dato['Ejecucion']]
        gap_minimo = ((dato['Minimo'] - valor_teorico) / valor_teorico) * 100
        gap_maximo = ((dato['Maximo'] - valor_teorico) / valor_teorico) * 100
        gaps.append({'Ejecucion': dato['Ejecucion'], 'Gap_Minimo': gap_minimo, 'Gap_Maximo': gap_maximo})
    return gaps

# Valores teóricos asociados a cada ejecución
valores_teoricos = {
    1: wi29,
    2: dj38,
    3: uy734,
    4: zi929,
    5: lu980
}

# Calcular los gaps en porcentaje
gaps_calculados = calcular_gap_porcentaje(datos_proporcionados, valores_teoricos)

# Mostrar resultados
for gap in gaps_calculados:
    print(f"Ejecucion {gap['Ejecucion']}: Gap Minimo = {gap['Gap_Minimo']:.2f}%, Gap Maximo = {gap['Gap_Maximo']:.2f}%")






