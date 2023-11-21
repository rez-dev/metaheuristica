def swap_distance(arr1, arr2):
    if len(arr1) != len(arr2):
        raise ValueError("Los arreglos deben tener la misma longitud")

    # Creamos un diccionario para almacenar el índice de cada elemento en el segundo arreglo
    index_map = {val: i for i, val in enumerate(arr2)}
    
    distance = 0
    for i in range(len(arr1)):
        if arr1[i] != arr2[i]:
            # Buscamos el índice del elemento en arr2 que corresponde al elemento en arr1[i]
            idx = index_map[arr1[i]]
            
            # Intercambiamos los elementos en arr2 para que coincidan con arr1
            arr2[i], arr2[idx] = arr2[idx], arr2[i]
            
            # Actualizamos el índice del elemento movido en arr2
            index_map[arr2[idx]] = idx
            
            # Incrementamos la distancia
            distance += 1

    return distance

# Ejemplo de uso:
array1 = [1,2,3,4,5,6]
array2 = [1,2,4,5,6,3]
# array1 = [1,14,13,12,7,6,15,5,11,9,10,16,3,2,4,8]
# array2 = [1,14,13,12,15,5,7,6,11,9,10,16,3,2,4,8]

resultado = swap_distance(array1, array2)
print("La distancia de intercambio entre los arreglos es:", resultado)
