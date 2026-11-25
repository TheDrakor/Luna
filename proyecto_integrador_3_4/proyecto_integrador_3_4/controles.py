# Bibliotecas
# ============================================================
import pygame
import configuraciones as config


# ============================================================
# [INTERACCIÓN] Mapeo de eventos a parámetros de transformación
# ============================================================
def procesar_eventos(estado_luna, estado_mouse):
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return False

        # [TRANSFORMACIÓN - ESCALA] Rueda del ratón aumenta o reduce factor_escala
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                estado_mouse["presionado"] = True
                estado_mouse["posicion_anterior"] = evento.pos
            elif evento.button == 4:
                estado_luna["factor_escala"] += config.PASO_ESCALA
            elif evento.button == 5:
                estado_luna["factor_escala"] = max(
                    0.1, estado_luna["factor_escala"] - config.PASO_ESCALA
                )

        elif evento.type == pygame.MOUSEBUTTONUP:
            if evento.button == 1:
                estado_mouse["presionado"] = False

        # [TRANSFORMACIÓN - ROTACIÓN MANUAL] Arrastre con botón izquierdo gira en ejes X e Y
        elif evento.type == pygame.MOUSEMOTION:
            if estado_mouse["presionado"]:
                x, y = evento.pos
                cambio_x = x - estado_mouse["posicion_anterior"][0]
                cambio_y = y - estado_mouse["posicion_anterior"][1]
                estado_luna["rotacion_x"] += cambio_y * config.SENSIBILIDAD_ROTACION
                estado_luna["rotacion_y"] += cambio_x * config.SENSIBILIDAD_ROTACION
                estado_mouse["posicion_anterior"] = (x, y)

        elif evento.type == pygame.KEYDOWN:
            # [TRANSFORMACIÓN - TRASLACIÓN] Desplazamiento en los tres ejes (A/D: X, W/S: Y, Q/E: Z)
            if evento.key == pygame.K_a:
                estado_luna["desplazamiento_x"] -= config.PASO_TRASLACION
            elif evento.key == pygame.K_d:
                estado_luna["desplazamiento_x"] += config.PASO_TRASLACION
            elif evento.key == pygame.K_w:
                estado_luna["desplazamiento_y"] += config.PASO_TRASLACION
            elif evento.key == pygame.K_s:
                estado_luna["desplazamiento_y"] -= config.PASO_TRASLACION
            elif evento.key == pygame.K_q:
                estado_luna["desplazamiento_z"] += config.PASO_TRASLACION
            elif evento.key == pygame.K_e:
                estado_luna["desplazamiento_z"] -= config.PASO_TRASLACION
            # [TRANSFORMACIÓN - ROTACIÓN AUTOMÁTICA] Activa o pausa el giro continuo con tecla G
            elif evento.key == pygame.K_g:
                estado_luna["rotacion_automatica"] = not estado_luna["rotacion_automatica"]

            # [TRANSFORMACIÓN - SESGO / SHEAR] Deformación sobre ejes X e Y (teclas I, J, K, L)
            elif evento.key == pygame.K_j:
                estado_luna["sesgo_x"] -= config.PASO_SESGO
            elif evento.key == pygame.K_l:
                estado_luna["sesgo_x"] += config.PASO_SESGO
            elif evento.key == pygame.K_i:
                estado_luna["sesgo_y"] += config.PASO_SESGO
            elif evento.key == pygame.K_k:
                estado_luna["sesgo_y"] -= config.PASO_SESGO

            # [REINICIO] Regresa todas las transformaciones a sus valores iniciales con tecla R
            elif evento.key == pygame.K_r:
                estado_luna["desplazamiento_x"] = 0.0
                estado_luna["desplazamiento_y"] = 0.0
                estado_luna["desplazamiento_z"] = config.POSICION_INICIAL_Z
                estado_luna["rotacion_x"] = 0.0
                estado_luna["rotacion_y"] = 0.0
                estado_luna["factor_escala"] = 1.0
                estado_luna["sesgo_x"] = 0.0
                estado_luna["sesgo_y"] = 0.0
                estado_luna["rotacion_automatica"] = False
    return True