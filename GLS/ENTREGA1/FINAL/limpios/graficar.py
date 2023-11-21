from matplotlib import pyplot as plt
import numpy as np

# datos100iteraciones = [93343, 11100, 10750, 11153, 10817, 10920, 11506, 10820, 10880, 10746, 10536, 10297, 11211, 11357, 10636, 11403, 10874, 10798, 10441, 10528, 10816, 10525, 10686, 11017, 10512, 10149, 11204, 10425, 10896, 10479, 10600, 11145, 10149]
datos150iteraciones = [
    10837, 11372, 11310, 10912, 10864, 10545, 11099, 10360, 10521, 10564,
    10819, 10722, 10400, 11448, 10636, 10577, 10981, 10649, 11227, 10554,
    10600, 10993, 10503, 11392, 10405, 11304, 10806, 10876, 11092, 10558,
    11095
]

datos100iteraciones = [
    10710, 10570, 10703, 11175, 10861, 11501, 10934, 10925, 11074, 10486, 
    11403, 11384, 10633, 10786, 10846, 10918, 10730, 11129, 10986, 11093, 
    10439, 10678, 11035, 10723, 10951, 10664, 11518, 11117, 10639, 11025, 
    10748
]


# datos1000iteraciones = [90126, 10681, 10443, 10722, 10690, 10699, 10228, 10469, 10666, 10600, 10912, 11089, 11156, 10688, 11047, 10470, 10542, 10886, 11488, 10818, 11064, 11221, 11124, 10622, 10607, 11022, 10795, 10783, 10582, 11257, 10973, 11011, 10228]
# Crear el gráfico
# plt.plot(datos150iteraciones, marker='o', linestyle='-')
# # Configurar etiquetas y título
# plt.xlabel('Iteración')
# plt.ylabel('Costo')
# plt.title('Gráfico de Costos vs N Iteración (150 iteraciones)')
# # Mostrar el gráfico
# plt.grid(True)  # Agregar una cuadrícula
# plt.show()

# mediana100 = np.median(datos100iteraciones)
# mediana150 = np.median(datos150iteraciones)
# print(mediana100)
# print(mediana150)

# Crear un diagrama de cajas
# Crear un diagrama de cajas para la serie 1
plt.boxplot(datos100iteraciones, positions=[1], widths=0.6, patch_artist=True, boxprops=dict(facecolor="blue"))
# Crear un diagrama de cajas para la serie 2
plt.boxplot(datos150iteraciones, positions=[2], widths=0.6, patch_artist=True, boxprops=dict(facecolor="green"))
plt.xticks([1, 2], ['100 iteraciones', '150 iteraciones'])

# Etiquetas para los ejes
plt.xlabel('Iteraciones')
plt.ylabel('Costos')

# Título del gráfico
plt.title('Variación de Costos en 100 y 150 iteraciones')

# Mostrar el gráfico
plt.show()

# Calcular la media
media100 = np.mean(datos100iteraciones)
media150= np.mean(datos150iteraciones)

# Calcular la mediana
mediana100 = np.median(datos100iteraciones)
mediana150 = np.median(datos150iteraciones)

# Calcular la desviación estándar
desviacion_estandar100 = np.std(datos100iteraciones)
desviacion_estandar150 = np.std(datos150iteraciones)

# Imprimir los resultados
print("Media:", media100)
print("Media:", media150)
print("Mediana:", mediana100)
print("Mediana:", mediana150)
print("Desviación Estándar:", desviacion_estandar100)
print("Desviación Estándar:", desviacion_estandar150)
