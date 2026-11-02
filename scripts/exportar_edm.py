#!/usr/bin/env python3
"""Exporta «5 VAR-1 GPT7» al modelo de datos de Europeana (EDM), en RDF/XML.

Lee los registros del expediente y genera edm/edm.xml con las tres clases
básicas de EDM: edm:ProvidedCHO (la obra), edm:WebResource (su representación)
y ore:Aggregation (quién la aporta y con qué derechos).

La URL de la representación depende del depósito en Zenodo. Mientras no exista,
se usa un marcador; tras el depósito se vuelve a ejecutar con --url-imagen.

Uso:
  python3 scripts/exportar_edm.py expedientes/hibridaciones-algoritmicas [--url-imagen URL]
"""
import json
import sys
from pathlib import Path

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import DC, DCTERMS, RDF

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validar import ODA, cargar_expediente  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
EDM = Namespace("http://www.europeana.eu/schemas/edm/")
ORE = Namespace("http://www.openarchives.org/ore/terms/")
BASE = "https://w3id.org/oda-lab/expedientes/hibridaciones-algoritmicas#"
MARCADOR = "https://zenodo.org/records/23883743/files/5-VAR-1-GPT7_1200px.jpg"
PAGINA = "https://doi.org/10.5281/zenodo.23883743"
CCBYNCND = URIRef("http://creativecommons.org/licenses/by-nc-nd/4.0/")


def valor(g, sobre, elemento):
    for reg in g.subjects(ODA.elemento, ODA[elemento]):
        if str(g.value(reg, ODA.sobre)).endswith(sobre):
            v = g.value(reg, ODA.valor)
            if v is not None:
                return str(v)
    return None


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        sys.exit(__doc__)
    url = sys.argv[sys.argv.index("--url-imagen") + 1] if "--url-imagen" in sys.argv else MARCADOR
    carpeta = (RAIZ / args[0]).resolve()
    exp = cargar_expediente(carpeta)

    g = Graph()
    for p, ns in [("edm", EDM), ("ore", ORE), ("dc", DC), ("dcterms", DCTERMS)]:
        g.bind(p, ns)
    cho, agg, web = URIRef(BASE + "cho"), URIRef(BASE + "aggregation"), URIRef(url)

    g.add((cho, RDF.type, EDM.ProvidedCHO))
    g.add((cho, DC.title, Literal(valor(exp, "5-var-1-gpt7", "e1_1_titulo"), lang="es")))
    g.add((cho, DC.creator, Literal("Alonso López Iniesta, Juan")))
    g.add((cho, DC.contributor, Literal("Herrero Cantos, Mauro")))
    g.add((cho, DC.description, Literal(valor(exp, "5-var-1-gpt7", "e1_4_descripcion"), lang="es")))
    g.add((cho, DC.type, Literal("Dibujo", lang="es")))
    for t in valor(exp, "obra", "e5_9_generos_metodos").split(" (")[0].split("; "):
        g.add((cho, DC.type, Literal(t)))
    g.add((cho, DCTERMS.medium, Literal(valor(exp, "5-var-1-gpt7", "e5_4_tecnicas"), lang="es")))
    g.add((cho, DCTERMS.isPartOf, Literal("Hibridaciones algorítmicas", lang="es")))
    g.add((cho, DC.subject, Literal("Arte generativo", lang="es")))
    g.add((cho, EDM.type, Literal("IMAGE")))

    g.add((web, RDF.type, EDM.WebResource))
    g.add((web, EDM.rights, CCBYNCND))
    g.add((web, DC.format, Literal("image/jpeg")))

    g.add((agg, RDF.type, ORE.Aggregation))
    g.add((agg, EDM.aggregatedCHO, cho))
    g.add((agg, EDM.isShownBy, web))
    g.add((agg, EDM.isShownAt, URIRef(PAGINA)))
    g.add((agg, EDM.dataProvider, Literal("IPEX, Universidad Rey Juan Carlos")))
    g.add((agg, EDM.provider, Literal("IPEX, Universidad Rey Juan Carlos")))
    g.add((agg, EDM.rights, CCBYNCND))

    destino = carpeta / "edm" / "edm.xml"
    destino.parent.mkdir(parents=True, exist_ok=True)
    g.serialize(destination=destino, format="xml")
    aviso = ""
    print(f"Escrito {destino.relative_to(RAIZ)}{aviso}.")


if __name__ == "__main__":
    main()
