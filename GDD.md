# GDD - Mascota Virtual de Informática (IPET 249)

## 1. Concepto
**Personaje base:** un robot. Es la mascota virtual de la especialidad Informática del IPET 249 "Nicolás Copérnico".

**Identidad visual**
- Paleta institucional: bordó (fondo y bordes), amarillo (barra superior, botones), rojo (detalles) y blanco (cabeza y paneles).
- Atributos informáticos: anteojos, auriculares de gaming, antena, pantalla en el pecho con código `</>`.
- Escudo del IPET 249 visible en la esquina superior izquierda.

## 2. Variables de estado
| Variable | Inicio | Descripción |
|---|---|---|
| Energía (carga de batería) | 80 | Baja 2.0 por segundo. |
| Ánimo / Código | 80 | Baja 1.5 por segundo. |
| Salud (limpia de bugs) | 80 | Baja 1.2 por segundo. |

Los valores van de 0 a 100. Si la Energía llega a 0, Ánimo y Salud bajan el doble de rápido. Cuando la Salud es baja aparecen bugs flotando en pantalla.

## 3. Interacciones del usuario
| Acción | Tecla / botón | Efecto |
|---|---|---|
| Dar café / código | C | Energía +25 |
| Limpiar bugs | B | Salud +25 |
| Programar | P | Ánimo +20, Energía -10, dura 3 s (no se puede con Energía menor a 15) |

## 4. Estados visuales
| Estado | Condición | Aspecto |
|---|---|---|
| Sin batería | Energía <= 15 | Ojos en X, "Zzz", ícono de batería roja |
| Programando | Acción P activa | Ojos entrecerrados, brazos tipeando, líneas de código en pantalla |
| Triste | Ánimo < 30 o Salud < 30 | Cejas caídas, lágrima, boca hacia abajo |
| Feliz | Resto de los casos | Ojos con brillo y sonrisa |
