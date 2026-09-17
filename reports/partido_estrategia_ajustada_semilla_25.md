# Partido simulado paso a paso — BG FÚTBOL

- Semilla reproducible: `25`
- Jugador: DEF 15 · MED 15 · AT 10
- Bot: DEF 15 · MED 15 · AT 10
- Mazo: 28 CC, 12 CF y 10 CE
- Mano inicial: 0 CC; límite: 5 CC
- Gol del bot: al superar presión 9, la presión vuelve a 0
- Estrategia: buscar 1–0; conservar CC hasta 2 CR y después minimizar CR

## Leyenda visual

- 🟩 **CC** — carta de control: entra en la mano.
- 🟧 **CF** — carta de finalización: permite jugar CC y se resuelve.
- 🟪 **CE** — carta de evento: la IA elige una de sus tres opciones.
- 🟢 **+n** — bono +CF que las CC aplican al atributo del jugador en una CF.

## Desarrollo completo

### Turno 1 — 🟩 CC: Acción individual
- 🟩 Robo: CC **Acción individual**. Mano (1/5 🟩): Acción individual.
- Marcador jugador 0–0 bot; presión 0; +CC 0; +CF 0; CR 0; mano 1/5 🟩; mazo restante: 27 CC, 12 CF y 10 CE.
  - Registro: Roba CC: Acción individual.

### Turno 2 — 🟩 CC: Construcción desde atrás
- 🟩 Robo: CC **Construcción desde atrás**. Mano (2/5 🟩 🟩): Acción individual, Construcción desde atrás.
- Marcador jugador 0–0 bot; presión 0; +CC 0; +CF 0; CR 0; mano 2/5 🟩 🟩; mazo restante: 26 CC, 12 CF y 10 CE.
  - Registro: Roba CC: Construcción desde atrás.

### Turno 3 — 🟩 CC: Balón al espacio
- 🟩 Robo: CC **Balón al espacio**. Mano (3/5 🟩 🟩 🟩): Acción individual, Construcción desde atrás, Balón al espacio.
- Marcador jugador 0–0 bot; presión 0; +CC 0; +CF 0; CR 0; mano 3/5 🟩 🟩 🟩; mazo restante: 25 CC, 12 CF y 10 CE.
  - Registro: Roba CC: Balón al espacio.

### Turno 4 — 🟩 CC: Centro al área
- 🟩 Robo: CC **Centro al área**. Mano (4/5 🟩 🟩 🟩 🟩): Acción individual, Construcción desde atrás, Balón al espacio, Centro al área.
- Marcador jugador 0–0 bot; presión 0; +CC 0; +CF 0; CR 0; mano 4/5 🟩 🟩 🟩 🟩; mazo restante: 24 CC, 12 CF y 10 CE.
  - Registro: Roba CC: Centro al área.

### Turno 5 — 🟪 CE: Pérdida de tiempo
- 🟪 Robo: CE **Pérdida de tiempo**.
- 🟪 Opciones de la CE:
  - ⬜ Opción 1: +1 Presión; descarta 2 carta(s) del mazo.
  - ⬜ Opción 2: descarta 1 carta(s) del mazo.
  - **✅ Opción 3: +1 Presión.**
- 🟪 IA elige **Opción 3**.
- Los robos o CF extra que active el evento se resuelven inmediatamente según el motor.
- Marcador jugador 0–0 bot; presión 1; +CC 0; +CF 0; CR 0; mano 4/5 🟩 🟩 🟩 🟩; mazo restante: 24 CC, 12 CF y 9 CE.
  - Registro: Aparece CE: Pérdida de tiempo.
  - Registro: Pérdida de tiempo: Opción 3.

### Turno 6 — 🟧 CF: Pase de la muerte
- 🟧 Robo: CF **Pase de la muerte**. Mano antes de decidir (4/5 🟩 🟩 🟩 🟩): Acción individual, Construcción desde atrás, Balón al espacio, Centro al área.
- 🟩 CC 1: **Balón al espacio — Efecto base**: +2 CF; +1 Presión.
- 🟩 CC 2: **Acción individual — Efecto base**: +1 CF.
- 🟩 CC 3: **Construcción desde atrás — Efecto base**: +1 CC.
- 🟩 CC 4: **Centro al área — Comparación 1**: +2 CF. Comparación: MED jugador 16 >= DEF rival 16; superada.
- 🟧 Opciones de la CF tras jugar las CC:
  - **✅ Opción 1: MED jugador 15 🟢 **+2** 🟢 **+1** 🟢 **+2** = 20 > DEF rival 15 +4 = 19 → Gol.**
  - ⬜ Opción 2: MED jugador 15 🟢 **+2** 🟢 **+1** 🟢 **+2** = 20 > DEF rival 15 +2 = 17 → -1 Presión.
  - ⬜ Opción 3: Fallo: no se supera ninguna comparación anterior → Roba 1 CR.
- 🟧 CF aplicada: **Gol** (nivel 2).
- Marcador jugador 1–0 bot; presión 2; +CC 0; +CF 0; CR 0; mano 0/5; mazo restante: 24 CC, 11 CF y 9 CE.
  - Registro: Aparece CF: Pase de la muerte.
  - Registro: Juega Balón al espacio: Efecto base.
  - Registro: Juega Acción individual: Efecto base.
  - Registro: Juega Construcción desde atrás: Efecto base.
  - Registro: Juega Centro al área: Comparación 1.
  - Registro: Pase de la muerte: Gol.

### Turno 7 — 🟩 CC: Construcción desde atrás
- 🟩 Robo: CC **Construcción desde atrás**. Mano (1/5 🟩): Construcción desde atrás.
- Marcador jugador 1–0 bot; presión 2; +CC 0; +CF 0; CR 0; mano 1/5 🟩; mazo restante: 23 CC, 11 CF y 9 CE.
  - Registro: Roba CC: Construcción desde atrás.

### Turno 8 — 🟩 CC: Triangulación de equipo
- 🟩 Robo: CC **Triangulación de equipo**. Mano (2/5 🟩 🟩): Construcción desde atrás, Triangulación de equipo.
- Marcador jugador 1–0 bot; presión 2; +CC 0; +CF 0; CR 0; mano 2/5 🟩 🟩; mazo restante: 22 CC, 11 CF y 9 CE.
  - Registro: Roba CC: Triangulación de equipo.

### Turno 9 — 🟪 CE: Fuera de juego
- 🟪 Robo: CE **Fuera de juego**.
- 🟪 Opciones de la CE:
  - **✅ Opción 1: descarta 1 carta(s) del mazo; descarta 1 CC de la mano.**
  - ⬜ Opción 2: +2 Presión.
  - ⬜ Opción 3: -3 Presión; +1 CR.
- 🟪 IA elige **Opción 1**.
- Los robos o CF extra que active el evento se resuelven inmediatamente según el motor.
- Marcador jugador 1–0 bot; presión 2; +CC 0; +CF 0; CR 0; mano 1/5 🟩; mazo restante: 22 CC, 11 CF y 7 CE.
  - Registro: Aparece CE: Fuera de juego.
  - Registro: Descarta del mazo: Ley de la ventaja.
  - Registro: Descarta de la mano: Triangulación de equipo.
  - Registro: Fuera de juego: Opción 1.

### Turno 10 — 🟧 CF: Buscar el córner
- 🟧 Robo: CF **Buscar el córner**. Mano antes de decidir (1/5 🟩): Construcción desde atrás.
- IA: no gasta CC; no puede mejorar la CF de forma rentable.
- 🟧 Opciones de la CF tras jugar las CC:
  - ⬜ Opción 1: MED jugador 15 = 15 > DEF rival 15 +3 = 18 → -2 Presión.
  - ⬜ Opción 2: MED jugador 15 = 15 > DEF rival 15 +1 = 16 → -1 Presión.
  - **✅ Opción 3: Fallo: no se supera ninguna comparación anterior → +2 Presión.**
- 🟧 CF aplicada: **+2 Presión** (nivel 0).
- Marcador jugador 1–0 bot; presión 4; +CC 0; +CF 0; CR 0; mano 1/5 🟩; mazo restante: 22 CC, 10 CF y 7 CE.
  - Registro: Aparece CF: Buscar el córner.
  - Registro: Buscar el córner: +2 Presión.

### Turno 11 — 🟩 CC: Control del juego
- 🟩 Robo: CC **Control del juego**. Mano (2/5 🟩 🟩): Construcción desde atrás, Control del juego.
- Marcador jugador 1–0 bot; presión 4; +CC 0; +CF 0; CR 0; mano 2/5 🟩 🟩; mazo restante: 21 CC, 10 CF y 7 CE.
  - Registro: Roba CC: Control del juego.

### Turno 12 — 🟩 CC: Recuperación agresiva
- 🟩 Robo: CC **Recuperación agresiva**. Mano (3/5 🟩 🟩 🟩): Construcción desde atrás, Control del juego, Recuperación agresiva.
- Marcador jugador 1–0 bot; presión 4; +CC 0; +CF 0; CR 0; mano 3/5 🟩 🟩 🟩; mazo restante: 20 CC, 10 CF y 7 CE.
  - Registro: Roba CC: Recuperación agresiva.

### Turno 13 — 🟩 CC: Recuperación agresiva
- 🟩 Robo: CC **Recuperación agresiva**. Mano (4/5 🟩 🟩 🟩 🟩): Construcción desde atrás, Control del juego, Recuperación agresiva, Recuperación agresiva.
- Marcador jugador 1–0 bot; presión 4; +CC 0; +CF 0; CR 0; mano 4/5 🟩 🟩 🟩 🟩; mazo restante: 19 CC, 10 CF y 7 CE.
  - Registro: Roba CC: Recuperación agresiva.

### Turno 14 — 🟩 CC: Balón al espacio
- 🟩 Robo: CC **Balón al espacio**. Mano (5/5 🟩 🟩 🟩 🟩 🟩): Construcción desde atrás, Control del juego, Recuperación agresiva, Recuperación agresiva, Balón al espacio.
- Marcador jugador 1–0 bot; presión 4; +CC 0; +CF 0; CR 0; mano 5/5 🟩 🟩 🟩 🟩 🟩; mazo restante: 18 CC, 10 CF y 7 CE.
  - Registro: Roba CC: Balón al espacio.

### Turno 15 — 🟧 CF: Remate de cabeza
- 🟧 Robo: CF **Remate de cabeza**. Mano antes de decidir (5/5 🟩 🟩 🟩 🟩 🟩): Construcción desde atrás, Control del juego, Recuperación agresiva, Recuperación agresiva, Balón al espacio.
- 🟩 CC 1: **Recuperación agresiva — Comparación 1**: -2 Presión. Comparación: DEF jugador 15 >= MED rival 15; superada.
- 🟩 CC 2: **Recuperación agresiva — Comparación 1**: -2 Presión. Comparación: DEF jugador 15 >= MED rival 15; superada.
- 🟧 Opciones de la CF tras jugar las CC:
  - ⬜ Opción 1: AT jugador 10 = 10 > DEF rival 15 +3 = 18 → Gol.
  - ⬜ Opción 2: AT jugador 10 = 10 > DEF rival 15 → Descarta la primera carta del mazo.
  - **✅ Opción 3: Fallo: no se supera ninguna comparación anterior → Roba 1 CR.**
- 🟧 CF aplicada: **Roba 1 CR** (nivel 0).
- Marcador jugador 1–0 bot; presión 0; +CC 0; +CF 0; CR 1; mano 3/5 🟩 🟩 🟩; mazo restante: 18 CC, 9 CF y 7 CE.
  - Registro: Aparece CF: Remate de cabeza.
  - Registro: Juega Recuperación agresiva: Comparación 1.
  - Registro: Juega Recuperación agresiva: Comparación 1.
  - Registro: Remate de cabeza: Roba 1 CR.

### Turno 16 — 🟩 CC: Cambio de orientación
- 🟩 Robo: CC **Cambio de orientación**. Mano (4/5 🟩 🟩 🟩 🟩): Construcción desde atrás, Control del juego, Balón al espacio, Cambio de orientación.
- Marcador jugador 1–0 bot; presión 0; +CC 0; +CF 0; CR 1; mano 4/5 🟩 🟩 🟩 🟩; mazo restante: 17 CC, 9 CF y 7 CE.
  - Registro: Roba CC: Cambio de orientación.

### Turno 17 — 🟩 CC: Balón al espacio
- 🟩 Robo: CC **Balón al espacio**. Mano (5/5 🟩 🟩 🟩 🟩 🟩): Construcción desde atrás, Control del juego, Balón al espacio, Cambio de orientación, Balón al espacio.
- Marcador jugador 1–0 bot; presión 0; +CC 0; +CF 0; CR 1; mano 5/5 🟩 🟩 🟩 🟩 🟩; mazo restante: 16 CC, 9 CF y 7 CE.
  - Registro: Roba CC: Balón al espacio.

### Turno 18 — 🟩 CC: Pase entre líneas
- 🟩 Robo: CC **Pase entre líneas**. Mano (6/5 🟩 🟩 🟩 🟩 🟩 🟩): Construcción desde atrás, Control del juego, Balón al espacio, Cambio de orientación, Balón al espacio, Pase entre líneas.
- 🟩 Límite de mano: se descarta **Pase entre líneas** (copias: 1; comparaciones utilizables: 0; valor: 40).
- Marcador jugador 1–0 bot; presión 0; +CC 0; +CF 0; CR 1; mano 5/5 🟩 🟩 🟩 🟩 🟩; mazo restante: 15 CC, 9 CF y 7 CE.
  - Registro: Roba CC: Pase entre líneas.
  - Registro: Descarta de la mano: Pase entre líneas.

### Turno 19 — 🟪 CE: Pérdida de tiempo
- 🟪 Robo: CE **Pérdida de tiempo**.
- 🟪 Opciones de la CE:
  - ⬜ Opción 1: +1 Presión; descarta 2 carta(s) del mazo.
  - **✅ Opción 2: descarta 1 carta(s) del mazo.**
  - ⬜ Opción 3: +1 Presión.
- 🟪 IA elige **Opción 2**.
- Los robos o CF extra que active el evento se resuelven inmediatamente según el motor.
- Marcador jugador 1–0 bot; presión 0; +CC 0; +CF 0; CR 1; mano 5/5 🟩 🟩 🟩 🟩 🟩; mazo restante: 14 CC, 9 CF y 6 CE.
  - Registro: Aparece CE: Pérdida de tiempo.
  - Registro: Descarta del mazo: Triangulación de equipo.
  - Registro: Pérdida de tiempo: Opción 2.

### Turno 20 — 🟪 CE: Fuera de juego
- 🟪 Robo: CE **Fuera de juego**.
- 🟪 Opciones de la CE:
  - **✅ Opción 1: descarta 1 carta(s) del mazo; descarta 1 CC de la mano.**
  - ⬜ Opción 2: +2 Presión.
  - ⬜ Opción 3: -3 Presión; +1 CR.
- 🟪 IA elige **Opción 1**.
- Los robos o CF extra que active el evento se resuelven inmediatamente según el motor.
- Marcador jugador 1–0 bot; presión 0; +CC 0; +CF 0; CR 1; mano 4/5 🟩 🟩 🟩 🟩; mazo restante: 13 CC, 9 CF y 5 CE.
  - Registro: Aparece CE: Fuera de juego.
  - Registro: Descarta del mazo: Construcción desde atrás.
  - Registro: Descarta de la mano: Cambio de orientación.
  - Registro: Fuera de juego: Opción 1.

### Turno 21 — 🟩 CC: Control del juego
- 🟩 Robo: CC **Control del juego**. Mano (5/5 🟩 🟩 🟩 🟩 🟩): Construcción desde atrás, Control del juego, Balón al espacio, Balón al espacio, Control del juego.
- Marcador jugador 1–0 bot; presión 0; +CC 0; +CF 0; CR 1; mano 5/5 🟩 🟩 🟩 🟩 🟩; mazo restante: 12 CC, 9 CF y 5 CE.
  - Registro: Roba CC: Control del juego.

### Turno 22 — 🟧 CF: Remate de cabeza
- 🟧 Robo: CF **Remate de cabeza**. Mano antes de decidir (5/5 🟩 🟩 🟩 🟩 🟩): Construcción desde atrás, Control del juego, Balón al espacio, Balón al espacio, Control del juego.
- IA: no gasta CC; no puede mejorar la CF de forma rentable.
- 🟧 Opciones de la CF tras jugar las CC:
  - ⬜ Opción 1: AT jugador 10 = 10 > DEF rival 15 +3 = 18 → Gol.
  - ⬜ Opción 2: AT jugador 10 = 10 > DEF rival 15 → Descarta la primera carta del mazo.
  - **✅ Opción 3: Fallo: no se supera ninguna comparación anterior → Roba 1 CR.**
- 🟧 CF aplicada: **Roba 1 CR** (nivel 0).
- Marcador jugador 1–0 bot; presión 0; +CC 0; +CF 0; CR 2; mano 5/5 🟩 🟩 🟩 🟩 🟩; mazo restante: 12 CC, 8 CF y 5 CE.
  - Registro: Aparece CF: Remate de cabeza.
  - Registro: Remate de cabeza: Roba 1 CR.

### Turno 23 — 🟩 CC: Cambio de orientación
- 🟩 Robo: CC **Cambio de orientación**. Mano (6/5 🟩 🟩 🟩 🟩 🟩 🟩): Construcción desde atrás, Control del juego, Balón al espacio, Balón al espacio, Control del juego, Cambio de orientación.
- 🟩 Límite de mano: se descarta **Cambio de orientación** (copias: 1; comparaciones utilizables: 0; valor: 75).
- Marcador jugador 1–0 bot; presión 0; +CC 0; +CF 0; CR 2; mano 5/5 🟩 🟩 🟩 🟩 🟩; mazo restante: 11 CC, 8 CF y 5 CE.
  - Registro: Roba CC: Cambio de orientación.
  - Registro: Descarta de la mano: Cambio de orientación.

### Turno 24 — 🟧 CF: Provocar la falta
- 🟧 Robo: CF **Provocar la falta**. Mano antes de decidir (5/5 🟩 🟩 🟩 🟩 🟩): Construcción desde atrás, Control del juego, Balón al espacio, Balón al espacio, Control del juego.
- IA: no gasta CC; no puede mejorar la CF de forma rentable.
- 🟧 Opciones de la CF tras jugar las CC:
  - ⬜ Opción 1: AT jugador 10 = 10 > DEF rival 15 +4 = 19 → Tarjeta roja.
  - ⬜ Opción 2: AT jugador 10 = 10 > DEF rival 15 → Tarjeta amarilla.
  - **✅ Opción 3: Fallo: no se supera ninguna comparación anterior → Roba 1 CR.**
- 🟧 CF aplicada: **Roba 1 CR** (nivel 0).
- Marcador jugador 1–0 bot; presión 0; +CC 0; +CF 0; CR 3; mano 5/5 🟩 🟩 🟩 🟩 🟩; mazo restante: 11 CC, 7 CF y 5 CE.
  - Registro: Aparece CF: Provocar la falta.
  - Registro: Provocar la falta: Roba 1 CR.

### Turno 25 — 🟪 CE: Fuera de juego
- 🟪 Robo: CE **Fuera de juego**.
- 🟪 Opciones de la CE:
  - **✅ Opción 1: descarta 1 carta(s) del mazo; descarta 1 CC de la mano.**
  - ⬜ Opción 2: +2 Presión.
  - ⬜ Opción 3: -3 Presión; +1 CR.
- 🟪 IA elige **Opción 1**.
- Los robos o CF extra que active el evento se resuelven inmediatamente según el motor.
- Marcador jugador 1–0 bot; presión 0; +CC 0; +CF 0; CR 3; mano 4/5 🟩 🟩 🟩 🟩; mazo restante: 10 CC, 7 CF y 4 CE.
  - Registro: Aparece CE: Fuera de juego.
  - Registro: Descarta del mazo: Centro al área.
  - Registro: Descarta de la mano: Control del juego.
  - Registro: Fuera de juego: Opción 1.

### Turno 26 — 🟧 CF: Disparo lejano
- 🟧 Robo: CF **Disparo lejano**. Mano antes de decidir (4/5 🟩 🟩 🟩 🟩): Construcción desde atrás, Balón al espacio, Balón al espacio, Control del juego.
- IA: no gasta CC; no puede mejorar la CF de forma rentable.
- 🟧 Opciones de la CF tras jugar las CC:
  - ⬜ Opción 1: AT jugador 10 = 10 > DEF rival 15 +4 = 19 → Gol.
  - ⬜ Opción 2: AT jugador 10 = 10 > DEF rival 15 → -1 Presión.
  - **✅ Opción 3: Fallo: no se supera ninguna comparación anterior → Nada.**
- 🟧 CF aplicada: **Nada** (nivel 0).
- Marcador jugador 1–0 bot; presión 0; +CC 0; +CF 0; CR 3; mano 4/5 🟩 🟩 🟩 🟩; mazo restante: 10 CC, 6 CF y 4 CE.
  - Registro: Aparece CF: Disparo lejano.
  - Registro: Disparo lejano: Nada.

### Turno 27 — 🟪 CE: Ley de la ventaja
- 🟪 Robo: CE **Ley de la ventaja**.
- 🟪 Opciones de la CE:
  - **✅ Opción 1: +2 Presión; +1 amarilla rival.**
  - ⬜ Opción 2: tirada de lesión por amarilla (10%); roba 1 carta del mazo.
  - ⬜ Opción 3: -1 Presión; +1 amarilla propia; tirada de lesión por amarilla (10%).
- 🟪 IA elige **Opción 1**.
- Los robos o CF extra que active el evento se resuelven inmediatamente según el motor.
- Marcador jugador 1–0 bot; presión 2; +CC 0; +CF 0; CR 3; mano 4/5 🟩 🟩 🟩 🟩; mazo restante: 10 CC, 6 CF y 3 CE.
  - Registro: Aparece CE: Ley de la ventaja.
  - Registro: Ley de la ventaja: Opción 1.

### Turno 28 — 🟩 CC: Acción individual
- 🟩 Robo: CC **Acción individual**. Mano (5/5 🟩 🟩 🟩 🟩 🟩): Construcción desde atrás, Balón al espacio, Balón al espacio, Control del juego, Acción individual.
- Marcador jugador 1–0 bot; presión 2; +CC 0; +CF 0; CR 3; mano 5/5 🟩 🟩 🟩 🟩 🟩; mazo restante: 9 CC, 6 CF y 3 CE.
  - Registro: Roba CC: Acción individual.

### Turno 29 — 🟧 CF: Buscar el córner
- 🟧 Robo: CF **Buscar el córner**. Mano antes de decidir (5/5 🟩 🟩 🟩 🟩 🟩): Construcción desde atrás, Balón al espacio, Balón al espacio, Control del juego, Acción individual.
- 🟩 CC 1: **Balón al espacio — Efecto base**: +2 CF; +1 Presión.
- 🟩 CC 2: **Construcción desde atrás — Efecto base**: +1 CC.
- 🟩 CC 3: **Control del juego — Comparación 1**: -2 Presión. Comparación: MED jugador 16 >= MED rival 16; superada.
- 🟧 Opciones de la CF tras jugar las CC:
  - ⬜ Opción 1: MED jugador 15 🟢 **+2** = 17 > DEF rival 15 +3 = 18 → -2 Presión.
  - **✅ Opción 2: MED jugador 15 🟢 **+2** = 17 > DEF rival 15 +1 = 16 → -1 Presión.**
  - ⬜ Opción 3: Fallo: no se supera ninguna comparación anterior → +2 Presión.
- 🟧 CF aplicada: **-1 Presión** (nivel 1).
- Marcador jugador 1–0 bot; presión 0; +CC 0; +CF 0; CR 3; mano 2/5 🟩 🟩; mazo restante: 9 CC, 5 CF y 3 CE.
  - Registro: Aparece CF: Buscar el córner.
  - Registro: Juega Balón al espacio: Efecto base.
  - Registro: Juega Construcción desde atrás: Efecto base.
  - Registro: Juega Control del juego: Comparación 1.
  - Registro: Buscar el córner: -1 Presión.

### Turno 30 — 🟩 CC: Recuperación agresiva
- 🟩 Robo: CC **Recuperación agresiva**. Mano (3/5 🟩 🟩 🟩): Balón al espacio, Acción individual, Recuperación agresiva.
- Marcador jugador 1–0 bot; presión 0; +CC 0; +CF 0; CR 3; mano 3/5 🟩 🟩 🟩; mazo restante: 8 CC, 5 CF y 3 CE.
  - Registro: Roba CC: Recuperación agresiva.

### Turno 31 — 🟩 CC: Triangulación de equipo
- 🟩 Robo: CC **Triangulación de equipo**. Mano (4/5 🟩 🟩 🟩 🟩): Balón al espacio, Acción individual, Recuperación agresiva, Triangulación de equipo.
- Marcador jugador 1–0 bot; presión 0; +CC 0; +CF 0; CR 3; mano 4/5 🟩 🟩 🟩 🟩; mazo restante: 7 CC, 5 CF y 3 CE.
  - Registro: Roba CC: Triangulación de equipo.

### Turno 32 — 🟩 CC: Construcción desde atrás
- 🟩 Robo: CC **Construcción desde atrás**. Mano (5/5 🟩 🟩 🟩 🟩 🟩): Balón al espacio, Acción individual, Recuperación agresiva, Triangulación de equipo, Construcción desde atrás.
- Marcador jugador 1–0 bot; presión 0; +CC 0; +CF 0; CR 3; mano 5/5 🟩 🟩 🟩 🟩 🟩; mazo restante: 6 CC, 5 CF y 3 CE.
  - Registro: Roba CC: Construcción desde atrás.

### Turno 33 — 🟧 CF: Mano a mano
- 🟧 Robo: CF **Mano a mano**. Mano antes de decidir (5/5 🟩 🟩 🟩 🟩 🟩): Balón al espacio, Acción individual, Recuperación agresiva, Triangulación de equipo, Construcción desde atrás.
- IA: no gasta CC; no puede mejorar la CF de forma rentable.
- 🟧 Opciones de la CF tras jugar las CC:
  - ⬜ Opción 1: AT jugador 10 = 10 > DEF rival 15 +3 = 18 → Gol.
  - ⬜ Opción 2: AT jugador 10 = 10 > DEF rival 15 → +1 Presión.
  - **✅ Opción 3: Fallo: no se supera ninguna comparación anterior → Roba 1 CR.**
- 🟧 CF aplicada: **Roba 1 CR** (nivel 0).
- Marcador jugador 1–0 bot; presión 0; +CC 0; +CF 0; CR 4; mano 5/5 🟩 🟩 🟩 🟩 🟩; mazo restante: 6 CC, 4 CF y 3 CE.
  - Registro: Aparece CF: Mano a mano.
  - Registro: Mano a mano: Roba 1 CR.

### Turno 34 — 🟩 CC: Centro al área
- 🟩 Robo: CC **Centro al área**. Mano (6/5 🟩 🟩 🟩 🟩 🟩 🟩): Balón al espacio, Acción individual, Recuperación agresiva, Triangulación de equipo, Construcción desde atrás, Centro al área.
- 🟩 Límite de mano: se descarta **Acción individual** (copias: 1; comparaciones utilizables: 0; valor: 100).
- Marcador jugador 1–0 bot; presión 0; +CC 0; +CF 0; CR 4; mano 5/5 🟩 🟩 🟩 🟩 🟩; mazo restante: 5 CC, 4 CF y 3 CE.
  - Registro: Roba CC: Centro al área.
  - Registro: Descarta de la mano: Acción individual.

### Turno 35 — 🟩 CC: Apertura a banda
- 🟩 Robo: CC **Apertura a banda**. Mano (6/5 🟩 🟩 🟩 🟩 🟩 🟩): Balón al espacio, Recuperación agresiva, Triangulación de equipo, Construcción desde atrás, Centro al área, Apertura a banda.
- 🟩 Límite de mano: se descarta **Triangulación de equipo** (copias: 1; comparaciones utilizables: 0; valor: 80).
- Marcador jugador 1–0 bot; presión 0; +CC 0; +CF 0; CR 4; mano 5/5 🟩 🟩 🟩 🟩 🟩; mazo restante: 4 CC, 4 CF y 3 CE.
  - Registro: Roba CC: Apertura a banda.
  - Registro: Descarta de la mano: Triangulación de equipo.

### Turno 36 — 🟧 CF: Pase de la muerte
- 🟧 Robo: CF **Pase de la muerte**. Mano antes de decidir (5/5 🟩 🟩 🟩 🟩 🟩): Balón al espacio, Recuperación agresiva, Construcción desde atrás, Centro al área, Apertura a banda.
- 🟩 CC 1: **Balón al espacio — Efecto base**: +2 CF; +1 Presión.
- 🟩 CC 2: **Centro al área — Efecto base**: +1 CF.
- 🟧 Opciones de la CF tras jugar las CC:
  - ⬜ Opción 1: MED jugador 15 🟢 **+2** 🟢 **+1** = 18 > DEF rival 15 +4 = 19 → Gol.
  - **✅ Opción 2: MED jugador 15 🟢 **+2** 🟢 **+1** = 18 > DEF rival 15 +2 = 17 → -1 Presión.**
  - ⬜ Opción 3: Fallo: no se supera ninguna comparación anterior → Roba 1 CR.
- 🟧 CF aplicada: **-1 Presión** (nivel 1).
- Marcador jugador 1–0 bot; presión 0; +CC 0; +CF 0; CR 4; mano 3/5 🟩 🟩 🟩; mazo restante: 4 CC, 3 CF y 3 CE.
  - Registro: Aparece CF: Pase de la muerte.
  - Registro: Juega Balón al espacio: Efecto base.
  - Registro: Juega Centro al área: Efecto base.
  - Registro: Pase de la muerte: -1 Presión.

### Turno 37 — 🟩 CC: Apertura a banda
- 🟩 Robo: CC **Apertura a banda**. Mano (4/5 🟩 🟩 🟩 🟩): Recuperación agresiva, Construcción desde atrás, Apertura a banda, Apertura a banda.
- Marcador jugador 1–0 bot; presión 0; +CC 0; +CF 0; CR 4; mano 4/5 🟩 🟩 🟩 🟩; mazo restante: 3 CC, 3 CF y 3 CE.
  - Registro: Roba CC: Apertura a banda.

### Turno 38 — 🟪 CE: Pérdida de tiempo
- 🟪 Robo: CE **Pérdida de tiempo**.
- 🟪 Opciones de la CE:
  - ⬜ Opción 1: +1 Presión; descarta 2 carta(s) del mazo.
  - **✅ Opción 2: descarta 1 carta(s) del mazo.**
  - ⬜ Opción 3: +1 Presión.
- 🟪 IA elige **Opción 2**.
- Los robos o CF extra que active el evento se resuelven inmediatamente según el motor.
- Marcador jugador 1–0 bot; presión 0; +CC 0; +CF 0; CR 4; mano 4/5 🟩 🟩 🟩 🟩; mazo restante: 3 CC, 3 CF y 1 CE.
  - Registro: Aparece CE: Pérdida de tiempo.
  - Registro: Descarta del mazo: VAR.
  - Registro: Pérdida de tiempo: Opción 2.

### Turno 39 — 🟩 CC: Recuperación agresiva
- 🟩 Robo: CC **Recuperación agresiva**. Mano (5/5 🟩 🟩 🟩 🟩 🟩): Recuperación agresiva, Construcción desde atrás, Apertura a banda, Apertura a banda, Recuperación agresiva.
- Marcador jugador 1–0 bot; presión 0; +CC 0; +CF 0; CR 4; mano 5/5 🟩 🟩 🟩 🟩 🟩; mazo restante: 2 CC, 3 CF y 1 CE.
  - Registro: Roba CC: Recuperación agresiva.

### Turno 40 — 🟩 CC: Apertura a banda
- 🟩 Robo: CC **Apertura a banda**. Mano (6/5 🟩 🟩 🟩 🟩 🟩 🟩): Recuperación agresiva, Construcción desde atrás, Apertura a banda, Apertura a banda, Recuperación agresiva, Apertura a banda.
- 🟩 Límite de mano: se descarta **Recuperación agresiva** (copias: 2; comparaciones utilizables: 1; valor: 40).
- Marcador jugador 1–0 bot; presión 0; +CC 0; +CF 0; CR 4; mano 5/5 🟩 🟩 🟩 🟩 🟩; mazo restante: 1 CC, 3 CF y 1 CE.
  - Registro: Roba CC: Apertura a banda.
  - Registro: Descarta de la mano: Recuperación agresiva.

### Turno 41 — 🟧 CF: Provocar la falta
- 🟧 Robo: CF **Provocar la falta**. Mano antes de decidir (5/5 🟩 🟩 🟩 🟩 🟩): Construcción desde atrás, Apertura a banda, Apertura a banda, Recuperación agresiva, Apertura a banda.
- 🟩 CC 1: **Apertura a banda — Comparación 1**: +2 CF. Comparación: MED jugador 15 >= DEF rival 15; superada.
- 🟩 CC 2: **Apertura a banda — Comparación 1**: +2 CF. Comparación: MED jugador 15 >= DEF rival 15; superada.
- 🟩 CC 3: **Apertura a banda — Comparación 1**: +2 CF. Comparación: MED jugador 15 >= DEF rival 15; superada.
- 🟧 Opciones de la CF tras jugar las CC:
  - ⬜ Opción 1: AT jugador 10 🟢 **+2** 🟢 **+2** 🟢 **+2** = 16 > DEF rival 15 +4 = 19 → Tarjeta roja.
  - **✅ Opción 2: AT jugador 10 🟢 **+2** 🟢 **+2** 🟢 **+2** = 16 > DEF rival 15 → Tarjeta amarilla.**
  - ⬜ Opción 3: Fallo: no se supera ninguna comparación anterior → Roba 1 CR.
- 🟧 CF aplicada: **Tarjeta amarilla** (nivel 1).
- Marcador jugador 1–0 bot; presión 0; +CC 0; +CF 0; CR 4; mano 2/5 🟩 🟩; mazo restante: 1 CC, 2 CF y 1 CE.
  - Registro: Aparece CF: Provocar la falta.
  - Registro: Juega Apertura a banda: Comparación 1.
  - Registro: Juega Apertura a banda: Comparación 1.
  - Registro: Juega Apertura a banda: Comparación 1.
  - Registro: Provocar la falta: Tarjeta amarilla.

### Turno 42 — 🟧 CF: Mano a mano
- 🟧 Robo: CF **Mano a mano**. Mano antes de decidir (2/5 🟩 🟩): Construcción desde atrás, Recuperación agresiva.
- IA: no gasta CC; no puede mejorar la CF de forma rentable.
- 🟧 Opciones de la CF tras jugar las CC:
  - ⬜ Opción 1: AT jugador 10 = 10 > DEF rival 15 +3 = 18 → Gol.
  - ⬜ Opción 2: AT jugador 10 = 10 > DEF rival 15 → +1 Presión.
  - **✅ Opción 3: Fallo: no se supera ninguna comparación anterior → Roba 1 CR.**
- 🟧 CF aplicada: **Roba 1 CR** (nivel 0).
- Marcador jugador 1–0 bot; presión 0; +CC 0; +CF 0; CR 5; mano 2/5 🟩 🟩; mazo restante: 1 CC, 1 CF y 1 CE.
  - Registro: Aparece CF: Mano a mano.
  - Registro: Mano a mano: Roba 1 CR.

### Turno 43 — 🟩 CC: Pase entre líneas
- 🟩 Robo: CC **Pase entre líneas**. Mano (3/5 🟩 🟩 🟩): Construcción desde atrás, Recuperación agresiva, Pase entre líneas.
- Marcador jugador 1–0 bot; presión 0; +CC 0; +CF 0; CR 5; mano 3/5 🟩 🟩 🟩; mazo restante: 0 CC, 1 CF y 1 CE.
  - Registro: Roba CC: Pase entre líneas.

### Turno 44 — 🟪 CE: Córner
- 🟪 Robo: CE **Córner**.
- 🟪 Opciones de la CE:
  - ⬜ Opción 1: +2 Presión; juega una CF aleatoria del descarte.
  - ⬜ Opción 2: +1 Presión; roba 1 carta del mazo.
  - **✅ Opción 3: +1 Presión; descarta 1 carta(s) del mazo.**
- 🟪 IA elige **Opción 3**.
- Los robos o CF extra que active el evento se resuelven inmediatamente según el motor.
- Marcador jugador 1–0 bot; presión 1; +CC 0; +CF 0; CR 5; mano 3/5 🟩 🟩 🟩; mazo restante: 0 CC, 0 CF y 0 CE.
  - Registro: Aparece CE: Córner.
  - Registro: Descarta del mazo: Disparo lejano.
  - Registro: Córner: Opción 3.

## Resultado final

| Métrica | Resultado |
| --- | ---: |
| Goles del jugador | **1** |
| Goles del bot por presión | **0** |
| Goles del bot por CR | **0** |
| CR robadas | **5** |
| Presión final | **1** |
| CE resueltas | **8** |
| CF resueltas | **11** |
| CC finales en mano | **3** |
| Sustituciones por lesión | **0** |
