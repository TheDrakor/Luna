# Biblioteca
# ============================================================
from OpenGL.GL import *

# ============================================================
# [TRANSFORMACIONES] Pipeline de modelado (Espacio Local -> Mundo)
# ============================================================
def aplicar_transformaciones(desplazamiento, rotacion, escala, sesgo):
    """
    Aplica las transformaciones afines de la Luna sobre la matriz MODELVIEW actual
    en orden jerárquico: Traslación -> Rotación -> Escala -> Sesgo.
    """
    desplazamiento_x, desplazamiento_y, desplazamiento_z = desplazamiento
    rotacion_x, rotacion_y = rotacion
    sesgo_x, sesgo_y = sesgo

    # [TRANSFORMACIÓN - TRASLACIÓN] Desplaza el centro del objeto en los ejes X, Y, Z
    glTranslatef(desplazamiento_x, desplazamiento_y, desplazamiento_z)
    # [TRANSFORMACIÓN - ROTACIÓN] Gira el objeto sobre sus ejes locales X (inclinación) e Y (giro)
    glRotatef(rotacion_x, 1, 0, 0)
    glRotatef(rotacion_y, 0, 1, 0)
    # [TRANSFORMACIÓN - ESCALA] Redimensiona uniformemente la geometría
    glScalef(escala, escala, escala)

    # [TRANSFORMACIÓN - SESGO / SHEAR] Matriz 4x4 personalizada para inclinar los ejes X e Y respecto a Z
    # OpenGL recibe estos 16 valores en orden por columnas (column-major)
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