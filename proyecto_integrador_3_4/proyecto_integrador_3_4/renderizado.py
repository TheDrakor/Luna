# Bibliotecas
# ============================================================
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import configuraciones as config
from pathlib import Path

def cargar_textura(ruta_imagen):
    """Carga una imagen con Pygame y la sube como textura 2D a OpenGL."""
    ruta_completa = Path(__file__).resolve().parent / ruta_imagen

    superficie = pygame.image.load(str(ruta_completa))
    imagen_bytes = pygame.image.tostring(superficie, "RGBA", True)
    ancho, alto = superficie.get_size()

    textura_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textura_id)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glTexImage2D(
        GL_TEXTURE_2D, 0, GL_RGBA, ancho, alto, 0,
        GL_RGBA, GL_UNSIGNED_BYTE, imagen_bytes
    )
    glBindTexture(GL_TEXTURE_2D, 0)
    return textura_id


def configurar_opengl():
    """Configura la camara, la profundidad y la iluminacion."""
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    relacion_aspecto = config.DIMENSIONES_VENTANA[0] / config.DIMENSIONES_VENTANA[1]
    gluPerspective(45, relacion_aspecto, 0.1, 20.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glEnable(GL_DEPTH_TEST)

    # Activamos el sistema de iluminacion de OpenGL
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glShadeModel(GL_SMOOTH)

    # Configuracion de texturas 2D moduladas con la luz
    glEnable(GL_TEXTURE_2D)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

    # Registramos la fuente de luz antes de transformar la Luna
    glLightfv(GL_LIGHT0, GL_POSITION, [*config.POSICION_LUZ, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 0.95, 1.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.08, 0.08, 0.1, 1.0])


# 5. Dibujo de la geometria
# ============================================================
def dibujar_esfera_buffer(vertices_np, normales_np, caras_np, uvs_np=None):
    """Dibuja los triangulos usando vertices, normales, UVs e indices."""
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)

    glVertexPointer(3, GL_FLOAT, 0, vertices_np)
    glNormalPointer(GL_FLOAT, 0, normales_np)

    if uvs_np is not None:
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glTexCoordPointer(2, GL_FLOAT, 0, uvs_np)

    glDrawElements(GL_TRIANGLES, caras_np.size, GL_UNSIGNED_INT, caras_np)

    if uvs_np is not None:
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)

    glDisableClientState(GL_NORMAL_ARRAY)
    glDisableClientState(GL_VERTEX_ARRAY)


def dibujar_luna(vertices_np, normales_np, uvs_np, caras_np, textura_id):
    """Dibuja la superficie texturizada e iluminada y despues su malla visible."""
    # Primera pasada: superficie rellena con textura e iluminacion
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textura_id)
    glColor3f(1.0, 1.0, 1.0)
    dibujar_esfera_buffer(vertices_np, normales_np, caras_np, uvs_np)
    glBindTexture(GL_TEXTURE_2D, 0)

    glColor3f(0.15, 0.15, 0.2)
    dibujar_esfera_buffer(vertices_np, normales_np, caras_np)

    # Restauramos los estados que necesita el resto de la escena
    glDisable(GL_POLYGON_OFFSET_LINE)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glEnable(GL_LIGHTING)


def dibujar_sol(vertices_np, normales_np, caras_np):
    """Muestra una esfera amarilla en la posicion de la luz."""
    glPushMatrix()
    glTranslatef(*config.POSICION_LUZ)

    # Dibujamos el indicador del Sol sin textura ni iluminacion
    glDisable(GL_TEXTURE_2D)
    glDisable(GL_LIGHTING)
    glColor3f(1.0, 0.9, 0.2)
    dibujar_esfera_buffer(vertices_np, normales_np, caras_np)
    glEnable(GL_LIGHTING)

    glPopMatrix()