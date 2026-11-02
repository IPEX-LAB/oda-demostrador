#!/usr/bin/env bash
# Regenera todo el expediente en el orden correcto.
# Uso: bash scripts/construir_todo.sh [carpeta-de-ficheros-restringidos]
set -euo pipefail
cd "$(dirname "$0")/.."
EXP=expedientes/hibridaciones-algoritmicas
RESTR="${1:-../restringido-hibridaciones}"
python3 scripts/generar_shapes.py
python3 scripts/validar.py "$EXP"
python3 scripts/exportar_edm.py "$EXP"
python3 scripts/grafo.py "$EXP"
python3 scripts/ficha.py "$EXP"
python3 scripts/construir_crate.py "$EXP" "$RESTR"
python3 scripts/checksums.py "$EXP" "$RESTR"
# segunda pasada: el crate recoge el tamaño del manifiesto y el manifiesto la suma del crate
python3 scripts/construir_crate.py "$EXP" "$RESTR"
python3 scripts/checksums.py "$EXP" "$RESTR"
rocrate-validator validate --offline -p ro-crate-1.2 -l required --no-paging -f text "$EXP"
