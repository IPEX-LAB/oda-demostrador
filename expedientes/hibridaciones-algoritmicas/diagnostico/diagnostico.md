# Diagnóstico y condición de preservación

**Obra:** Hibridaciones algorítmicas (Juan Alonso López Iniesta)
**Obra resultante:** «5 VAR-1 GPT7» (Juan Alonso López Iniesta; montaje y soporte de Mauro Herrero Cantos). Técnica mixta: plotter de pluma e intervención del autor.
**Preparado por:** IPEX, Grupo de Investigación en Interfaces y Prototipos Experimentales (URJC), 2 de noviembre de 2026
**Carácter:** demostrador del método ODA. No es una evaluación de Fund_ODA, y todas las afirmaciones interpretativas están pendientes de revisión por el autor.

## Resumen

La obra está bien documentada en lo que más pesa en el libro: la intención, el proceso y la técnica. El expediente cubre 24 de los 25 elementos obligatorios. El restante, el idioma, está declarado como no aplicable. El identificador es el DOI de depósito 10.5281/zenodo.23883743; el lugar donde se conserva el original sigue sin constar. De los 15 elementos opcionales, constan 11.

Los riesgos principales son dos. En lo estructural, no se puede saber qué versión del código y qué parámetros produjeron «5 VAR-1 GPT7». En lo experiencial, la intervención del autor no está descrita, y es por definición irrepetible. Se proponen medidas concretas para ambos.

## Cobertura del perfil

| | Cubierto | Laguna declarada | No consta |
|---|---|---|---|
| Obligatorios (C) | 24 | 1 | 0 |
| Opcionales (O) | 11 | 0 | 4 |

No constan cobertura (1.11), simbolismo (5.3), recepción crítica (5.6) ni contexto histórico (5.7). El detalle está en [`informe-validacion.md`](informe-validacion.md).

## Diagnóstico por dimensión

### Informacional: archivos, contenidos y documentación. Riesgo alto.

- **El código se conserva copiado en un documento de Word y ha perdido la sangría.** En Python la sangría forma parte de la sintaxis, así que el código no se puede reconstruir con seguridad. Por ejemplo, en la función que genera las líneas verticales no se puede saber si un bloque condicional va dentro de otro o al mismo nivel, y cada lectura da un dibujo distinto.
- **El SVG que se envía al plotter no se conserva.** El código lo escribe en una carpeta temporal y lo sobrescribe en cada ejecución. Ese fichero es el componente más fácil de preservar y el que permitiría verificar una reproducción.
- **El cuaderno de proceso lo conserva el autor y no se deposita en esta versión.**
- **No consta la autoría de la fotografía,** necesaria para su crédito y su licencia.
- **La fotografía recibida llevaba incrustadas las coordenadas GPS de la captura.** Se han eliminado de todas las copias depositadas. Conviene revisar este punto en cualquier imagen que se publique.

**Recomendación.** Recuperar los ficheros `.py` originales de cada versión y conservarlos en texto UTF-8 con control de versiones. Guardar el SVG de cada trazado junto a sus parámetros. Confirmar la autoría de la fotografía.

### Estructural: organización y relaciones entre componentes. Riesgo alto.

- **No hay vínculo entre cada dibujo y la versión del código y los parámetros que lo produjeron.**
- **La versión que generó «5 VAR-1 GPT7» no se ha identificado.** El código conservado corresponde al sistema de silueta con dos sistemas de relleno (H y V). La obra, en cambio, muestra líneas que se curvan hacia la derecha y no presenta líneas verticales. Eso apunta a la variación de la "curva derecha" que describe el cuaderno (afirmación interpretativa, incertidumbre media).
- **La cronología no encaja.** El cuaderno (18-10-2026) describe la curva derecha como una variación en curso, pero la obra se expuso en 2025. Puede que el cuaderno se redactara después del trabajo o que la curva tenga varias fases. Solo los autores pueden aclararlo.

**Recomendación.** Abrir un registro de trazados. Cada dibujo de la serie tendría su fila con fecha, versión del código, parámetros, papel, pluma, suma del SVG y fotografía. Para «5 VAR-1 GPT7», reconstruir esa fila con lo que los autores recuerden y declarar como desconocido lo que no.

### Funcional: código, dependencias y condiciones de ejecución. Riesgo medio.

- **El cálculo del dibujo es determinista y solo usa la biblioteca estándar de Python.** Con el código correcto y los mismos parámetros, el SVG sale idéntico, y el riesgo de obsolescencia de esta parte es bajo.
- **El fichero conservado no se ejecuta tal cual.** Llama a una función de previsualización que no está definida.
- **El trazado depende de una biblioteca de control del plotter y del propio plotter de pluma.** No constan el modelo, la versión de la biblioteca ni la versión de Python.

**Recomendación.** Completar el código, fijar las versiones de Python y de la biblioteca de control y comprobar que regenera el SVG. A partir de ahí, el SVG es la vía de migración natural: se puede trazar con otros plotters o reproducir en pantalla.

### Experiencial: comportamiento y presencia de la obra. Riesgo alto.

- **La técnica es mixta: plotter de pluma e intervención del autor.** La parte trazada por el plotter es repetible; la intervención no lo es. En la fotografía se aprecia una capa de líneas rojas de trazo irregular, distinta de la serie oscura. La hipótesis de que esa capa sea la intervención es interpretativa, con incertidumbre alta.
- **No constan las dimensiones de la hoja, el papel, las plumas ni las tintas.** El montaje y el soporte los realizó Mauro Herrero Cantos; sus materiales tampoco constan.
- **No consta dónde se conserva el original.**

**Recomendación.** Describir la intervención: en qué consiste, con qué material se hizo y en qué momento del proceso. Registrar dimensiones, papel y tintas. Hacer una captura en alta resolución con luz controlada y una carta de color. Indicar dónde se custodia el original.

## Propiedades significativas

Son las propiedades que cualquier migración, reproducción o exhibición futura debería respetar (en PREMIS, *significantProperties*). Es una propuesta pendiente de validación por los autores:

1. La acumulación de planos horizontales en perspectiva cónica, con su densidad y su ritmo.
2. La ruptura: una franja sin trazos que separa los volúmenes.
3. La curvatura del contorno.
4. La superposición desplazada de dos series de líneas y el contraste entre ellas: líneas oscuras regulares y líneas rojas de trazo irregular.
5. La coexistencia del trazo mecánico y la intervención manual sobre la misma hoja.
6. El soporte de papel y la escala física de la obra.

## Plan de preservación

| Prioridad | Acción | Responsable |
|---|---|---|
| 1 | Revisar y validar las afirmaciones interpretativas y las síntesis del expediente | Autores |
| 2 | Recuperar el código de cada versión y conservarlo con control de versiones | Autor |
| 3 | Reconstruir la fila de «5 VAR-1 GPT7» en un registro de trazados | Autores |
| 4 | Documentar la intervención, las dimensiones, el papel y las tintas | Autores |
| 5 | Captura maestra con luz controlada y carta de color | Autores e IPEX |
| 6 | Depósito en Zenodo (registro abierto y registro restringido) y verificación anual de las sumas | IPEX |
| 7 | Actualizar el expediente con una versión nueva cada vez que aparezca información | IPEX |

## Vías de migración

- **Código:** pasar de Word a ficheros `.py` en UTF-8 con control de versiones. Conservar el SVG de cada trazado como formato de intercambio estable entre el código y cualquier plotter.
- **Imagen:** conservar el máster en PNG sin pérdida (o en TIFF si se hace una captura nueva) y usar JPEG solo para las representaciones.
- **Metadatos:** mantener el expediente en JSON-LD y RO-Crate, con exportación a EDM para Hispana y Europeana.

## Valoración razonada de la condición de preservación

El demostrador sitúa la condición de preservación de la obra en un continuum entre débil y fuerte, a partir del planteamiento del libro (cap. 3–5). Depende de los metadatos que la obra satisface y de una valoración experta y colegiada. Lo que sigue aplica los criterios del libro a la documentación disponible. Es una propuesta del equipo y se puede revisar en cuanto aparezca información nueva.

| Criterio del libro | Evidencia disponible | Efecto |
|---|---|---|
| Singularidad | La técnica mixta combina un trazado repetible con una intervención irrepetible: cada hoja es única aunque el código sea determinista | Refuerza |
| Interacción con la tecnología digital | La obra se genera con un sistema de código propio y un plotter, en diálogo con la mano del autor | Refuerza |
| Condiciones de creación | El autor documenta la intención, la hibridación y la evolución del sistema en su cuaderno | Refuerza |
| Documentación | Están cubiertos 24 de 25 elementos obligatorios, pero falta la versión exacta del código y la intervención no está descrita | Refuerza en parte |
| Condiciones de exhibición | Consta una exposición (COAM, 2025), sin título, fechas ni catálogo | Sin datos suficientes |
| Importancia cultural | No hay recepción crítica ni contexto histórico documentados | Sin datos suficientes |
| Impacto en los espectadores | No hay registros | Sin datos suficientes |

**Propuesta: condición de preservación intermedia, con potencial para reforzarse.** Los criterios que dependen de la obra y de su proceso (singularidad, relación con lo digital, condiciones de creación) apuntan hacia el polo fuerte. Los que dependen de su recorrido público (exhibición, recepción, impacto) carecen de datos, y mientras falten la valoración no puede ir más allá. Los pasos que más la harían avanzar son documentar la intervención, identificar la versión del código y reunir la documentación de la exposición en el COAM y cualquier texto crítico.

## Cuestiones abiertas

A 2 de noviembre de 2026 no tienen respuesta y quedan declaradas como desconocidas. El expediente es válido con ellas abiertas; cuando se respondan, se publicará una versión nueva.

1. ¿En qué consistió la intervención del autor? ¿Es la capa roja?
2. ¿Con qué versión del código y qué parámetros se trazó la obra? ¿Se conserva el fichero?
3. ¿Cómo encaja la fecha de la obra (2025) con el cuaderno, que describe la curva derecha como una variación en curso en 2026?
4. ¿Qué medidas tiene la hoja, qué papel, plumas y tintas se usaron, y con qué materiales se hicieron el montaje y el soporte?
5. ¿Dónde se conserva el original?
6. ¿Qué datos hay de la exposición en el COAM (título, fechas, comisariado, catálogo)?
7. ¿Quién hizo la fotografía?
8. ¿Qué significa el título «5 VAR-1 GPT7»? Si responde a una nomenclatura de la serie, conviene registrarla.
