# Partido simulado paso a paso — BG FÚTBOL

- Semilla reproducible: `20260917`
- Jugador: DEF 15 · MED 15 · AT 15
- Bot: DEF 15 · MED 15 · AT 15
- Mazo: 28 CC, 12 CF y 10 CE; mazo de CR aparte: 16 (8 tipos × 2)
- Mano inicial: 0 CC; límite: 3 CC
- Gol del bot: al superar presión 9, la presión vuelve a 0
- Estrategia: IA estándar

## Leyenda visual

- 🟩 **CC** — carta de control: entra en la mano.
- 🟧 **CF** — carta de finalización: permite jugar CC y se resuelve.
- 🟪 **CE** — carta de evento: la IA elige una de sus tres opciones.
- 🔴 **CR** — carta roja: sustituye al contador de CR; se roba y se resuelve al instante.
- 🟢 **+n** — bono +CF que las CC aplican al atributo del jugador en una CF.

## Desarrollo completo

### Turno 1 — 🟧 CF: Provocar la falta
- 🟧 Robo: CF **Provocar la falta**. Mano antes de decidir (0/3): —.
- IA: no gasta CC; no puede mejorar la CF de forma rentable.
- 🟧 Opciones de la CF tras jugar las CC:
  - ⬜ Opción 1: AT jugador 15 = 15 > DEF rival 15 +5 = 20 → Tarjeta roja y descarta una carta del mazo.
  - ⬜ Opción 2: AT jugador 15 = 15 > DEF rival 15 → Tarjeta amarilla y -1 Presión.
  - **✅ Opción 3: Fallo: no se supera ninguna comparación anterior → Roba 1 CR y descarta la primera carta del mazo.**
- 🟧 CF aplicada: **Roba 1 CR y descarta la primera carta del mazo** (nivel 0).
- 🔴 CR ejecutada: **Control de la posesión**.
  - ⬜ Opción 1: MED rival 15 > MED jugador 15 +3 = 18 → +5 Presión; descarta 1 CC de la mano.
  - ⬜ Opción 2: MED rival 15 > MED jugador 15 +2 = 17 → +4 Presión; descarta 1 CC de la mano.
  - **✅ Opción de reserva: Ninguna acción anterior se cumple → +1 Presión; descarta 1 CC de la mano.**
  - ⬜ Esquina inferior izquierda (independiente): Si el rival está ganando → descarta 1 carta(s) del mazo.
- Marcador jugador 0–0 bot; presión 1; +CC 0; +CF 0; CR 1; mano 0/3; mazo restante: 27 CC, 11 CF y 10 CE; CR disponibles: 16.
  - Registro: Aparece CF: Provocar la falta.
  - Registro: Descarta del mazo: Apertura a banda.
  - Registro: Roba CR: Control de la posesión.
  - Registro: No hay CC en mano para descartar.
  - Registro: Control de la posesión: acción de reserva.
  - Registro: Provocar la falta: Roba 1 CR y descarta la primera carta del mazo.

### Turno 2 — 🟪 CE: Pérdida de tiempo
- 🟪 Robo: CE **Pérdida de tiempo**.
- 🟪 Opciones de la CE:
  - ⬜ Opción 1: +1 Presión; +1 amarilla rival; descarta 2 carta(s) del mazo.
  - **✅ Opción 2: -4 Presión; +1 CR; descarta 1 CC de la mano.**
  - ⬜ Opción 3: +1 Presión; tirada de lesión por amarilla (10%); descarta 1 carta(s) del mazo.
- 🟪 IA elige **Opción 2**.
- Los robos o CF extra que active el evento se resuelven inmediatamente según el motor.
- 🔴 CR ejecutada: **Centro al área**.
  - ⬜ Opción 1: MED rival 15 > DEF jugador 15 +4 = 19 → +5 Presión.
  - ⬜ Opción 2: AT rival 15 > DEF jugador 15 +2 = 17 → +4 Presión.
  - **✅ Opción de reserva: Ninguna acción anterior se cumple → +2 Presión.**
  - ⬜ Esquina inferior izquierda (independiente): Si el rival está perdiendo → +1 Presión.
- Marcador jugador 0–0 bot; presión 2; +CC 0; +CF 0; CR 2; mano 0/3; mazo restante: 27 CC, 11 CF y 9 CE; CR disponibles: 16.
  - Registro: Aparece CE: Pérdida de tiempo.
  - Registro: No hay CC en mano para descartar.
  - Registro: Roba CR: Centro al área.
  - Registro: Centro al área: acción de reserva.
  - Registro: Pérdida de tiempo: Opción 2.

### Turno 3 — 🟩 CC: Centro al área
- 🟩 Robo: CC **Centro al área**. Mano (1/3 🟩): Centro al área.
- Marcador jugador 0–0 bot; presión 2; +CC 0; +CF 0; CR 2; mano 1/3 🟩; mazo restante: 26 CC, 11 CF y 9 CE; CR disponibles: 16.
  - Registro: Roba CC: Centro al área.

### Turno 4 — 🟩 CC: Triangulación de equipo
- 🟩 Robo: CC **Triangulación de equipo**. Mano (2/3 🟩 🟩): Centro al área, Triangulación de equipo.
- Marcador jugador 0–0 bot; presión 2; +CC 0; +CF 0; CR 2; mano 2/3 🟩 🟩; mazo restante: 25 CC, 11 CF y 9 CE; CR disponibles: 16.
  - Registro: Roba CC: Triangulación de equipo.

### Turno 5 — 🟧 CF: Disparo lejano
- 🟧 Robo: CF **Disparo lejano**. Mano antes de decidir (2/3 🟩 🟩): Centro al área, Triangulación de equipo.
- IA: no gasta CC; no puede mejorar la CF de forma rentable.
- 🟧 Opciones de la CF tras jugar las CC:
  - ⬜ Opción 1: AT jugador 15 = 15 > DEF rival 15 +4 = 19 → Gol.
  - ⬜ Opción 2: AT jugador 15 = 15 > DEF rival 15 +1 = 16 → -2 Presión.
  - **✅ Opción 3: Fallo: no se supera ninguna comparación anterior → Descarta una CC de la mano y roba 1 CR.**
- 🟧 CF aplicada: **Descarta una CC de la mano y roba 1 CR** (nivel 0).
- 🔴 CR ejecutada: **Balón parado**.
  - ⬜ Opción 1: AT rival 15 > DEF jugador 15 +4 = 19 → +1 gol en contra.
  - ⬜ Opción 2: AT rival 15 > DEF jugador 15 +2 = 17 → +3 Presión.
  - **✅ Opción de reserva: Ninguna acción anterior se cumple → +2 Presión.**
  - ⬜ Esquina inferior izquierda (independiente): Si el rival está ganando → descarta 1 carta(s) del mazo.
- Marcador jugador 0–0 bot; presión 4; +CC 0; +CF 0; CR 3; mano 1/3 🟩; mazo restante: 25 CC, 10 CF y 9 CE; CR disponibles: 16.
  - Registro: Aparece CF: Disparo lejano.
  - Registro: Descarta de la mano: Centro al área.
  - Registro: Roba CR: Balón parado.
  - Registro: Balón parado: acción de reserva.
  - Registro: Disparo lejano: Descarta una CC de la mano y roba 1 CR.

### Turno 6 — 🟩 CC: Triangulación de equipo
- 🟩 Robo: CC **Triangulación de equipo**. Mano (2/3 🟩 🟩): Triangulación de equipo, Triangulación de equipo.
- Marcador jugador 0–0 bot; presión 4; +CC 0; +CF 0; CR 3; mano 2/3 🟩 🟩; mazo restante: 24 CC, 10 CF y 9 CE; CR disponibles: 16.
  - Registro: Roba CC: Triangulación de equipo.

### Turno 7 — 🟩 CC: Construcción desde atrás
- 🟩 Robo: CC **Construcción desde atrás**. Mano (3/3 🟩 🟩 🟩): Triangulación de equipo, Triangulación de equipo, Construcción desde atrás.
- Marcador jugador 0–0 bot; presión 4; +CC 0; +CF 0; CR 3; mano 3/3 🟩 🟩 🟩; mazo restante: 23 CC, 10 CF y 9 CE; CR disponibles: 16.
  - Registro: Roba CC: Construcción desde atrás.

### Turno 8 — 🟩 CC: Apertura a banda
- 🟩 Robo: CC **Apertura a banda**. Mano (4/3 🟩 🟩 🟩 🟩): Triangulación de equipo, Triangulación de equipo, Construcción desde atrás, Apertura a banda.
- 🟩 Límite de mano: se descarta **Apertura a banda** (copias: 1; comparaciones utilizables: 0; valor: 100).
- Marcador jugador 0–0 bot; presión 4; +CC 0; +CF 0; CR 3; mano 3/3 🟩 🟩 🟩; mazo restante: 22 CC, 10 CF y 9 CE; CR disponibles: 16.
  - Registro: Roba CC: Apertura a banda.
  - Registro: Descarta de la mano: Apertura a banda.

### Turno 9 — 🟩 CC: Pase entre líneas
- 🟩 Robo: CC **Pase entre líneas**. Mano (4/3 🟩 🟩 🟩 🟩): Triangulación de equipo, Triangulación de equipo, Construcción desde atrás, Pase entre líneas.
- 🟩 Límite de mano: se descarta **Pase entre líneas** (copias: 1; comparaciones utilizables: 0; valor: 40).
- Marcador jugador 0–0 bot; presión 4; +CC 0; +CF 0; CR 3; mano 3/3 🟩 🟩 🟩; mazo restante: 21 CC, 10 CF y 9 CE; CR disponibles: 16.
  - Registro: Roba CC: Pase entre líneas.
  - Registro: Descarta de la mano: Pase entre líneas.

### Turno 10 — 🟪 CE: Fuera de juego
- 🟪 Robo: CE **Fuera de juego**.
- 🟪 Opciones de la CE:
  - ⬜ Opción 1: descarta 1 carta(s) del mazo; descarta 2 CC de la mano.
  - ⬜ Opción 2: +2 Presión.
  - **✅ Opción 3: -3 Presión; +1 CR.**
- 🟪 IA elige **Opción 3**.
- Los robos o CF extra que active el evento se resuelven inmediatamente según el motor.
- 🔴 CR ejecutada: **Ataque por banda**.
  - ⬜ Opción 1: MED rival 15 > DEF jugador 15 +2 = 17 → +5 Presión.
  - ⬜ Opción 2: MED rival 15 > MED jugador 15 +1 = 16 → +4 Presión.
  - **✅ Opción de reserva: Ninguna acción anterior se cumple → +2 Presión.**
  - ⬜ Esquina inferior izquierda (independiente): Si el rival está ganando → descarta 1 carta(s) del mazo.
- Marcador jugador 0–0 bot; presión 3; +CC 0; +CF 0; CR 4; mano 3/3 🟩 🟩 🟩; mazo restante: 21 CC, 10 CF y 8 CE; CR disponibles: 16.
  - Registro: Aparece CE: Fuera de juego.
  - Registro: Roba CR: Ataque por banda.
  - Registro: Ataque por banda: acción de reserva.
  - Registro: Fuera de juego: Opción 3.

### Turno 11 — 🟩 CC: Cambio de orientación
- 🟩 Robo: CC **Cambio de orientación**. Mano (4/3 🟩 🟩 🟩 🟩): Triangulación de equipo, Triangulación de equipo, Construcción desde atrás, Cambio de orientación.
- 🟩 Límite de mano: se descarta **Cambio de orientación** (copias: 1; comparaciones utilizables: 0; valor: 75).
- Marcador jugador 0–0 bot; presión 3; +CC 0; +CF 0; CR 4; mano 3/3 🟩 🟩 🟩; mazo restante: 20 CC, 10 CF y 8 CE; CR disponibles: 16.
  - Registro: Roba CC: Cambio de orientación.
  - Registro: Descarta de la mano: Cambio de orientación.

### Turno 12 — 🟧 CF: Disparo lejano
- 🟧 Robo: CF **Disparo lejano**. Mano antes de decidir (3/3 🟩 🟩 🟩): Triangulación de equipo, Triangulación de equipo, Construcción desde atrás.
- 🟩 CC 1: **Triangulación de equipo — Efecto base**: +1 CC.
- 🟩 CC 2: **Construcción desde atrás — Comparación 1**: +2 CC. Comparación: MED jugador 16 > DEF rival 15; superada.
- 🟩 CC 3: **Triangulación de equipo — Comparación 2**: +2 CF. Comparación: AT jugador 17 > MED rival 16; superada.
- 🟧 Opciones de la CF tras jugar las CC:
  - ⬜ Opción 1: AT jugador 15 🟢 **+2** = 17 > DEF rival 15 +4 = 19 → Gol.
  - **✅ Opción 2: AT jugador 15 🟢 **+2** = 17 > DEF rival 15 +1 = 16 → -2 Presión.**
  - ⬜ Opción 3: Fallo: no se supera ninguna comparación anterior → Descarta una CC de la mano y roba 1 CR.
- 🟧 CF aplicada: **-2 Presión** (nivel 1).
- Marcador jugador 0–0 bot; presión 1; +CC 0; +CF 0; CR 4; mano 0/3; mazo restante: 20 CC, 9 CF y 8 CE; CR disponibles: 16.
  - Registro: Aparece CF: Disparo lejano.
  - Registro: Juega Triangulación de equipo: Efecto base.
  - Registro: Juega Construcción desde atrás: Comparación 1.
  - Registro: Juega Triangulación de equipo: Comparación 2.
  - Registro: Disparo lejano: -2 Presión.

### Turno 13 — 🟧 CF: Remate de cabeza
- 🟧 Robo: CF **Remate de cabeza**. Mano antes de decidir (0/3): —.
- IA: no gasta CC; no puede mejorar la CF de forma rentable.
- 🟧 Opciones de la CF tras jugar las CC:
  - ⬜ Opción 1: AT jugador 15 = 15 > DEF rival 15 +4 = 19 → Gol.
  - ⬜ Opción 2: AT jugador 15 = 15 > DEF rival 15 +1 = 16 → Descarta la primera carta del mazo y -1 Presión.
  - **✅ Opción 3: Fallo: no se supera ninguna comparación anterior → Roba 1 CR y -1 Presión.**
- 🟧 CF aplicada: **Roba 1 CR y -1 Presión** (nivel 0).
- 🔴 CR ejecutada: **Ataque por banda**.
  - ⬜ Opción 1: MED rival 15 > DEF jugador 15 +2 = 17 → +5 Presión.
  - ⬜ Opción 2: MED rival 15 > MED jugador 15 +1 = 16 → +4 Presión.
  - **✅ Opción de reserva: Ninguna acción anterior se cumple → +2 Presión.**
  - ⬜ Esquina inferior izquierda (independiente): Si el rival está ganando → descarta 1 carta(s) del mazo.
- Marcador jugador 0–0 bot; presión 2; +CC 0; +CF 0; CR 5; mano 0/3; mazo restante: 20 CC, 8 CF y 8 CE; CR disponibles: 16.
  - Registro: Aparece CF: Remate de cabeza.
  - Registro: Roba CR: Ataque por banda.
  - Registro: Ataque por banda: acción de reserva.
  - Registro: Remate de cabeza: Roba 1 CR y -1 Presión.

### Turno 14 — 🟩 CC: Balón al espacio
- 🟩 Robo: CC **Balón al espacio**. Mano (1/3 🟩): Balón al espacio.
- Marcador jugador 0–0 bot; presión 2; +CC 0; +CF 0; CR 5; mano 1/3 🟩; mazo restante: 19 CC, 8 CF y 8 CE; CR disponibles: 16.
  - Registro: Roba CC: Balón al espacio.

### Turno 15 — 🟪 CE: Córner
- 🟪 Robo: CE **Córner**.
- 🟪 Opciones de la CE:
  - ⬜ Opción 1: +2 Presión; juega una CF aleatoria del descarte.
  - **✅ Opción 2: +1 Presión; roba 1 carta del mazo.**
  - ⬜ Opción 3: +1 Presión; descarta 1 carta(s) del mazo.
- 🟪 IA elige **Opción 2**.
- Los robos o CF extra que active el evento se resuelven inmediatamente según el motor.
- 🔴 CR ejecutada: **Contraataque rival**.
  - ⬜ Opción 1: AT rival 15 > MED jugador 15 +3 = 18 → +1 gol en contra; recupera 1 CC del descarte.
  - ⬜ Opción 2: AT rival 15 > MED jugador 15 → recupera 1 CC del descarte; juega 1 CR adicional(es).
  - **✅ Opción de reserva: Ninguna acción anterior se cumple → +3 Presión.**
  - ⬜ Esquina inferior izquierda (independiente): Si el rival está ganando → +1 amarilla propia; recupera 1 CC del descarte.
- Marcador jugador 0–0 bot; presión 6; +CC 0; +CF 0; CR 6; mano 1/3 🟩; mazo restante: 19 CC, 7 CF y 7 CE; CR disponibles: 16.
  - Registro: Aparece CE: Córner.
  - Registro: Aparece CF: Ultimo pase.
  - Registro: Roba CR: Contraataque rival.
  - Registro: Contraataque rival: acción de reserva.
  - Registro: Ultimo pase: Roba 1 CR.
  - Registro: Córner: Opción 2.

### Turno 17 — 🟩 CC: Acción individual
- 🟩 Robo: CC **Acción individual**. Mano (2/3 🟩 🟩): Balón al espacio, Acción individual.
- Marcador jugador 0–0 bot; presión 6; +CC 0; +CF 0; CR 6; mano 2/3 🟩 🟩; mazo restante: 18 CC, 7 CF y 7 CE; CR disponibles: 16.
  - Registro: Roba CC: Acción individual.

### Turno 18 — 🟩 CC: Construcción desde atrás
- 🟩 Robo: CC **Construcción desde atrás**. Mano (3/3 🟩 🟩 🟩): Balón al espacio, Acción individual, Construcción desde atrás.
- Marcador jugador 0–0 bot; presión 6; +CC 0; +CF 0; CR 6; mano 3/3 🟩 🟩 🟩; mazo restante: 17 CC, 7 CF y 7 CE; CR disponibles: 16.
  - Registro: Roba CC: Construcción desde atrás.

### Turno 19 — 🟩 CC: Balón al espacio
- 🟩 Robo: CC **Balón al espacio**. Mano (4/3 🟩 🟩 🟩 🟩): Balón al espacio, Acción individual, Construcción desde atrás, Balón al espacio.
- 🟩 Límite de mano: se descarta **Acción individual** (copias: 1; comparaciones utilizables: 0; valor: 100).
- Marcador jugador 0–0 bot; presión 6; +CC 0; +CF 0; CR 6; mano 3/3 🟩 🟩 🟩; mazo restante: 16 CC, 7 CF y 7 CE; CR disponibles: 16.
  - Registro: Roba CC: Balón al espacio.
  - Registro: Descarta de la mano: Acción individual.

### Turno 20 — 🟪 CE: Pérdida de tiempo
- 🟪 Robo: CE **Pérdida de tiempo**.
- 🟪 Opciones de la CE:
  - ⬜ Opción 1: +1 Presión; +1 amarilla rival; descarta 2 carta(s) del mazo.
  - **✅ Opción 2: -4 Presión; +1 CR; descarta 1 CC de la mano.**
  - ⬜ Opción 3: +1 Presión; tirada de lesión por amarilla (10%); descarta 1 carta(s) del mazo.
- 🟪 IA elige **Opción 2**.
- Los robos o CF extra que active el evento se resuelven inmediatamente según el motor.
- 🔴 CR ejecutada: **Acción rival individual**.
  - ⬜ Opción 1: AT rival 15 > DEF jugador 15 +3 = 18 → +1 gol en contra.
  - ⬜ Opción 2: AT rival 15 > DEF jugador 15 +1 = 16 → +3 Presión; +1 amarilla propia.
  - **✅ Opción de reserva: Ninguna acción anterior se cumple → +1 amarilla propia; descarta 1 carta(s) del mazo.**
  - ⬜ Esquina inferior izquierda (independiente): Si el rival está perdiendo → +1 Presión.
- Marcador jugador 0–0 bot; presión 2; +CC 0; +CF 0; CR 7; mano 2/3 🟩 🟩; mazo restante: 16 CC, 6 CF y 6 CE; CR disponibles: 16.
  - Registro: Aparece CE: Pérdida de tiempo.
  - Registro: Descarta de la mano: Construcción desde atrás.
  - Registro: Roba CR: Acción rival individual.
  - Registro: Descarta del mazo: Mano a mano.
  - Registro: Acción rival individual: acción de reserva.
  - Registro: Pérdida de tiempo: Opción 2.

### Turno 21 — 🟧 CF: Ultimo pase
- 🟧 Robo: CF **Ultimo pase**. Mano antes de decidir (2/3 🟩 🟩): Balón al espacio, Balón al espacio.
- 🟩 CC 1: **Balón al espacio — Efecto base**: +2 CF; +1 Presión.
- 🟩 CC 2: **Balón al espacio — Efecto base**: +2 CF; +1 Presión.
- 🟧 Opciones de la CF tras jugar las CC:
  - ⬜ Opción 1: MED jugador 15 🟢 **+2** 🟢 **+2** = 19 > DEF rival 15 +4 = 19 → Gol.
  - **✅ Opción 2: MED jugador 15 🟢 **+2** 🟢 **+2** = 19 > DEF rival 15 +2 = 17 → -1 Presión.**
  - ⬜ Opción 3: Fallo: no se supera ninguna comparación anterior → Roba 1 CR.
- 🟧 CF aplicada: **-1 Presión** (nivel 1).
- Marcador jugador 0–0 bot; presión 3; +CC 0; +CF 0; CR 7; mano 0/3; mazo restante: 16 CC, 5 CF y 6 CE; CR disponibles: 16.
  - Registro: Aparece CF: Ultimo pase.
  - Registro: Juega Balón al espacio: Efecto base.
  - Registro: Juega Balón al espacio: Efecto base.
  - Registro: Ultimo pase: -1 Presión.

### Turno 22 — 🟩 CC: Recuperación agresiva
- 🟩 Robo: CC **Recuperación agresiva**. Mano (1/3 🟩): Recuperación agresiva.
- Marcador jugador 0–0 bot; presión 3; +CC 0; +CF 0; CR 7; mano 1/3 🟩; mazo restante: 15 CC, 5 CF y 6 CE; CR disponibles: 16.
  - Registro: Roba CC: Recuperación agresiva.

### Turno 23 — 🟩 CC: Centro al área
- 🟩 Robo: CC **Centro al área**. Mano (2/3 🟩 🟩): Recuperación agresiva, Centro al área.
- Marcador jugador 0–0 bot; presión 3; +CC 0; +CF 0; CR 7; mano 2/3 🟩 🟩; mazo restante: 14 CC, 5 CF y 6 CE; CR disponibles: 16.
  - Registro: Roba CC: Centro al área.

### Turno 24 — 🟩 CC: Acción individual
- 🟩 Robo: CC **Acción individual**. Mano (3/3 🟩 🟩 🟩): Recuperación agresiva, Centro al área, Acción individual.
- Marcador jugador 0–0 bot; presión 3; +CC 0; +CF 0; CR 7; mano 3/3 🟩 🟩 🟩; mazo restante: 13 CC, 5 CF y 6 CE; CR disponibles: 16.
  - Registro: Roba CC: Acción individual.

### Turno 25 — 🟩 CC: Construcción desde atrás
- 🟩 Robo: CC **Construcción desde atrás**. Mano (4/3 🟩 🟩 🟩 🟩): Recuperación agresiva, Centro al área, Acción individual, Construcción desde atrás.
- 🟩 Límite de mano: se descarta **Acción individual** (copias: 1; comparaciones utilizables: 0; valor: 100).
- Marcador jugador 0–0 bot; presión 3; +CC 0; +CF 0; CR 7; mano 3/3 🟩 🟩 🟩; mazo restante: 12 CC, 5 CF y 6 CE; CR disponibles: 16.
  - Registro: Roba CC: Construcción desde atrás.
  - Registro: Descarta de la mano: Acción individual.

### Turno 26 — 🟪 CE: Ley de la ventaja
- 🟪 Robo: CE **Ley de la ventaja**.
- 🟪 Opciones de la CE:
  - ⬜ Opción 1: +3 Presión; +1 amarilla rival.
  - ⬜ Opción 2: +1 Presión; tirada de lesión por amarilla (10%); descarta 1 carta(s) del mazo.
  - **✅ Opción 3: -1 Presión; +1 amarilla propia; tirada de lesión por amarilla (10%).**
- 🟪 IA elige **Opción 3**.
- Los robos o CF extra que active el evento se resuelven inmediatamente según el motor.
- Marcador jugador 0–0 bot; presión 2; +CC 0; +CF 0; CR 7; mano 3/3 🟩 🟩 🟩; mazo restante: 12 CC, 5 CF y 5 CE; CR disponibles: 16.
  - Registro: Aparece CE: Ley de la ventaja.
  - Registro: Ley de la ventaja: Opción 3.

### Turno 27 — 🟪 CE: Pérdida de tiempo
- 🟪 Robo: CE **Pérdida de tiempo**.
- 🟪 Opciones de la CE:
  - ⬜ Opción 1: +1 Presión; +1 amarilla rival; descarta 2 carta(s) del mazo.
  - **✅ Opción 2: -4 Presión; +1 CR; descarta 1 CC de la mano.**
  - ⬜ Opción 3: +1 Presión; tirada de lesión por amarilla (10%); descarta 1 carta(s) del mazo.
- 🟪 IA elige **Opción 2**.
- Los robos o CF extra que active el evento se resuelven inmediatamente según el motor.
- 🔴 CR ejecutada: **Robo en medio campo**.
  - ⬜ Opción 1: DEF rival 15 > MED jugador 15 +3 = 18 → +4 Presión.
  - ⬜ Opción 2: MED rival 15 > MED jugador 15 +3 = 18 → +4 Presión.
  - **✅ Opción de reserva: Ninguna acción anterior se cumple → +2 Presión.**
  - ⬜ Esquina inferior izquierda (independiente): Si el rival está perdiendo → +1 amarilla propia.
- Marcador jugador 0–0 bot; presión 2; +CC 0; +CF 0; CR 8; mano 2/3 🟩 🟩; mazo restante: 12 CC, 5 CF y 4 CE; CR disponibles: 16.
  - Registro: Aparece CE: Pérdida de tiempo.
  - Registro: Descarta de la mano: Construcción desde atrás.
  - Registro: Roba CR: Robo en medio campo.
  - Registro: Robo en medio campo: acción de reserva.
  - Registro: Pérdida de tiempo: Opción 2.

### Turno 28 — 🟪 CE: Fuera de juego
- 🟪 Robo: CE **Fuera de juego**.
- 🟪 Opciones de la CE:
  - ⬜ Opción 1: descarta 1 carta(s) del mazo; descarta 2 CC de la mano.
  - ⬜ Opción 2: +2 Presión.
  - **✅ Opción 3: -3 Presión; +1 CR.**
- 🟪 IA elige **Opción 3**.
- Los robos o CF extra que active el evento se resuelven inmediatamente según el motor.
- 🔴 CR ejecutada: **Pase cortado**.
  - ⬜ Opción 1: MED rival 15 > AT jugador 15 +4 = 19 → +4 Presión; recupera 1 CC del descarte.
  - ⬜ Opción 2: MED rival 15 > MED jugador 15 +2 = 17 → +5 Presión.
  - **✅ Opción de reserva: Ninguna acción anterior se cumple → +2 Presión.**
  - ⬜ Esquina inferior izquierda (independiente): Si el rival está perdiendo → descarta 1 CC de la mano.
- Marcador jugador 0–0 bot; presión 2; +CC 0; +CF 0; CR 9; mano 2/3 🟩 🟩; mazo restante: 12 CC, 5 CF y 3 CE; CR disponibles: 16.
  - Registro: Aparece CE: Fuera de juego.
  - Registro: Roba CR: Pase cortado.
  - Registro: Pase cortado: acción de reserva.
  - Registro: Fuera de juego: Opción 3.

### Turno 29 — 🟧 CF: Provocar la falta
- 🟧 Robo: CF **Provocar la falta**. Mano antes de decidir (2/3 🟩 🟩): Recuperación agresiva, Centro al área.
- 🟩 CC 1: **Centro al área — Efecto base**: +1 CF.
- 🟧 Opciones de la CF tras jugar las CC:
  - ⬜ Opción 1: AT jugador 15 🟢 **+1** = 16 > DEF rival 15 +5 = 20 → Tarjeta roja y descarta una carta del mazo.
  - **✅ Opción 2: AT jugador 15 🟢 **+1** = 16 > DEF rival 15 → Tarjeta amarilla y -1 Presión.**
  - ⬜ Opción 3: Fallo: no se supera ninguna comparación anterior → Roba 1 CR y descarta la primera carta del mazo.
- 🟧 CF aplicada: **Tarjeta amarilla y -1 Presión** (nivel 1).
- Marcador jugador 0–0 bot; presión 1; +CC 0; +CF 0; CR 9; mano 1/3 🟩; mazo restante: 12 CC, 4 CF y 3 CE; CR disponibles: 16.
  - Registro: Aparece CF: Provocar la falta.
  - Registro: Juega Centro al área: Efecto base.
  - Registro: Provocar la falta: Tarjeta amarilla y -1 Presión.

### Turno 30 — 🟩 CC: Cambio de orientación
- 🟩 Robo: CC **Cambio de orientación**. Mano (2/3 🟩 🟩): Recuperación agresiva, Cambio de orientación.
- Marcador jugador 0–0 bot; presión 1; +CC 0; +CF 0; CR 9; mano 2/3 🟩 🟩; mazo restante: 11 CC, 4 CF y 3 CE; CR disponibles: 16.
  - Registro: Roba CC: Cambio de orientación.

### Turno 31 — 🟪 CE: Fuera de juego
- 🟪 Robo: CE **Fuera de juego**.
- 🟪 Opciones de la CE:
  - ⬜ Opción 1: descarta 1 carta(s) del mazo; descarta 2 CC de la mano.
  - ⬜ Opción 2: +2 Presión.
  - **✅ Opción 3: -3 Presión; +1 CR.**
- 🟪 IA elige **Opción 3**.
- Los robos o CF extra que active el evento se resuelven inmediatamente según el motor.
- 🔴 CR ejecutada: **Centro al área**.
  - ⬜ Opción 1: MED rival 15 > DEF jugador 15 +4 = 19 → +5 Presión.
  - ⬜ Opción 2: AT rival 15 > DEF jugador 15 +2 = 17 → +4 Presión.
  - **✅ Opción de reserva: Ninguna acción anterior se cumple → +2 Presión.**
  - ⬜ Esquina inferior izquierda (independiente): Si el rival está perdiendo → +1 Presión.
- Marcador jugador 0–0 bot; presión 2; +CC 0; +CF 0; CR 10; mano 2/3 🟩 🟩; mazo restante: 11 CC, 4 CF y 2 CE; CR disponibles: 16.
  - Registro: Aparece CE: Fuera de juego.
  - Registro: Roba CR: Centro al área.
  - Registro: Centro al área: acción de reserva.
  - Registro: Fuera de juego: Opción 3.

### Turno 32 — 🟩 CC: Recuperación agresiva
- 🟩 Robo: CC **Recuperación agresiva**. Mano (3/3 🟩 🟩 🟩): Recuperación agresiva, Cambio de orientación, Recuperación agresiva.
- Marcador jugador 0–0 bot; presión 2; +CC 0; +CF 0; CR 10; mano 3/3 🟩 🟩 🟩; mazo restante: 10 CC, 4 CF y 2 CE; CR disponibles: 16.
  - Registro: Roba CC: Recuperación agresiva.

### Turno 33 — 🟧 CF: Buscar el córner
- 🟧 Robo: CF **Buscar el córner**. Mano antes de decidir (3/3 🟩 🟩 🟩): Recuperación agresiva, Cambio de orientación, Recuperación agresiva.
- 🟩 CC 1: **Recuperación agresiva — Efecto base**: +1 CC.
- 🟩 CC 2: **Recuperación agresiva — Comparación 2**: +2 CF; +1 amarilla rival. Comparación: MED jugador 16 > MED rival 15; superada.
- 🟧 Opciones de la CF tras jugar las CC:
  - ⬜ Opción 1: MED jugador 15 🟢 **+2** = 17 > DEF rival 15 +3 = 18 → -2 Presión.
  - **✅ Opción 2: MED jugador 15 🟢 **+2** = 17 > DEF rival 15 +1 = 16 → -1 Presión.**
  - ⬜ Opción 3: Fallo: no se supera ninguna comparación anterior → +2 Presión y descarta una CC de la mano.
- 🟧 CF aplicada: **-1 Presión** (nivel 1).
- Marcador jugador 0–0 bot; presión 1; +CC 0; +CF 0; CR 10; mano 1/3 🟩; mazo restante: 10 CC, 3 CF y 2 CE; CR disponibles: 16.
  - Registro: Aparece CF: Buscar el córner.
  - Registro: Juega Recuperación agresiva: Efecto base.
  - Registro: Juega Recuperación agresiva: Comparación 2.
  - Registro: Buscar el córner: -1 Presión.

### Turno 34 — 🟩 CC: Control del juego
- 🟩 Robo: CC **Control del juego**. Mano (2/3 🟩 🟩): Cambio de orientación, Control del juego.
- Marcador jugador 0–0 bot; presión 1; +CC 0; +CF 0; CR 10; mano 2/3 🟩 🟩; mazo restante: 9 CC, 3 CF y 2 CE; CR disponibles: 16.
  - Registro: Roba CC: Control del juego.

### Turno 35 — 🟧 CF: Mano a mano
- 🟧 Robo: CF **Mano a mano**. Mano antes de decidir (2/3 🟩 🟩): Cambio de orientación, Control del juego.
- IA: no gasta CC; no puede mejorar la CF de forma rentable.
- 🟧 Opciones de la CF tras jugar las CC:
  - ⬜ Opción 1: AT jugador 15 = 15 > DEF rival 15 +4 = 19 → Gol.
  - ⬜ Opción 2: AT jugador 15 = 15 > DEF rival 15 → Descarta 1 CC de la mano y -1 Presión.
  - **✅ Opción 3: Fallo: no se supera ninguna comparación anterior → Roba 1 CR.**
- 🟧 CF aplicada: **Roba 1 CR** (nivel 0).
- 🔴 CR ejecutada: **Contraataque rival**.
  - ⬜ Opción 1: AT rival 15 > MED jugador 15 +3 = 18 → +1 gol en contra; recupera 1 CC del descarte.
  - ⬜ Opción 2: AT rival 15 > MED jugador 15 → recupera 1 CC del descarte; juega 1 CR adicional(es).
  - **✅ Opción de reserva: Ninguna acción anterior se cumple → +3 Presión.**
  - ⬜ Esquina inferior izquierda (independiente): Si el rival está ganando → +1 amarilla propia; recupera 1 CC del descarte.
- Marcador jugador 0–0 bot; presión 4; +CC 0; +CF 0; CR 11; mano 2/3 🟩 🟩; mazo restante: 9 CC, 2 CF y 2 CE; CR disponibles: 16.
  - Registro: Aparece CF: Mano a mano.
  - Registro: Roba CR: Contraataque rival.
  - Registro: Contraataque rival: acción de reserva.
  - Registro: Mano a mano: Roba 1 CR.

### Turno 36 — 🟧 CF: Buscar el córner
- 🟧 Robo: CF **Buscar el córner**. Mano antes de decidir (2/3 🟩 🟩): Cambio de orientación, Control del juego.
- IA: no gasta CC; no puede mejorar la CF de forma rentable.
- 🟧 Opciones de la CF tras jugar las CC:
  - ⬜ Opción 1: MED jugador 15 = 15 > DEF rival 15 +3 = 18 → -2 Presión.
  - ⬜ Opción 2: MED jugador 15 = 15 > DEF rival 15 +1 = 16 → -1 Presión.
  - **✅ Opción 3: Fallo: no se supera ninguna comparación anterior → +2 Presión y descarta una CC de la mano.**
- 🟧 CF aplicada: **+2 Presión y descarta una CC de la mano** (nivel 0).
- Marcador jugador 0–0 bot; presión 6; +CC 0; +CF 0; CR 11; mano 1/3 🟩; mazo restante: 9 CC, 1 CF y 2 CE; CR disponibles: 16.
  - Registro: Aparece CF: Buscar el córner.
  - Registro: Descarta de la mano: Control del juego.
  - Registro: Buscar el córner: +2 Presión y descarta una CC de la mano.

### Turno 37 — 🟩 CC: Recuperación agresiva
- 🟩 Robo: CC **Recuperación agresiva**. Mano (2/3 🟩 🟩): Cambio de orientación, Recuperación agresiva.
- Marcador jugador 0–0 bot; presión 6; +CC 0; +CF 0; CR 11; mano 2/3 🟩 🟩; mazo restante: 8 CC, 1 CF y 2 CE; CR disponibles: 16.
  - Registro: Roba CC: Recuperación agresiva.

### Turno 38 — 🟩 CC: Recuperación agresiva
- 🟩 Robo: CC **Recuperación agresiva**. Mano (3/3 🟩 🟩 🟩): Cambio de orientación, Recuperación agresiva, Recuperación agresiva.
- Marcador jugador 0–0 bot; presión 6; +CC 0; +CF 0; CR 11; mano 3/3 🟩 🟩 🟩; mazo restante: 7 CC, 1 CF y 2 CE; CR disponibles: 16.
  - Registro: Roba CC: Recuperación agresiva.

### Turno 39 — 🟩 CC: Balón al espacio
- 🟩 Robo: CC **Balón al espacio**. Mano (4/3 🟩 🟩 🟩 🟩): Cambio de orientación, Recuperación agresiva, Recuperación agresiva, Balón al espacio.
- 🟩 Límite de mano: se descarta **Cambio de orientación** (copias: 1; comparaciones utilizables: 0; valor: 75).
- Marcador jugador 0–0 bot; presión 6; +CC 0; +CF 0; CR 11; mano 3/3 🟩 🟩 🟩; mazo restante: 6 CC, 1 CF y 2 CE; CR disponibles: 16.
  - Registro: Roba CC: Balón al espacio.
  - Registro: Descarta de la mano: Cambio de orientación.

### Turno 40 — 🟪 CE: Ley de la ventaja
- 🟪 Robo: CE **Ley de la ventaja**.
- 🟪 Opciones de la CE:
  - ⬜ Opción 1: +3 Presión; +1 amarilla rival.
  - ⬜ Opción 2: +1 Presión; tirada de lesión por amarilla (10%); descarta 1 carta(s) del mazo.
  - **✅ Opción 3: -1 Presión; +1 amarilla propia; tirada de lesión por amarilla (10%).**
- 🟪 IA elige **Opción 3**.
- Los robos o CF extra que active el evento se resuelven inmediatamente según el motor.
- Marcador jugador 0–0 bot; presión 5; +CC 0; +CF 0; CR 11; mano 3/3 🟩 🟩 🟩; mazo restante: 6 CC, 1 CF y 1 CE; CR disponibles: 16.
  - Registro: Aparece CE: Ley de la ventaja.
  - Registro: Ley de la ventaja: Opción 3.

### Turno 41 — 🟧 CF: Remate de cabeza
- 🟧 Robo: CF **Remate de cabeza**. Mano antes de decidir (3/3 🟩 🟩 🟩): Recuperación agresiva, Recuperación agresiva, Balón al espacio.
- 🟩 CC 1: **Balón al espacio — Efecto base**: +2 CF; +1 Presión.
- 🟧 Opciones de la CF tras jugar las CC:
  - ⬜ Opción 1: AT jugador 15 🟢 **+2** = 17 > DEF rival 15 +4 = 19 → Gol.
  - **✅ Opción 2: AT jugador 15 🟢 **+2** = 17 > DEF rival 15 +1 = 16 → Descarta la primera carta del mazo y -1 Presión.**
  - ⬜ Opción 3: Fallo: no se supera ninguna comparación anterior → Roba 1 CR y -1 Presión.
- 🟧 CF aplicada: **Descarta la primera carta del mazo y -1 Presión** (nivel 1).
- Marcador jugador 0–0 bot; presión 5; +CC 0; +CF 0; CR 11; mano 2/3 🟩 🟩; mazo restante: 5 CC, 0 CF y 1 CE; CR disponibles: 16.
  - Registro: Aparece CF: Remate de cabeza.
  - Registro: Juega Balón al espacio: Efecto base.
  - Registro: Descarta del mazo: Triangulación de equipo.
  - Registro: Remate de cabeza: Descarta la primera carta del mazo y -1 Presión.

### Turno 42 — 🟩 CC: Control del juego
- 🟩 Robo: CC **Control del juego**. Mano (3/3 🟩 🟩 🟩): Recuperación agresiva, Recuperación agresiva, Control del juego.
- Marcador jugador 0–0 bot; presión 5; +CC 0; +CF 0; CR 11; mano 3/3 🟩 🟩 🟩; mazo restante: 4 CC, 0 CF y 1 CE; CR disponibles: 16.
  - Registro: Roba CC: Control del juego.

### Turno 43 — 🟩 CC: Centro al área
- 🟩 Robo: CC **Centro al área**. Mano (4/3 🟩 🟩 🟩 🟩): Recuperación agresiva, Recuperación agresiva, Control del juego, Centro al área.
- 🟩 Límite de mano: se descarta **Control del juego** (copias: 1; comparaciones utilizables: 0; valor: 55).
- Marcador jugador 0–0 bot; presión 5; +CC 0; +CF 0; CR 11; mano 3/3 🟩 🟩 🟩; mazo restante: 3 CC, 0 CF y 1 CE; CR disponibles: 16.
  - Registro: Roba CC: Centro al área.
  - Registro: Descarta de la mano: Control del juego.

### Turno 44 — 🟩 CC: Construcción desde atrás
- 🟩 Robo: CC **Construcción desde atrás**. Mano (4/3 🟩 🟩 🟩 🟩): Recuperación agresiva, Recuperación agresiva, Centro al área, Construcción desde atrás.
- 🟩 Límite de mano: se descarta **Construcción desde atrás** (copias: 1; comparaciones utilizables: 0; valor: 100).
- Marcador jugador 0–0 bot; presión 5; +CC 0; +CF 0; CR 11; mano 3/3 🟩 🟩 🟩; mazo restante: 2 CC, 0 CF y 1 CE; CR disponibles: 16.
  - Registro: Roba CC: Construcción desde atrás.
  - Registro: Descarta de la mano: Construcción desde atrás.

### Turno 45 — 🟩 CC: Pase entre líneas
- 🟩 Robo: CC **Pase entre líneas**. Mano (4/3 🟩 🟩 🟩 🟩): Recuperación agresiva, Recuperación agresiva, Centro al área, Pase entre líneas.
- 🟩 Límite de mano: se descarta **Pase entre líneas** (copias: 1; comparaciones utilizables: 0; valor: 40).
- Marcador jugador 0–0 bot; presión 5; +CC 0; +CF 0; CR 11; mano 3/3 🟩 🟩 🟩; mazo restante: 1 CC, 0 CF y 1 CE; CR disponibles: 16.
  - Registro: Roba CC: Pase entre líneas.
  - Registro: Descarta de la mano: Pase entre líneas.

### Turno 46 — 🟩 CC: Apertura a banda
- 🟩 Robo: CC **Apertura a banda**. Mano (4/3 🟩 🟩 🟩 🟩): Recuperación agresiva, Recuperación agresiva, Centro al área, Apertura a banda.
- 🟩 Límite de mano: se descarta **Apertura a banda** (copias: 1; comparaciones utilizables: 0; valor: 100).
- Marcador jugador 0–0 bot; presión 5; +CC 0; +CF 0; CR 11; mano 3/3 🟩 🟩 🟩; mazo restante: 0 CC, 0 CF y 1 CE; CR disponibles: 16.
  - Registro: Roba CC: Apertura a banda.
  - Registro: Descarta de la mano: Apertura a banda.

### Turno 47 — 🟪 CE: VAR
- 🟪 Robo: CE **VAR**.
- 🟪 Opciones de la CE:
  - ⬜ Opción 1: +3 Presión; +1 amarilla rival.
  - **✅ Opción 2: -3 Presión; +1 CR.**
  - ⬜ Opción 3: +2 Presión; recupera 1 CC del descarte.
- 🟪 IA elige **Opción 2**.
- Los robos o CF extra que active el evento se resuelven inmediatamente según el motor.
- 🔴 CR ejecutada: **Robo en medio campo**.
  - ⬜ Opción 1: DEF rival 15 > MED jugador 15 +3 = 18 → +4 Presión.
  - ⬜ Opción 2: MED rival 15 > MED jugador 15 +3 = 18 → +4 Presión.
  - **✅ Opción de reserva: Ninguna acción anterior se cumple → +2 Presión.**
  - ⬜ Esquina inferior izquierda (independiente): Si el rival está perdiendo → +1 amarilla propia.
- Marcador jugador 0–0 bot; presión 4; +CC 0; +CF 0; CR 12; mano 3/3 🟩 🟩 🟩; mazo restante: 0 CC, 0 CF y 0 CE; CR disponibles: 16.
  - Registro: Aparece CE: VAR.
  - Registro: Roba CR: Robo en medio campo.
  - Registro: Robo en medio campo: acción de reserva.
  - Registro: VAR: Opción 2.

## Resultado final

### 🤝 Marcador final: Jugador 0 – 0 Bot

| Métrica | Resultado |
| --- | ---: |
| Goles del jugador | **0** |
| Goles del bot por presión | **0** |
| Goles del bot por CR | **0** |
| 🟨 Amarillas al rival | **2** |
| 🟥 Rojas al rival | **0** |
| 🟨 Amarillas propias | **3** |
| 🟥 Rojas propias | **0** |
| CR robadas | **12** |
| Presión final | **4** |
| CE resueltas | **10** |
| CF resueltas | **11** |
| CC finales en mano | **3** |
| Sustituciones por lesión | **0** |
