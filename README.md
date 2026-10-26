# Guía de usuario — Alquiler de vehículos

Guía paso a paso, con capturas, del módulo `vehicle_rental` (Odoo 19) para el personal de Sunset y Pinveco.

- **Web**: carpeta `docs/` (estática, publicada con GitHub Pages).
- **Capturas**: carpeta `capture/` (Playwright). Genera `docs/img/<tarea>/` y `docs/data/tasks.json`.

Todos los datos de las capturas son **inventados** (base de datos de demostración). No uses nunca una base de datos de producción.

## Regenerar las capturas

Necesitas Python 3 con Playwright (`pip install playwright && playwright install chromium`) y un Odoo de desarrollo con la base de demostración restaurada desde su plantilla limpia (las tareas dependen unas de otras).

```bash
export GUIA_URL=http://localhost:8071   # Odoo de desarrollo
export GUIA_DB=guia_demo                # base de demostración
export GUIA_USER=...                    # usuario de esa base
export GUIA_PASSWORD=...
python3 capture/run.py                  # todas las tareas, en orden
python3 capture/run.py reservar entregar   # solo algunas (por id)
```

Cada tarea es un fichero en `capture/tareas/` con su `TASK` (textos) y `run(g)` (pasos). El orden de ejecución está en `capture/tareas/__init__.py`.

## Textos fijos

Temas, flujos, sinónimos de búsqueda, glosario y errores frecuentes están en `docs/assets/meta.js`.

## Ver la web en local

```bash
cd docs && python3 -m http.server 8765
```
