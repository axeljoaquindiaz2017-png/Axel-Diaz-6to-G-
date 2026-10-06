<p align="center"><img src="escudo.png" alt="Escudo IPET 249" height="120"></p>

# Mascota Virtual de Informática

- **Institución:** IPET 249 "Nicolás Copérnico"
- **Especialidad:** Informática
- **Asignatura:** Laboratorio de Aplicaciones II
- **Año:** 2026
- **Autor/a:** _(Axel Diaz)_

## Concepto de la mascota
Un robot con anteojos, auriculares de gaming y una pantalla con código en el pecho, que representa a la especialidad de Informática. Usa los colores del colegio (bordó, amarillo, rojo y blanco) y muestra el escudo del IPET 249. Sus necesidades (energía, ánimo y salud) son metáforas del trabajo informático: la batería, la motivación para programar y los bugs.

## Cómo ejecutar
1. Instalar Python 3.
2. Instalar Pygame: `pip install pygame`
3. Copiar el escudo como `escudo.png` en esta carpeta (si no está, se dibuja uno provisorio).
4. Ejecutar: `python main.py`

## Controles
| Tecla | Acción |
|---|---|
| C | Café / código (sube Energía) |
| B | Limpiar bugs (sube Salud) |
| P | Programar (sube Ánimo, gasta Energía) |
| ESC | Salir |

También se puede usar el mouse sobre los botones.

## Necesidades de la mascota
- **Energía:** baja con el tiempo. Si llega a 15 o menos, el robot se queda sin batería.
- **Ánimo / Código:** baja con el tiempo y sube al programar.
- **Salud:** baja con el tiempo y aparecen bugs en pantalla; se recupera limpiándolos.

Más detalle en [GDD.md](GDD.md) y la transparencia sobre el uso de IA en [IA_LOG.md](IA_LOG.md).
