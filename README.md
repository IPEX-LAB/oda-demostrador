# Demostrador ODA: Hibridaciones algorítmicas

Este repositorio aplica de principio a fin el método ODA (*Objeto Digital Aurático*) a una obra real: **Hibridaciones algorítmicas**, de Juan Alonso López Iniesta, y su obra resultante **«5 VAR-1 GPT7»** (técnica mixta: plotter de pluma e intervención del autor; montaje y soporte de Mauro Herrero Cantos).

Repositorio: <https://github.com/IPEX-LAB/oda-demostrador>. Lo prepara el grupo IPEX (Grupo de Investigación en Interfaces y Prototipos Experimentales, Universidad Rey Juan Carlos). Parte del esquema de metadatos del libro *Objeto Digital Aurático* (Battaner Moro y López Iniesta, Peter Lang, 2025).

## Qué contiene

| Carpeta | Contenido |
|---|---|
| [`perfil/`](perfil/) | Perfil de aplicación ODA: los 40 elementos del libro con su obligatoriedad (C/O), contexto JSON-LD y reglas SHACL |
| [`correspondencias/`](correspondencias/) | Correspondencias con Dublin Core, EDM, Linked Art / CIDOC-CRM, PREMIS, RiC-O y schema.org |
| [`expedientes/hibridaciones-algoritmicas/`](expedientes/hibridaciones-algoritmicas/) | Expediente de la obra empaquetado como RO-Crate 1.2 |
| [`scripts/`](scripts/) | Generación de reglas, validación, empaquetado, exportación EDM, grafo y sumas de verificación |
| [`web/`](web/) | Ficha web del expediente |

Dentro del expediente:

- `expediente-oda.jsonld`: 44 registros que cubren los elementos del perfil y 13 afirmaciones relacionales, cada una con su estatuto (documentada por el autor, observable o interpretativa);
- `diagnostico/`: diagnóstico de preservación en cuatro dimensiones, valoración razonada de la condición aurática e informe de validación;
- `relaciones/grafo.svg`: las afirmaciones dibujadas por estatuto;
- `edm/edm.xml`: exportación al modelo de datos de Europeana, preparada para Hispana;
- `preservacion/manifiesto-sha256.txt`: sumas de verificación de todos los ficheros, también de los restringidos;
- `representaciones/`: imágenes de la obra en baja resolución, sin metadatos incrustados.

## El criterio: un continuum, no un sí o no

El libro plantea que el aura de un objeto digital no es binaria. La condición aurática es más fuerte o más débil según los metadatos que la obra satisface y según una valoración experta. Por eso:

- un elemento obligatorio tiene que estar **tratado**: cubierto, o declarado como laguna con su motivo;
- un elemento opcional ausente genera un **aviso**, no un error;
- el expediente **no declara que la obra sea un ODA**, porque eso corresponde al proceso colegiado de Fund_ODA. Propone una valoración razonada y revisable.

## Resultado

- **Validación SHACL sin errores.** De los 25 elementos obligatorios, 24 están cubiertos y 1 declarado como laguna (el idioma, no aplicable). De los 15 opcionales constan 11.
- **RO-Crate 1.2 válido** en el nivel obligatorio, según rocrate-validator 0.13.1.
- **Condición aurática propuesta: intermedia, con potencial para reforzarse.** Ver [`diagnostico.md`](expedientes/hibridaciones-algoritmicas/diagnostico/diagnostico.md).

## Cómo regenerarlo

```bash
pip install pyshacl rdflib roc-validator
bash scripts/construir_todo.sh ruta/a/ficheros-restringidos
```

Para verificar la integridad:

```bash
python3 scripts/checksums.py expedientes/hibridaciones-algoritmicas ruta/a/ficheros-restringidos --verificar
```

## Acceso y licencias

| Contenido | Licencia | Dónde |
|---|---|---|
| Metadatos (expediente, RO-Crate, EDM, manifiesto) | CC0 1.0 | Abierto |
| Perfil, correspondencias y diagnóstico | CC BY 4.0 | Abierto |
| Scripts | MIT ([`LICENSE`](LICENSE)) | Abierto |
| Representaciones de la obra en baja resolución | CC BY-NC-ND 4.0 | Abierto |
| Fotografía maestra y código de la obra | Todos los derechos reservados | Zenodo, acceso restringido bajo solicitud |


## Depósito en Zenodo (comunidad IPEX)

| Registro | DOI | Acceso |
|---|---|---|
| Método (este repositorio) | [10.5281/zenodo.23883605](https://doi.org/10.5281/zenodo.23883605) | Abierto |
| Expediente de Hibridaciones algorítmicas | [10.5281/zenodo.23883743](https://doi.org/10.5281/zenodo.23883743) | Abierto |
| Ficheros maestros de «5 VAR-1 GPT7» | [10.5281/zenodo.23884055](https://doi.org/10.5281/zenodo.23884055) | Restringido |

## Cita

Ver [`CITATION.cff`](CITATION.cff).
