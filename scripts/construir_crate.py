#!/usr/bin/env python3
"""Genera ro-crate-metadata.json (RO-Crate 1.2) para el expediente de Hibridaciones algorítmicas.

Las entidades de la obra, los eventos de preservación y los ficheros restringidos
se describen aquí; los tamaños se leen del disco. Ejecutar antes de checksums.py.

Uso:
  python3 scripts/construir_crate.py expedientes/hibridaciones-algoritmicas restringido/
"""
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PERFIL = "https://w3id.org/oda-lab/perfil"
PREMIS = "http://id.loc.gov/vocabulary/preservation/eventType/"
CC0 = "https://creativecommons.org/publicdomain/zero/1.0/"
CCBY = "https://creativecommons.org/licenses/by/4.0/"
CCBYNCND = "https://creativecommons.org/licenses/by-nc-nd/4.0/"
INC = "http://rightsstatements.org/vocab/InC/1.0/"
HOY = "2026-11-02"

# Ficheros del paquete abierto: ruta relativa -> (nombre, tipo MIME, licencia, descripción)
FICHEROS = {
    "expediente-oda.jsonld": ("Expediente ODA (registros y afirmaciones)", "application/ld+json", CC0,
                              "Registros de los 40 elementos del perfil ODA y afirmaciones relacionales con estatuto epistemológico."),
    "representaciones/5-VAR-1-GPT7_1200px.jpg": ("«5 VAR-1 GPT7», representación 1200 px", "image/jpeg", CCBYNCND,
                              "Representación de la obra a partir de la fotografía del 07-10-2026, sin metadatos incrustados."),
    "representaciones/5-VAR-1-GPT7_400px.jpg": ("«5 VAR-1 GPT7», miniatura 400 px", "image/jpeg", CCBYNCND,
                              "Miniatura de la representación."),
    "relaciones/grafo.svg": ("Grafo de relaciones", "image/svg+xml", CC0,
                             "Afirmaciones del expediente dibujadas por estatuto: documentadas por el autor, observables e interpretativas."),
    "diagnostico/diagnostico.md": ("Diagnóstico de preservación y valoración aurática", "text/markdown", CCBY,
                                   "Diagnóstico en cuatro dimensiones, plan de preservación y propuesta razonada de condición aurática."),
    "diagnostico/informe-validacion.md": ("Informe de validación SHACL", "text/markdown", CC0,
                                          "Cobertura de los elementos obligatorios y opcionales del perfil."),
    "edm/edm.xml": ("Exportación EDM", "application/rdf+xml", CC0,
                    "Registro en el modelo de datos de Europeana, preparado para Hispana."),
    "preservacion/manifiesto-sha256.txt": ("Manifiesto SHA-256", "text/plain", CC0,
                                           "Sumas de verificación de todos los ficheros, abiertos y restringidos."),
}

# Ficheros maestros: se depositan en un registro de Zenodo de acceso restringido.
RESTRINGIDOS = {
    "5-VAR-1-GPT7_maestro_3024px.png": ("Fotografía maestra de «5 VAR-1 GPT7»", "image/png",
                                        "PNG sin pérdida, 3024 × 3024 px, sin metadatos incrustados."),
    "codigo-base-sistema-HV.docx": ("Código base del sistema de silueta H+V", "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                    "Código Python copiado en un documento de Word, sin sangría. No es la versión que produjo «5 VAR-1 GPT7»."),
}


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    carpeta = (RAIZ / sys.argv[1]).resolve() if not Path(sys.argv[1]).is_absolute() else Path(sys.argv[1])
    restr = Path(sys.argv[2]).resolve()

    grafo = [
        {"@id": "ro-crate-metadata.json", "@type": "CreativeWork",
         "conformsTo": {"@id": "https://w3id.org/ro/crate/1.2"}, "about": {"@id": "./"}},
        {"@id": "./", "@type": "Dataset",
         "name": "Expediente ODA de Hibridaciones algorítmicas",
         "description": ("Demostrador del método ODA (Objeto Digital Aurático) aplicado a la obra Hibridaciones algorítmicas "
                         "de Juan Alonso López Iniesta y a su obra resultante «5 VAR-1 GPT7». Reúne el expediente de metadatos, "
                         "las relaciones con su estatuto epistemológico, el diagnóstico de preservación y una valoración razonada "
                         "de la condición aurática. No es una evaluación de Fund_ODA."),
         "datePublished": HOY,
         "license": {"@id": CC0},
         "conformsTo": {"@id": PERFIL},
         "about": [{"@id": "#obra"}, {"@id": "#5-var-1-gpt7"}],
         "author": {"@id": "#ipex"},
         "publisher": {"@id": "#ipex"},
         "url": "https://github.com/IPEX-LAB/oda-demostrador",
         "keywords": ["Objeto Digital Aurático", "preservación digital", "arte generativo", "dibujo", "RO-Crate", "metadatos"],
         "inLanguage": "es",
         "hasPart": [{"@id": r} for r in FICHEROS],
         "mentions": [{"@id": "#evento-captura"}, {"@id": "#evento-recorte"}, {"@id": "#evento-creacion"},
                      {"@id": "#exposicion-coam"}, {"@id": "#evento-ingreso"}, {"@id": "#evento-derivados"},
                      {"@id": "#evento-sumas"}, {"@id": "#evento-validacion"}]},
        {"@id": PERFIL, "@type": ["CreativeWork", "Profile"], "name": "Perfil de aplicación ODA (demostrador)",
         "description": "Esquema de metadatos del libro Objeto Digital Aurático (2025, cap. 4) con elementos obligatorios (C) y opcionales (O)."},
    ]

    for ruta, (nombre, mime, lic, desc) in FICHEROS.items():
        f = carpeta / ruta
        ent = {"@id": ruta, "@type": "File", "name": nombre, "encodingFormat": mime, "description": desc}
        if lic != CC0:
            ent["license"] = {"@id": lic}
        if f.exists():
            ent["contentSize"] = str(f.stat().st_size)
        if ruta.startswith("representaciones/"):
            ent["about"] = {"@id": "#5-var-1-gpt7"}
            ent["creditText"] = "Fotografía: autoría pendiente de confirmar"
        if ruta == "expediente-oda.jsonld":
            ent["conformsTo"] = {"@id": PERFIL}
        grafo.append(ent)

    for nombre_f, (nombre, mime, desc) in RESTRINGIDOS.items():
        f = restr / nombre_f
        grafo.append({"@id": f"#restringido-{Path(nombre_f).stem}", "@type": "CreativeWork", "name": nombre,
                      "alternateName": nombre_f, "encodingFormat": mime, "description": desc,
                      "contentSize": str(f.stat().st_size) if f.exists() else None,
                      "conditionsOfAccess": "Acceso restringido bajo solicitud en un registro aparte de Zenodo (comunidad IPEX). Suma SHA-256 en el manifiesto.",
                      "license": {"@id": INC}})

    grafo += [
        {"@id": "#obra", "@type": "CreativeWork", "name": "Hibridaciones algorítmicas",
         "creator": {"@id": "https://orcid.org/0000-0003-3630-5474"},
         "description": ("Serie de investigación artística en dibujo generativo: un sistema escrito en código construye volúmenes "
                         "por acumulación de planos horizontales en perspectiva cónica con dos puntos de fuga, sometidos a "
                         "principios tomados de la obra de Nasreen Mohamedi (ritmo, ruptura o silencio, acumulación)."),
         "genre": ["Generative art / arte generativo", "Computer art"],
         "hasPart": {"@id": "#5-var-1-gpt7"},
         "isBasedOn": {"@id": "#mohamedi"}},
        {"@id": "#5-var-1-gpt7", "@type": "VisualArtwork", "name": "5 VAR-1 GPT7",
         "creator": {"@id": "https://orcid.org/0000-0003-3630-5474"},
         "contributor": {"@id": "https://orcid.org/0000-0002-0449-9975"},
         "creditText": "Juan Alonso López Iniesta. Realización de la parte física: Mauro Herrero Cantos.",
         "artMedium": "Técnica mixta: plotter de pluma e intervención del autor",
         "artworkSurface": "Papel",
         "isPartOf": {"@id": "#obra"},
         "image": {"@id": "representaciones/5-VAR-1-GPT7_1200px.jpg"},
         "license": {"@id": INC}},
        {"@id": "https://orcid.org/0000-0003-3630-5474", "@type": "Person", "name": "Juan Alonso López Iniesta",
         "affiliation": {"@id": "#urjc"}},
        {"@id": "https://orcid.org/0000-0002-0449-9975", "@type": "Person", "name": "Mauro Herrero Cantos", "affiliation": {"@id": "#urjc"}},
        {"@id": "https://orcid.org/0000-0002-5521-6445", "@type": "Person", "name": "Elena Battaner Moro",
         "affiliation": {"@id": "#urjc"}},
        {"@id": "#ipex", "@type": "Organization",
         "name": "IPEX, Grupo de Investigación en Interfaces y Prototipos Experimentales",
         "url": "https://github.com/IPEX-LAB",
         "parentOrganization": {"@id": "#urjc"},
         "member": [{"@id": "https://orcid.org/0000-0003-3630-5474"}, {"@id": "https://orcid.org/0000-0002-0449-9975"}, {"@id": "https://orcid.org/0000-0002-5521-6445"}]},
        {"@id": "#urjc", "@type": "Organization", "name": "Universidad Rey Juan Carlos", "url": "https://www.urjc.es"},
        {"@id": "#mohamedi", "@type": "Person", "name": "Nasreen Mohamedi", "birthDate": "1937", "deathDate": "1990"},
        {"@id": "#coam", "@type": "Place", "name": "Colegio Oficial de Arquitectos de Madrid (COAM)"},
        {"@id": "#iphone", "@type": "IndividualProduct", "name": "iPhone 11 Pro Max"},
        {"@id": "#photoshop", "@type": "SoftwareApplication", "name": "Adobe Photoshop", "version": "27.11",
         "url": "https://www.adobe.com/products/photoshop.html"},
        {"@id": "#pyshacl", "@type": "SoftwareApplication", "name": "pySHACL", "version": "0.40.2",
         "url": "https://github.com/RDFLib/pySHACL"},
        {"@id": "#rocrate-validator", "@type": "SoftwareApplication", "name": "rocrate-validator", "version": "0.13.1",
         "url": "https://github.com/crs4/rocrate-validator"},

        {"@id": "#evento-creacion", "@type": "CreateAction", "name": "Creación de «5 VAR-1 GPT7»",
         "additionalType": {"@id": PREMIS + "cre"},
         "description": "Técnica mixta: plotter de pluma e intervención del autor. Fecha de ejecución no documentada; la obra se expuso en 2025.",
         "agent": {"@id": "https://orcid.org/0000-0003-3630-5474"}, "participant": {"@id": "https://orcid.org/0000-0002-0449-9975"}, "result": {"@id": "#5-var-1-gpt7"}},
        {"@id": "#exposicion-coam", "@type": "ExhibitionEvent", "name": "Exposición de «5 VAR-1 GPT7» en el COAM",
         "startDate": "2025", "location": {"@id": "#coam"}, "workFeatured": {"@id": "#5-var-1-gpt7"},
         "description": "No constan el título de la exposición, las fechas exactas ni el catálogo."},
        {"@id": "#evento-captura", "@type": "CreateAction", "name": "Captura fotográfica de «5 VAR-1 GPT7»",
         "additionalType": {"@id": PREMIS + "cap"}, "endTime": "2026-10-07",
         "instrument": {"@id": "#iphone"}, "object": {"@id": "#5-var-1-gpt7"},
         "result": {"@id": "#restringido-5-VAR-1-GPT7_maestro_3024px"},
         "description": "Fecha y dispositivo tomados de los metadatos de la fotografía; autoría no documentada."},
        {"@id": "#evento-recorte", "@type": "UpdateAction", "name": "Recorte cuadrado de la fotografía",
         "endTime": "2026-10-13", "instrument": {"@id": "#photoshop"},
         "object": {"@id": "#restringido-5-VAR-1-GPT7_maestro_3024px"},
         "description": "De 4032 × 3024 px a 3024 × 3024 px, según los metadatos de edición."},
        {"@id": "#evento-ingreso", "@type": "CreateAction", "name": "Ingreso de la documentación en el expediente",
         "additionalType": {"@id": PREMIS + "ing"}, "endTime": HOY, "agent": {"@id": "#ipex"},
         "result": {"@id": "expediente-oda.jsonld"}},
        {"@id": "#evento-derivados", "@type": "CreateAction",
         "name": "Eliminación de metadatos incrustados y generación de representaciones",
         "endTime": HOY, "agent": {"@id": "#ipex"},
         "object": {"@id": "#restringido-5-VAR-1-GPT7_maestro_3024px"},
         "result": [{"@id": "representaciones/5-VAR-1-GPT7_1200px.jpg"}, {"@id": "representaciones/5-VAR-1-GPT7_400px.jpg"}],
         "description": "Se eliminaron los metadatos XMP y EXIF, incluidas las coordenadas GPS de la captura."},
        {"@id": "#evento-sumas", "@type": "CreateAction", "name": "Cálculo de sumas SHA-256",
         "additionalType": {"@id": PREMIS + "mes"}, "endTime": HOY, "agent": {"@id": "#ipex"},
         "result": {"@id": "preservacion/manifiesto-sha256.txt"}},
        {"@id": "#evento-validacion", "@type": "AssessAction", "name": "Validación SHACL y RO-Crate",
         "additionalType": {"@id": PREMIS + "val"}, "endTime": HOY, "agent": {"@id": "#ipex"},
         "instrument": [{"@id": "#pyshacl"}, {"@id": "#rocrate-validator"}], "object": {"@id": "expediente-oda.jsonld"},
         "result": {"@id": "diagnostico/informe-validacion.md"}},

        {"@id": CC0, "@type": "CreativeWork", "name": "CC0 1.0", "description": "Dedicación al dominio público; se aplica a los metadatos."},
        {"@id": CCBY, "@type": "CreativeWork", "name": "CC BY 4.0", "description": "Atribución 4.0 Internacional; se aplica al diagnóstico."},
        {"@id": CCBYNCND, "@type": "CreativeWork", "name": "CC BY-NC-ND 4.0", "description": "Atribución-NoComercial-SinDerivadas 4.0 Internacional; se aplica a las representaciones de la obra."},
        {"@id": INC, "@type": "CreativeWork", "name": "In Copyright", "description": "Obra protegida por derechos de autor; todos los derechos reservados."},
    ]
    for e in grafo:
        for k in [k for k, v in e.items() if v is None]:
            del e[k]
    crate = {"@context": "https://w3id.org/ro/crate/1.2/context", "@graph": grafo}
    (carpeta / "ro-crate-metadata.json").write_text(json.dumps(crate, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Escrito ro-crate-metadata.json con {len(grafo)} entidades.")


if __name__ == "__main__":
    main()
