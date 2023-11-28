from scipy import stats

# Resultados de los dos programas
modificado = [
    13106.0,
    13881.0,
    14068.0,
    13567.0,
    13507.0,
    13348.0,
    14019.0,
    13532.0,
    13547.0,
    13430.0,
    13573.0,
    13588.0,
    13567.0,
    13634.0,
    13647.0,
    13336.0,
    14092.0,
    13448.0,
    13573.0,
    13427.0,
    13574.0
]

original = [
    13436.0, 14133.0, 14269.0, 13895.0, 13760.0, 14011.0, 14358.0, 13863.0, 
    13803.0, 13651.0, 13839.0, 13892.0, 13749.0, 13868.0, 13974.0, 14014.0, 
    14249.0, 13960.0, 13877.0, 13750.0, 13860.0
]


# programa_2 = [/* inserta aquí los 21 resultados del segundo programa */]

# Realizar la prueba t de Student
t_statistic, p_value = stats.ttest_ind(modificado, original)

# Imprimir los resultados
print("Estadística t:", t_statistic)
print("Valor p:", p_value)

# Interpretación del resultado
alpha = 0.05  # Nivel de significancia
if p_value < alpha:
    print("Se rechaza la hipótesis nula. Hay evidencia significativa de diferencia entre las medias.")
else:
    print("No se puede rechazar la hipótesis nula. No hay suficiente evidencia para afirmar que hay diferencia entre las medias.")
