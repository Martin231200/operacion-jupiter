# Términos nuevos para el glosario (agregar a los 10 existentes)

**REPL** (Read-Eval-Print Loop) — El entorno interactivo donde escribes una
línea de código, se ejecuta al momento, y ves el resultado inmediatamente.
Python, R y Julia tienen su propio REPL.

**IDE** (Integrated Development Environment / Entorno de Desarrollo
Integrado) — Un programa que junta editor de código, ejecución y depuración
en un solo lugar (ejemplos: RStudio para R, VS Code para cualquiera de los
tres lenguajes).

**Paquete / biblioteca** — Conjunto de código reutilizable, escrito por
alguien más, que instalas y luego importas en tu programa (`pip install` en
Python, `install.packages()` en R, `]add` en Julia) para no reinventar
funcionalidad ya existente.

**Broadcasting** — Aplicar una operación elemento por elemento sobre un
arreglo completo, sin escribir un ciclo explícito. En Python (NumPy) ocurre
automáticamente al operar arreglos; en Julia requiere el operador `.`
explícito (`x .+ 1`) — **no es automático por diseño**, hay que pedirlo.

**Aserción (assert)** — Una instrucción que verifica que una condición es
verdadera y detiene el programa con un error si no lo es. Se usa para
confirmar supuestos durante el desarrollo o las pruebas (`assert` en Python,
`stopifnot()` en R, `@assert` en Julia).

---

### Corrección a un término existente

Si el glosario actual dice que la vectorización es automática "por diseño"
en Julia, es impreciso: Julia sí está optimizada para operaciones
vectorizadas, pero el broadcasting **requiere el operador `.` explícito**
(ver arriba) — no ocurre solo.
