luciernaga_i = [6, 7, 8, 4, 2, 1, 5, 15, 12, 3, 16, 11, 9, 10, 13, 14]
nodos_x = [8, 4, 2]
nodos_y = [3, 16, 11, 9, 10]

# Definir las posiciones x e y
x = 4
y = 9

# Eliminar elementos de nodos_x y nodos_y de luciernaga_i
for i in nodos_x:
    luciernaga_i.remove(i)
for j in nodos_y:
    luciernaga_i.remove(j)

# Insertar nodos_x en la posición x
for i in range(len(nodos_x)):
    luciernaga_i.insert(x + i, nodos_x[i])

# Insertar nodos_y en la posición y
for i in range(len(nodos_y)):
    luciernaga_i.insert(y + i, nodos_y[i])

# Crear las soluciones firefly_i1, firefly_i2, firefly_i3, firefly_i4
firefly_i1 = luciernaga_i[:]
firefly_i2 = luciernaga_i[:]
firefly_i3 = luciernaga_i[:]
firefly_i4 = luciernaga_i[:]

# Intercambiar los elementos en las posiciones específicas para firefly_i2, firefly_i3 y firefly_i4
firefly_i2[x:y + len(nodos_x)] = nodos_y
firefly_i3[x:y + len(nodos_x)] = nodos_y[::-1]
firefly_i4[y:y + len(nodos_y)] = nodos_x

# Mostrar los resultados
print("firefly_i1:", firefly_i1)
print("firefly_i2:", firefly_i2)
print("firefly_i3:", firefly_i3)
print("firefly_i4:", firefly_i4)
