from matplotlib import pyplot as plt
import numpy as np

# datos100iteraciones = [93343, 11100, 10750, 11153, 10817, 10920, 11506, 10820, 10880, 10746, 10536, 10297, 11211, 11357, 10636, 11403, 10874, 10798, 10441, 10528, 10816, 10525, 10686, 11017, 10512, 10149, 11204, 10425, 10896, 10479, 10600, 11145, 10149]
datos150iteraciones = [10295, 10579, 10692, 11360, 10756, 10425, 11300, 11122, 11058, 11178, 10807, 11175, 11377, 10927, 11778, 10824, 10882, 10334, 10348, 11539, 11294, 11428, 11182, 10966, 11159, 10527, 10962, 10958, 11008, 10435, 10664, 10295]
datos100iteraciones = [10899, 11166, 10805, 10215, 10030, 11395, 10803, 10889, 11165, 11334, 10676, 11560, 11151, 11424, 10775, 10942, 11587, 11127, 10903, 11272, 10489, 10649, 10548, 10522, 11157, 10901, 11252, 10297, 10909, 10696, 10237]

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

mediana100 = np.median(datos100iteraciones)
mediana150 = np.median(datos150iteraciones)
print(mediana100)
print(mediana150)

# Crear un diagrama de cajas
# Crear un diagrama de cajas para la serie 1
# plt.boxplot(datos100iteraciones, positions=[1], widths=0.6, patch_artist=True, boxprops=dict(facecolor="blue"))
# # Crear un diagrama de cajas para la serie 2
# plt.boxplot(datos150iteraciones, positions=[2], widths=0.6, patch_artist=True, boxprops=dict(facecolor="green"))
# plt.xticks([1, 2], ['100 iteraciones', '150 iteraciones'])

# # Etiquetas para los ejes
# plt.xlabel('Iteraciones')
# plt.ylabel('Costos')

# # Título del gráfico
# plt.title('Comparación iteraciones v/s costos')

# # Mostrar el gráfico
# plt.show()
