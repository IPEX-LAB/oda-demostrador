# Informe de validación: hibridaciones-algoritmicas

Resultado SHACL: **sin errores**, 4 avisos.

Un elemento obligatorio (C) cuenta como tratado si está cubierto o declarado como laguna con su motivo.
Los avisos señalan elementos opcionales (O) que no constan: no bloquean, pero cuentan en la valoración.

## Resumen

| | Cubierto | Laguna declarada | No consta |
|---|---|---|---|
| Obligatorios (C) | 22 | 3 | 0 |
| Opcionales (O) | 11 | 0 | 4 |

Afirmaciones relacionales: 13 (7 documentada autor, 3 interpretativa, 3 observable).

## Elementos

| Id | Categoría | Elemento | C/O | Estado | Situación |
|---|---|---|---|---|---|
| 1.1 | Descriptiva | Título | C | documentado | cubierto |
| 1.2 | Descriptiva | Creador | C | documentado | cubierto |
| 1.3 | Descriptiva | Asunto | O | documentado | cubierto |
| 1.4 | Descriptiva | Descripción | C | documentado | cubierto |
| 1.5 | Descriptiva | Fecha | C | desconocido, inferido | cubierto |
| 1.6 | Descriptiva | Formato | C | inferido | cubierto |
| 1.7 | Descriptiva | Identificador | C | pendiente | laguna declarada |
| 1.8 | Descriptiva | Fuente | O | documentado | cubierto |
| 1.9 | Descriptiva | Idioma | C | no aplicable | laguna declarada |
| 1.10 | Descriptiva | Relación | O | documentado | cubierto |
| 1.11 | Descriptiva | Cobertura | O | — | no consta (aviso) |
| 2.1 | Técnica | Formato de archivo | C | documentado | cubierto |
| 2.2 | Técnica | Resolución | C | documentado, no aplicable | cubierto |
| 2.3 | Técnica | Compresión | O | documentado | cubierto |
| 2.4 | Técnica | Profundidad de bits | O | documentado | cubierto |
| 2.5 | Técnica | Metadatos incrustados | O | documentado | cubierto |
| 2.6 | Técnica | Suma de comprobación | C | documentado | cubierto |
| 2.7 | Técnica | Tamaño del fichero | C | documentado | cubierto |
| 2.8 | Técnica | Metadatos de reproducibilidad y control de versiones | C | reconstruido | cubierto |
| 2.9 | Técnica | Dependencias técnicas | O | documentado | cubierto |
| 2.10 | Técnica | Relaciones detalladas entre componentes | C | documentado | cubierto |
| 3.1 | Preservación | Plan de preservación a largo plazo | C | documentado | cubierto |
| 3.2 | Preservación | Vías de migración | C | documentado | cubierto |
| 3.3 | Preservación | Suma de comprobación y valores hash | C | documentado | cubierto |
| 3.4 | Preservación | Estructura compleja de objetos | O | documentado | cubierto |
| 3.5 | Preservación | Lugar de almacenamiento | C | desconocido, pendiente | laguna declarada |
| 4.1 | Derechos | Estado de los derechos | C | documentado | cubierto |
| 4.2 | Derechos | Términos de la licencia | C | documentado | cubierto |
| 4.3 | Derechos | Permisos y restricciones | C | documentado | cubierto |
| 4.4 | Derechos | Propiedad y atribución | C | desconocido, documentado | cubierto |
| 5.1 | Arte | Intención artística | C | documentado | cubierto |
| 5.2 | Arte | Influencias | O | documentado | cubierto |
| 5.3 | Arte | Simbolismo | O | — | no consta (aviso) |
| 5.4 | Arte | Técnicas | C | documentado | cubierto |
| 5.5 | Arte | Historial de exposiciones | O | documentado | cubierto |
| 5.6 | Arte | Recepción crítica | O | — | no consta (aviso) |
| 5.7 | Arte | Contexto histórico | O | — | no consta (aviso) |
| 5.8 | Arte | Innovación | C | documentado | cubierto |
| 5.9 | Arte | Géneros/Métodos artísticos | C | inferido | cubierto |
| 5.10 | Arte | Temas | O | inferido | cubierto |

## Avisos

- 1.11 Cobertura [opcional (O)]: no consta; no bloquea, pero se tiene en cuenta en la valoración.
- 5.3 Simbolismo [opcional (O)]: no consta; no bloquea, pero se tiene en cuenta en la valoración.
- 5.6 Recepción crítica [opcional (O)]: no consta; no bloquea, pero se tiene en cuenta en la valoración.
- 5.7 Contexto histórico [opcional (O)]: no consta; no bloquea, pero se tiene en cuenta en la valoración.
