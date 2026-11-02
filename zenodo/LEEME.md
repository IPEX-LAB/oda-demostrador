# Depósito en Zenodo (comunidad IPEX)

El demostrador se deposita en tres registros enlazados entre sí. Hacen falta tres porque en Zenodo el acceso a los ficheros se fija para el registro entero: o todos son abiertos o todos restringidos.

| Registro | Contenido | Acceso | Metadatos |
|---|---|---|---|
| 1. Método | Este repositorio (perfil, correspondencias, scripts, ficha web) | Abierto | [`01-metodo.json`](01-metodo.json); también `.zenodo.json` en la raíz, para la integración con GitHub |
| 2. Expediente | La carpeta `expedientes/hibridaciones-algoritmicas/`, comprimida | Abierto | [`02-expediente.json`](02-expediente.json) |
| 3. Ficheros maestros | Fotografía maestra y código base | Restringido, bajo solicitud | [`03-maestros-restringido.json`](03-maestros-restringido.json) |

## Orden recomendado

1. **Comprobar el identificador de la comunidad.** Los ficheros usan `ipex`; hay que confirmarlo con la URL de la comunidad (`zenodo.org/communities/<identificador>`).
2. **Crear los tres registros como borrador y reservar sus DOI** con la opción de reserva del formulario. Los DOI reservados no se publican hasta que se publica el registro.
3. **Sustituir los marcadores** `DOI-DEL-REGISTRO-DEL-METODO`, `DOI-DEL-EXPEDIENTE` y `DOI-DEL-REGISTRO-RESTRINGIDO` por los DOI reservados. Actualizar también el registro 1.7 (Identificador) del expediente y volver a ejecutar `scripts/exportar_edm.py --url-imagen` con la URL definitiva de la imagen.
4. **Regenerar el expediente** con `scripts/construir_todo.sh` y verificar las sumas.
5. **Probar el proceso completo en sandbox.zenodo.org** antes del depósito real.
6. **Publicar** cuando los autores hayan revisado el contenido. Un DOI publicado no se puede retirar: solo admite versiones nuevas.

Las rutas `restringido/` del manifiesto corresponden a los ficheros del registro 3.
