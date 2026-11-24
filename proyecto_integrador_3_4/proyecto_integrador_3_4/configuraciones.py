import pygame
from OpenGL.GL import *
from pathlib import Path

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
POSICION_LUZ = (1.0, 0.25, -2.0)

# Sensibilidad de los controles
PASO_TRASLACION = 0.2
PASO_ESCALA = 0.1
PASO_SESGO = 0.1
SENSIBILIDAD_ROTACION = 0.5



def cargar_textura(ruta_imagen):
    # Cargar imagen y voltear en Y para coincidir con el origen (0,0) inferior izquierdo de OpenGL
    ruta_textura = Path(__file__).resolve().parent / ruta_imagen
    superficie = pygame.image.load(str(ruta_textura))
    imagen_bytes = pygame.image.tostring(superficie, "RGBA", True)
    ancho, alto = superficie.get_size()

    textura_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textura_id)

    # Configurar wrapping (repetición en U y V) y filtrado suave
    
    # T y S vendrian siendo las coordenadas U y V
    # GL_TEXTURE_2D: Configurando una textura bidimensional plana
    # GL_REPEAT: Pega perfectamente con el inicio del lado izquierdo del objeto
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
   
    """Define cuando la esfera se ve lejos o pequeña en pantalla,
    por lo que varios texeles deben comprimirse en un solo píxel, GL_LINEAR nos sirve para suavizar
    los pixeles vecinos cuando se aumente o disminuye el tamaño"""
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # Subir datos a la GPU
    glTexImage2D(
        GL_TEXTURE_2D, 0, GL_RGBA, ancho, alto, 0,
        GL_RGBA, GL_UNSIGNED_BYTE, imagen_bytes
    )
    glBindTexture(GL_TEXTURE_2D, 0)
    return textura_id