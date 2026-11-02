# Perfil de aplicación ODA (versión del demostrador)

Este perfil traduce a datos el esquema de metadatos del libro *Objeto Digital Aurático* (Battaner Moro y López Iniesta, Peter Lang, 2025, cap. 4). Mantiene sus cinco categorías (Descriptiva, Técnica, Preservación, Derechos y Arte) y la marca de cada elemento como obligatorio (C) u opcional (O). La lista completa está en [`perfil-oda.csv`](perfil-oda.csv).

## El continuum

El libro plantea que el aura de un objeto digital no es un atributo binario. La condición aurática es más fuerte o más débil según los metadatos que satisfaga y según una valoración experta y colegiada (cap. 3–5). El perfil lo recoge así:

- **Un elemento obligatorio tiene que estar tratado, no necesariamente presente.** Se considera tratado si está cubierto o si está declarado como laguna con su motivo.
- **Un elemento opcional que falta genera un aviso**, no un error. Ese aviso se tiene en cuenta al valorar la condición aurática.
- **El expediente no declara que una obra "es" un ODA.** En el libro, un ODA es el identificador que asigna Fund_ODA tras un proceso colegiado. El expediente reúne la documentación y propone una valoración razonada y revisable.

## Estado de cada dato

| Estado | Significado | Requisitos |
|---|---|---|
| documentado | Consta en una fuente del autor o de la institución | valor y fuente |
| reconstruido | Se ha recompuesto a partir de fuentes indirectas | valor y fuente |
| inferido | Lo deduce el equipo a partir de la evidencia disponible | valor y fuente |
| pendiente | Se completará en una fase prevista (por ejemplo, el depósito) | motivo |
| desconocido | No se ha podido averiguar | motivo |
| perdido | Existió y ya no se conserva | motivo |
| no aplicable | El elemento no tiene sentido para esta obra | motivo |

## Afirmaciones relacionales

Las relaciones entre entidades se registran como afirmaciones. Cada una tiene sujeto, predicado, objeto, responsable, evidencia, fecha, estatuto y validación. El estatuto distingue tres casos:

- **documentada por el autor:** consta en sus notas o declaraciones;
- **observable:** se comprueba en la obra o en sus ficheros;
- **interpretativa:** es una hipótesis del equipo. En este caso, la afirmación declara además su grado de incertidumbre.

## Ficheros

- `perfil-oda.csv`: los 40 elementos del libro, con su obligatoriedad y su término.
- `context.jsonld`: contexto JSON-LD con los términos del perfil.
- `shapes.ttl`: reglas SHACL, generadas con `scripts/generar_shapes.py`. Un elemento C sin tratar da error (`sh:Violation`) y un elemento O ausente da aviso (`sh:Warning`).

El espacio de nombres `https://w3id.org/oda-lab/perfil#` está pendiente de registro en w3id.org, con redirección al repositorio <https://github.com/IPEX-LAB/oda-demostrador> (ver `w3id/`). Hasta entonces es provisional.
