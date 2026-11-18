cubo = {"x": 0.0, "y": 0.0, "z": 0.0}


def mover(diccionario, dx, dy, dz):
    diccionario["x"] += dx
    diccionario["y"] += dy
    diccionario["z"] += dz


mover(cubo, 2, 3, -1)

print(cubo)