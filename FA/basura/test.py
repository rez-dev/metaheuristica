# def contar_aristas_distintas(ruta1, ruta2):
#     aristas_ruta1 = set(zip(ruta1[:-1], ruta1[1:]))
#     aristas_ruta2 = set(zip(ruta2[:-1], ruta2[1:]))
    
#     aristas_distintas = aristas_ruta2 - aristas_ruta1
    
#     return len(aristas_distintas)

# # ruta1 = [1, 14, 13, 12, 7, 6, 15, 5, 11, 9, 10, 16, 3, 2, 4, 8]
# # ruta2 = [1, 14, 13, 12, 15, 5, 7, 6, 11, 9, 10, 16, 3, 2, 4, 8]
# ruta1 = [1, 14, 13, 12, 3, 2, 4, 8]
# ruta2 = [1, 14, 13, 12, 2, 3, 4, 8]

# diferencia_aristas = contar_aristas_distintas(ruta1, ruta2)
# print(f"La diferencia en aristas es: {diferencia_aristas}")


def contar_aristas_distintas(ruta1, ruta2):
    aristas_ruta1 = set(zip(ruta1[:-1], ruta1[1:]))
    aristas_ruta1_inversas = set(zip(ruta1[1:], ruta1[:-1]))
    
    aristas_ruta2 = set(zip(ruta2[:-1], ruta2[1:]))
    aristas_ruta2_inversas = set(zip(ruta2[1:], ruta2[:-1]))
    
    aristas_distintas_directas = (aristas_ruta2 - aristas_ruta1) | (aristas_ruta1 - aristas_ruta2)
    aristas_distintas_inversas = (aristas_ruta2_inversas - aristas_ruta1_inversas) | (aristas_ruta1_inversas - aristas_ruta2_inversas)
    
    return len(aristas_distintas_directas) + len(aristas_distintas_inversas)

ruta1 = [1, 14, 13, 12, 3, 2, 4, 8]
ruta2 = [1, 14, 13, 12, 2, 3, 4, 8]

diferencia_aristas = contar_aristas_distintas(ruta1, ruta2)
print(f"La diferencia en aristas es: {diferencia_aristas}")



