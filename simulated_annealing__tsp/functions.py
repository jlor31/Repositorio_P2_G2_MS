def read_file(filename):
    """
        Funcion para leer el archivo de coordenadas
    """
    file = open(filename, "r", encoding="utf-8")
    lines = [tuple(map(float, n.split(' '))) for n in file.readlines()]
    file.close()
    return lines
    