"""
Mascota Virtual de Informática - IPET 249 "Nicolás Copérnico"
Laboratorio de Aplicaciones II - Año 2026

Controles:
    C -> Dar café/código (sube Energía)
    B -> Limpiar bugs (sube Salud)
    P -> Programar (sube Ánimo, gasta Energía)
    ESC -> Salir
También se puede jugar haciendo clic en los botones.
"""
import math
import os
import random
import sys
import pygame
# ---------------------------------------------------------------- Constantes
ANCHO, ALTO = 800, 600
FPS = 60

# Paleta institucional
BORDO = (122, 18, 40)
AMARILLO = (255, 200, 30)
ROJO = (205, 32, 44)
BLANCO = (255, 255, 255)
# Auxiliares
NEGRO = (25, 25, 30)
GRIS = (200, 205, 212)
GRIS_OSC = (120, 125, 135)
VERDE = (60, 170, 90)
CELESTE = (90, 170, 255)

# Cuánto baja cada barra por segundo
DESGASTE = {"energia": 2.0, "animo": 1.5, "salud": 1.2}

CARPETA = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- Utilidades
def limitar(valor, minimo=0.0, maximo=100.0):
    return max(minimo, min(maximo, valor))


def cargar_escudo():
    """Carga escudo.png si existe; si no, devuelve None y se dibuja uno provisorio."""
    ruta = os.path.join(CARPETA, "escudo.png")
    if os.path.exists(ruta):
        img = pygame.image.load(ruta).convert_alpha()
        alto = 90
        ancho = int(img.get_width() * alto / img.get_height())
        return pygame.transform.smoothscale(img, (ancho, alto))
    return None


def dibujar_escudo(pantalla, escudo, x, y, fuente):
    if escudo:
        pantalla.blit(escudo, (x, y))
        return
    # Escudo provisorio (reemplazar poniendo escudo.png en la carpeta)
    puntos = [(x, y), (x + 80, y), (x + 80, y + 55), (x + 40, y + 90), (x, y + 55)]
    pygame.draw.polygon(pantalla, BLANCO, puntos)
    pygame.draw.polygon(pantalla, BORDO, puntos, 4)
    texto = fuente.render("IPET", True, BORDO)
    pantalla.blit(texto, texto.get_rect(center=(x + 40, y + 30)))
    texto = fuente.render("249", True, ROJO)
    pantalla.blit(texto, texto.get_rect(center=(x + 40, y + 52)))


def dibujar_barra(pantalla, fuente, x, y, valor, color, etiqueta):
    ancho, alto = 270, 24
    pantalla.blit(fuente.render(f"{etiqueta}: {int(valor)}%", True, NEGRO), (x, y - 22))
    pygame.draw.rect(pantalla, GRIS, (x, y, ancho, alto), border_radius=8)
    relleno = int(ancho * valor / 100)
    if relleno > 0:
        c = ROJO if valor < 25 else color
        pygame.draw.rect(pantalla, c, (x, y, relleno, alto), border_radius=8)
    pygame.draw.rect(pantalla, NEGRO, (x, y, ancho, alto), 2, border_radius=8)


def dibujar_bug(pantalla, x, y):
    pygame.draw.ellipse(pantalla, ROJO, (x - 9, y - 6, 18, 12))
    pygame.draw.circle(pantalla, NEGRO, (x + 9, y), 4)
    for dx in (-6, 0, 6):
        pygame.draw.line(pantalla, NEGRO, (x + dx, y - 6), (x + dx - 3, y - 12), 2)
        pygame.draw.line(pantalla, NEGRO, (x + dx, y + 6), (x + dx - 3, y + 12), 2)


# ---------------------------------------------------------------- Robot
def dibujar_robot(pantalla, fuente, cx, cy, estado, t):
    """Dibuja el robot con formas. Cambia según 'estado'."""
    rebote = int(math.sin(t * 3) * 4) if estado != "sin_bateria" else 0
    cy += rebote

    # Cuerpo
    cuerpo = pygame.Rect(0, 0, 170, 140)
    cuerpo.center = (cx, cy + 95)
    pygame.draw.rect(pantalla, GRIS, cuerpo, border_radius=18)
    pygame.draw.rect(pantalla, BORDO, cuerpo, 5, border_radius=18)

    # Brazos (cuando programa, se mueven como tipeando)
    mov = int(math.sin(t * 20) * 8) if estado == "programando" else 0
    for lado in (-1, 1):
        brazo = pygame.Rect(0, 0, 26, 80)
        brazo.center = (cx + lado * 105, cy + 95 + (mov * lado))
        pygame.draw.rect(pantalla, GRIS_OSC, brazo, border_radius=10)
        pygame.draw.rect(pantalla, BORDO, brazo, 3, border_radius=10)

    # Pantalla del pecho
    pant = pygame.Rect(0, 0, 120, 70)
    pant.center = (cx, cy + 95)
    pygame.draw.rect(pantalla, NEGRO, pant, border_radius=8)
    if estado == "programando":
        for i in range(4):
            largo = 20 + ((int(t * 8) + i * 37) % 80)
            pygame.draw.line(pantalla, AMARILLO, (pant.x + 10, pant.y + 14 + i * 14),
                             (pant.x + 10 + largo, pant.y + 14 + i * 14), 4)
    elif estado == "sin_bateria":
        pygame.draw.rect(pantalla, ROJO, (pant.x + 30, pant.y + 22, 50, 26), 3)
        pygame.draw.rect(pantalla, ROJO, (pant.x + 80, pant.y + 30, 6, 10))
        pygame.draw.rect(pantalla, ROJO, (pant.x + 34, pant.y + 26, 8, 18))
    else:
        texto = fuente.render("</>", True, AMARILLO)
        pantalla.blit(texto, texto.get_rect(center=pant.center))

    # Antena
    antena_color = GRIS_OSC if estado == "sin_bateria" else AMARILLO
    pygame.draw.line(pantalla, NEGRO, (cx, cy - 75), (cx, cy - 105), 4)
    pygame.draw.circle(pantalla, antena_color, (cx, cy - 110), 9)
    pygame.draw.circle(pantalla, NEGRO, (cx, cy - 110), 9, 2)

    # Cabeza
    cabeza = pygame.Rect(0, 0, 160, 115)
    cabeza.center = (cx, cy - 20)
    pygame.draw.rect(pantalla, BLANCO, cabeza, border_radius=22)
    pygame.draw.rect(pantalla, BORDO, cabeza, 5, border_radius=22)

    # Auriculares de gaming
    pygame.draw.arc(pantalla, NEGRO, (cx - 92, cy - 95, 184, 150), 0.1, math.pi - 0.1, 8)
    for lado in (-1, 1):
        oreja = pygame.Rect(0, 0, 26, 50)
        oreja.center = (cx + lado * 90, cy - 20)
        pygame.draw.rect(pantalla, ROJO, oreja, border_radius=10)
        pygame.draw.rect(pantalla, AMARILLO, oreja, 3, border_radius=10)

    ojo_y = cy - 32
    ojos = (cx - 36, cx + 36)

    # Ojos y boca según estado
    if estado == "feliz":
        for ox in ojos:
            pygame.draw.circle(pantalla, NEGRO, (ox, ojo_y), 11)
            pygame.draw.circle(pantalla, BLANCO, (ox - 3, ojo_y - 3), 3)
        pygame.draw.arc(pantalla, NEGRO, (cx - 28, cy - 22, 56, 38), math.pi, 2 * math.pi, 5)
    elif estado == "triste":
        for ox in ojos:
            pygame.draw.circle(pantalla, NEGRO, (ox, ojo_y), 10)
        pygame.draw.line(pantalla, NEGRO, (ojos[0] - 14, ojo_y - 20), (ojos[0] + 10, ojo_y - 14), 4)
        pygame.draw.line(pantalla, NEGRO, (ojos[1] + 14, ojo_y - 20), (ojos[1] - 10, ojo_y - 14), 4)
        pygame.draw.circle(pantalla, CELESTE, (ojos[0] - 6, ojo_y + 20 + int(t * 20) % 12), 5)
        pygame.draw.arc(pantalla, NEGRO, (cx - 24, cy - 2, 48, 30), 0, math.pi, 5)
    elif estado == "sin_bateria":
        for ox in ojos:
            pygame.draw.line(pantalla, NEGRO, (ox - 9, ojo_y - 9), (ox + 9, ojo_y + 9), 5)
            pygame.draw.line(pantalla, NEGRO, (ox - 9, ojo_y + 9), (ox + 9, ojo_y - 9), 5)
        pygame.draw.line(pantalla, NEGRO, (cx - 20, cy + 12), (cx + 20, cy + 12), 5)
        z = fuente.render("Zzz", True, ROJO)
        pantalla.blit(z, (cx + 70, cy - 90 - int(t * 10) % 15))
    else:  # programando
        for ox in ojos:
            pygame.draw.ellipse(pantalla, NEGRO, (ox - 12, ojo_y - 5, 24, 12))
        pygame.draw.line(pantalla, NEGRO, (cx - 14, cy + 10), (cx + 14, cy + 10), 5)

    # Anteojos (atributo informático)
    if estado != "sin_bateria":
        for ox in ojos:
            pygame.draw.rect(pantalla, ROJO, (ox - 22, ojo_y - 18, 44, 36), 4, border_radius=8)
        pygame.draw.line(pantalla, ROJO, (ojos[0] + 22, ojo_y), (ojos[1] - 22, ojo_y), 4)


# ---------------------------------------------------------------- Juego
def calcular_estado(energia, animo, salud, programando):
    if energia <= 15:
        return "sin_bateria"
    if programando:
        return "programando"
    if animo < 30 or salud < 30:
        return "triste"
    return "feliz"


NOMBRES_ESTADO = {
    "feliz": "Feliz",
    "triste": "Triste",
    "sin_bateria": "Sin batería",
    "programando": "Programando",
}


def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Mascota Virtual - IPET 249 Informática")
    reloj = pygame.time.Clock()
    fuente = pygame.font.Font(None, 26)
    fuente_g = pygame.font.Font(None, 40)
    fuente_t = pygame.font.Font(None, 52)
    escudo = cargar_escudo()

    energia, animo, salud = 80.0, 80.0, 80.0
    programando_hasta = 0.0
    mensaje, mensaje_hasta = "", 0.0
    bugs_pos = [(random.randint(380, 760), random.randint(150, 440)) for _ in range(5)]

    botones = [
        ("[C] Café / Código", pygame.Rect(40, 500, 220, 60), "cafe"),
        ("[B] Limpiar bugs", pygame.Rect(290, 500, 220, 60), "bugs"),
        ("[P] Programar", pygame.Rect(540, 500, 220, 60), "programar"),
    ]

    def accion(nombre, ahora):
        nonlocal energia, animo, salud, programando_hasta, mensaje, mensaje_hasta
        if nombre == "cafe":
            energia = limitar(energia + 25)
            mensaje = "¡Café y código! +Energía"
        elif nombre == "bugs":
            salud = limitar(salud + 25)
            mensaje = "Bugs eliminados. +Salud"
        elif nombre == "programar":
            if energia < 15:
                mensaje = "Sin batería: dale café primero"
            elif ahora < programando_hasta:
                return
            else:
                programando_hasta = ahora + 3
                energia = limitar(energia - 10)
                animo = limitar(animo + 20)
                mensaje = "Programando... +Ánimo"
        mensaje_hasta = ahora + 1.5

    while True:
        dt = reloj.tick(FPS) / 1000
        ahora = pygame.time.get_ticks() / 1000

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif evento.key == pygame.K_c:
                    accion("cafe", ahora)
                elif evento.key == pygame.K_b:
                    accion("bugs", ahora)
                elif evento.key == pygame.K_p:
                    accion("programar", ahora)
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                for _, rect, nombre in botones:
                    if rect.collidepoint(evento.pos):
                        accion(nombre, ahora)

        # Desgaste gradual (más rápido si no hay energía)
        factor = 2 if energia <= 0 else 1
        energia = limitar(energia - DESGASTE["energia"] * dt)
        animo = limitar(animo - DESGASTE["animo"] * factor * dt)
        salud = limitar(salud - DESGASTE["salud"] * factor * dt)

        programando = ahora < programando_hasta
        estado = calcular_estado(energia, animo, salud, programando)

        # ------------------------------------------------------------ Dibujo
        pantalla.fill(BORDO)
        pygame.draw.rect(pantalla, AMARILLO, (0, 0, ANCHO, 100))
        pygame.draw.rect(pantalla, ROJO, (0, 94, ANCHO, 6))
        titulo = fuente_t.render("Mascota Virtual - Informática", True, BORDO)
        pantalla.blit(titulo, (130, 18))
        sub = fuente.render('IPET 249 "Nicolás Copérnico"  |  Lab. de Aplicaciones II', True, BORDO)
        pantalla.blit(sub, (132, 62))
        dibujar_escudo(pantalla, escudo, 20, 5, fuente)

        # Panel de estado
        pygame.draw.rect(pantalla, BLANCO, (30, 120, 310, 260), border_radius=16)
        pygame.draw.rect(pantalla, AMARILLO, (30, 120, 310, 260), 4, border_radius=16)
        dibujar_barra(pantalla, fuente, 50, 165, energia, AMARILLO, "Energía")
        dibujar_barra(pantalla, fuente, 50, 235, animo, ROJO, "Ánimo / Código")
        dibujar_barra(pantalla, fuente, 50, 305, salud, VERDE, "Salud (sin bugs)")
        est = fuente_g.render(f"Estado: {NOMBRES_ESTADO[estado]}", True, BORDO)
        pantalla.blit(est, (50, 335))

        # Bugs flotando cuando la salud es baja
        for i in range(int((100 - salud) / 20)):
            bx, by = bugs_pos[i]
            dibujar_bug(pantalla, bx, by + int(math.sin(ahora * 2 + i) * 6))

        dibujar_robot(pantalla, fuente_g, 560, 270, estado, ahora)

        # Botones
        raton = pygame.mouse.get_pos()
        for texto, rect, _ in botones:
            color = ROJO if rect.collidepoint(raton) else AMARILLO
            pygame.draw.rect(pantalla, color, rect, border_radius=12)
            pygame.draw.rect(pantalla, BLANCO, rect, 3, border_radius=12)
            tcol = BLANCO if color == ROJO else BORDO
            tsup = fuente_g.render(texto, True, tcol)
            pantalla.blit(tsup, tsup.get_rect(center=rect.center))

        if ahora < mensaje_hasta:
            m = fuente_g.render(mensaje, True, BLANCO)
            pantalla.blit(m, m.get_rect(center=(ANCHO // 2, 470)))

        pygame.display.flip()


if __name__ == "__main__":
    main()