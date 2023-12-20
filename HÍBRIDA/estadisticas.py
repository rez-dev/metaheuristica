# import numpy as np
# import scikit_posthocs as sp
# from scipy.stats import kruskal

# def run_dunn_test(data_groups, group_labels):
#     """
#     Realiza la prueba de Kruskal-Wallis seguida por la prueba post-hoc de Dunn.

#     :param data_groups: Lista de listas, donde cada sublista contiene los datos de un grupo.
#     :param group_labels: Lista de etiquetas para los grupos.
#     :return: Resultados de la prueba de Dunn.
#     """
#     # Primero, realiza la prueba de Kruskal-Wallis
#     stat, p = kruskal(*data_groups)
#     print(f"Kruskal-Wallis Test: H={stat}, p={p}")

#     # Si Kruskal-Wallis es significativo, procede con Dunn
#     if p < 0.05:
#         print("\nRealizando la prueba post-hoc de Dunn...")
#         dunn_result = sp.posthoc_dunn(data_groups, p_adjust='holm')
#         # Formatear los resultados para mejor visualización
#         dunn_result.columns = group_labels
#         dunn_result.index = group_labels
#         return dunn_result
#     else:
#         print("\nNo hay diferencias significativas según Kruskal-Wallis. No se realiza Dunn.")
#         return None

# # Ejemplo de uso
# gls_data = [26856.0, 28583.0, 27748.0, 28360.0, 27282.0, 26444.0, 26772.0, 27086.0, 26961.0, 27506.0, 27026.0, 28087.0, 27820.0, 26924.0, 27771.0, 27470.0, 26696.0, 27127.0, 27455.0, 27813.0, 27357.0]
# fa_data = [28242.0,30998.0,29024.0,28652.0,29902.0,27756.0,28048.0,28878.0,28471.0,28664.0,27914.0,28184.0,29020.0,28648.0,27878.0,28933.0,28003.0,28562.0,29011.0,28194.0,28457.0]
# hybrid_data = [27376.0, 27306.0, 26527.0, 28211.0, 27289.0, 27032.0, 27270.0, 27481.0, 28432.0, 27395.0, 27672.0, 27450.0, 27136.0, 27496.0, 26842.0, 27108.0, 27233.0, 27268.0, 26973.0, 27246.0, 27485.0]

# # Etiquetas para tus grupos
# labels = ["GLS", "FA", "HYBRID"]

# # Llamada a la función
# dunn_results = run_dunn_test([gls_data, fa_data, hybrid_data], labels)

# # Imprimir resultados si están disponibles
# if dunn_results is not None:
#     print("\nResultados de la prueba de Dunn:")
#     print(dunn_results)

kroB150 = [26856.0, 28583.0, 27748.0, 28360.0, 27282.0, 26444.0, 26772.0, 27086.0, 26961.0, 27506.0, 27026.0, 28087.0, 27820.0, 26924.0, 27771.0, 27470.0, 26696.0, 27127.0, 27455.0, 27813.0, 27357.0]
print(min(kroB150))