# BG FÚTBOL — simulador del sistema de partido

Motor Python para simular partidos de BG FÚTBOL. Ejecuta un mazo de partido de
28 cartas de control (CC), 12 de finalización (CF) y 10 de evento (CE), además
de un mazo independiente de 16 cartas rojas (CR: 8 tipos con 2 copias cada
uno). Resuelve comparaciones, efectos y decisiones de la IA antes de cada
finalización.

La IA explora las secuencias legales por capas, no mediante muestreo. Prioriza:

1. El resultado superior de la CF.
2. El resultado intermedio si el superior no es alcanzable.
3. No gastar ninguna CC si no se puede alcanzar el intermedio.
4. En empates, gastar menos CC y terminar con menor presión.

La memoización une únicamente posiciones equivalentes para la CF pendiente. No
elimina posibilidades: evita recalcular el mismo subárbol cuando cartas iguales
llegan al mismo estado de mano y bonos.

## Estructura

| Archivo | Responsabilidad |
| --- | --- |
| `bg_futbol_simulator/cards.py` | Datos inmutables de CC, CF, CE y CR, comparaciones y efectos. |
| `bg_futbol_simulator/game_state.py` | Equipos, estado mutable del partido, órdenes y resultados. |
| `bg_futbol_simulator/engine.py` | Único módulo que resuelve y muta las reglas. |
| `bg_futbol_simulator/decision_tree.py` | Exploración exacta, por capas y con memoización. |
| `bg_futbol_simulator/ai.py` | IA automática que solicita el mejor plan. |
| `bg_futbol_simulator/simulation.py` | Tandas reproducibles y paralelizables de 1 a 1.000.000 partidos. |
| `bg_futbol_simulator/statistics.py` | Agregación de métricas y frecuencias de resultados. |
| `bg_futbol_simulator/strategies.py` | Estrategia estándar y estrategia de buscar 1–0 con pocas CR. |
| `bg_futbol_simulator/trace.py` | Generación de informes Markdown, carta por carta. |
| `main.py` | Interfaz de línea de comandos. |
| `tests/` | Pruebas del motor, mazos, IA, gestión de mano y reproducibilidad. |

## Ejecutar

El proyecto no tiene dependencias externas. Desde la carpeta del proyecto:

```powershell
python main.py --matches 100 --seed 20260719
```

Para una tanda grande, usa varios procesos disponibles en tu máquina:

```powershell
python main.py --matches 1000000 --workers 8 --seed 20260719
```

También se pueden cambiar los atributos:

```powershell
python main.py --matches 10000 --player-def 16 --player-med 14 --player-at 17 --opponent-def 15 --opponent-med 15 --opponent-at 15
```

Para crear un informe de un partido, carta por carta y con la misma semilla:

```powershell
python -m bg_futbol_simulator.trace --seed 20260829 --output reports\partido_paso_a_paso.md
```

Para una partida con la estrategia de intentar ganar 1–0 y recibir las menores
CR posibles:

```powershell
python -m bg_futbol_simulator.trace --strategy one_nil_low_cr --seed 1 --output reports\partido_1_0.md
```

### Lanzador con menú

En Windows, abre con doble clic `Simular_BG_Futbol.bat`. Solicita los atributos
DEF/MED/AT de ambos equipos y el número de simulaciones. Con un único partido,
permite elegir una semilla y crea un informe carta por carta. Con dos o más,
no pide semilla y crea solo un informe de totales y medias. En ambos casos se
puede elegir entre la estrategia 1–0 con pocas CR o la agresiva; el informe se
guarda en `reports/` y el Explorador de archivos muestra el resultado recién
creado seleccionado.

La salida es JSON e incluye goles del jugador, goles del bot por presión, goles
del bot por CR, CR robadas, tarjetas, sustituciones por lesión, presión final,
cartas en mano y frecuencia de cada resultado de CF.

Para comparar el equilibrio de distintos niveles de atributos frente a un bot
fijo, se puede usar el segundo lanzador de Windows o ejecutar:

```powershell
python -m bg_futbol_simulator.balance_report --matches 100 --bot 15 15 15 --player-levels 12 13 14 15 16 17 18 --seed 7
```

## Reglas de flujo fijadas en esta primera versión

La especificación de cartas está implementada literalmente. Estas reglas de
flujo no venían definidas y se han aislado en `MatchRules` o en el motor para
que puedan cambiarse sin tocar las cartas:

- El partido empieza con el mazo combinado barajado y sin CC en mano; se roba
  hasta agotarlo. Las CC robadas entran en la mano y cada CF se resuelve en el
  momento en que aparece.
- En las CC y las CF, un empate en una comparación **no** la supera: se exige
  una comparación estricta (`>`) por defecto; se puede cambiar con
  `MatchRules(ties_succeed=True)` para que el empate cuente como éxito (`>=`).
  Las CF definen además sus propias comparaciones estrictas de forma explícita.
- Un `+CC` se suma al atributo del jugador en la siguiente comparación de CC y
  se consume al jugar esa carta. Un `+CF` se acumula y se suma al atributo del
  jugador al resolver la siguiente CF; entonces se consume.
- La mano inicial es siempre 0. La presión se mantiene entre 0 y 9; si un
  efecto la lleva por encima de 9, el bot marca un gol por presión y el
  contador vuelve a 0. El umbral está configurado en `MatchRules`.
- La mano tiene un límite estricto de 5 CC. Al robar una sexta, la IA descarta
  la menos útil según una valoración combinada de comparaciones aprovechables,
  mejor efecto disponible y redundancia de copias; la política está aislada en
  `AutomaticPlayerAI`.
- Las 10 CE se mezclan en el mismo mazo de partido. El jugador elige una de
  sus tres opciones; en la simulación, la IA selecciona la de mayor valor
  inmediato. «Descarta» retira cartas de la parte superior del mazo y «roba»
  procesa normalmente la carta robada, incluso si es una CF o CE.
- Una amarilla propia lanza una prueba de lesión del 10%; una roja propia, del
  15%. Una lesión registra una sustitución aleatoria DEF/MED/AT. Como aún no
  existe plantilla individual, esa sustitución no altera los atributos globales
  del equipo.
- «Descarta la primera carta del mazo» quita esa carta sin resolverla.
- Las CR se roban y se resuelven al instante desde un mazo separado, sin
  devolverse al mazo. Cada CR aplica primero, si procede, su efecto condicional
  de marcador y después una única acción: la primera comparación que cumpla o
  su efecto de reserva. Algunas condiciones modifican temporalmente un atributo
  rival para las comparaciones de esa CR.
- Un gol en contra causado por una CR se registra por separado de los goles del
  bot por presión. Ambos forman el total de goles del bot.
- No hay turno ofensivo independiente del rival: su intervención se modela
  mediante presión, efectos de cartas y CR.

## Pruebas

```powershell
python -m unittest discover -s tests -v
```

Las pruebas cubren la composición del mazo de partido, bonos `+CC`/`+CF`,
descarte, decisiones de IA, efectos de CR y reproducibilidad con semilla.
