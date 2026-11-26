# ============================================================
# LUNA 3D - Proyecto Completo Fusionado (Luna sin textura + Malla)
# ============================================================
import math
from pathlib import Path
import numpy as np
import pygame
from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GL import *
from OpenGL.GLU import *


# ============================================================
# 1. CONFIGURACIONES (configuraciones.py)
# ============================================================
DIMENSIONES_VENTANA = (1280, 720)
FPS = 60

# Resolución de la geometría
RADIO_LUNA = 1.5
ANILLOS_LUNA = 4
SEGMENTOS_LUNA = 5

RADIO_SOL = 0.15
ANILLOS_SOL = 16
SEGMENTOS_SOL = 32

# Posición inicial de la Luna y de la fuente de luz
POSICION_INICIAL_Z = -5.0
POSICION_LUZ = (1.0, 0.25, -2.0)

# Sensibilidad y velocidades de los controles
PASO_TRASLACION = 0.2
PASO_ESCALA = 0.1
PASO_SESGO = 0.1
SENSIBILIDAD_ROTACION = 0.5
VELOCIDAD_ROTACION_AUTO = 0.5
VELOCIDAD_ROTACION_SOL = 0.3


# ============================================================
# 2. GEOMETRÍA (geometria.py)
# ============================================================
def esfera_3d(radio, anillos, segmentos):
    """Genera vértices, normales, UVs y triángulos de una esfera."""
    vertices_originales = []
    normales = []
    uvs = []

    for anillo in range(anillos + 1):
        phi = (math.pi * anillo) / anillos
        v = 1.0 - (anillo / anillos)

        for segmento in range(segmentos + 1):
            theta = (2 * math.pi * segmento) / segmentos
            u = segmento / segmentos

            normal_x = math.sin(phi) * math.cos(theta)
            normal_y = math.cos(phi)
            normal_z = math.sin(phi) * math.sin(theta)

            x = radio * normal_x
            y = radio * normal_y
            z = radio * normal_z

            vertices_originales.append((x, y, z))
            normales.append((normal_x, normal_y, normal_z))
            uvs.append((u, v))

    triangulos = []
    for anillo in range(anillos):
        for segmento in range(segmentos):
            a = anillo * (segmentos + 1) + segmento
            b = a + 1
            c = a + (segmentos + 1)
            d = c + 1

            triangulos.append((a, b, d))
            triangulos.append((a, d, c))

    return vertices_originales, normales, uvs, triangulos


def preparar_geometria(radio, anillos, segmentos):
    """Convierte la geometría a arreglos contiguos compatibles con OpenGL."""
    vertices, normales, uvs, caras = esfera_3d(radio, anillos, segmentos)

    vertices_np = np.ascontiguousarray(vertices, dtype=np.float32)
    normales_np = np.ascontiguousarray(normales, dtype=np.float32)
    uvs_np = np.ascontiguousarray(uvs, dtype=np.float32)
    caras_np = np.ascontiguousarray(caras, dtype=np.uint32)

    return vertices_np, normales_np, uvs_np, caras_np


# ============================================================
# 3. TRANSFORMACIONES (transformaciones.py)
# ============================================================
def aplicar_transformaciones(desplazamiento, rotacion, escala, sesgo):
    """Aplica traslación, rotación, escala y sesgo sobre la matriz MODELVIEW."""
    desplazamiento_x, desplazamiento_y, desplazamiento_z = desplazamiento
    rotacion_x, rotacion_y = rotacion
    sesgo_x, sesgo_y = sesgo

    glTranslatef(desplazamiento_x, desplazamiento_y, desplazamiento_z)
    glRotatef(rotacion_x, 1, 0, 0)
    glRotatef(rotacion_y, 0, 1, 0)
    glScalef(escala, escala, escala)

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


# ============================================================
# 4. RENDERIZADO (renderizado.py)
# ============================================================
def cargar_textura(ruta_imagen):
    """Carga una imagen desde disco y la sube a la GPU."""
    ruta_textura = Path(__file__).resolve().parent / ruta_imagen
    superficie = pygame.image.load(str(ruta_textura))
    imagen_bytes = pygame.image.tostring(superficie, "RGBA", True)
    ancho, alto = superficie.get_size()

    textura_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textura_id)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glTexImage2D(
        GL_TEXTURE_2D,
        0,
        GL_RGBA,
        ancho,
        alto,
        0,
        GL_RGBA,
        GL_UNSIGNED_BYTE,
        imagen_bytes,
    )
    glBindTexture(GL_TEXTURE_2D, 0)
    return textura_id


def configurar_opengl():
    """Configura la cámara, la profundidad, la iluminación y las texturas."""
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    relacion_aspecto = DIMENSIONES_VENTANA[0] / DIMENSIONES_VENTANA[1]
    gluPerspective(45, relacion_aspecto, 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glEnable(GL_DEPTH_TEST)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glShadeModel(GL_SMOOTH)

    glEnable(GL_TEXTURE_2D)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

    glLightfv(GL_LIGHT0, GL_POSITION, [*POSICION_LUZ, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 0.95, 1.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.08, 0.08, 0.1, 1.0])


def dibujar_esfera_buffer(vertices_np, normales_np, caras_np, uvs_np=None):
    """Dibuja una malla usando Vertex Arrays de OpenGL."""
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


def dibujar_luna(vertices_np, normales_np, caras_np):
    """Dibuja la Luna SIN textura: cuerpo sólido iluminado + malla wireframe exterior."""
    glDisable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, 0)

    # 1. Esfera sólida gris iluminada por el Sol
    glEnable(GL_POLYGON_OFFSET_FILL)
    glPolygonOffset(1.0, 1.0)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glColor3f(0.55, 0.57, 0.60)
    dibujar_esfera_buffer(vertices_np, normales_np, caras_np, uvs_np=None)
    glDisable(GL_POLYGON_OFFSET_FILL)

    # 2. Malla exterior (wireframe) visible sobre la superficie
    glDisable(GL_LIGHTING)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glLineWidth(1.0)
    glColor3f(0.85, 0.88, 0.95)
    dibujar_esfera_buffer(vertices_np, normales_np, caras_np, uvs_np=None)

    # Restaurar estado base
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glEnable(GL_LIGHTING)
    glEnable(GL_TEXTURE_2D)


def dibujar_sol(vertices_np, normales_np, uvs_np, caras_np, textura_id, rotacion_y=0.0):
    """Dibuja el Sol texturizado con rotación propia."""
    glPushMatrix()
    glTranslatef(*POSICION_LUZ)
    glRotatef(rotacion_y, 0, 1, 0)

    glDisable(GL_LIGHTING)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textura_id)
    glColor3f(1.0, 1.0, 1.0)
    dibujar_esfera_buffer(vertices_np, normales_np, caras_np, uvs_np)
    glBindTexture(GL_TEXTURE_2D, 0)
    glDisable(GL_TEXTURE_2D)
    glEnable(GL_LIGHTING)

    glPopMatrix()


# ============================================================
# 5. ESPACIO / FONDO ESTELAR (espacio.py)
# ============================================================
def generar_estrellas(cantidad=1200, radio=45.0, semilla=42):
    """Genera posiciones 3D y colores aleatorios en una esfera lejana."""
    rng = np.random.default_rng(semilla)
    theta = rng.uniform(0.0, 2.0 * np.pi, cantidad)
    cos_phi = rng.uniform(-1.0, 1.0, cantidad)
    sin_phi = np.sqrt(1.0 - cos_phi ** 2)

    x = radio * sin_phi * np.cos(theta)
    y = radio * cos_phi
    z = radio * sin_phi * np.sin(theta)
    posiciones = np.column_stack((x, y, z)).astype(np.float32)

    brillos = rng.uniform(0.45, 1.0, (cantidad, 1)).astype(np.float32)
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


# ============================================================
# 6. CONTROLES (controles.py)
# ============================================================
def procesar_eventos(estado_luna, estado_mouse):
    """Procesa teclado y ratón para transformar la Luna."""
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return False

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                estado_mouse["presionado"] = True
                estado_mouse["posicion_anterior"] = evento.pos
            elif evento.button == 4:
                estado_luna["factor_escala"] += PASO_ESCALA
            elif evento.button == 5:
                estado_luna["factor_escala"] = max(
                    0.1, estado_luna["factor_escala"] - PASO_ESCALA
                )

        elif evento.type == pygame.MOUSEBUTTONUP:
            if evento.button == 1:
                estado_mouse["presionado"] = False

        elif evento.type == pygame.MOUSEMOTION:
            if estado_mouse["presionado"]:
                x, y = evento.pos
                cambio_x = x - estado_mouse["posicion_anterior"][0]
                cambio_y = y - estado_mouse["posicion_anterior"][1]
                estado_luna["rotacion_x"] += cambio_y * SENSIBILIDAD_ROTACION
                estado_luna["rotacion_y"] += cambio_x * SENSIBILIDAD_ROTACION
                estado_mouse["posicion_anterior"] = (x, y)

        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_a:
                estado_luna["desplazamiento_x"] -= PASO_TRASLACION
            elif evento.key == pygame.K_d:
                estado_luna["desplazamiento_x"] += PASO_TRASLACION
            elif evento.key == pygame.K_w:
                estado_luna["desplazamiento_y"] += PASO_TRASLACION
            elif evento.key == pygame.K_s:
                estado_luna["desplazamiento_y"] -= PASO_TRASLACION
            elif evento.key == pygame.K_q:
                estado_luna["desplazamiento_z"] += PASO_TRASLACION
            elif evento.key == pygame.K_e:
                estado_luna["desplazamiento_z"] -= PASO_TRASLACION
            elif evento.key == pygame.K_g:
                estado_luna["rotacion_automatica"] = not estado_luna["rotacion_automatica"]
            elif evento.key == pygame.K_j:
                estado_luna["sesgo_x"] -= PASO_SESGO
            elif evento.key == pygame.K_l:
                estado_luna["sesgo_x"] += PASO_SESGO
            elif evento.key == pygame.K_i:
                estado_luna["sesgo_y"] += PASO_SESGO
            elif evento.key == pygame.K_k:
                estado_luna["sesgo_y"] -= PASO_SESGO
            elif evento.key == pygame.K_r:
                estado_luna["desplazamiento_x"] = 0.0
                estado_luna["desplazamiento_y"] = 0.0
                estado_luna["desplazamiento_z"] = POSICION_INICIAL_Z
                estado_luna["rotacion_x"] = 0.0
                estado_luna["rotacion_y"] = 0.0
                estado_luna["factor_escala"] = 1.0
                estado_luna["sesgo_x"] = 0.0
                estado_luna["sesgo_y"] = 0.0
                estado_luna["rotacion_automatica"] = False

    return True


# ============================================================
# 7. PROGRAMA PRINCIPAL (main.py)
# ============================================================
def main():
    pygame.init()
    pygame.display.set_mode(DIMENSIONES_VENTANA, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Luna 3D - Solido e iluminacion")
    configurar_opengl()

    # Solo cargamos la textura del Sol (la Luna va sin textura y con malla)
    textura_sol = cargar_textura("sol_texture.jpg")

    vertices_luna, normales_luna, _, caras_luna = preparar_geometria(
        RADIO_LUNA, ANILLOS_LUNA, SEGMENTOS_LUNA
    )
    vertices_sol, normales_sol, uvs_sol, caras_sol = preparar_geometria(
        RADIO_SOL, ANILLOS_SOL, SEGMENTOS_SOL
    )

    estado_luna = {
        "desplazamiento_x": 0.0,
        "desplazamiento_y": 0.0,
        "desplazamiento_z": POSICION_INICIAL_Z,
        "rotacion_x": 0.0,
        "rotacion_y": 0.0,
        "factor_escala": 1.0,
        "sesgo_x": 0.0,
        "sesgo_y": 0.0,
        "rotacion_automatica": False,
    }

    estado_mouse = {"presionado": False, "posicion_anterior": (0, 0)}

    pos_estrellas, col_estrellas = generar_estrellas(cantidad=1200, radio=45.0)
    rotacion_sol_y = 0.0

    reloj = pygame.time.Clock()
    ejecutando = True

    while ejecutando:
        ejecutando = procesar_eventos(estado_luna, estado_mouse)
        if not ejecutando:
            break

        if estado_luna["rotacion_automatica"]:
            estado_luna["rotacion_y"] = (
                estado_luna["rotacion_y"] + VELOCIDAD_ROTACION_AUTO
            ) % 360.0

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # 1. Fondo espacial
        dibujar_estrellas(pos_estrellas, col_estrellas)

        # 2. Luna sin textura + malla exterior
        glPushMatrix()
        aplicar_transformaciones(
            (
                estado_luna["desplazamiento_x"],
                estado_luna["desplazamiento_y"],
                estado_luna["desplazamiento_z"],
            ),
            (estado_luna["rotacion_x"], estado_luna["rotacion_y"]),
            estado_luna["factor_escala"],
            (estado_luna["sesgo_x"], estado_luna["sesgo_y"]),
        )
        dibujar_luna(vertices_luna, normales_luna, caras_luna)
        glPopMatrix()

        # 3. Sol texturizado con rotación propia
        rotacion_sol_y = (rotacion_sol_y + VELOCIDAD_ROTACION_SOL) % 360.0
        dibujar_sol(
            vertices_sol, normales_sol, uvs_sol, caras_sol, textura_sol, rotacion_sol_y
        )

        pygame.display.flip()
        reloj.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()