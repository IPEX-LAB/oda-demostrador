#!/usr/bin/env python3
"""Genera la ficha web del expediente a partir de sus datos.

Escribe web/ficha.html (fragmento con <title>, <style> y contenido) y
web/index.html (el mismo contenido con el esqueleto HTML, para GitHub Pages),
y copia la representación y el grafo en web/img/.

Uso:
  python3 scripts/ficha.py expedientes/hibridaciones-algoritmicas
"""
import csv
import shutil
import sys
from collections import defaultdict
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validar import ODA, cargar_expediente  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
CUBIERTOS = {"documentado", "reconstruido", "inferido"}
SOBRE = {"obra": "Hibridaciones algorítmicas", "5-var-1-gpt7": "«5 VAR-1 GPT7»", "foto": "Fotografía",
         "codigo-base": "Código base", "cuaderno": "Cuaderno"}

DIMENSIONES = [
    ("Informacional", "alto", "El código se conserva copiado en Word, sin la sangría que Python necesita. El SVG enviado al plotter no se guarda."),
    ("Estructural", "alto", "No se sabe qué versión del código y qué parámetros produjeron la obra. La cronología entre la obra (2025) y el cuaderno (2026) no encaja."),
    ("Funcional", "medio", "El cálculo es determinista y solo usa la biblioteca estándar de Python, pero el fichero conservado no se ejecuta tal cual."),
    ("Experiencial", "alto", "La intervención del autor es irrepetible y no está descrita. No constan dimensiones, papel ni tintas."),
]
CRITERIOS = [
    ("Singularidad", "refuerza", "Trazado repetible e intervención irrepetible: cada hoja es única."),
    ("Interacción con la tecnología digital", "refuerza", "Sistema de código propio y plotter, en diálogo con la mano."),
    ("Condiciones de creación", "refuerza", "Intención y proceso documentados por el autor."),
    ("Documentación", "en parte", "22 de 25 obligatorios cubiertos; falta la versión del código."),
    ("Condiciones de exhibición", "sin datos", "Una exposición (COAM, 2025), sin más detalle."),
    ("Importancia cultural", "sin datos", "Sin recepción crítica ni contexto histórico documentados."),
    ("Impacto en los espectadores", "sin datos", "Sin registros."),
]
PREGUNTAS = [
    "¿En qué consistió la intervención del autor? ¿Es la capa roja?",
    "¿Qué abarcó la parte física de la que se encargó Mauro Herrero Cantos?",
    "¿Con qué versión del código y qué parámetros se trazó la obra?",
    "¿Cómo encaja la fecha de la obra (2025) con el cuaderno de 2026?",
    "¿Qué medidas tiene la hoja y qué papel, plumas y tintas se usaron?",
    "¿Dónde se conserva el original?",
    "¿Qué datos hay de la exposición en el COAM?",
    "¿Quién hizo la fotografía?",
    "¿Qué significa el título «5 VAR-1 GPT7»?",
]

CSS = """
:root {
  /* Ficha de catálogo: columna de lámina a la izquierda, datos a la derecha; debajo, el continuum en celdas. */
  --paper: #f5f6f8; --sheet: #ffffff; --ink: #1d2230; --ink-soft: #5b6173; --rule: #d8dbe2;
  --line: #2c4a80; --red: #b03445; --ok: #2c4a80; --warn: #a3651c;
  --f-display: "Newsreader", "Iowan Old Style", Georgia, serif;
  --f-body: "Public Sans", "Helvetica Neue", Arial, sans-serif;
  --f-data: "IBM Plex Mono", ui-monospace, Menlo, monospace;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --paper: #13151b; --sheet: #1b1e26; --ink: #e7e8ed; --ink-soft: #a3a8b6; --rule: #2e323d;
  --line: #8fa9de; --red: #e2717f; --ok: #8fa9de; --warn: #e0a457; color-scheme: dark } }
:root[data-theme="dark"] {
  --paper: #13151b; --sheet: #1b1e26; --ink: #e7e8ed; --ink-soft: #a3a8b6; --rule: #2e323d;
  --line: #8fa9de; --red: #e2717f; --ok: #8fa9de; --warn: #e0a457; color-scheme: dark }
* { box-sizing: border-box; }
body { background: var(--paper); color: var(--ink); font-family: var(--f-body); font-size: 15px; line-height: 1.55;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }
.page { max-width: 1060px; margin: 0 auto; padding-block: 40px 64px; display: grid; gap: 56px; }
h1, h2, h3 { font-family: var(--f-display); font-weight: 500; text-wrap: balance; margin: 0; }
h1 { font-size: clamp(2rem, 4.4vw, 3.1rem); line-height: 1.05; letter-spacing: -0.01em; }
h2 { font-size: 1.6rem; line-height: 1.2; }
h3 { font-size: 1.12rem; }
p { margin: 0; max-width: 66ch; }
.label { font-family: var(--f-data); font-size: 0.72rem; letter-spacing: 0.08em; text-transform: uppercase; color: var(--ink-soft); }
.lead { font-size: 1.05rem; color: var(--ink-soft); }
section { display: grid; gap: 18px; }
.head { display: grid; gap: 8px; }

.record { display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 6fr); gap: 40px; align-items: start; }
.plate { margin: 0; display: grid; gap: 10px; }
.plate img { width: 100%; height: auto; display: block; border: 1px solid var(--rule); background: #fff; }
.plate figcaption { font-size: 0.82rem; color: var(--ink-soft); }
.titles { display: grid; gap: 10px; padding-bottom: 20px; border-bottom: 1px solid var(--rule); }
.titles .sub { font-family: var(--f-display); font-style: italic; font-size: 1.35rem; color: var(--ink-soft); }
dl.meta { display: grid; grid-template-columns: 9.5rem minmax(0, 1fr); gap: 10px 18px; margin: 20px 0 0; }
dl.meta dt { font-family: var(--f-data); font-size: 0.74rem; letter-spacing: 0.06em; text-transform: uppercase; color: var(--ink-soft); padding-top: 3px; }
dl.meta dd { margin: 0; }
.note { border-left: 2px solid var(--red); padding: 2px 0 2px 14px; color: var(--ink-soft); font-size: 0.9rem; margin-top: 22px; }

.cells-wrap { display: grid; gap: 18px; }
.cat { display: grid; grid-template-columns: 8.5rem minmax(0, 1fr); gap: 14px; align-items: center; }
.cat .name { font-family: var(--f-data); font-size: 0.78rem; color: var(--ink-soft); text-transform: uppercase; letter-spacing: 0.06em; }
.cells { display: flex; flex-wrap: wrap; gap: 6px; }
.cell { width: 46px; height: 34px; display: grid; place-items: center; font-family: var(--f-data); font-size: 0.72rem;
  font-variant-numeric: tabular-nums; border-radius: 3px; border: 1px solid var(--rule); color: var(--ink-soft); background: transparent; }
.cell.c { border-width: 2px; }
.cell.cubierto { background: var(--line); border-color: var(--line); color: var(--sheet); }
.cell.laguna { border-color: var(--red); color: var(--red); background:
  repeating-linear-gradient(135deg, transparent 0 5px, color-mix(in srgb, var(--red) 22%, transparent) 5px 6px); }
.cell.falta { border-style: dashed; }
.legend { display: flex; flex-wrap: wrap; gap: 8px 22px; font-size: 0.85rem; color: var(--ink-soft); }
.legend span { display: inline-flex; align-items: center; gap: 8px; }
.legend .cell { width: 26px; height: 18px; font-size: 0; }
.totals { font-variant-numeric: tabular-nums; }

details.elements { border-top: 1px solid var(--rule); }
details.elements summary { cursor: pointer; padding: 12px 0; font-weight: 600; }
details.elements summary:focus-visible, a:focus-visible { outline: 2px solid var(--line); outline-offset: 3px; }
.table-scroll { overflow-x: auto; }
table { border-collapse: collapse; width: 100%; font-size: 0.88rem; }
th, td { text-align: left; vertical-align: top; padding: 8px 10px 8px 0; border-bottom: 1px solid var(--rule); }
th { font-family: var(--f-data); font-size: 0.7rem; letter-spacing: 0.07em; text-transform: uppercase; color: var(--ink-soft); font-weight: 500; }
td.id { font-family: var(--f-data); white-space: nowrap; color: var(--ink-soft); }
.state { font-family: var(--f-data); font-size: 0.72rem; white-space: nowrap; }
.state.cubierto { color: var(--line); } .state.laguna { color: var(--red); } .state.falta { color: var(--ink-soft); }

.graph { margin: 0; background: #fff; border: 1px solid var(--rule); overflow-x: auto; }
.graph img { display: block; width: 100%; min-width: 620px; height: auto; }

.dims { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0 36px; }
.dim { display: grid; gap: 6px; padding: 16px 0; border-top: 1px solid var(--rule); }
.dim-head { display: flex; justify-content: space-between; align-items: baseline; gap: 12px; }
.risk { font-family: var(--f-data); font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.06em; padding: 2px 8px; border-radius: 999px; border: 1px solid currentColor; }
.risk.alto { color: var(--red); } .risk.medio { color: var(--warn); }

.scale { display: grid; gap: 8px; max-width: 640px; }
.bar { position: relative; height: 14px; border-radius: 7px; background: linear-gradient(90deg, var(--rule), var(--line)); }
.band { position: absolute; top: -6px; bottom: -6px; left: 36%; width: 26%; border: 2px solid var(--red); border-radius: 6px; }
.ends { display: flex; justify-content: space-between; font-family: var(--f-data); font-size: 0.76rem; color: var(--ink-soft); }
.verdict { font-family: var(--f-display); font-size: 1.3rem; }
.crit .eff { font-family: var(--f-data); font-size: 0.72rem; white-space: nowrap; }
.eff.refuerza { color: var(--line); } .eff.en-parte { color: var(--warn); } .eff.sin-datos { color: var(--ink-soft); }

.two { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 36px; }
ol.qs { margin: 0; padding-left: 1.3rem; display: grid; gap: 6px; }
ul.files { list-style: none; margin: 0; padding: 0; display: grid; gap: 6px; }
ul.files code { font-family: var(--f-data); font-size: 0.8rem; }
footer { font-size: 0.82rem; color: var(--ink-soft); border-top: 1px solid var(--rule); padding-top: 18px; display: grid; gap: 6px; }

@media (max-width: 760px) {
  .record, .two, .dims { grid-template-columns: minmax(0, 1fr); }
  .cat { grid-template-columns: minmax(0, 1fr); gap: 6px; }
  dl.meta { grid-template-columns: minmax(0, 1fr); gap: 2px; }
  dl.meta dd { margin-bottom: 10px; }
}
"""


def main():
    carpeta = (RAIZ / sys.argv[1]).resolve()
    g = cargar_expediente(carpeta)
    perfil = list(csv.DictReader((RAIZ / "perfil" / "perfil-oda.csv").open(encoding="utf-8")))

    regs = defaultdict(list)
    for r in g.subjects(ODA.elemento, None):
        el = str(g.value(r, ODA.elemento)).split("#")[-1]
        regs[el].append({
            "estado": str(g.value(r, ODA.estado)).split("#")[-1],
            "sobre": SOBRE.get(str(g.value(r, ODA.sobre)).split("#")[-1], ""),
            "texto": str(g.value(r, ODA.valor) or g.value(r, ODA.motivo) or ""),
        })

    cats, filas, cuenta = defaultdict(list), [], defaultdict(int)
    for f in perfil:
        clave = f["termino"].split(":")[-1]
        rs = regs.get(clave, [])
        sit = "falta" if not rs else ("cubierto" if any(x["estado"] in CUBIERTOS for x in rs) else "laguna")
        cuenta[(f["obligatoriedad"], sit)] += 1
        cats[f["categoria"]].append((f, sit))
        if rs:
            for x in rs:
                filas.append((f, sit, x))
        else:
            filas.append((f, sit, {"estado": "no consta", "sobre": "", "texto": "—"}))

    nombre_sit = {"cubierto": "cubierto", "laguna": "laguna declarada", "falta": "no consta"}
    celdas = []
    for cat, items in cats.items():
        cs = "".join(
            f'<span class="cell {sit} {"c" if f["obligatoriedad"] == "C" else "o"}" role="img" '
            f'aria-label="{escape(f["id"])} {escape(f["elemento"])}, {"obligatorio" if f["obligatoriedad"] == "C" else "opcional"}: {nombre_sit[sit]}" '
            f'title="{escape(f["id"])} {escape(f["elemento"])} ({f["obligatoriedad"]}): {nombre_sit[sit]}">{escape(f["id"])}</span>'
            for f, sit in items)
        celdas.append(f'<div class="cat"><span class="name">{escape(cat)}</span><div class="cells">{cs}</div></div>')

    tabla = "".join(
        f'<tr><td class="id">{escape(f["id"])}</td><td>{escape(f["elemento"])} <span class="label">{f["obligatoriedad"]}</span></td>'
        f'<td><span class="state {sit}">{escape(x["estado"].replace("_", " "))}</span></td>'
        f'<td>{escape(x["sobre"])}</td><td>{escape(x["texto"])}</td></tr>'
        for f, sit, x in filas)

    dims = "".join(
        f'<div class="dim"><div class="dim-head"><h3>{d}</h3><span class="risk {r}">riesgo {r}</span></div><p>{escape(t)}</p></div>'
        for d, r, t in DIMENSIONES)
    crit = "".join(
        f'<tr class="crit"><td>{escape(c)}</td><td><span class="eff {e.replace(" ", "-")}">{e}</span></td><td>{escape(t)}</td></tr>'
        for c, e, t in CRITERIOS)
    qs = "".join(f"<li>{escape(q)}</li>" for q in PREGUNTAS)

    cC, lC, fC = cuenta[("C", "cubierto")], cuenta[("C", "laguna")], cuenta[("C", "falta")]
    cO, lO, fO = cuenta[("O", "cubierto")], cuenta[("O", "laguna")], cuenta[("O", "falta")]

    cuerpo = f"""<title>Hibridaciones algorítmicas</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&family=Public+Sans:wght@400;600&display=swap">
<style>{CSS}</style>
<main class="page">
  <section class="record" aria-labelledby="t">
    <figure class="plate">
      <img src="img/5-VAR-1-GPT7_1200px.jpg" width="1200" height="1200" alt="«5 VAR-1 GPT7»: volumen de líneas oscuras de contorno curvo, interrumpido por una franja sin trazos, con una serie de líneas rojas superpuesta y desplazada.">
      <figcaption>«5 VAR-1 GPT7». Fotografía del 7 de octubre de 2026; autoría pendiente de confirmar. CC BY-NC-ND 4.0.</figcaption>
    </figure>
    <div>
      <div class="titles">
        <span class="label">Expediente ODA · demostrador</span>
        <h1 id="t">Hibridaciones algorítmicas</h1>
        <span class="sub">Obra resultante: «5 VAR-1 GPT7»</span>
      </div>
      <dl class="meta">
        <dt>Autor</dt><dd>Juan Alonso López Iniesta</dd>
        <dt>Parte física</dt><dd>Mauro Herrero Cantos</dd>
        <dt>Técnica</dt><dd>Técnica mixta: plotter de pluma e intervención del autor</dd>
        <dt>Soporte</dt><dd>Papel (dimensiones sin documentar)</dd>
        <dt>Referente</dt><dd>Principios operativos de la obra de Nasreen Mohamedi: ritmo, ruptura o silencio, acumulación</dd>
        <dt>Sistema</dt><dd>Perspectiva cónica con dos puntos de fuga (30° y 60°), escrita en código</dd>
        <dt>Exposición</dt><dd>Colegio Oficial de Arquitectos de Madrid (COAM), 2025</dd>
        <dt>Géneros</dt><dd>Generative art / arte generativo; Computer art (taxonomía AEMA)</dd>
        <dt>Identificador</dt><dd>DOI de Zenodo pendiente (identificador de depósito, no identificador ODA)</dd>
      </dl>
      <p class="note">Este expediente lo prepara el grupo IPEX (URJC) como demostrador del método ODA. No es una evaluación de Fund_ODA ni declara que la obra sea un ODA reconocido: registra qué metadatos satisface la obra y propone una valoración revisable.</p>
    </div>
  </section>

  <section aria-labelledby="s-cont">
    <div class="head">
      <span class="label">Esquema del libro · 40 elementos</span>
      <h2 id="s-cont">Qué metadatos satisface la obra</h2>
      <p class="lead totals">Obligatorios: {cC} cubiertos y {lC} declarados como laguna{f", {fC} sin tratar" if fC else ""}. Opcionales: {cO} cubiertos y {fO} que no constan. La validación SHACL no da errores.</p>
    </div>
    <div class="cells-wrap">{''.join(celdas)}</div>
    <div class="legend">
      <span><span class="cell cubierto c"></span>Cubierto</span>
      <span><span class="cell laguna c"></span>Laguna declarada, con su motivo</span>
      <span><span class="cell falta o"></span>No consta</span>
      <span>Borde grueso: obligatorio (C). Borde fino: opcional (O)</span>
    </div>
    <details class="elements">
      <summary>Ver los 40 elementos y sus registros</summary>
      <div class="table-scroll"><table>
        <thead><tr><th>Id</th><th>Elemento</th><th>Estado</th><th>Sobre</th><th>Valor o motivo</th></tr></thead>
        <tbody>{tabla}</tbody>
      </table></div>
    </details>
  </section>

  <section aria-labelledby="s-rel">
    <div class="head">
      <span class="label">13 afirmaciones · 7 de los autores · 3 observables · 3 hipótesis</span>
      <h2 id="s-rel">Relaciones y su estatuto</h2>
      <p class="lead">Cada relación dice quién la sostiene y con qué evidencia. Las discontinuas son hipótesis del equipo que los autores deben confirmar.</p>
    </div>
    <figure class="graph"><img src="img/grafo.svg" alt="Grafo de relaciones: Hibridaciones algorítmicas se basa en la perspectiva cónica, toma como referente a Nasreen Mohamedi y traduce su silencio en la ruptura; «5 VAR-1 GPT7» es su obra resultante, se expuso en el COAM en 2025, Mauro Herrero Cantos se encargó de su parte física, y presenta una franja sin trazos y una capa roja de trazo irregular. Son hipótesis que la capa roja sea la intervención del autor, que la obra se generara con el estado de curva derecha y que el código base no sea su versión."></figure>
  </section>

  <section aria-labelledby="s-diag">
    <div class="head">
      <span class="label">Diagnóstico de preservación</span>
      <h2 id="s-diag">Cuatro dimensiones</h2>
    </div>
    <div class="dims">{dims}</div>
  </section>

  <section aria-labelledby="s-val">
    <div class="head">
      <span class="label">Propuesta del equipo, revisable</span>
      <h2 id="s-val">Condición aurática</h2>
    </div>
    <div class="scale" aria-label="Posición propuesta: intermedia, entre débil y fuerte">
      <div class="bar"><span class="band"></span></div>
      <div class="ends"><span>débil</span><span>fuerte</span></div>
    </div>
    <p class="verdict">Intermedia, con potencial para reforzarse.</p>
    <p>Los criterios que dependen de la obra y de su proceso apuntan hacia el polo fuerte. Los que dependen de su recorrido público no tienen datos todavía. Lo que más la haría avanzar: describir la intervención, identificar la versión del código y documentar la exposición y su recepción.</p>
    <div class="table-scroll"><table>
      <thead><tr><th>Criterio del libro</th><th>Efecto</th><th>Evidencia</th></tr></thead>
      <tbody>{crit}</tbody>
    </table></div>
  </section>

  <section class="two" aria-label="Preguntas y ficheros">
    <div class="head">
      <span class="label">Para los autores</span>
      <h2>Preguntas abiertas</h2>
      <ol class="qs">{qs}</ol>
    </div>
    <div class="head">
      <span class="label">RO-Crate 1.2 · válido</span>
      <h2>Qué contiene el paquete</h2>
      <ul class="files">
        <li><code>expediente-oda.jsonld</code> registros y afirmaciones</li>
        <li><code>ro-crate-metadata.json</code> entidades, ficheros y eventos</li>
        <li><code>diagnostico/diagnostico.md</code> diagnóstico y valoración</li>
        <li><code>edm/edm.xml</code> exportación para Hispana y Europeana</li>
        <li><code>preservacion/manifiesto-sha256.txt</code> sumas de verificación</li>
        <li><code>representaciones/</code> imágenes sin metadatos incrustados</li>
      </ul>
      <p class="lead">La fotografía maestra y el código de la obra se depositan aparte, en acceso restringido.</p>
    </div>
  </section>

  <footer>
    <span>IPEX, Grupo de Investigación en Interfaces y Prototipos Experimentales · Universidad Rey Juan Carlos · 2 de noviembre de 2026</span>
    <span>Repositorio: github.com/IPEX-LAB/oda-demostrador · Método: <i>Objeto Digital Aurático</i> (Peter Lang, 2025). Metadatos CC0 1.0 · textos CC BY 4.0 · imágenes de la obra CC BY-NC-ND 4.0</span>
  </footer>
</main>
"""
    web = RAIZ / "web"
    (web / "img").mkdir(parents=True, exist_ok=True)
    shutil.copy(carpeta / "representaciones" / "5-VAR-1-GPT7_1200px.jpg", web / "img")
    shutil.copy(carpeta / "relaciones" / "grafo.svg", web / "img")
    (web / "ficha.html").write_text(cuerpo, encoding="utf-8")
    (web / "index.html").write_text(
        '<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        + cuerpo.replace("</style>", "</style>\n</head>\n<body>", 1) + "</body>\n</html>\n", encoding="utf-8")
    print("Escritos web/ficha.html y web/index.html.")


if __name__ == "__main__":
    main()
