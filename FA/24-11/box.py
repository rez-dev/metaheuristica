from matplotlib import pyplot as plt


# wi29 = [33201.0, 36972.0, 31844.0, 31123.0, 31123.0, 30187.0, 30560.0, 34409.0, 31123.0, 30187.0, 35332.0, 31844.0, 30187.0, 32858.0, 30187.0, 32814.0, 30187.0, 35216.0, 35108.0, 35332.0, 30804.0]
# dj38 = [7209.0, 6759.0, 6983.0, 6759.0, 6759.0, 6767.0, 7986.0, 8322.0, 6930.0, 7424.0,7986.0, 7706.0, 6760.0, 6758.0, 6850.0, 8289.0, 7424.0, 7209.0, 6792.0, 7942.0,6767.0]
# uy734 = [96210.0, 97358.0, 99462.0, 95207.0, 96075.0, 95132.0, 95095.0, 94609.0, 96197.0, 96277.0, 95396.0, 97306.0, 94441.0, 95678.0, 98600.0, 97859.0, 95993.0, 95371.0, 96719.0, 98583.0, 98699.0]
# zi929 = [114336.0, 118121.0, 111479.0, 114553.0, 113697.0, 118563.0, 118244.0, 113083.0, 116776.0, 117849.0, 111007.0, 110611.0, 117671.0, 114121.0, 118492.0, 112511.0, 111431.0, 112949.0, 117981.0, 119442.0, 119476.0]
# lu980 = [13106.0, 13881.0, 14068.0, 13567.0, 13507.0, 13348.0, 14019.0, 13532.0, 13547.0, 13430.0, 13573.0, 13588.0, 13567.0, 13634.0, 13647.0, 13336.0, 14092.0, 13448.0, 13573.0, 13427.0, 13574.0]

# datos = [wi29, dj38, uy734, zi929, lu980]
# nombres = ["wi29", "dj38", "uy734", "zi929", "lu980"]

# for i in range(len(datos)):
#     plt.figure(figsize=(8, 6))
#     boxprops = dict(color = "lightblue")
#     plt.boxplot(datos[i], patch_artist = True,
#                boxprops = dict(facecolor = "lightblue"))
#     plt.title("Variación 21 ejecuciones " + nombres[i])
#     plt.xlabel("Mejores soluciones")
#     plt.ylabel("Costo de recorrido")
#     plt.grid()
#     plt.xticks([1], [nombres[i]])
#     # plt.savefig("boxplot"+str(i)+".png")
#     plt.show()

# graficar los datos en boxplot
# plt.figure(figsize=(8, 6))
# boxprops = dict(color = "lightblue")
# plt.boxplot(wi29, patch_artist = True,
#            boxprops = dict(facecolor = "lightblue"))
# plt.title("Variación 21 ejecuciones wi29")
# plt.xlabel("Mejores soluciones")
# plt.ylabel("Costo de recorrido")
# plt.grid()
# plt.xticks([1], ["wi29"])
# # plt.savefig("boxplot.png")
# plt.show()


# calcular gaps
wi29 = 27603
dj38 = 6656
uy734 = 79114
zi929 = 95345
lu980 = 11340

wi29_mejor = 30187
wi29_peor = 36972

dj38_mejor = 6758
dj38_peor = 8322

uy734_mejor = 94441
uy734_peor = 99462

zi929_mejor = 110611
zi929_peor = 119476

lu980_mejor = 13106
lu980_peor = 14092

wi29_gap_mejor = (wi29_mejor - wi29) / wi29 * 100
wi29_gap_peor = (wi29_peor - wi29) / wi29 * 100

dj38_gap_mejor = (dj38_mejor - dj38) / dj38 * 100
dj38_gap_peor = (dj38_peor - dj38) / dj38 * 100

uy734_gap_mejor = (uy734_mejor - uy734) / uy734 * 100
uy734_gap_peor = (uy734_peor - uy734) / uy734 * 100

zi929_gap_mejor = (zi929_mejor - zi929) / zi929 * 100
zi929_gap_peor = (zi929_peor - zi929) / zi929 * 100

lu980_gap_mejor = (lu980_mejor - lu980) / lu980 * 100
lu980_gap_peor = (lu980_peor - lu980) / lu980 * 100

print("wi29_gap_mejor: ", wi29_gap_mejor)
print("wi29_gap_peor: ", wi29_gap_peor)
print("dj38_gap_mejor: ", dj38_gap_mejor)
print("dj38_gap_peor: ", dj38_gap_peor)
print("uy734_gap_mejor: ", uy734_gap_mejor)
print("uy734_gap_peor: ", uy734_gap_peor)
print("zi929_gap_mejor: ", zi929_gap_mejor)
print("zi929_gap_peor: ", zi929_gap_peor)
print("lu980_gap_mejor: ", lu980_gap_mejor)
print("lu980_gap_peor: ", lu980_gap_peor)





