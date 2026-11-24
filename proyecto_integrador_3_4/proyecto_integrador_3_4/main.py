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
import espacio


# Programa principal
# ============================================================
def main():
    pygame.init()
    pygame.display.set_mode(config.DIMENSIONES_VENTANA, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Luna 3D - Solido e iluminacion")
    render.configurar_opengl()

    textura_luna = render.cargar_textura("moon_texture.jpg")
    textura_sol = render.cargar_textura("sol_texture.jpg")

    # Creamos por separado la geometria de la Luna y del Sol
    vertices_luna, normales_luna, uvs_luna, caras_luna = preparar_geometria(
        config.RADIO_LUNA, config.ANILLOS_LUNA, config.SEGMENTOS_LUNA
    )
    # 1. Al crear la geometría del Sol, guarda uvs_sol en lugar de usar "_"
    vertices_sol, normales_sol, uvs_sol, caras_sol = preparar_geometria(
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
        "rotacion_automatica": False,
    }

    estado_mouse = {"presionado": False, "posicion_anterior": (0, 0)}

    reloj = pygame.time.Clock()
    ejecutando = True
    
    # Solo estrellas procedurales (no requiere imagen)
    pos_estrellas, col_estrellas = espacio.generar_estrellas(cantidad=1200, radio=45.0)

    # (Opcional) Si también tienes una imagen de nebulosa / Vía Láctea:
    # v_cielo, n_cielo, uvs_cielo, c_cielo, tex_cielo = espacio.preparar_skydome("espacio_texture.jpg")

    rotacion_sol_y = 0.0
    # Ciclo principal
    while ejecutando:

        ejecutando = controles.procesar_eventos(estado_luna, estado_mouse)

        if not ejecutando:
            break
        
        if estado_luna["rotacion_automatica"]:
            estado_luna["rotacion_y"] = (
                estado_luna["rotacion_y"] + config.VELOCIDAD_ROTACION_AUTO
            ) % 360.0    
        
        # Limpiamos el color y la profundidad del fotograma anterior
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # 1. Primero dibujamos el fondo espacial
        # espacio.dibujar_skydome(v_cielo, n_cielo, uvs_cielo, c_cielo, tex_cielo)  # Opcional si usas textura
        espacio.dibujar_estrellas(pos_estrellas, col_estrellas)

        # 2. Después dibujamos la Luna y el Sol como ya lo tenías

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
        
        rotacion_sol_y = (rotacion_sol_y + config.VELOCIDAD_ROTACION_SOL) % 360.0

        # ... dibujo de la Luna ...

        # Dibujamos el Sol pasándole su rotación actual
        render.dibujar_sol(
            vertices_sol, normales_sol, uvs_sol, caras_sol, textura_sol, rotacion_sol_y)
        
        pygame.display.flip()
        reloj.tick(config.FPS)

    pygame.quit()


# Inicio del programa
# ============================================================
if __name__ == "__main__":
    main()