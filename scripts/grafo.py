#!/usr/bin/env python3
"""Dibuja relaciones/grafo.svg a partir de las afirmaciones del expediente.

El estilo de cada flecha depende del estatuto de la afirmación:
documentada por el autor (línea continua oscura), observable (línea continua azul)
o interpretativa (línea discontinua naranja). La disposición de los nodos es fija.

Uso:
  python3 scripts/grafo.py expedientes/hibridaciones-algoritmicas
"""
import sys
from pathlib import Path
from xml.sax.saxutils import escape

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validar import ODA, cargar_expediente  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent

NODOS = {  # clave: (x centro, y centro, texto, destacado)
    "moh": (140, 80, "Nasreen Mohamedi", False),
    "obra": (420, 80, "Hibridaciones algorítmicas", True),
    "persp": (720, 80, "Perspectiva cónica (2 fugas)", False),
    "rupt": (140, 180, "Ruptura: zona sin planos", False),
    "mauro": (140, 250, "Mauro Herrero Cantos", False),
    "cuad": (720, 200, "Cuaderno de proceso", False),
    "coam": (140, 320, "COAM, 2025", False),
    "obra5": (420, 320, "«5 VAR-1 GPT7»", True),
    "foto": (720, 320, "Fotografía (07-10-2026)", False),
    "franja": (120, 450, "Franja sin trazos", False),
    "roja": (330, 450, "Capa roja de trazo irregular", False),
    "curva": (560, 450, "Estado con curva derecha", False),
    "codigo": (760, 450, "Código base H+V", False),
    "interv": (330, 560, "Intervención del autor", False),
}
# afirmación -> (origen, destino, etiqueta corta)
ARISTAS = {
    "a01": ("obra5", "obra", "obra resultante de"),
    "a02": ("obra", "moh", "referente"),
    "a03": ("obra", "persp", "se basa en"),
    "a04": ("obra", "rupt", "silencio como"),
    "a05": ("obra5", "franja", "presenta"),
    "a06": ("obra5", "roja", "presenta"),
    "a07": ("roja", "interv", "¿corresponde a?"),
    "a08": ("obra5", "curva", "¿generada con?"),
    "a09": ("codigo", "obra5", "no es su versión"),
    "a10": ("obra5", "coam", "expuesta en"),
    "a11": ("foto", "obra5", "representa"),
    "a12": ("cuad", "obra", "documenta"),
    "a13": ("mauro", "obra5", "montaje y soporte"),
}
ESTILO = {
    "documentada_autor": ("#3a3f4b", ""),
    "observable": ("#2f6db5", ""),
    "interpretativa": ("#c26a17", "6 5"),
}
ALTO = 40


def ancho(texto):
    return max(120, int(len(texto) * 7.4) + 28)


def borde(x, y, w, tx, ty):
    """Punto del borde del rectángulo (x, y, w, ALTO) en dirección a (tx, ty)."""
    dx, dy = tx - x, ty - y
    if dx == 0 and dy == 0:
        return x, y
    sx = (w / 2) / abs(dx) if dx else float("inf")
    sy = (ALTO / 2) / abs(dy) if dy else float("inf")
    s = min(sx, sy)
    return x + dx * s, y + dy * s


def main():
    carpeta = (RAIZ / sys.argv[1]).resolve()
    g = cargar_expediente(carpeta)
    estatuto = {}
    for a in g.subjects(ODA.estatuto, None):
        estatuto[str(a).split("#")[-1]] = str(g.value(a, ODA.estatuto)).split("#")[-1]

    W, H = 900, 640
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Helvetica, Arial, sans-serif" font-size="13">',
           "<title>Relaciones del expediente de Hibridaciones algorítmicas</title>",
           '<rect width="100%" height="100%" fill="#ffffff"/>', "<defs>"]
    for k, (color, _) in ESTILO.items():
        out.append(f'<marker id="m-{k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
                   f'<path d="M0 0L10 5L0 10z" fill="{color}"/></marker>')
    out.append("</defs>")

    for aid, (o, d, etq) in ARISTAS.items():
        est = estatuto.get(aid, "interpretativa")
        color, dash = ESTILO[est]
        xo, yo, to, _ = NODOS[o]
        xd, yd, td, _ = NODOS[d]
        x1, y1 = borde(xo, yo, ancho(to), xd, yd)
        x2, y2 = borde(xd, yd, ancho(td), xo, yo)
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="1.4"{dash_attr} marker-end="url(#m-{est})"><title>{aid}</title></line>')
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        lw = len(etq) * 6.4 + 10
        out.append(f'<rect x="{mx - lw / 2:.1f}" y="{my - 9:.1f}" width="{lw:.1f}" height="18" rx="4" fill="#ffffff"/>'
                   f'<text x="{mx:.1f}" y="{my + 4:.1f}" text-anchor="middle" font-size="11.5" fill="{color}">{escape(etq)}</text>')

    for clave, (x, y, texto, dest) in NODOS.items():
        w = ancho(texto)
        relleno, trazo, peso = ("#eef1f6", "#3a3f4b", "600") if dest else ("#ffffff", "#9aa0aa", "400")
        out.append(f'<g><rect x="{x - w / 2:.1f}" y="{y - ALTO / 2}" width="{w}" height="{ALTO}" rx="8" fill="{relleno}" stroke="{trazo}" stroke-width="1.2"/>'
                   f'<text x="{x}" y="{y + 4.5}" text-anchor="middle" font-weight="{peso}" fill="#1d2129">{escape(texto)}</text></g>')

    ly = 612
    for i, (k, nombre) in enumerate([("documentada_autor", "documentada por los autores"), ("observable", "observable"),
                                      ("interpretativa", "interpretativa (hipótesis)")]):
        color, dash = ESTILO[k]
        x0 = 40 + i * 260
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        out.append(f'<line x1="{x0}" y1="{ly}" x2="{x0 + 40}" y2="{ly}" stroke="{color}" stroke-width="1.6"{dash_attr}/>'
                   f'<text x="{x0 + 50}" y="{ly + 4.5}" font-size="12" fill="#1d2129">{nombre}</text>')
    out.append("</svg>")
    destino = carpeta / "relaciones" / "grafo.svg"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"Escrito {destino.relative_to(RAIZ)} con {len(ARISTAS)} relaciones.")


if __name__ == "__main__":
    main()
