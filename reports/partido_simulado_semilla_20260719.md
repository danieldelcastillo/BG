# Informe histórico — Partido simulado paso a paso

> Este informe se generó antes de actualizar las CF el 24 de julio de 2026. No debe usarse para equilibrar las reglas actuales; conserva únicamente el ejemplo de trazabilidad paso a paso.

- Semilla: `20260719`
- Jugador: DEF 15 · MED 15 · AT 15
- Rival: DEF 15 · MED 15 · AT 15
- Mano inicial: 0 CC; límite: 5 CC
- Presión: mínimo 0, máximo 9
- Empates: superan la comparación

## Desarrollo del partido

### Turnos 1 y 2

En el turno 1 se roba **Centro al área**, que entra en la mano. En el turno 2 aparece **Disparo lejano**. La IA no juega la única CC disponible: +1 CF no basta para alcanzar el resultado intermedio (requiere AT 17 frente a DEF 17). El disparo termina en **Nada**.

### Turnos 3 a 8 — La mano alcanza el límite

| Turno | Robo / decisión |
| --- | --- |
| 3 | Roba Cambio de orientación. |
| 4 | Roba Apertura a banda. |
| 5 | Roba Acción individual. |
| 6 | Roba Pase entre líneas; la mano llega a 5. |
| 7 | Roba una segunda Apertura a banda: sería la sexta CC. La IA descarta **Cambio de orientación**, que no tiene comparaciones aprovechables con esta mano y tiene valor bajo. |
| 8 | Roba Control del juego: vuelve a ser la sexta CC. La IA descarta **Control del juego**; con presión 0 su efecto base no aporta valor inmediato. |

La mano antes de la siguiente CF es: Centro al área, Apertura a banda, Acción individual, Pase entre líneas y Apertura a banda.

### Turno 9 — CF: Pase de la muerte

La IA usa las dos copias de **Apertura a banda — Comparación 1**:

1. MED 15 frente a DEF 15, superada: +2 CF.
2. MED 15 frente a DEF 15, superada: +2 CF adicionales.

AT 15 + 4 CF = 19 frente a DEF rival 15 + 4 = 19. Resultado: **Gol** (nivel 2). Marcador: 1. Mano restante: Centro al área, Acción individual y Pase entre líneas.

### Turno 10 — CF: Buscar el córner

La IA encuentra una línea de tres cartas para el resultado superior:

1. **Acción individual — Efecto base**: +1 CF.
2. **Pase entre líneas — Efecto base**: +1 CC.
3. **Centro al área — Comparación 1**: MED 15 + 1 CC = 16 frente a DEF 15 + 1 = 16; +2 CF.

AT 15 + 3 CF = 18 frente a DEF rival 15 + 3 = 18. Resultado: **-2 Presión** (nivel 2). La presión se mantiene en 0 y la mano queda vacía.

### Turnos 11 a 14

Se roban Recuperación agresiva, Centro al área, Apertura a banda y Pared. La mano llega a 4 cartas, por debajo del límite.

### Turno 15 — CF: Mano a mano

1. **Centro al área — Efecto base**: +1 CF.
2. **Pared — Comparación 2**: AT 15 frente a DEF 15; +2 CF.
3. **Apertura a banda — Comparación 1**: MED 15 frente a DEF 15; +2 CF.

AT 15 + 5 CF = 20 frente a DEF rival 15 + 5 = 20. Resultado: **Gol** (nivel 2). Marcador: 2. Solo queda Recuperación agresiva en mano.

### Turnos 16 a 20 — Segundo descarte por límite de mano

| Turno | Robo / decisión |
| --- | --- |
| 16 | Roba Balón al espacio. |
| 17 | Roba Recuperación agresiva. |
| 18 | Roba Pared. |
| 19 | Roba una tercera Recuperación agresiva; mano de 5. |
| 20 | Roba Construcción desde atrás como sexta CC. La IA descarta una **Recuperación agresiva** repetida: aporta poco con presión 0 y mantiene dos copias para opciones futuras. |

### Turno 21 — CF: Buscar el córner

1. **Construcción desde atrás — Comparación 1**: MED 15 frente a MED 15; +2 CC.
2. **Balón al espacio — Comparación 1**: MED 15 + 2 CC = 17 frente a DEF 15 + 2 = 17; +3 CF.

AT 18 frente a DEF rival 18. Resultado: **-2 Presión** (nivel 2). La presión sigue en 0.

### Turno 22 — CF: Remate de cabeza

La IA juega **Pared — Comparación 2**: AT 15 frente a DEF 15; +2 CF. Con AT 17 frente a DEF 17 logra el resultado intermedio: **descarta la primera carta del mazo**. Se descarta **Provocar la falta** sin resolverla.

### Turno 23 — CF: Mano a mano

Solo quedan dos Recuperación agresiva en mano. No pueden generar +CF, así que la IA no gasta cartas. Resultado: **Roba 1 CR**. Marcador: 2; CR robadas: 1.

### Turnos 24 a 29 — Tercer ciclo de mano llena

| Turno | Robo / decisión |
| --- | --- |
| 24 | Roba Construcción desde atrás. |
| 25 | Roba Cambio de orientación. |
| 26 | Roba Balón al espacio; mano de 5. |
| 27 | Roba Centro al área como sexta CC; descarta **Cambio de orientación**, sin comparaciones alcanzables. |
| 28 | Roba Recuperación agresiva como sexta CC; descarta una **Recuperación agresiva** repetida y de bajo valor con presión 0. |
| 29 | Aparece Remate de cabeza. |

En el turno 29 la IA usa **Balón al espacio — Efecto base**: +2 CF y +1 Presión. AT 17 frente a DEF 17 alcanza el nivel intermedio de Remate de cabeza: se descarta **Disparo lejano** sin resolver. La presión sube a 1.

### Turno 30 — CC robada: Pared

La mano llega a 5: Recuperación agresiva, Construcción desde atrás, Centro al área, Recuperación agresiva y Pared.

### Turno 31 — CF: Provocar la falta

La IA alcanza el resultado superior:

1. **Construcción desde atrás — Efecto base**: +1 CC.
2. **Centro al área — Comparación 1**: MED 15 + 1 CC = 16 frente a DEF 15 + 1 = 16; +2 CF.
3. **Pared — Comparación 2**: AT 15 frente a DEF 15; +2 CF.

AT 15 + 4 CF = 19 frente a DEF rival 15 + 4 = 19. Resultado: **Tarjeta roja** (nivel 2). Presión: 1.

### Turnos 32 a 36 — Últimos descartes de mano

| Turno | Robo / decisión |
| --- | --- |
| 32 | Roba Pase entre líneas. |
| 33 | Roba Acción individual. |
| 34 | Roba Construcción desde atrás; mano de 5. |
| 35 | Roba Control del juego como sexta CC; se descarta Control del juego por su baja utilidad relativa. |
| 36 | Roba Balón al espacio como sexta CC; se descarta una Recuperación agresiva repetida y de bajo valor. |

### Turno 37 — CF: Pase de la muerte

1. **Construcción desde atrás — Comparación 1**: MED 15 frente a MED 15; +2 CC.
2. **Pase entre líneas — Comparación 1**: MED 15 + 2 CC = 17 frente a DEF 15 + 2 = 17; +3 CF.
3. **Acción individual — Efecto base**: +1 CF.

AT 15 + 4 CF = 19 frente a DEF rival 15 + 4 = 19. Resultado: **Gol** (nivel 2). Marcador: 3.

### Turno 38 — CC robada: Construcción desde atrás

El mazo queda vacío tras este robo, por lo que termina el partido. La mano final contiene Recuperación agresiva, Balón al espacio y Construcción desde atrás.

## Resultado final

| Métrica | Resultado |
| --- | ---: |
| Goles del jugador | **3** |
| Tarjetas amarillas | **0** |
| Tarjetas rojas | **1** |
| CR robadas | **1** |
| Presión final | **1** |
| CC conservadas | **3** |
| CF resueltas | **10** |

## Comprobación del límite de mano

La mano nunca conserva más de cinco CC. Durante esta simulación se aplicaron siete descartes automáticos al robar la sexta carta. Además, dos CF descartaron cartas de la parte superior del mazo sin resolverlas, por lo que el partido tuvo 38 turnos de robo en lugar de 40.
