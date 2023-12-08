from scipy import stats
import numpy as np

# Generar datos de ejemplo (reemplaza esto con tus propios datos)
# np.random.seed(0)
# datos_ejemplo = np.random.normal(loc=0, scale=1, size=100)
datos_random_3 = [77408.0,78486.0,76720.0,78829.0,78174.0,80554.0,79432.0,77212.0,77839.0,79041.0,78822.0,76437.0,78494.0,77596.0,78238.0,79028.0,78640.0,80783.0,78448.0,81496.0,77805.0]
# print(len(datos_random_3))

datos_random_5 = [86940.0,87402.0,87714.0,86982.0,90453.0,87475.0,86984.0,86772.0,89366.0,88523.0,87490.0,88229.0,88276.0,88877.0,87349.0,90893.0,87730.0,88551.0,87983.0,88029.0,88845.0]


# # Prueba de Shapiro-Wilk para verificar normalidad
# resultado_shapiro, p_valor_shapiro = stats.shapiro(datos_random_5)
# print("Prueba de Shapiro-Wilk:")
# print(f"Estadístico de prueba: {resultado_shapiro}")
# print(f"P-valor: {p_valor_shapiro}")

# # Prueba de Kolmogorov-Smirnov para verificar normalidad
# resultado_ks, p_valor_ks = stats.kstest(datos_random_5, 'norm')
# print("\nPrueba de Kolmogorov-Smirnov:")
# print(f"Estadístico de prueba: {resultado_ks}")
# print(f"P-valor: {p_valor_ks}")

from scipy import stats

def prueba_mann_whitney(datos1, datos2):
    """
    Realiza la prueba de Mann-Whitney U para comparar dos muestras independientes.

    Argumentos:
    datos1: Una lista o array que contiene el primer conjunto de datos.
    datos2: Una lista o array que contiene el segundo conjunto de datos.

    Retorna:
    U_statistic: Estadístico U de la prueba de Mann-Whitney.
    p_valor: Valor p correspondiente a la prueba.
    """
    U_statistic, p_valor = stats.mannwhitneyu(datos1, datos2)
    return U_statistic, p_valor

estadistico_U, valor_p = prueba_mann_whitney(datos_random_3, datos_random_5)
print(f"Estadístico U: {estadistico_U}")
print(f"Valor p: {valor_p}")
