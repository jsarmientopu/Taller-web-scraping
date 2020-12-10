from bs4 import BeautifulSoup
from urllib.request import urlopen

def info_pag(texto):
    lineas = [linea for linea in texto.split('\n') if linea != '']
    bandera = False

    listo = []
    for i in lineas:
        if i == 'Blue paradise':
            listo.append(i.strip())
            bandera = True
        elif i == ' Añadir a la cesta' or i == 'Cantidad:' or 'Libro impreso' in i or i == 'Autor:'or 'Ebook (epub):' in i or i == 'Agotado':
            continue
        elif i == '← Anterior':
            bandera = False
        elif bandera:
            listo.append(i.strip())


    libros = []
    libro = {}
    for elemento in listo:
        if ':' not in elemento:
            if len(elemento) <= 0:
                if len(libro) == 6:
                    libro_ordenado = []
                    for d in libro.keys():
                        if d == 'Descripcion':
                            continue
                        libro_ordenado.append(libro[d])
                    libros.append(libro_ordenado)
                    libro = {}
                else:
                    continue
            elif len(libro) == 0:
                libro['nombre'] = elemento.strip()
            elif len(libro) == 1:
                libro['autor'] = elemento.strip()
            elif len(libro) == 5:
                libro['Descripcion'] = elemento
            else:
                continue
        elif len(libro) == 5:
            libro['Descripcion'] = elemento
        else:
            elemento = elemento.split(':')
            libro [elemento[0].strip()] = elemento[1].strip()

    return libros

def comprobar(libros_pagina):
    libros_archivo = []
    archivo = open("../archivos/ejemplo.txt", "r")
    lines = archivo.readlines()
    for line in lines:
        datos = line.split(',')
        libros_archivo.append(datos)
    archivo.close()

    libros_falta= []
    for indice in range(len(libros_pagina)):
        bandera = False
        for libro_archivo in libros_archivo:
            if libros_pagina[indice][0] == libro_archivo[0]:
                bandera = True
        if bandera == False:
            libros_falta.append(libros_pagina[indice])

    return libros_falta


def main():
    url = "https://editorialamarante.es/libros"
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    texto = soup.get_text()
    libros_pagina = info_pag(texto)
    libros = comprobar(libros_pagina)
    print(libros)
    archivo = open("../archivos/ejemplo.txt", "a")
    for libro in libros:
        libro.insert(1, '0')
        libro = ','.join(libro)
        archivo.write(libro + '\n')
    archivo.close()

main()