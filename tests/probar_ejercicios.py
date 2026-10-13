#!/usr/bin/env python3
"""
Pruebas de «Operación Jupyter»: ejecuta los ejercicios de ingeniería de los tres
lenguajes tal como están publicados y comprueba que den los mismos resultados.

Qué verifica:
  1. Que cada bloque de código corra sin error (incluidos sus assert / stopifnot / @assert).
  2. Que, para cada ejercicio, Python, R y Julia impriman los mismos números y valores
     lógicos (se comparan los valores, no el texto: R imprime 45 y Python 45.0).
  3. Que la «Salida» escrita a mano en la página de Julia coincida con lo que Julia imprime.

Uso:
  python tests/probar_ejercicios.py                  # usa los lenguajes instalados
  python tests/probar_ejercicios.py --exigir-todos   # falla si falta alguno (modo CI)
"""
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LENGUAJES = {
    "python": {
        "archivo": "python/07-ejercicios-ingenieria.qmd",
        "fence": re.compile(r"^```\{pyodide-python\}\s*$"),
        "ext": ".py",
        "cmd": lambda f: [sys.executable, f],
        "exe": sys.executable,
    },
    "r": {
        "archivo": "r/07-ejercicios-ingenieria.qmd",
        "fence": re.compile(r"^```\{webr-r\}\s*$"),
        "ext": ".R",
        "cmd": lambda f: ["Rscript", "--vanilla", f],
        "exe": shutil.which("Rscript"),
    },
    "julia": {
        "archivo": "julia/07-ejercicios-ingenieria.qmd",
        "fence": re.compile(r"^```julia\s*$"),
        "ext": ".jl",
        "cmd": lambda f: ["julia", "--startup-file=no", f],
        "exe": shutil.which("julia"),
    },
}

RE_TITULO = re.compile(r"^##\s+(\d+)\.")
RE_SALIDA = re.compile(r"\*\*Salida:\*\*\s*`([^`]*)`")
RE_TOKEN = re.compile(r"-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?|\btrue\b|\bfalse\b", re.IGNORECASE)


def extraer(lenguaje):
    """Devuelve {n.º de ejercicio: (código, salida documentada o None)}."""
    cfg = LENGUAJES[lenguaje]
    ruta = os.path.join(RAIZ, cfg["archivo"])
    ejercicios, actual, dentro, buffer = {}, None, False, []
    ultimo = None
    with open(ruta, encoding="utf-8") as f:
        for linea in f:
            linea = linea.rstrip("\n")
            if not dentro:
                m = RE_TITULO.match(linea)
                if m:
                    actual = int(m.group(1))
                elif cfg["fence"].match(linea) and actual is not None:
                    dentro, buffer = True, []
                else:
                    s = RE_SALIDA.search(linea)
                    if s and ultimo is not None:
                        ejercicios[ultimo] = (ejercicios[ultimo][0], s.group(1))
            elif linea.strip() == "```":
                dentro = False
                ejercicios[actual] = ("\n".join(buffer) + "\n", None)
                ultimo = actual
            else:
                buffer.append(linea)
    return ejercicios


def ejecutar(lenguaje, codigo):
    cfg = LENGUAJES[lenguaje]
    with tempfile.TemporaryDirectory() as tmp:
        ruta = os.path.join(tmp, "ejercicio" + cfg["ext"])
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(codigo)
        env = dict(os.environ, PYTHONIOENCODING="utf-8", LC_ALL="C.UTF-8")
        p = subprocess.run(cfg["cmd"](ruta), capture_output=True, text=True,
                           encoding="utf-8", timeout=300, env=env)
    return p.returncode, p.stdout, p.stderr


def tokens(texto):
    """Números (como float) y valores lógicos (como 'true'/'false') de un texto."""
    salida = []
    for t in RE_TOKEN.findall(texto):
        tl = t.lower()
        salida.append(tl if tl in ("true", "false") else float(t))
    return salida


def iguales(a, b, tol=1e-9):
    if len(a) != len(b):
        return False
    for x, y in zip(a, b):
        if isinstance(x, str) or isinstance(y, str):
            if x != y:
                return False
        elif not math.isclose(x, y, rel_tol=tol, abs_tol=tol):
            return False
    return True


def main():
    exigir = "--exigir-todos" in sys.argv
    disponibles, errores = [], []

    for l, cfg in LENGUAJES.items():
        if cfg["exe"]:
            disponibles.append(l)
        else:
            msg = f"No está instalado el intérprete de {l}."
            if exigir:
                errores.append(msg)
            else:
                print(f"AVISO: {msg} Se omite.")

    resultados = {}   # (lenguaje, n) -> tokens
    documentadas = {} # n -> salida documentada de Julia
    for l in disponibles:
        for n, (codigo, doc) in sorted(extraer(l).items()):
            rc, out, err = ejecutar(l, codigo)
            etiqueta = f"{l} · ejercicio {n}"
            if rc != 0:
                errores.append(f"{etiqueta}: terminó con error.\n{(err or out).strip()}")
                continue
            resultados[(l, n)] = tokens(out)
            print(f"OK   {etiqueta}: {out.strip()}")
            if l == "julia" and doc is not None:
                documentadas[n] = doc

    # Comparación entre lenguajes
    numeros = sorted({n for (_, n) in resultados})
    for n in numeros:
        presentes = {l: resultados[(l, n)] for l in disponibles if (l, n) in resultados}
        if exigir:
            for l in disponibles:
                if (l, n) not in resultados and not any("{} · ejercicio {}".format(l, n) in e for e in errores):
                    errores.append(f"{l}: falta el ejercicio {n} (otros lenguajes sí lo tienen).")
        ref_l = next(iter(presentes))
        for l, tk in presentes.items():
            if not iguales(presentes[ref_l], tk):
                errores.append(
                    f"Ejercicio {n}: {ref_l} da {presentes[ref_l]} pero {l} da {tk}.")

    # Salida documentada de Julia contra la real. Si Julia no está instalada, se usa
    # como referencia el primer lenguaje disponible (los tres deben coincidir).
    referencia = "julia" if "julia" in disponibles else (disponibles[0] if disponibles else None)
    if referencia:
        doc_julia = {n: d for n, (_, d) in extraer("julia").items() if d is not None}
        for n, doc in sorted(doc_julia.items()):
            real = resultados.get((referencia, n))
            if real is not None and not iguales(tokens(doc), real):
                errores.append(
                    f"Julia · ejercicio {n}: la «Salida» escrita en la página dice «{doc}», "
                    f"pero {referencia} produce {real}.")

    print()
    if errores:
        print(f"FALLARON {len(errores)} comprobaciones:\n")
        for e in errores:
            print(" -", e)
        sys.exit(1)
    print(f"Todo coincide ({', '.join(disponibles)}).")


if __name__ == "__main__":
    main()
