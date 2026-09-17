# BG FÚTBOL — simulador del sistema de partido

Motor Python para ejecutar el mazo de 28 CC, 12 CF y 10 CE, resolver las
comparaciones y elegir automáticamente la mejor secuencia de cartas de control
antes de cada finalización.

El detalle completo de todas las cartas y reglas está en
[`COMPENDIO_REGLAS_Y_CARTAS.md`](COMPENDIO_REGLAS_Y_CARTAS.md).

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
| `bg_futbol_simulator/cards.py` | Datos inmutables de CC, CF, CE, comparaciones y efectos. |
| `bg_futbol_simulator/game_state.py` | Equipos, estado mutable del partido, órdenes y resultados. |
| `bg_futbol_simulator/engine.py` | Único módulo que resuelve y muta las reglas. |
| `bg_futbol_simulator/decision_tree.py` | Exploración exacta, por capas y con memoización. |
| `bg_futbol_simulator/ai.py` | IA automática que solicita el mejor plan. |
| `bg_futbol_simulator/simulation.py` | Tandas reproducibles y paralelizables de 1 a 1.000.000 partidos. |
| `bg_futbol_simulator/statistics.py` | Agregación de métricas y frecuencias de resultados. |
| `main.py` | Interfaz de línea de comandos. |
| `tests/` | Pruebas de mazo, bonos, descarte, IA y reproducibilidad. |

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
del bot por CR (actualmente 0), CR robadas, tarjetas, presión final, cartas en
mano y frecuencia de cada resultado de CF.

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
- Las CR todavía no tienen mazo ni efectos especificados: el motor registra
  cada robo de CR para poder integrar sus reglas después sin falsear los datos.
- No se inventa un turno ofensivo del rival ni un marcador rival, porque esa
  parte del sistema de partido no figura en las reglas recibidas.

## Pruebas

```powershell
python -m unittest discover -s tests -v
```

Las pruebas cubren las 40 cartas del mazo, el consumo de `+CC`/`+CF`, el
descarte de la parte superior del mazo, las prioridades de la IA y la
reproducibilidad con semilla.
