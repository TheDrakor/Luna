import pygame
from OpenGL.GL import *
from pathlib import Path

DIMENSIONES_VENTANA = (1280, 720)
FPS = 60

# [GEOMETRÍA] Resolución de la malla esférica (radio, anillos horizontales y segmentos verticales)
RADIO_LUNA = 1.5
ANILLOS_LUNA = 32
SEGMENTOS_LUNA = 64

RADIO_SOL = 0.15
ANILLOS_SOL = 16
SEGMENTOS_SOL = 32

# [TRANSFORMACIONES E ILUMINACIÓN] Posición inicial en el espacio 3D y coordenadas de la luz puntual
POSICION_INICIAL_Z = -5.0
#              (  x,    y,   z )
POSICION_LUZ = (1.50, 0.25, -3.0)

# Sensibilidad y velocidades para las transformaciones interactivas y automáticas
PASO_TRASLACION = 0.2
PASO_ESCALA = 0.1
PASO_SESGO = 0.1
SENSIBILIDAD_ROTACION = 0.5
VELOCIDAD_ROTACION_AUTO = 0.5
VELOCIDAD_ROTACION_SOL = 0.3


def cargar_textura(ruta_imagen):
    # [TEXTURAS - CARGA EN MEMORIA]
    # Cargar imagen y voltear en Y (True) para coincidir con el origen (0,0) inferior izquierdo de OpenGL
    ruta_textura = Path(__file__).resolve().parent / ruta_imagen
    superficie = pygame.image.load(str(ruta_textura))
    imagen_bytes = pygame.image.tostring(superficie, "RGBA", True)
    ancho, alto = superficie.get_size()

    # [TEXTURAS - RESERVA EN GPU] Genera un identificador de textura en VRAM y lo enlaza
    textura_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textura_id)

    # [TEXTURAS - WRAPPING (ENVOLTURA)]
    # T y S equivalen a las coordenadas U y V
    # GL_TEXTURE_2D: Configurando una textura bidimensional plana
    # GL_REPEAT: Repite la imagen en los bordes para cerrar sin cortes la unión alrededor de la esfera
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
   
    # [TEXTURAS - FILTRADO DE ESCALA]
    """Define cuando la esfera se ve lejos o pequeña en pantalla,
    por lo que varios texeles deben comprimirse en un solo píxel, GL_LINEAR nos sirve para suavizar
    los pixeles vecinos cuando se aumente o disminuye el tamaño"""
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # [TEXTURAS - TRANSFERENCIA A GPU] Sube la matriz de píxeles RGBA a la memoria de video
    glTexImage2D(
        GL_TEXTURE_2D, 0, GL_RGBA, ancho, alto, 0,
        GL_RGBA, GL_UNSIGNED_BYTE, imagen_bytes
    )
    glBindTexture(GL_TEXTURE_2D, 0)
    return textura_id