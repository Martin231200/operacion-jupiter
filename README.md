# Operación Jupyter

Sitio del proyecto de servicio social «Operación Jupyter» (Facultad de Ingeniería, UNAM): tutoriales comparados de **Python, R y Julia** para Jupyter, construido con [Quarto](https://quarto.org) y publicado en GitHub Pages.

**Sitio:** https://martin231200.github.io/operacion-jupiter/

## Qué contiene

| Carpeta o archivo | Contenido |
|---|---|
| `python/`, `r/`, `julia/` | Ocho subtemas por lenguaje: introducción, tipos y variables, estructuras de control, estructuras de datos, funciones, particularidades, ejercicios de ingeniería y visualización. En Python los nombres de los subtemas 02, 03, 05 y 06 son distintos. |
| `tutoriales/` | Tutoriales, quiz comparativo y ficha comparativa en PDF. |
| `libros/` | Libros de acceso libre, con portadas y enlaces a páginas oficiales. |
| `semblanza/` | Semblanza de los profesores. |
| `glosario.qmd`, `recursos.qmd`, `comparar.qmd`, `progreso.qmd`, `novedades.qmd` | Páginas del sitio. |
| `_quarto.yml` | Configuración del sitio, navegación y temas. |
| `custom.scss`, `custom-dark.scss` | Tema claro y tema oscuro (paleta guinda de la Facultad). |
| `tests/` | Pruebas automáticas que comparan Python, R y Julia. |
| `.github/workflows/` | Flujos automáticos (ver más abajo). |

R (webR) y Python (Pyodide) se ejecutan en vivo en el navegador. Julia no tiene un equivalente maduro: sus páginas muestran el código y salidas precalculadas, y así se aclara en el sitio.

Colores por lenguaje: Python `#2C5F8A`, R `#1B7A5C`, Julia `#7B4EA3`.

## Verlo en tu computadora

1. Instala [Quarto](https://quarto.org/docs/get-started/).
2. Desde la carpeta del proyecto:
   ```
   quarto preview
   ```
   Se abre una vista previa con recarga automática. Si algo no se actualiza, detén el comando con `Ctrl+C`, borra la caché con `rmdir /s /q .quarto` y vuelve a lanzarlo.

## Cómo hacer cambios (flujo de ramas)

**Nunca se trabaja directo en `main`.** Todo cambio entra por una rama y una solicitud de integración (PR). Estos son los comandos para la terminal CMD de Windows:

```
git checkout main
git pull origin main
git checkout -b nombre-de-la-rama
```
Cambia a `main`, la actualiza y crea una rama nueva para tu cambio.

Haz tus cambios y revisa:
```
quarto preview
git status -sb
```
`git status -sb` debe mostrar solo los archivos que querías tocar.

```
git add ruta/del/archivo1 ruta/del/archivo2
git commit -m "Descripcion corta del cambio"
git push -u origin nombre-de-la-rama
```
Sube la rama. Después, en GitHub: abre el PR, **espera a que los checks estén en verde** y presiona «Merge pull request». Al fusionar, el sitio se publica solo.

### Reglas que conviene recordar

1. **No uses `git add .`**: usa siempre rutas específicas. Puede haber carpetas sueltas que no deben subirse.
2. Los `.ipynb` son JSON: no se editan a mano. Se reemplaza el archivo completo. Los `.qmd` sí se pueden editar con texto.
3. En `_quarto.yml` y en los `.qmd`, las rutas que empiezan con `/` (por ejemplo `/reading-time.js`) las reescribe Quarto según la profundidad de la página. **No les pongas el prefijo `/operacion-jupiter/`.** En cambio, las rutas dentro de strings de JavaScript deben ser relativas.
4. **Nunca hagas `git checkout gh-pages`.** Esa rama la genera el flujo automático.
5. `_site/` no se versiona (está en `.gitignore`).
6. Al descomprimir un paquete de archivos sobre el repo, revisa `git status -sb` antes de `git add`: si aparece algún `D` (borrado) que no esperabas, restáuralo con `git restore ruta`.
7. Después de publicar, el navegador puede mostrar la versión anterior durante unos 10 minutos. Para verificar qué sirve el servidor: `curl.exe -sI <url>` y revisa la línea `Last-Modified`.

## Flujos automáticos

| Flujo | Cuándo corre | Qué hace |
|---|---|---|
| **Publicar sitio Quarto** (`publish.yml`) | En cada push a `main`; en un PR solo verifica | Renderiza el sitio y lo sube a la rama `gh-pages`. En un PR solo hace `quarto render` para detectar errores, sin publicar. |
| **Pruebas de ejercicios** (`pruebas.yml`) | En cada PR y en cada push a `main` que toque los ejercicios | Ejecuta de verdad los ejercicios de ingeniería en Python, R y Julia y comprueba que den los mismos resultados. |
| **Verificar enlaces** (`enlaces.yml`) | Cada lunes y a mano | Revisa los enlaces del sitio publicado con `lychee` y abre un aviso si encuentra alguno roto. No bloquea la publicación. |

Si la publicación (`pages build and deployment`) no se dispara: en GitHub → Settings → Pages, cambia la fuente a otra rama, guarda y vuelve a elegir `gh-pages`.

Para correr las pruebas en tu computadora (se omiten los lenguajes que no tengas instalados):
```
python tests\probar_ejercicios.py
```

## Pendientes

- Datos reales de la semblanza de cada profesor.
- Analítica sin cookies con GoatCounter.
- Pruebas automáticas para las demás páginas de Julia.
- Ampliar «Comparar» con más ejercicios y completar «Mi progreso» (barra por lenguaje y «continuar donde lo dejaste»).

## Licencia

MIT. Ver el archivo `LICENSE`.
