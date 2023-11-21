def swap_distance(arr1, arr2):
    # Verificar si los arreglos tienen la misma longitud
    if len(arr1) != len(arr2):
        raise ValueError("Los arreglos deben tener la misma longitud")

    # Crear un diccionario para mapear elementos del arr2 a sus índices
    index_map = {element: i for i, element in enumerate(arr2)}

    # Inicializar la distancia de intercambio
    distance = 0

    # Iterar sobre el primer arreglo
    for i in range(len(arr1)):
        # Verificar si el elemento en la posición i del arr1 es diferente al arr2
        if arr1[i] != arr2[i]:
            # Incrementar la distancia de intercambio
            distance += 1

            # Encontrar la posición del elemento en arr2 que debería estar en la posición i de arr1
            correct_index = index_map[arr1[i]]

            # Intercambiar los elementos en las posiciones i y correct_index de arr1
            arr1[i], arr1[correct_index] = arr1[correct_index], arr1[i]

            # Actualizar el diccionario de mapeo para reflejar el intercambio
            index_map[arr1[correct_index]] = correct_index
            index_map[arr1[i]] = i

    return distance

# Ejemplo de uso
# arr1 = [1, 2, 3, 4, 5, 6]
# # arr2 = [1, 2, 4, 3, 6, 5]
# arr2 = [1, 2, 4, 5, 6, 3]
arr1 = [1, 14, 13, 12, 3, 2, 4, 8]
arr2 = [1, 14, 13, 12, 2, 3, 4, 8]
resultado = swap_distance(arr1, arr2)
print(f"La swap distance entre los arreglos es: {resultado}")
