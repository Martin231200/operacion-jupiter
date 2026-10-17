#!/usr/bin/env python3
"""
Pruebas de los temas 01 a 06 de «Operación Jupyter».

Qué verifica:
  1. Que los ejercicios de cada tema (los que están bajo un título «### n. …») corran
     sin error en su lenguaje, incluidos sus assert / stopifnot / @assert. Los ejercicios de
     una misma página se ejecutan en orden y acumulados, porque algunos dependen de
     un import o una definición anterior.
  2. Que los ejercicios que aparecen con el mismo título en dos o tres lenguajes impriman los
     mismos números y valores lógicos. Los títulos se emparejan sin tildes, sin las
     etiquetas de dificultad y sin los paréntesis. Esta comparación solo avisa, no falla,
     a menos que se use --comparar-estricto.

Uso:
  python tests/probar_temas.py                      # usa los lenguajes instalados
  python tests/probar_temas.py --exigir-todos       # falla si falta algún lenguaje (modo CI)
  python tests/probar_temas.py --comparar-estricto  # las diferencias entre lenguajes también fallan
"""
import glob
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGINAS = ["01", "02", "03", "04", "05", "06"]

LENGUAJES = {
    "python": {"ext": ".py", "cmd": lambda f: [sys.executable, f], "exe": sys.executable,
               "marca": lambda k: f'print("@@EJ@@ {k}")'},
    "r": {"ext": ".R", "cmd": lambda f: ["Rscript", "--vanilla", f], "exe": shutil.which("Rscript"),
          "marca": lambda k: f'cat("@@EJ@@ {k}\\n")'},
    "julia": {"ext": ".jl", "cmd": lambda f: ["julia", "--startup-file=no", f], "exe": shutil.which("julia"),
              "marca": lambda k: f'println("@@EJ@@ {k}")'},
}

RE_ENCAB = re.compile(r"^###\s+(\d+)\.\s+(.*)$")
RE_ASERCION = re.compile(r"\bassert\b|stopifnot|@assert")
RE_TOKEN = re.compile(r"-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?|\btrue\b|\bfalse\b", re.IGNORECASE)


def clave(titulo):
    t = re.sub(r"<span[^>]*>.*?</span>", " ", titulo)
    t = re.sub(r"\([^)]*\)", " ", t)
    t = unicodedata.normalize("NFD", t.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return " ".join(re.sub(r"[^a-z0-9]+", " ", t).split())


def archivos(lenguaje):
    out = {}
    for n in PAGINAS:
        for f in glob.glob(os.path.join(RAIZ, lenguaje, n + "-*.ipynb")) + \
                 glob.glob(os.path.join(RAIZ, lenguaje, n + "-*.qmd")):
            out[n] = f
    return out


RE_IMPORT = {
    "python": re.compile(r"^(import \S+.*|from \S+ import .*)$"),
    "r": re.compile(r"^library\(.*\)$"),
    "julia": re.compile(r"^using \S+$"),
}


def imports_de(lenguaje, fuentes):
    """Líneas de importación que aparecen en cualquier bloque de código de la página
    (los ejercicios suelen apoyarse en un import hecho antes, en otra celda)."""
    vistos = []
    for src in fuentes:
        for linea in src.split("\n"):
            linea = re.sub(r"\s+#.*$", "", linea.strip())
            if RE_IMPORT[lenguaje].match(linea) and linea != "using Pkg" and linea not in vistos:
                vistos.append(linea)
    return vistos


def ejercicios_ipynb(ruta):
    nb = json.load(open(ruta, encoding="utf-8"))
    res, actual = [], None
    for c in nb["cells"]:
        src = "".join(c["source"])
        if c["cell_type"] == "markdown":
            primera = src.split("\n")[0]
            m = RE_ENCAB.match(primera)
            actual = m if m else (None if primera.startswith("#") else actual)
        elif c["cell_type"] == "code" and actual is not None:
            if RE_ASERCION.search(src):
                res.append((actual.group(1), actual.group(2), src))
            actual = None          # solo la primera celda de código tras el título
    return res


def ejercicios_qmd(ruta):
    res, actual, dentro, buf = [], None, False, []
    for linea in open(ruta, encoding="utf-8").read().split("\n"):
        if not dentro:
            m = RE_ENCAB.match(linea)
            if m:
                actual = m
            elif linea.startswith("#"):
                actual = None
            elif actual is not None and re.match(r"^```julia\s*$", linea):
                dentro, buf = True, []
        elif linea.strip() == "```":
            dentro = False
            src = "\n".join(buf)
            if RE_ASERCION.search(src):
                res.append((actual.group(1), actual.group(2), src))
            actual = None
        else:
            buf.append(linea)
    return res


def bloques_qmd(ruta):
    out, dentro, buf = [], False, []
    for linea in open(ruta, encoding="utf-8").read().split("\n"):
        if not dentro and re.match(r"^```julia\s*$", linea):
            dentro, buf = True, []
        elif dentro and linea.strip() == "```":
            dentro = False
            out.append("\n".join(buf))
        elif dentro:
            buf.append(linea)
    return out


def extraer(lenguaje):
    """{página: ([(n.º, título, código), ...], [líneas de import])}"""
    out = {}
    for pag, f in sorted(archivos(lenguaje).items()):
        if f.endswith(".ipynb"):
            eje = ejercicios_ipynb(f)
            nb = json.load(open(f, encoding="utf-8"))
            fuentes = ["".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code"]
        else:
            eje = ejercicios_qmd(f)
            fuentes = bloques_qmd(f)
        if eje:
            out[pag] = (eje, imports_de(lenguaje, fuentes))
    return out


def ejecutar(lenguaje, codigo):
    cfg = LENGUAJES[lenguaje]
    with tempfile.TemporaryDirectory() as tmp:
        ruta = os.path.join(tmp, "tema" + cfg["ext"])
        open(ruta, "w", encoding="utf-8").write(codigo)
        env = dict(os.environ, PYTHONIOENCODING="utf-8", LC_ALL="C.UTF-8", MPLBACKEND="Agg")
        p = subprocess.run(cfg["cmd"](ruta), capture_output=True, text=True,
                           encoding="utf-8", timeout=300, env=env)
    return p.returncode, p.stdout, p.stderr


def tokens(texto):
    texto = re.sub(r"\[\d+\]", " ", texto)      # índices que imprime R: [1]
    return [t.lower() if t.lower() in ("true", "false") else float(t) for t in RE_TOKEN.findall(texto)]


def iguales(a, b, tol=1e-9):
    if len(a) != len(b):
        return False
    return all((x == y) if isinstance(x, str) or isinstance(y, str)
               else math.isclose(x, y, rel_tol=tol, abs_tol=tol) for x, y in zip(a, b))


def main():
    exigir = "--exigir-todos" in sys.argv
    estricto = "--comparar-estricto" in sys.argv
    disponibles, errores, avisos = [], [], []
    for l, cfg in LENGUAJES.items():
        if cfg["exe"]:
            disponibles.append(l)
        elif exigir:
            errores.append(f"No está instalado el intérprete de {l}.")
        else:
            print(f"AVISO: no está instalado el intérprete de {l}. Se omite.")

    salidas = {}      # (lenguaje, clave) -> tokens
    total = 0
    for l in disponibles:
        for pag, (eje, imps) in extraer(l).items():
            partes, ids = [], []
            for n, titulo, codigo in eje:
                k = f"{pag}-{n}"
                ids.append((k, titulo))
                partes.append(LENGUAJES[l]["marca"](k) + "\n" + codigo)
            rc, out, err = ejecutar(l, "\n".join(imps + partes) + "\n")
            etiqueta = f"{l} · tema {pag}"
            if rc != 0:
                errores.append(f"{etiqueta}: terminó con error.\n{(err or out).strip()[-600:]}")
                continue
            trozos = re.split(r"@@EJ@@ (\S+)\n", out)
            por_k = {trozos[i]: trozos[i + 1] for i in range(1, len(trozos) - 1, 2)}
            for k, titulo in ids:
                salidas[(l, clave(titulo))] = tokens(por_k.get(k, ""))
            total += len(eje)
            print(f"OK   {etiqueta}: {len(eje)} ejercicios")

    # Comparación entre lenguajes por título de ejercicio
    claves = sorted({k for (_, k) in salidas})
    pares = 0
    for k in claves:
        presentes = {l: salidas[(l, k)] for l in disponibles if (l, k) in salidas}
        if len(presentes) < 2:
            continue
        pares += 1
        ref = next(iter(presentes))
        for l, tk in presentes.items():
            if not iguales(presentes[ref], tk):
                msg = f"«{k}»: {ref} imprime {presentes[ref]} pero {l} imprime {tk}."
                (errores if estricto else avisos).append(msg)

    print(f"\n{total} ejercicios ejecutados; {pares} emparejados entre lenguajes por título.")
    if avisos:
        print(f"\nAVISOS ({len(avisos)}), diferencias entre lenguajes que conviene revisar:")
        for a in avisos:
            print(" -", a)
    print()
    if errores:
        print(f"FALLARON {len(errores)} comprobaciones:\n")
        for e in errores:
            print(" -", e)
        sys.exit(1)
    print(f"Todo bien ({', '.join(disponibles)}).")


if __name__ == "__main__":
    main()
