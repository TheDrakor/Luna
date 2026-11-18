import pygame
from OpenGL.GL import *

DIMENSIONES_VENTANA = (1280, 720)
FPS = 60

# Resolucion de la geometria
RADIO_LUNA = 1.5
ANILLOS_LUNA = 32
SEGMENTOS_LUNA = 64

RADIO_SOL = 0.15
ANILLOS_SOL = 16
SEGMENTOS_SOL = 32

# Posicion inicial de la Luna y de la fuente de luz
POSICION_INICIAL_Z = -5.0
POSICION_LUZ = (1.40, 0.80, -2.0)

# Sensibilidad de los controles
PASO_TRASLACION = 0.2
PASO_ESCALA = 0.1
PASO_SESGO = 0.1
SENSIBILIDAD_ROTACION = 0.5



def cargar_textura(ruta_imagen):
    # Cargar imagen y voltear en Y para coincidir con el origen (0,0) inferior izquierdo de OpenGL
    superficie = pygame.image.load("C:\Users\chimi\OneDrive\Desktop\Vscode_Projets\proyecto_integrador_3_4\proyecto_integrador_3_4")
    imagen_bytes = pygame.image.tostring(superficie, "RGBA", True)
    ancho, alto = superficie.get_size()

    textura_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textura_id)

    # Configurar wrapping (repetición en U y V) y filtrado suave
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # Subir datos a la GPU
    glTexImage2D(
        GL_TEXTURE_2D, 0, GL_RGBA, ancho, alto, 0,
        GL_RGBA, GL_UNSIGNED_BYTE, imagen_bytes
    )
    glBindTexture(GL_TEXTURE_2D, 0)
    return textura_id