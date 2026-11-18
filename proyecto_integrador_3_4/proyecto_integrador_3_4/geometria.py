import math
import numpy as np

# 3. Generacion de geometria
# ============================================================
def esfera_3d(radio, anillos, segmentos):
    """Genera vertices, normales y triangulos de una esfera."""
    vertices_originales = []
    normales = []

    # Primero calculamos la posicion y la normal de cada vertice
    for anillo in range(anillos + 1):
        phi = (math.pi * anillo) / anillos

        for segmento in range(segmentos + 1):
            theta = (2 * math.pi * segmento) / segmentos

            # La normal apunta hacia afuera de la esfera
            normal_x = math.sin(phi) * math.cos(theta)
            normal_y = math.cos(phi)
            normal_z = math.sin(phi) * math.sin(theta)

            x = radio * normal_x
            y = radio * normal_y
            z = radio * normal_z

            vertices_originales.append((x, y, z))
            normales.append((normal_x, normal_y, normal_z))

    # Despues conectamos los vertices para construir la malla
    triangulos = []

    for anillo in range(anillos):
        for segmento in range(segmentos):
            a = anillo * (segmentos + 1) + segmento
            b = a + 1
            c = a + (segmentos + 1)
            d = c + 1

            triangulos.append((a, b, d))
            triangulos.append((a, d, c))

    return vertices_originales, normales, triangulos


def preparar_geometria(radio, anillos, segmentos):
    """Convierte la geometria a arreglos compatibles con OpenGL."""
    vertices, normales, caras = esfera_3d(radio, anillos, segmentos)

    vertices_np = np.ascontiguousarray(vertices, dtype=np.float32)
    normales_np = np.ascontiguousarray(normales, dtype=np.float32)
    caras_np = np.ascontiguousarray(caras, dtype=np.uint32)

    return vertices_np, normales_np, caras_np
