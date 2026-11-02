#!/usr/bin/env python3
"""Valida un expediente ODA contra las reglas SHACL del perfil y escribe un informe.

El informe no aprueba ni suspende la obra: muestra qué elementos del perfil
satisface, cuáles están declarados como laguna y cuáles faltan.

Uso:
  python3 scripts/validar.py expedientes/hibridaciones-algoritmicas
"""
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

from pyshacl import validate
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import SH

RAIZ = Path(__file__).resolve().parent.parent
ODA = Namespace("https://w3id.org/oda-lab/perfil#")
CUBIERTOS = {"documentado", "reconstruido", "inferido"}


def cargar_expediente(carpeta: Path) -> Graph:
    datos = json.loads((carpeta / "expediente-oda.jsonld").read_text(encoding="utf-8"))
    contexto = json.loads((RAIZ / "perfil" / "context.jsonld").read_text(encoding="utf-8"))
    datos["@context"] = contexto["@context"]
    g = Graph()
    g.parse(data=json.dumps(datos), format="json-ld", base=(carpeta / "expediente-oda.jsonld").as_uri())
    return g


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    carpeta = (RAIZ / sys.argv[1]).resolve()
    datos = cargar_expediente(carpeta)
    formas = Graph().parse(RAIZ / "perfil" / "shapes.ttl")
    conforme, resultados, _ = validate(datos, shacl_graph=formas, inference="none", advanced=True)

    errores, avisos = [], []
    for r in resultados.subjects(SH.resultSeverity, None):
        sev = resultados.value(r, SH.resultSeverity)
        msg = str(resultados.value(r, SH.resultMessage))
        foco = str(resultados.value(r, SH.focusNode)).split("#")[-1]
        if not foco.startswith("expediente"):
            msg += f" (#{foco})"
        (errores if sev == SH.Violation else avisos).append(msg)

    perfil = list(csv.DictReader((RAIZ / "perfil" / "perfil-oda.csv").open(encoding="utf-8")))
    estados = defaultdict(list)
    for reg in datos.subjects(ODA.elemento, None):
        el = str(datos.value(reg, ODA.elemento)).split("#")[-1]
        est = str(datos.value(reg, ODA.estado)).split("#")[-1]
        estados[el].append(est)

    filas, cuenta = [], defaultdict(int)
    for f in perfil:
        clave = f["termino"].split(":")[-1]
        ests = estados.get(clave, [])
        if not ests:
            situacion = "falta (error)" if f["obligatoriedad"] == "C" else "no consta (aviso)"
        elif any(e in CUBIERTOS for e in ests):
            situacion = "cubierto"
        else:
            situacion = "laguna declarada"
        cuenta[(f["obligatoriedad"], situacion)] += 1
        filas.append((f["id"], f["categoria"], f["elemento"], f["obligatoriedad"],
                      ", ".join(sorted(set(ests))).replace("_", " ") or "—", situacion))

    n_afirm = len(set(datos.subjects(None, ODA.Afirmacion)))
    estatutos = defaultdict(int)
    for a in datos.subjects(ODA.estatuto, None):
        estatutos[str(datos.value(a, ODA.estatuto)).split("#")[-1].replace("_", " ")] += 1

    lineas = [
        f"# Informe de validación: {carpeta.name}",
        "",
        f"Resultado SHACL: **{'sin errores' if not errores else f'{len(errores)} errores'}**, {len(avisos)} avisos.",
        "",
        "Un elemento obligatorio (C) cuenta como tratado si está cubierto o declarado como laguna con su motivo.",
        "Los avisos señalan elementos opcionales (O) que no constan: no bloquean, pero cuentan en la valoración.",
        "",
        "## Resumen",
        "",
        "| | Cubierto | Laguna declarada | No consta |",
        "|---|---|---|---|",
        f"| Obligatorios (C) | {cuenta[('C','cubierto')]} | {cuenta[('C','laguna declarada')]} | {cuenta[('C','falta (error)')]} |",
        f"| Opcionales (O) | {cuenta[('O','cubierto')]} | {cuenta[('O','laguna declarada')]} | {cuenta[('O','no consta (aviso)')]} |",
        "",
        f"Afirmaciones relacionales: {n_afirm} (" + ", ".join(f"{v} {k}" for k, v in sorted(estatutos.items())) + ").",
        "",
        "## Elementos",
        "",
        "| Id | Categoría | Elemento | C/O | Estado | Situación |",
        "|---|---|---|---|---|---|",
    ]
    lineas += [f"| {a} | {b} | {c} | {d} | {e} | {s} |" for a, b, c, d, e, s in filas]
    if errores:
        lineas += ["", "## Errores", ""] + [f"- {m}" for m in sorted(set(errores))]
    if avisos:
        lineas += ["", "## Avisos", ""] + [f"- {m}" for m in sorted(set(avisos))]
    salida = carpeta / "diagnostico" / "informe-validacion.md"
    salida.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    print("\n".join(lineas[:16]))
    print(f"\nInforme completo en {salida.relative_to(RAIZ)}")
    sys.exit(0 if not errores else 1)


if __name__ == "__main__":
    main()
