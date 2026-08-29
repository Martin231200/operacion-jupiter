# Operación Jupyter

Sitio del proyecto de servicio social "Operación Jupyter" (tutoriales de R, Python y Julia), construido con [Quarto](https://quarto.org).

## Estructura

```
operacion-jupyter/
├── _quarto.yml              # Configuración del sitio y navegación
├── index.qmd                 # Página de inicio
├── python/introduccion-python.ipynb   # Tutorial de Python (notebook)
├── r/introduccion-r.qmd      # Tutorial de R
├── julia/introduccion-julia.qmd  # Tutorial de Julia (pendiente de contenido)
├── libros/index.qmd          # Sección Libros (pendiente, migrar de Google Sites)
├── semblanza/index.qmd       # Semblanza de los profesores (pendiente)
└── .github/workflows/publish.yml  # Publica el sitio automáticamente en cada push a main
```

## Cómo correrlo en local

1. Instala Quarto: https://quarto.org/docs/get-started/
2. Desde esta carpeta:
   ```
   quarto preview
   ```
   Esto abre una vista previa en el navegador con recarga automática.

## Cómo publicarlo

**Manual (primera vez):**
```
quarto publish gh-pages
```
Esto construye el sitio y lo sube a la rama `gh-pages` del repositorio. Después, en GitHub → Settings → Pages, confirma que la fuente sea esa rama.

**Automático (después de la primera publicación):** cada `push` a `main` dispara el workflow en `.github/workflows/publish.yml`, que renderiza y publica el sitio solo, sin repetir el paso manual.

## Pendientes

- [ ] Migrar el contenido de "Libros" desde el sitio de Google Sites
- [ ] Migrar el contenido de "Semblanza de los profesores" desde el sitio de Google Sites
- [ ] Agregar el notebook de R (actualmente el tutorial de R vive como página `.qmd`, no como notebook ejecutable)
- [ ] Agregar contenido de Julia
