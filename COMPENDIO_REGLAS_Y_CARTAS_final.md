# BG FÚTBOL — compendio de cartas y reglas

Este documento describe la versión actualmente implementada del partido. Las
decisiones de una carta las toma el jugador; cuando se ejecuta una simulación,
la IA las toma siguiendo las políticas explicadas al final.

## 1. Componentes y preparación

El mazo de partido es único, combinado y se baraja antes de empezar. Tiene
**50 cartas**:

| Tipo | Cantidad | Uso |
| --- | ---: | --- |
| CC — cartas de control | 28 | Van a la mano y se pueden jugar antes de una CF. |
| CF — cartas de finalización | 12 | Se resuelven al aparecer, después de jugar las CC deseadas. |
| CE — cartas de evento | 10 | Se resuelven inmediatamente eligiendo una de tres opciones. |

Cada equipo tiene tres atributos: **DEF**, **MED** y **AT**. No pueden ser
negativos. El informe los muestra siempre en ese orden: `DEF / MED / AT`.

El partido comienza con estas condiciones:

- Mano del jugador: **0 CC**.
- Límite de mano: **5 CC**.
- Presión: **0**.
- Goles del jugador y del bot: **0**.
- CR robadas: **0**.

Se roba una carta tras otra hasta que el mazo queda vacío. No hay reciclaje ni
barajado del descarte.

## 2. Comparaciones y bonos

### Comparaciones de CC

Las comparaciones de las **CC** se muestran en cada carta y se resuelven según la lógica del sistema.

Ejemplo: `MED 15 ≥ MED rival +1 (16)` no se supera; si el jugador tuviera un
`+1 CC`, se compararía `16 ≥ 16` y sí se superaría.

### Comparaciones de CF

Todas las comparaciones de una **CF** son estrictas: `>`.

Ejemplo: para `AT > DEF rival`, un `15` contra `15` falla; hace falta al menos
`16`.

### Bono +CC

- Un `+CC` se aplica **solo a la siguiente CC** que juegues, para su
  comparación.
- Se consume incluso si la siguiente CC usa el efecto base y no compara.
- Si esa CC genera otro `+CC`, el nuevo bono queda preparado para la CC
  siguiente; no se acumula con el anterior ya consumido.

### Bono +CF

- Un `+CF` se suma al atributo usado en la **siguiente CF**.
- Varios `+CF` se acumulan.
- Tras resolver esa CF, todos los `+CF` acumulados se pierden.
- En los informes se muestra como, por ejemplo,
  `MED jugador 15 🟢 +2 🟢 +1 = 18`.

## 3. Flujo de cada tipo de carta

### Al robar una CC

La CC entra en la mano. Si con ella hay 6 CC, se descarta una CC de la mano y
se termina con 5. En una partida física el jugador determina cuál descartar.

### Al robar una CF

1. El jugador puede jugar cero, una o varias CC de su mano, en el orden que
   quiera.
2. Cada CC jugada va al descarte y se aplica una sola de sus tres opciones.
   Una opción con comparación solo se puede elegir si se supera.
3. Se resuelve la CF: se revisan sus resultados en el orden 1, 2 y 3, y se
   aplica el primer resultado cuya comparación se cumpla. El resultado 3 es el
   fallo y no tiene comparación.
4. La CF va al descarte.

### Al robar una CE

El jugador elige una de sus tres opciones y se aplica inmediatamente. La CE
va al descarte. Si su efecto roba una carta del mazo, esa carta se procesa
inmediatamente con las reglas normales: una CC entra en mano, una CF se
resuelve y una CE exige otra decisión.

## 4. Reglas globales

### Presión y gol del bot

- La presión nunca baja de 0.
- Si un efecto hace que supere 9 (es decir, llegue a 10 o más), el bot marca
  un gol por presión y la presión vuelve a 0.
- Estar exactamente en 9 **no** da gol al bot.
- Por ahora las CR no generan goles del bot: el contador de «goles del bot por
  CR» siempre es 0.

### Descartar la primera carta del mazo

La carta superior del mazo se mueve al descarte sin resolver nada. Puede ser
una CC, CF o CE; no entra en mano, no aplica efectos y no cuenta como turno
resuelto.

### Descartar una CC de la mano

La CC elegida pasa al descarte. La opción 1 de **Fuera de juego** exige este
descarte además del descarte de la primera carta del mazo. Si no hay CC en la
mano, no hay carta que descartar y solo se descarta la del mazo.

### Recuperar una CC

Se mueve una CC del descarte a la mano. Si la mano superara 5 CC, se descarta
una hasta volver al límite de 5.

### CF aleatoria del descarte

Se elige al azar una CF que ya esté en el descarte y se resuelve de inmediato.
No se pueden jugar CC antes de esa CF extra. Si no hay CF en el descarte, no
ocurre nada salvo los otros efectos de la opción que la haya activado.

### Amarillas, rojas y lesiones

- Una tirada de lesión por amarilla tiene **10%** de probabilidad.
- Una tirada de lesión por roja tiene **15%** de probabilidad.
- Si hay lesión, se pierde un jugador al azar (DEF, MED o AT) y se realiza una
  sustitución. Por ahora esa sustitución se registra, pero **no modifica los
  atributos** globales del equipo.
- En las cartas actuales, las tiradas de lesión se indican expresamente. Las
  amarillas o rojas al rival no lanzan por sí solas una tirada adicional.

### CR

Una CR robada solo aumenta el contador de CR. Aún no existe mazo ni efecto de
CR definido.

## 5. Cartas de control (CC) — 28 cartas

Cada CC tiene tres opciones: efecto base, comparación 1 y comparación 2.
Las comparaciones de las CC se resuelven según la regla general del sistema.

### Construcción desde atrás ×4

1. **Efecto base:** `+1 CC`.
2. **Comparación 1:** `MED > DEF rival` → `+2 CC`.
3. **Comparación 2:** `DEF > MED rival +1` → `+1 CF`.

### Recuperación agresiva ×4

1. **Efecto base:** `+1 CC`.
2. **Comparación 1:** `DEF > MED rival` → `-2 Presión`.
3. **Comparación 2:** `MED > MED rival` → tarjeta amarilla y `+2 CF`.

### Apertura a banda ×3

1. **Efecto base:** `+1 CF`.
2. **Comparación 1:** `MED > DEF rival +2` → `+2 CF`.
3. **Comparación 2:** `MED > MED rival +1` → `+2 CC`.

### Balón al espacio ×3

1. **Efecto base:** `+2 CF` y `+1 Presión`.
2. **Comparación 1:** `MED > DEF rival +2` → `+3 CF`.
3. **Comparación 2:** `AT > DEF rival +3` → `+2 CC`.

### Triangulación de equipo ×3

1. **Efecto base:** `+1 CC`.
2. **Comparación 1:** `MED > MED rival +1` → `+2 CC`.
3. **Comparación 2:** `AT > MED rival +1` → `+2 CF`.

### Centro al área ×3

1. **Efecto base:** `+1 CF`.
2. **Comparación 1:** `MED > DEF rival +1` → `+2 CF`.
3. **Comparación 2:** `AT > DEF rival +3` → `+3 CF`.

### Cambio de orientación ×2

1. **Efecto base:** `+2 CC` y descarta la primera carta del mazo.
2. **Comparación 1:** `MED > MED rival +3` → `+2 CF`.
3. **Comparación 2:** `MED > DEF rival +2` → `-1 Presión`.

### Pase entre líneas ×2

1. **Efecto base:** `+1 CC`.
2. **Comparación 1:** `MED > DEF rival +3` → `+3 CF`.
3. **Comparación 2:** `AT > DEF rival +2` → `+2 CC`.

### Acción individual ×2

1. **Efecto base:** `+1 CF`.
2. **Comparación 1:** `AT > DEF rival +1` → `+1 CF` y tarjeta amarilla.
3. **Comparación 2:** `AT > DEF rival +4` → `+3 CF`.

### Control del juego ×2

1. **Efecto base:** `+1 CC`.
2. **Comparación 1:** `MED > MED rival +2` → `-2 Presión` y `+1 CC`.
3. **Comparación 2:** `MED > MED rival` → `-1 Presión` y `+1 CC`.

## 6. Cartas de finalización (CF) — 12 cartas

Hay dos copias de cada CF. Sus comparaciones son estrictas: `>`.

### Mano a mano ×2

1. `AT > DEF rival +4` → **Gol**.
2. `AT > DEF rival` → descarta 1 CC de la mano y `-1 Presión`.
3. Fallo → roba 1 CR.

### Ultimo pase ×2

1. `MED > DEF rival +4` → **Gol**.
2. `MED > DEF rival +2` → `-1 Presión`.
3. Fallo → roba 1 CR.

### Remate de cabeza ×2

1. `AT > DEF rival +4` → **Gol**.
2. `AT > DEF rival` → descarta la primera carta del mazo y `-1 Presión`.
3. Fallo → roba 1 CR y `-1 Presión`.

### Disparo lejano ×2

1. `AT > DEF rival +4` → **Gol**.
2. `AT > DEF rival` → `-2 Presión`.
3. Fallo → descarta 1 CC de la mano y roba 1 CR.

### Buscar el córner ×2

1. `MED > DEF rival +3` → `-2 Presión`.
2. `MED > DEF rival +1` → `-1 Presión`.
3. Fallo → `+2 Presión` y descarta 1 CC de la mano.

### Provocar la falta ×2

1. `AT > DEF rival +5` → el rival recibe tarjeta roja.
2. `AT > DEF rival` → el rival recibe tarjeta amarilla y `-1 Presión`.
3. Fallo → roba 1 CR y descarta la primera carta del mazo.

## 7. Cartas de evento (CE) — 10 cartas

Todas las CE van mezcladas en el mismo mazo de partido.

### Pérdida de tiempo ×3

1. Descarta 2 cartas del mazo, `+1 Presión` y tarjeta amarilla.
2. Roba 1 CR, descarta 1 CC de tu mano y `-4 Presión`.
3. `+1 Presión`, tira 1d6 por lesión amarilla y descarta 1 carta del mazo.

### Fuera de juego ×3

1. Descarta 1 carta del mazo y 2 CC de tu mano.
2. `+2 Presión`.
3. Roba 1 CR y `-3 Presión`.

### Ley de la ventaja ×2

1. El rival recibe tarjeta amarilla y `+3 Presión`.
2. Descarta 1 carta del mazo, tira 1d6 por lesión amarilla y `+1 Presión`.
3. El jugador recibe tarjeta amarilla, tira 1d6 por lesión y `-1 Presión`.

### VAR ×1

1. El rival recibe tarjeta amarilla y `+3 Presión`.
2. Roba 1 CR y `-3 Presión`.
3. Recupera 1 CC del descarte y `+2 Presión`.

### Córner ×1

1. Juega inmediatamente una CF aleatoria del descarte y `+2 Presión`.
2. Roba 1 carta del mazo y `+1 Presión`.
3. Descarta la primera carta del mazo y `+1 Presión`.

## 8. Simulación automática

Esta sección no cambia las reglas de una partida física; describe cómo decide
el programa al ejecutar el lanzador `Simular_BG_Futbol.bat`.

### Descartes automáticos

Cuando debe elegir una CC para descartar por exceso de mano o por Fuera de
juego, la IA elige la menos útil según comparaciones alcanzables, mejor efecto
posible y cartas repetidas. El informe muestra la carta descartada.

### Estilo «Juego agresivo»

Antes de una CF, busca el mejor resultado alcanzable: primero resultado 1,
después resultado 2 y, si ninguno es alcanzable, no gasta CC. En empates usa
menos CC y procura terminar con menos presión.

### Estilo «Buscar 1–0 y pocas CR»

1. Antes del primer gol y con menos de 2 CR, conserva CC; solo las gasta si
   una secuencia permite marcar.
2. Desde la segunda CR y mientras siga 0–0, prioriza evitar nuevas CR antes que
   marcar.
3. Tras el primer gol, intenta mantener el 1–0: evita goles adicionales,
   nuevas CR, gol del bot por presión, presión alta y gasto de cartas, en ese
   orden.
4. Antes del primer gol, sus elecciones de CE procuran mantener el mazo y
   obtener recursos; después aplica una política de menor riesgo.

### Informes y tandas

- Con **1 simulación**, el lanzador pide una semilla opcional y produce un
  informe completo, turno a turno, con la mano, el mazo restante, todas las
  opciones de CF y CE, y la opción elegida.
- Con **2 o más simulaciones**, no pide semilla y produce un informe resumido
  con totales y medias por partido.
- Los informes se guardan en la carpeta `reports/`.

## 9. Límites actuales del sistema

- No existe un mazo ni efectos jugables de CR.
- El bot no tiene turnos ofensivos propios: solo puede marcar cuando la presión
  supera 9.
- Las tarjetas y las sustituciones no alteran todavía los atributos de los
  equipos; quedan registradas en el informe.
