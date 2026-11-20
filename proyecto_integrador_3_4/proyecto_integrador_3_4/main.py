# Bibliotecas
# ============================================================
import pygame
from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GL import *
import configuraciones as config
from geometria import preparar_geometria
from transformaciones import aplicar_transformaciones
import renderizado as render
import controles

# Programa principal
# ============================================================
def main():
    pygame.init()
    pygame.display.set_mode(config.DIMENSIONES_VENTANA, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Luna 3D - Solido e iluminacion")
    render.configurar_opengl()

    # C:\Users\lata_\OneDrive\Pictures\Camera Roll 1
    textura_luna = render.cargar_textura("moon_texture.jpg")
    textura_sol = render.cargar_textura("sol_texture.jpg")

    # Creamos por separado la geometria de la Luna y del Sol
    vertices_luna, normales_luna, uvs_luna, caras_luna = preparar_geometria(
        config.RADIO_LUNA, config.ANILLOS_LUNA, config.SEGMENTOS_LUNA
    )
    vertices_sol, normales_sol, _, caras_sol = preparar_geometria(
        config.RADIO_SOL, config.ANILLOS_SOL, config.SEGMENTOS_SOL
    )

    # Estado inicial de la Luna
    estado_luna = {
        "desplazamiento_x": 0.0,
        "desplazamiento_y": 0.0,
        "desplazamiento_z": config.POSICION_INICIAL_Z,
        "rotacion_x": 0.0,
        "rotacion_y": 0.0,
        "factor_escala": 1.0,
        "sesgo_x": 0.0,
        "sesgo_y": 0.0,
    }

    estado_mouse = {"presionado": False, "posicion_anterior": (0, 0)}

    reloj = pygame.time.Clock()
    ejecutando = True

    # Ciclo principal
    while ejecutando:

        ejecutando = controles.procesar_eventos(estado_luna, estado_mouse)

        if not ejecutando:
            break

        # Limpiamos el color y la profundidad del fotograma anterior
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # La Luna tiene sus propias transformaciones
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
        render.dibujar_luna(
            vertices_luna, normales_luna, uvs_luna, caras_luna, textura_luna
        )
        glPopMatrix()

        # El Sol se dibuja aparte y no sigue los movimientos de la Luna
        render.dibujar_sol(vertices_sol, normales_sol, caras_sol)

        pygame.display.flip()
        reloj.tick(config.FPS)

    pygame.quit()


# Inicio del programa
# ============================================================
if __name__ == "__main__":
    main()