#!/usr/bin/env python3
"""Calcula o verifica las sumas SHA-256 de un expediente y de sus ficheros restringidos.

Escribe preservacion/manifiesto-sha256.txt con una línea por fichero
(formato de sha256sum). Los ficheros restringidos aparecen con el prefijo
"restringido/": no están en el paquete abierto, pero su suma sí.

Uso:
  python3 scripts/checksums.py expedientes/hibridaciones-algoritmicas restringido/
  python3 scripts/checksums.py expedientes/hibridaciones-algoritmicas restringido/ --verificar
"""
import hashlib
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
MANIFIESTO = Path("preservacion/manifiesto-sha256.txt")


def sha256(ruta: Path) -> str:
    h = hashlib.sha256()
    with ruta.open("rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def inventario(carpeta: Path, restr: Path):
    for f in sorted(p for p in carpeta.rglob("*") if p.is_file()):
        rel = f.relative_to(carpeta)
        if rel != MANIFIESTO:
            yield rel.as_posix(), f
    for f in sorted(p for p in restr.glob("*") if p.is_file()):
        yield f"restringido/{f.name}", f


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 2:
        sys.exit(__doc__)
    carpeta = (RAIZ / args[0]).resolve()
    restr = Path(args[1]).resolve()
    destino = carpeta / MANIFIESTO

    if "--verificar" in sys.argv:
        esperado = {}
        for linea in destino.read_text(encoding="utf-8").splitlines():
            if linea and not linea.startswith("#"):
                suma, nombre = linea.split("  ", 1)
                esperado[nombre] = suma
        actual = dict((n, sha256(f)) for n, f in inventario(carpeta, restr))
        fallos = [n for n in esperado if actual.get(n) != esperado[n]]
        nuevos = [n for n in actual if n not in esperado]
        for n in fallos:
            print(f"DISTINTO O AUSENTE: {n}")
        for n in nuevos:
            print(f"NO REGISTRADO: {n}")
        print("Integridad correcta." if not fallos and not nuevos else "Revisar las diferencias.")
        sys.exit(1 if fallos or nuevos else 0)

    lineas = ["# SHA-256 del expediente. Generado por scripts/checksums.py",
              "# Las rutas restringido/ se depositan en un registro de acceso restringido."]
    for nombre, f in inventario(carpeta, restr):
        lineas.append(f"{sha256(f)}  {nombre}")
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    print(f"Escrito {destino.relative_to(RAIZ)} con {len(lineas) - 2} ficheros.")


if __name__ == "__main__":
    main()
