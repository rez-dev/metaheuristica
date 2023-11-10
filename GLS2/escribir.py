def escribir_en_archivo(arreglo, nombre_archivo, nombre_entrada):
    try:
        with open(nombre_archivo, 'a') as archivo:
            archivo.write("### " + nombre_entrada + " ###" + '\n')
            archivo.write(str(arreglo) + '\n\n')
                
        print(f"El arreglo se ha escrito exitosamente en {nombre_archivo}.")
    except Exception as e:
        print(f"Error al escribir en el archivo: {e}")

# Ejemplo de uso:
mi_arreglo = [1, 2, 3, 4, 5]
nombre_del_archivo = 'texto.txt'

escribir_en_archivo(mi_arreglo, nombre_del_archivo, "dj38")
