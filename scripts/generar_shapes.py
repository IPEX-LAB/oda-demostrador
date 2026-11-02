#!/usr/bin/env python3
"""Genera perfil/shapes.ttl (reglas SHACL) a partir de perfil/perfil-oda.csv.

Criterio (libro ODA, cap. 3-5): la condición de preservación es un continuum, no un sí/no.
- Elemento obligatorio (C): debe estar TRATADO, es decir, cubierto o declarado como
  laguna con su motivo. Si no está tratado -> sh:Violation.
- Elemento opcional (O): si falta -> sh:Warning (informa, no bloquea).
Uso: python3 scripts/generar_shapes.py
"""
import csv
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CSV = RAIZ / "perfil" / "perfil-oda.csv"
SALIDA = RAIZ / "perfil" / "shapes.ttl"

CABECERA = """@prefix sh:     <http://www.w3.org/ns/shacl#> .
@prefix xsd:    <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs:   <http://www.w3.org/2000/01/rdf-schema#> .
@prefix oda:    <https://w3id.org/oda-lab/perfil#> .
@prefix shp:    <https://w3id.org/oda-lab/perfil/shapes#> .

# Reglas SHACL del perfil de aplicación ODA (demostrador).
# Generado por scripts/generar_shapes.py a partir de perfil/perfil-oda.csv. No editar a mano.

# --- Registro: cada dato del expediente ---------------------------------------
shp:Registro a sh:NodeShape ;
    sh:targetClass oda:Registro ;
    sh:property [ sh:path oda:elemento ; sh:minCount 1 ; sh:maxCount 1 ; sh:nodeKind sh:IRI ;
                  sh:message "Cada registro indica un único elemento del perfil."@es ] ;
    sh:property [ sh:path oda:sobre ; sh:minCount 1 ; sh:nodeKind sh:IRI ;
                  sh:message "Cada registro indica la entidad a la que se refiere (oda:sobre)."@es ] ;
    sh:property [ sh:path oda:estado ; sh:minCount 1 ; sh:maxCount 1 ;
                  sh:in ( oda:documentado oda:reconstruido oda:inferido oda:pendiente oda:desconocido oda:perdido oda:no_aplicable ) ;
                  sh:message "Estado no válido o ausente."@es ] ;
    sh:or ( shp:RegistroCubierto shp:RegistroLaguna ) ;
    sh:message "Un registro cubierto necesita valor y fuente; una laguna necesita motivo."@es .

shp:RegistroCubierto a sh:NodeShape ;
    sh:property [ sh:path oda:estado ; sh:in ( oda:documentado oda:reconstruido oda:inferido ) ] ;
    sh:or ( [ sh:path oda:valor ; sh:minCount 1 ] [ sh:path oda:valorRef ; sh:minCount 1 ] ) ;
    sh:property [ sh:path oda:fuente ; sh:minCount 1 ] .

shp:RegistroLaguna a sh:NodeShape ;
    sh:property [ sh:path oda:estado ; sh:in ( oda:pendiente oda:desconocido oda:perdido oda:no_aplicable ) ] ;
    sh:property [ sh:path oda:motivo ; sh:minCount 1 ] .

# --- Afirmación relacional ------------------------------------------------------
shp:Afirmacion a sh:NodeShape ;
    sh:targetClass oda:Afirmacion ;
    sh:property [ sh:path oda:sujeto ; sh:minCount 1 ; sh:maxCount 1 ] ;
    sh:property [ sh:path oda:predicado ; sh:minCount 1 ; sh:maxCount 1 ] ;
    sh:property [ sh:path oda:objeto ; sh:minCount 1 ] ;
    sh:property [ sh:path oda:responsable ; sh:minCount 1 ] ;
    sh:property [ sh:path oda:evidencia ; sh:minCount 1 ] ;
    sh:property [ sh:path oda:fecha ; sh:minCount 1 ; sh:maxCount 1 ; sh:datatype xsd:date ] ;
    sh:property [ sh:path oda:estatuto ; sh:minCount 1 ; sh:maxCount 1 ;
                  sh:in ( oda:documentada_autor oda:observable oda:interpretativa ) ] ;
    sh:property [ sh:path oda:validacion ; sh:minCount 1 ; sh:maxCount 1 ;
                  sh:in ( oda:validada oda:pendiente_validacion ) ] ;
    sh:property [ sh:path oda:incertidumbre ; sh:maxCount 1 ; sh:in ( oda:baja oda:media oda:alta ) ] ;
    sh:or ( [ sh:not [ sh:path oda:estatuto ; sh:hasValue oda:interpretativa ] ]
            [ sh:path oda:incertidumbre ; sh:minCount 1 ] ) ;
    sh:message "Las afirmaciones interpretativas declaran su grado de incertidumbre."@es .

# --- Expediente: cobertura de los elementos del perfil ---------------------------
shp:Expediente a sh:NodeShape ;
    sh:targetClass oda:Expediente ;
    sh:property [ sh:path oda:describe ; sh:minCount 1 ] ;
"""


def main():
    filas = list(csv.DictReader(CSV.open(encoding="utf-8")))
    bloques = []
    for f in filas:
        obligatorio = f["obligatoriedad"] == "C"
        sev = "sh:Violation" if obligatorio else "sh:Warning"
        tipo = "obligatorio (C)" if obligatorio else "opcional (O)"
        accion = ("debe cubrirse o declararse como laguna" if obligatorio
                  else "no consta; no bloquea, pero se tiene en cuenta en la valoración")
        msg = f'{f["id"]} {f["elemento"]} [{tipo}]: {accion}.'
        bloques.append(
            "    sh:property [ sh:path oda:registro ;\n"
            f"        sh:name \"{f['id']} {f['elemento']}\"@es ;\n"
            f"        sh:qualifiedValueShape [ sh:path oda:elemento ; sh:hasValue {f['termino']} ] ;\n"
            "        sh:qualifiedMinCount 1 ;\n"
            f"        sh:severity {sev} ;\n"
            f"        sh:message \"{msg}\"@es ]"
        )
    elementos = " ".join(f["termino"] for f in filas)
    texto = CABECERA + " ;\n".join(bloques) + " .\n\n"
    texto += ("# Lista cerrada de elementos válidos\n"
              "shp:ElementoValido a sh:NodeShape ;\n"
              "    sh:targetClass oda:Registro ;\n"
              f"    sh:property [ sh:path oda:elemento ; sh:in ( {elementos} ) ;\n"
              "                  sh:message \"El elemento no pertenece al perfil ODA.\"@es ] .\n")
    SALIDA.write_text(texto, encoding="utf-8")
    print(f"Escrito {SALIDA.relative_to(RAIZ)} con {len(filas)} elementos.")


if __name__ == "__main__":
    main()
