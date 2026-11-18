# Biblioteca
# ============================================================
from OpenGL.GL import *

def aplicar_transformaciones(desplazamiento, rotacion, escala, sesgo):
    """Aplica las transformaciones de la Luna sobre la matriz actual."""
    desplazamiento_x, desplazamiento_y, desplazamiento_z = desplazamiento
    rotacion_x, rotacion_y = rotacion
    sesgo_x, sesgo_y = sesgo

    glTranslatef(desplazamiento_x, desplazamiento_y, desplazamiento_z)
    glRotatef(rotacion_x, 1, 0, 0)
    glRotatef(rotacion_y, 0, 1, 0)
    glScalef(escala, escala, escala)

    # OpenGL recibe estos 16 valores en orden por columnas
    matriz_sesgo = (
        1.0,
        0.0,
        0.0,
        0.0,
        0.0,
        1.0,
        0.0,
        0.0,
        sesgo_x,
        sesgo_y,
        1.0,
        0.0,
        0.0,
        0.0,
        0.0,
        1.0,
    )
    glMultMatrixf(matriz_sesgo)
