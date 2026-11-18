# Bibliotecas
# ============================================================
from OpenGL.GL import *
from OpenGL.GLU import *
import configuraciones as config

def configurar_opengl():
    """Configura la camara, la profundidad y la iluminacion."""
    glMatrixMode(GL_PROJECTION) #Modifica la matriz con la que trabajaremos (Projection = Cámara)
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

    # Registramos la fuente de luz antes de transformar la Luna
    glLightfv(GL_LIGHT0, GL_POSITION, [*config.POSICION_LUZ, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 0.95, 1.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.08, 0.08, 0.1, 1.0])


# 5. Dibujo de la geometria
# ============================================================
def dibujar_esfera_buffer(vertices_np, normales_np, caras_np):
    """Dibuja los triangulos usando vertices, normales e indices."""
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)

    glVertexPointer(3, GL_FLOAT, 0, vertices_np)
    glNormalPointer(GL_FLOAT, 0, normales_np)

    glDrawElements(GL_TRIANGLES, caras_np.size, GL_UNSIGNED_INT, caras_np)

    glDisableClientState(GL_NORMAL_ARRAY)
    glDisableClientState(GL_VERTEX_ARRAY)


def dibujar_luna(vertices_np, normales_np, caras_np):
    """Dibuja la superficie iluminada y despues su malla visible."""
    # Primera pasada: superficie rellena con iluminacion
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glColor3f(0.75, 0.75, 0.78)
    dibujar_esfera_buffer(vertices_np, normales_np, caras_np)

    # Segunda pasada: lineas oscuras sobre la superficie
    glDisable(GL_LIGHTING)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glEnable(GL_POLYGON_OFFSET_LINE)
    glPolygonOffset(-1.0, -1.0)

    glLineWidth(1.0)
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

    # Dibujamos el indicador del Sol sin afectarlo con la iluminacion
    glDisable(GL_LIGHTING)
    glColor3f(1.0, 0.9, 0.2)
    dibujar_esfera_buffer(vertices_np, normales_np, caras_np)
    glEnable(GL_LIGHTING)

    glPopMatrix()
