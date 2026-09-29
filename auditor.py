"""Auditor de proyecto.

Recorre una carpeta de código, cuenta las líneas por tipo de archivo
y lista los comentarios pendientes (TODO, FIXME, HACK).
Genera un reporte en formato Markdown.

Uso:
    python auditor.py                  # analiza la carpeta actual
    python auditor.py ruta/proyecto    # analiza otra carpeta
    python auditor.py . -o informe.md  # cambia el nombre del reporte
"""

import argparse
from collections import Counter
from datetime import datetime
from pathlib import Path

EXTENSIONES = {".py", ".js", ".ts", ".java", ".c", ".cpp", ".html", ".css"}
CARPETAS_IGNORADAS = {".git", "node_modules", "__pycache__", "venv", ".venv"}
ETIQUETAS = ("TODO", "FIXME", "HACK")


def buscar_archivos(raiz: Path):
    """Devuelve los archivos de código de la carpeta, ignorando carpetas comunes."""
    este_script = Path(__file__).resolve()
    for ruta in raiz.rglob("*"):
        if not ruta.is_file() or ruta.suffix not in EXTENSIONES:
            continue
        if CARPETAS_IGNORADAS & set(ruta.relative_to(raiz).parts):
            continue
        if ruta.resolve() == este_script:
            continue
        yield ruta


def analizar(raiz: Path):
    """Cuenta líneas por extensión y recolecta los pendientes."""
    lineas_por_ext = Counter()
    pendientes = []  # (archivo, número de línea, texto)

    for ruta in buscar_archivos(raiz):
        try:
            lineas = ruta.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError as error:
            print(f"No se pudo leer {ruta}: {error}")
            continue

        lineas_por_ext[ruta.suffix] += len(lineas)
        for numero, linea in enumerate(lineas, start=1):
            if any(etiqueta in linea for etiqueta in ETIQUETAS):
                pendientes.append((ruta.relative_to(raiz), numero, linea.strip()))

    return lineas_por_ext, pendientes


def generar_reporte(raiz: Path, lineas_por_ext: Counter, pendientes: list) -> str:
    """Construye el reporte en Markdown."""
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
    salida = [
        "# Reporte del proyecto",
        f"\nCarpeta: `{raiz.resolve()}`  \nFecha: {fecha}\n",
        "## Líneas de código por tipo de archivo\n",
        "| Extensión | Líneas |",
        "|-----------|--------|",
    ]
    for ext, total in lineas_por_ext.most_common():
        salida.append(f"| {ext} | {total} |")
    salida.append(f"| **Total** | **{sum(lineas_por_ext.values())}** |")

    salida.append(f"\n## Pendientes encontrados ({len(pendientes)})\n")
    if pendientes:
        for archivo, numero, texto in pendientes:
            salida.append(f"- `{archivo}` (línea {numero}): {texto}")
    else:
        salida.append("No se encontraron pendientes. ¡Buen trabajo!")

    return "\n".join(salida) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Auditor simple de proyectos.")
    parser.add_argument("ruta", nargs="?", default=".", help="carpeta a analizar")
    parser.add_argument("-o", "--salida", default="reporte.md", help="archivo de reporte")
    args = parser.parse_args()

    raiz = Path(args.ruta)
    if not raiz.is_dir():
        parser.error(f"'{raiz}' no es una carpeta válida")

    lineas_por_ext, pendientes = analizar(raiz)
    reporte = generar_reporte(raiz, lineas_por_ext, pendientes)
    Path(args.salida).write_text(reporte, encoding="utf-8")
    print(f"Reporte generado: {args.salida}")


if __name__ == "__main__":
    main()
