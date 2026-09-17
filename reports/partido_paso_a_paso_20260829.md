# Partido simulado paso a paso — BG FÚTBOL

- Semilla reproducible: `20260829`
- Jugador: DEF 15 · MED 15 · AT 15
- Bot: DEF 15 · MED 15 · AT 15
- Mazo: 28 CC, 12 CF y 10 CE
- Mano inicial: 0 CC; límite: 5 CC
- Gol del bot: al superar presión 9, la presión vuelve a 0

## Desarrollo completo

### Turno 1 — Provocar la falta
- Robo: CF **Provocar la falta**. Mano antes de decidir: —.
- IA: no gasta CC; no puede mejorar la CF de forma rentable.
- CF: **Roba 1 CR** (nivel 0); prueba: resultado de fallo.
- Marcador jugador 0–0 bot; presión 0; +CC 0; +CF 0; CR 1; mano 0.
  - Registro: Aparece CF: Provocar la falta.
  - Registro: Provocar la falta: Roba 1 CR.

### Turno 2 — Control del juego
- Robo: CC **Control del juego**. Mano: Control del juego.
- Marcador jugador 0–0 bot; presión 0; +CC 0; +CF 0; CR 1; mano 1.
  - Registro: Roba CC: Control del juego.

### Turno 3 — Cambio de orientación
- Robo: CC **Cambio de orientación**. Mano: Control del juego, Cambio de orientación.
- Marcador jugador 0–0 bot; presión 0; +CC 0; +CF 0; CR 1; mano 2.
  - Registro: Roba CC: Cambio de orientación.

### Turno 4 — Pérdida de tiempo
- Robo: CE **Pérdida de tiempo**.
- IA elige **Opción 3**: +1 Presión.
- Los robos o CF extra que active el evento se resuelven inmediatamente según el motor.
- Marcador jugador 0–0 bot; presión 1; +CC 0; +CF 0; CR 1; mano 2.
  - Registro: Aparece CE: Pérdida de tiempo.
  - Registro: Pérdida de tiempo: Opción 3.

### Turno 5 — Pérdida de tiempo
- Robo: CE **Pérdida de tiempo**.
- IA elige **Opción 3**: +1 Presión.
- Los robos o CF extra que active el evento se resuelven inmediatamente según el motor.
- Marcador jugador 0–0 bot; presión 2; +CC 0; +CF 0; CR 1; mano 2.
  - Registro: Aparece CE: Pérdida de tiempo.
  - Registro: Pérdida de tiempo: Opción 3.

### Turno 6 — Recuperación agresiva
- Robo: CC **Recuperación agresiva**. Mano: Control del juego, Cambio de orientación, Recuperación agresiva.
- Marcador jugador 0–0 bot; presión 2; +CC 0; +CF 0; CR 1; mano 3.
  - Registro: Roba CC: Recuperación agresiva.

### Turno 7 — Construcción desde atrás
- Robo: CC **Construcción desde atrás**. Mano: Control del juego, Cambio de orientación, Recuperación agresiva, Construcción desde atrás.
- Marcador jugador 0–0 bot; presión 2; +CC 0; +CF 0; CR 1; mano 4.
  - Registro: Roba CC: Construcción desde atrás.

### Turno 8 — Construcción desde atrás
- Robo: CC **Construcción desde atrás**. Mano: Control del juego, Cambio de orientación, Recuperación agresiva, Construcción desde atrás, Construcción desde atrás.
- Marcador jugador 0–0 bot; presión 2; +CC 0; +CF 0; CR 1; mano 5.
  - Registro: Roba CC: Construcción desde atrás.

### Turno 9 — Apertura a banda
- Robo: CC **Apertura a banda**. Mano: Control del juego, Cambio de orientación, Recuperación agresiva, Construcción desde atrás, Construcción desde atrás, Apertura a banda.
- Límite de mano: se descarta **Cambio de orientación** (copias: 1; comparaciones utilizables: 0; valor: 75).
- Marcador jugador 0–0 bot; presión 2; +CC 0; +CF 0; CR 1; mano 5.
  - Registro: Roba CC: Apertura a banda.
  - Registro: Descarta de la mano: Cambio de orientación.

### Turno 10 — Construcción desde atrás
- Robo: CC **Construcción desde atrás**. Mano: Control del juego, Recuperación agresiva, Construcción desde atrás, Construcción desde atrás, Apertura a banda, Construcción desde atrás.
- Límite de mano: se descarta **Construcción desde atrás** (copias: 3; comparaciones utilizables: 0; valor: 100).
- Marcador jugador 0–0 bot; presión 2; +CC 0; +CF 0; CR 1; mano 5.
  - Registro: Roba CC: Construcción desde atrás.
  - Registro: Descarta de la mano: Construcción desde atrás.

### Turno 11 — Fuera de juego
- Robo: CE **Fuera de juego**.
- IA elige **Opción 3**: -2 Presión; +1 CR.
- Los robos o CF extra que active el evento se resuelven inmediatamente según el motor.
- Marcador jugador 0–0 bot; presión 0; +CC 0; +CF 0; CR 2; mano 5.
  - Registro: Aparece CE: Fuera de juego.
  - Registro: Fuera de juego: Opción 3.

### Turno 12 — Fuera de juego
- Robo: CE **Fuera de juego**.
- IA elige **Opción 3**: -2 Presión; +1 CR.
- Los robos o CF extra que active el evento se resuelven inmediatamente según el motor.
- Marcador jugador 0–0 bot; presión 0; +CC 0; +CF 0; CR 3; mano 5.
  - Registro: Aparece CE: Fuera de juego.
  - Registro: Fuera de juego: Opción 3.

### Turno 13 — Apertura a banda
- Robo: CC **Apertura a banda**. Mano: Control del juego, Recuperación agresiva, Construcción desde atrás, Apertura a banda, Construcción desde atrás, Apertura a banda.
- Límite de mano: se descarta **Control del juego** (copias: 1; comparaciones utilizables: 0; valor: 80).
- Marcador jugador 0–0 bot; presión 0; +CC 0; +CF 0; CR 3; mano 5.
  - Registro: Roba CC: Apertura a banda.
  - Registro: Descarta de la mano: Control del juego.

### Turno 14 — Mano a mano
- Robo: CF **Mano a mano**. Mano antes de decidir: Recuperación agresiva, Construcción desde atrás, Apertura a banda, Construcción desde atrás, Apertura a banda.
- CC 1: **Apertura a banda — Comparación 1**: +2 CF. Comparación: MED jugador 15 >= DEF rival 15; superada.
- CC 2: **Apertura a banda — Comparación 1**: +2 CF. Comparación: MED jugador 15 >= DEF rival 15; superada.
- CF: **Gol** (nivel 2); prueba: AT jugador 19 > DEF rival 18.
- Marcador jugador 1–0 bot; presión 0; +CC 0; +CF 0; CR 3; mano 3.
  - Registro: Aparece CF: Mano a mano.
  - Registro: Juega Apertura a banda: Comparación 1.
  - Registro: Juega Apertura a banda: Comparación 1.
  - Registro: Mano a mano: Gol.

### Turno 15 — Apertura a banda
- Robo: CC **Apertura a banda**. Mano: Recuperación agresiva, Construcción desde atrás, Construcción desde atrás, Apertura a banda.
- Marcador jugador 1–0 bot; presión 0; +CC 0; +CF 0; CR 3; mano 4.
  - Registro: Roba CC: Apertura a banda.

### Turno 16 — Triangulación de equipo
- Robo: CC **Triangulación de equipo**. Mano: Recuperación agresiva, Construcción desde atrás, Construcción desde atrás, Apertura a banda, Triangulación de equipo.
- Marcador jugador 1–0 bot; presión 0; +CC 0; +CF 0; CR 3; mano 5.
  - Registro: Roba CC: Triangulación de equipo.

### Turno 17 — Remate de cabeza
- Robo: CF **Remate de cabeza**. Mano antes de decidir: Recuperación agresiva, Construcción desde atrás, Construcción desde atrás, Apertura a banda, Triangulación de equipo.
- CC 1: **Triangulación de equipo — Comparación 2**: +2 CF. Comparación: AT jugador 15 >= DEF rival 15; superada.
- CC 2: **Apertura a banda — Comparación 1**: +2 CF. Comparación: MED jugador 15 >= DEF rival 15; superada.
- CF: **Gol** (nivel 2); prueba: AT jugador 19 > DEF rival 18.
- Marcador jugador 2–0 bot; presión 0; +CC 0; +CF 0; CR 3; mano 3.
  - Registro: Aparece CF: Remate de cabeza.
  - Registro: Juega Triangulación de equipo: Comparación 2.
  - Registro: Juega Apertura a banda: Comparación 1.
  - Registro: Remate de cabeza: Gol.

### Turno 18 — Buscar el córner
- Robo: CF **Buscar el córner**. Mano antes de decidir: Recuperación agresiva, Construcción desde atrás, Construcción desde atrás.
- IA: no gasta CC; no puede mejorar la CF de forma rentable.
- CF: **+2 Presión** (nivel 0); prueba: resultado de fallo.
- Marcador jugador 2–0 bot; presión 2; +CC 0; +CF 0; CR 3; mano 3.
  - Registro: Aparece CF: Buscar el córner.
  - Registro: Buscar el córner: +2 Presión.

### Turno 19 — Pérdida de tiempo
- Robo: CE **Pérdida de tiempo**.
- IA elige **Opción 3**: +1 Presión.
- Los robos o CF extra que active el evento se resuelven inmediatamente según el motor.
- Marcador jugador 2–0 bot; presión 3; +CC 0; +CF 0; CR 3; mano 3.
  - Registro: Aparece CE: Pérdida de tiempo.
  - Registro: Pérdida de tiempo: Opción 3.

### Turno 20 — Centro al área
- Robo: CC **Centro al área**. Mano: Recuperación agresiva, Construcción desde atrás, Construcción desde atrás, Centro al área.
- Marcador jugador 2–0 bot; presión 3; +CC 0; +CF 0; CR 3; mano 4.
  - Registro: Roba CC: Centro al área.

### Turno 21 — Pase de la muerte
- Robo: CF **Pase de la muerte**. Mano antes de decidir: Recuperación agresiva, Construcción desde atrás, Construcción desde atrás, Centro al área.
- IA: no gasta CC; no puede mejorar la CF de forma rentable.
- CF: **Roba 1 CR** (nivel 0); prueba: resultado de fallo.
- Marcador jugador 2–0 bot; presión 3; +CC 0; +CF 0; CR 4; mano 4.
  - Registro: Aparece CF: Pase de la muerte.
  - Registro: Pase de la muerte: Roba 1 CR.

### Turno 22 — Buscar el córner
- Robo: CF **Buscar el córner**. Mano antes de decidir: Recuperación agresiva, Construcción desde atrás, Construcción desde atrás, Centro al área.
- CC 1: **Construcción desde atrás — Efecto base**: +1 CC.
- CC 2: **Centro al área — Comparación 1**: +2 CF. Comparación: MED jugador 16 >= DEF rival 16; superada.
- CF: **-1 Presión** (nivel 1); prueba: MED jugador 17 > DEF rival 16.
- Marcador jugador 2–0 bot; presión 2; +CC 0; +CF 0; CR 4; mano 2.
  - Registro: Aparece CF: Buscar el córner.
  - Registro: Juega Construcción desde atrás: Efecto base.
  - Registro: Juega Centro al área: Comparación 1.
  - Registro: Buscar el córner: -1 Presión.

### Turno 23 — Recuperación agresiva
- Robo: CC **Recuperación agresiva**. Mano: Recuperación agresiva, Construcción desde atrás, Recuperación agresiva.
- Marcador jugador 2–0 bot; presión 2; +CC 0; +CF 0; CR 4; mano 3.
  - Registro: Roba CC: Recuperación agresiva.

### Turno 24 — Pase entre líneas
- Robo: CC **Pase entre líneas**. Mano: Recuperación agresiva, Construcción desde atrás, Recuperación agresiva, Pase entre líneas.
- Marcador jugador 2–0 bot; presión 2; +CC 0; +CF 0; CR 4; mano 4.
  - Registro: Roba CC: Pase entre líneas.

### Turno 25 — Provocar la falta
- Robo: CF **Provocar la falta**. Mano antes de decidir: Recuperación agresiva, Construcción desde atrás, Recuperación agresiva, Pase entre líneas.
- CC 1: **Pase entre líneas — Efecto base**: +1 CC.
- CC 2: **Construcción desde atrás — Comparación 2**: +1 CF. Comparación: DEF jugador 16 >= MED rival 16; superada.
- CF: **Tarjeta amarilla** (nivel 1); prueba: AT jugador 16 > DEF rival 15.
- Marcador jugador 2–0 bot; presión 2; +CC 0; +CF 0; CR 4; mano 2.
  - Registro: Aparece CF: Provocar la falta.
  - Registro: Juega Pase entre líneas: Efecto base.
  - Registro: Juega Construcción desde atrás: Comparación 2.
  - Registro: Provocar la falta: Tarjeta amarilla.

### Turno 26 — Pase entre líneas
- Robo: CC **Pase entre líneas**. Mano: Recuperación agresiva, Recuperación agresiva, Pase entre líneas.
- Marcador jugador 2–0 bot; presión 2; +CC 0; +CF 0; CR 4; mano 3.
  - Registro: Roba CC: Pase entre líneas.

### Turno 27 — VAR
- Robo: CE **VAR**.
- IA elige **Opción 2**: -2 Presión; +1 CR.
- Los robos o CF extra que active el evento se resuelven inmediatamente según el motor.
- Marcador jugador 2–0 bot; presión 0; +CC 0; +CF 0; CR 5; mano 3.
  - Registro: Aparece CE: VAR.
  - Registro: VAR: Opción 2.

### Turno 28 — Construcción desde atrás
- Robo: CC **Construcción desde atrás**. Mano: Recuperación agresiva, Recuperación agresiva, Pase entre líneas, Construcción desde atrás.
- Marcador jugador 2–0 bot; presión 0; +CC 0; +CF 0; CR 5; mano 4.
  - Registro: Roba CC: Construcción desde atrás.

### Turno 29 — Remate de cabeza
- Robo: CF **Remate de cabeza**. Mano antes de decidir: Recuperación agresiva, Recuperación agresiva, Pase entre líneas, Construcción desde atrás.
- CC 1: **Pase entre líneas — Efecto base**: +1 CC.
- CC 2: **Construcción desde atrás — Comparación 2**: +1 CF. Comparación: DEF jugador 16 >= MED rival 16; superada.
- CF: **Descarta la primera carta del mazo** (nivel 1); prueba: AT jugador 16 > DEF rival 15.
- Marcador jugador 2–0 bot; presión 0; +CC 0; +CF 0; CR 5; mano 2.
  - Registro: Aparece CF: Remate de cabeza.
  - Registro: Juega Pase entre líneas: Efecto base.
  - Registro: Juega Construcción desde atrás: Comparación 2.
  - Registro: Descarta del mazo: Disparo lejano.
  - Registro: Remate de cabeza: Descarta la primera carta del mazo.

### Turno 30 — Triangulación de equipo
- Robo: CC **Triangulación de equipo**. Mano: Recuperación agresiva, Recuperación agresiva, Triangulación de equipo.
- Marcador jugador 2–0 bot; presión 0; +CC 0; +CF 0; CR 5; mano 3.
  - Registro: Roba CC: Triangulación de equipo.

### Turno 31 — Ley de la ventaja
- Robo: CE **Ley de la ventaja**.
- IA elige **Opción 2**: tirada de lesión por amarilla (10%); roba 1 carta del mazo.
- Los robos o CF extra que active el evento se resuelven inmediatamente según el motor.
- Marcador jugador 2–0 bot; presión 0; +CC 0; +CF 0; CR 5; mano 4.
  - Registro: Aparece CE: Ley de la ventaja.
  - Registro: Lesión por amarilla: sustitución aleatoria (MED).
  - Registro: Ley de la ventaja: Opción 2.
  - Registro: Roba CC: Recuperación agresiva.

### Turno 33 — Balón al espacio
- Robo: CC **Balón al espacio**. Mano: Recuperación agresiva, Recuperación agresiva, Triangulación de equipo, Recuperación agresiva, Balón al espacio.
- Marcador jugador 2–0 bot; presión 0; +CC 0; +CF 0; CR 5; mano 5.
  - Registro: Roba CC: Balón al espacio.

### Turno 34 — Control del juego
- Robo: CC **Control del juego**. Mano: Recuperación agresiva, Recuperación agresiva, Triangulación de equipo, Recuperación agresiva, Balón al espacio, Control del juego.
- Límite de mano: se descarta **Recuperación agresiva** (copias: 3; comparaciones utilizables: 1; valor: 40).
- Marcador jugador 2–0 bot; presión 0; +CC 0; +CF 0; CR 5; mano 5.
  - Registro: Roba CC: Control del juego.
  - Registro: Descarta de la mano: Recuperación agresiva.

### Turno 35 — Balón al espacio
- Robo: CC **Balón al espacio**. Mano: Recuperación agresiva, Triangulación de equipo, Recuperación agresiva, Balón al espacio, Control del juego, Balón al espacio.
- Límite de mano: se descarta **Control del juego** (copias: 1; comparaciones utilizables: 0; valor: 80).
- Marcador jugador 2–0 bot; presión 0; +CC 0; +CF 0; CR 5; mano 5.
  - Registro: Roba CC: Balón al espacio.
  - Registro: Descarta de la mano: Control del juego.

### Turno 36 — Centro al área
- Robo: CC **Centro al área**. Mano: Recuperación agresiva, Triangulación de equipo, Recuperación agresiva, Balón al espacio, Balón al espacio, Centro al área.
- Límite de mano: se descarta **Recuperación agresiva** (copias: 2; comparaciones utilizables: 1; valor: 40).
- Marcador jugador 2–0 bot; presión 0; +CC 0; +CF 0; CR 5; mano 5.
  - Registro: Roba CC: Centro al área.
  - Registro: Descarta de la mano: Recuperación agresiva.

### Turno 37 — Centro al área
- Robo: CC **Centro al área**. Mano: Triangulación de equipo, Recuperación agresiva, Balón al espacio, Balón al espacio, Centro al área, Centro al área.
- Límite de mano: se descarta **Recuperación agresiva** (copias: 1; comparaciones utilizables: 1; valor: 40).
- Marcador jugador 2–0 bot; presión 0; +CC 0; +CF 0; CR 5; mano 5.
  - Registro: Roba CC: Centro al área.
  - Registro: Descarta de la mano: Recuperación agresiva.

### Turno 38 — Fuera de juego
- Robo: CE **Fuera de juego**.
- IA elige **Opción 3**: -2 Presión; +1 CR.
- Los robos o CF extra que active el evento se resuelven inmediatamente según el motor.
- Marcador jugador 2–0 bot; presión 0; +CC 0; +CF 0; CR 6; mano 5.
  - Registro: Aparece CE: Fuera de juego.
  - Registro: Fuera de juego: Opción 3.

### Turno 39 — Balón al espacio
- Robo: CC **Balón al espacio**. Mano: Triangulación de equipo, Balón al espacio, Balón al espacio, Centro al área, Centro al área, Balón al espacio.
- Límite de mano: se descarta **Centro al área** (copias: 2; comparaciones utilizables: 0; valor: 200).
- Marcador jugador 2–0 bot; presión 0; +CC 0; +CF 0; CR 6; mano 5.
  - Registro: Roba CC: Balón al espacio.
  - Registro: Descarta de la mano: Centro al área.

### Turno 40 — Triangulación de equipo
- Robo: CC **Triangulación de equipo**. Mano: Triangulación de equipo, Balón al espacio, Balón al espacio, Centro al área, Balón al espacio, Triangulación de equipo.
- Límite de mano: se descarta **Centro al área** (copias: 1; comparaciones utilizables: 0; valor: 200).
- Marcador jugador 2–0 bot; presión 0; +CC 0; +CF 0; CR 6; mano 5.
  - Registro: Roba CC: Triangulación de equipo.
  - Registro: Descarta de la mano: Centro al área.

### Turno 41 — Cambio de orientación
- Robo: CC **Cambio de orientación**. Mano: Triangulación de equipo, Balón al espacio, Balón al espacio, Balón al espacio, Triangulación de equipo, Cambio de orientación.
- Límite de mano: se descarta **Cambio de orientación** (copias: 1; comparaciones utilizables: 0; valor: 75).
- Marcador jugador 2–0 bot; presión 0; +CC 0; +CF 0; CR 6; mano 5.
  - Registro: Roba CC: Cambio de orientación.
  - Registro: Descarta de la mano: Cambio de orientación.

### Turno 42 — Pase de la muerte
- Robo: CF **Pase de la muerte**. Mano antes de decidir: Triangulación de equipo, Balón al espacio, Balón al espacio, Balón al espacio, Triangulación de equipo.
- CC 1: **Triangulación de equipo — Comparación 2**: +2 CF. Comparación: AT jugador 15 >= DEF rival 15; superada.
- CC 2: **Triangulación de equipo — Comparación 2**: +2 CF. Comparación: AT jugador 15 >= DEF rival 15; superada.
- CC 3: **Balón al espacio — Efecto base**: +2 CF; +1 Presión.
- CF: **Gol** (nivel 2); prueba: MED jugador 21 > DEF rival 19.
- Marcador jugador 3–0 bot; presión 1; +CC 0; +CF 0; CR 6; mano 2.
  - Registro: Aparece CF: Pase de la muerte.
  - Registro: Juega Triangulación de equipo: Comparación 2.
  - Registro: Juega Triangulación de equipo: Comparación 2.
  - Registro: Juega Balón al espacio: Efecto base.
  - Registro: Pase de la muerte: Gol.

### Turno 43 — Recuperación agresiva
- Robo: CC **Recuperación agresiva**. Mano: Balón al espacio, Balón al espacio, Recuperación agresiva.
- Marcador jugador 3–0 bot; presión 1; +CC 0; +CF 0; CR 6; mano 3.
  - Registro: Roba CC: Recuperación agresiva.

### Turno 44 — Ley de la ventaja
- Robo: CE **Ley de la ventaja**.
- IA elige **Opción 2**: tirada de lesión por amarilla (10%); roba 1 carta del mazo.
- Los robos o CF extra que active el evento se resuelven inmediatamente según el motor.
- Marcador jugador 4–0 bot; presión 3; +CC 0; +CF 0; CR 6; mano 1.
  - Registro: Aparece CE: Ley de la ventaja.
  - Registro: Lesión por amarilla: sustitución aleatoria (MED).
  - Registro: Ley de la ventaja: Opción 2.
  - Registro: Aparece CF: Mano a mano.
  - Registro: Juega Balón al espacio: Efecto base.
  - Registro: Juega Balón al espacio: Efecto base.
  - Registro: Mano a mano: Gol.

### Turno 46 — Córner
- Robo: CE **Córner**.
- IA elige **Opción 2**: +1 Presión; roba 1 carta del mazo.
- Los robos o CF extra que active el evento se resuelven inmediatamente según el motor.
- Marcador jugador 4–0 bot; presión 4; +CC 0; +CF 0; CR 6; mano 2.
  - Registro: Aparece CE: Córner.
  - Registro: Córner: Opción 2.
  - Registro: Roba CC: Acción individual.

### Turno 48 — Disparo lejano
- Robo: CF **Disparo lejano**. Mano antes de decidir: Recuperación agresiva, Acción individual.
- CC 1: **Acción individual — Efecto base**: +1 CF.
- CF: **-1 Presión** (nivel 1); prueba: AT jugador 16 > DEF rival 15.
- Marcador jugador 4–0 bot; presión 3; +CC 0; +CF 0; CR 6; mano 1.
  - Registro: Aparece CF: Disparo lejano.
  - Registro: Juega Acción individual: Efecto base.
  - Registro: Disparo lejano: -1 Presión.

### Turno 49 — Acción individual
- Robo: CC **Acción individual**. Mano: Recuperación agresiva, Acción individual.
- Marcador jugador 4–0 bot; presión 3; +CC 0; +CF 0; CR 6; mano 2.
  - Registro: Roba CC: Acción individual.

## Resultado final

| Métrica | Resultado |
| --- | ---: |
| Goles del jugador | **4** |
| Goles del bot por presión | **0** |
| Goles del bot por CR | **0** |
| CR robadas | **6** |
| Presión final | **3** |
| CE resueltas | **10** |
| CF resueltas | **11** |
| CC finales en mano | **2** |
| Sustituciones por lesión | **2** |
