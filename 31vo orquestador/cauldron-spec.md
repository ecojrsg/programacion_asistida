# Requerimiento: el caldero del goblin alquimista

Gorgo es un goblin que prepara pociones. El problema es que nunca se acuerda de las recetas. Escribe un programa para decidir qué poción sale de su caldero.

## Validación

- **R1**: Los ingredientes válidos son `"rana"`, `"hongo"`, `"escama de dragón"`, `"agua lunar"` y `"calcetín"`. Cualquier otro lanza `ValueError`.
- **R2**: No importan las mayúsculas ni los espacios al inicio o al final. `" RANA "` cuenta como `"rana"`.
- **R3**: Se necesitan de 2 a 4 ingredientes. Con menos o con más se lanza `ValueError`.
- **R4**: La temperatura del caldero va de 20 a 100 y ambos valores son válidos. Fuera de ese rango se lanza `ValueError`.

## Recetas

Se revisan en este orden. Gana la primera que se cumpla.

- **R5**: Si hay un `"calcetín"` sale `"sopa apestosa"`. Es la favorita de Gorgo.
- **R6**: `"escama de dragón"` con `"agua lunar"` a 80 grados o más da `"poción de vuelo"`.
- **R7**: Dos o más `"rana"` dan `"poción de salto"`.
- **R8**: Con `"hongo"` abajo de 50 grados sale `"poción diminuta"`. A 50 grados o más sale `"poción gigante"`.
- **R9**: Si no se cumple ninguna receta sale `"agua turbia"`.

## Otras reglas

- **R10**: El orden de los ingredientes no importa.
- **R11**: La función no debe modificar la lista que recibe.

## Ejemplos

| ingredientes | temp | resultado |
| --- | --- | --- |
| `["calcetín", "escama de dragón", "agua lunar"]` | 90 | `"sopa apestosa"` |
| `["agua lunar", "escama de dragón"]` | 80 | `"poción de vuelo"` |
| `["escama de dragón", "agua lunar"]` | 79 | `"agua turbia"` |
| `["rana", "rana", "hongo"]` | 30 | `"poción de salto"` |
| `[" Hongo ", "agua lunar"]` | 49 | `"poción diminuta"` |
| `["hongo", "agua lunar"]` | 50 | `"poción gigante"` |
| `["rana"]` | 50 | `ValueError` |
| `["rana", "unicornio"]` | 50 | `ValueError` |
| `["rana", "hongo"]` | 101 | `ValueError` |

## Requisito adicional de ejecución

- Debe incluir un `main` para poder hacer pociones desde la terminal.
