# Correspondencias entre ODA y los estándares en uso

[`oda-correspondencias.csv`](oda-correspondencias.csv) relaciona cada elemento del perfil ODA con los estándares más usados en patrimonio y preservación digital:

- Dublin Core;
- EDM, el modelo de datos de Europeana (y de Hispana);
- Linked Art / CIDOC-CRM, con CRMdig para procesos digitales y CRMinf para hipótesis;
- PREMIS 3, para preservación;
- RiC-O, para descripción archivística;
- schema.org, que es la base de los metadatos RO-Crate.

La columna `cobertura_estandares` resume cuánto del elemento resuelven ya esos estándares. La columna `aportacion_oda` indica qué añade el perfil.

## Resultado

De los 40 elementos del libro y las 2 extensiones del perfil (42 filas):

| Cobertura por los estándares | Elementos |
|---|---|
| Completa | 19 |
| Parcial | 18 |
| Ninguna estructurada | 5 |

Los huecos se concentran en los metadatos-arte: intención artística, innovación y contexto histórico no tienen un campo estructurado en ningún estándar. Tampoco el estado de cada dato ni el estatuto epistemológico de las relaciones, que CIDOC-CRM solo cubre en parte con E13 y CRMinf. Esa es la respuesta a la pregunta de qué aporta ODA frente a lo que ya existe.

## Pendiente

La columna RiC-O está marcada como "revisar" donde la correspondencia exacta del término no está confirmada. Debe revisarla una persona experta en RiC-O antes de publicar.
