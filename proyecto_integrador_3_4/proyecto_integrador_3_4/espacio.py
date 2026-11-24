# Bibliotecas
# ============================================================
import numpy as np
from OpenGL.GL import *
from geometria import preparar_geometria
import renderizado as render


def generar_estrellas(cantidad=5000, radio=45.0, semilla=42):
    """Genera posiciones 3D y colores aleatorios en una esfera lejana."""
    rng = np.random.default_rng(semilla)
    theta = rng.uniform(0.0, 2.0 * np.pi, cantidad)
    cos_phi = rng.uniform(-1.0, 1.0, cantidad)
    sin_phi = np.sqrt(1.0 - cos_phi ** 2)

    x = radio * sin_phi * np.cos(theta)
    y = radio * cos_phi
    z = radio * sin_phi * np.sin(theta)
    posiciones = np.column_stack((x, y, z)).astype(np.float32)

    # Tonos entre blanco cálido y blanco azulado con distinto brillo
    brillos = rng.uniform(0.80, 1.0, (cantidad, 1)).astype(np.float32)
    colores = np.hstack(
        (brillos, brillos, np.clip(brillos * 1.12, 0.0, 1.0))
    ).astype(np.float32)

    return np.ascontiguousarray(posiciones), np.ascontiguousarray(colores)


def dibujar_estrellas(posiciones_np, colores_np, tamano=2.0):
    """Dibuja las estrellas al fondo sin afectar profundidad ni iluminación."""
    glPushAttrib(GL_ENABLE_BIT | GL_POINT_BIT | GL_DEPTH_BUFFER_BIT)
    glDisable(GL_LIGHTING)
    glDisable(GL_TEXTURE_2D)
    glDepthMask(GL_FALSE)
    glPointSize(tamano)

    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_COLOR_ARRAY)

    glVertexPointer(3, GL_FLOAT, 0, posiciones_np)
    glColorPointer(3, GL_FLOAT, 0, colores_np)
    glDrawArrays(GL_POINTS, 0, len(posiciones_np))

    glDisableClientState(GL_COLOR_ARRAY)
    glDisableClientState(GL_VERTEX_ARRAY)
    glPopAttrib()


def preparar_skydome(ruta_textura, radio=50.0, anillos=32, segmentos=64):
    """Crea la esfera envolvente y carga la textura del fondo espacial."""
    textura_id = render.cargar_textura(ruta_textura)
    vertices, normales, uvs, caras = preparar_geometria(radio, anillos, segmentos)
    return vertices, normales, uvs, caras, textura_id


def dibujar_skydome(vertices_np, normales_np, uvs_np, caras_np, textura_id):
    """Dibuja la esfera envolvente del espacio en el fondo de la escena."""
    glPushAttrib(GL_ENABLE_BIT | GL_DEPTH_BUFFER_BIT)
    glDisable(GL_LIGHTING)
    glDepthMask(GL_FALSE)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textura_id)
    glColor3f(1.0, 1.0, 1.0)

    render.dibujar_esfera_buffer(vertices_np, normales_np, caras_np, uvs_np)

    glBindTexture(GL_TEXTURE_2D, 0)
    glPopAttrib()