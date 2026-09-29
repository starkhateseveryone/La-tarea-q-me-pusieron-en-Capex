# Auditor de Proyecto

Automatización en Python que analiza una carpeta de código y genera un reporte en Markdown con:

- Líneas de código por tipo de archivo (`.py`, `.js`, `.java`, etc.)
- Lista de comentarios pendientes: `TODO`, `FIXME` y `HACK`, con archivo y número de línea

## Requisitos

- Python 3.8 o superior
- No necesita instalar librerías externas

## Uso

```bash
# Analizar la carpeta actual
python auditor.py

# Analizar otra carpeta
python auditor.py ruta/al/proyecto

# Elegir el nombre del reporte
python auditor.py . -o informe.md
```

## Ejemplo de salida

```markdown
# Reporte del proyecto

## Líneas de código por tipo de archivo
| Extensión | Líneas |
|-----------|--------|
| .py | 120 |

## Pendientes encontrados (1)
- `main.py` (línea 14): # TODO: validar datos de entrada
```

## Personalización

En la parte superior de `auditor.py` puedes editar:

- `EXTENSIONES`: tipos de archivo a analizar
- `CARPETAS_IGNORADAS`: carpetas que se saltan
- `ETIQUETAS`: palabras que se buscan en los comentarios

## Autor

Andy
