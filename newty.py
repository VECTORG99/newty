#!/usr/bin/env python3
"""Newty — Extractor de proyectos trending de GitHub"""

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SALIDA_DIR = os.path.join(SCRIPT_DIR, "salida")
CONFIG_PATH = os.path.join(SCRIPT_DIR, "config.json")

CONFIG_POR_DEFECTO = {
    "cantidad": 1,
    "idioma": "",
    "historial": os.path.join(SALIDA_DIR, "investigaciones.md"),
    "periodo": "diario",
    "formato": "md",
    "salida_yaml": os.path.join(SALIDA_DIR, "yaml"),
}


def scrapear_github_trending(idioma="", cantidad=10, periodo="diario"):
    """Scrapea GitHub Trending y devuelve lista de proyectos."""
    url = "https://github.com/trending"
    if idioma:
        url += f"/{idioma}"
    # ponytail: daily is default (no param), weekly/monthly add ?since=
    if periodo == "semanal":
        url += "?since=weekly"
    elif periodo == "mensual":
        url += "?since=monthly"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html",
    }

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"  Error al obtener GitHub Trending: {e}", file=sys.stderr)
        return []

    proyectos = []
    bloques = html.split("<article")[1:]

    for bloque in bloques[:cantidad]:
        proyecto = {}

        slug_match = re.search(
            r'<h[23][^>]*>.*?<a[^>]*href="/([^"/]+/[^"/]+?)"[^>]*>',
            bloque, re.DOTALL
        )
        if slug_match:
            slug = slug_match.group(1)
            if "/" in slug and not slug.startswith(("login", "sponsors", "settings", "apps")):
                partes = slug.split("/")
                proyecto["autor"] = partes[0]
                proyecto["nombre"] = partes[1]
                proyecto["repo_url"] = f"https://github.com/{slug}"

        if not proyecto.get("nombre"):
            continue

        desc_match = re.search(
            r'<p[^>]*class="[^"]*color-fg-muted[^"]*"[^>]*>(.*?)</p>',
            bloque, re.DOTALL
        )
        if desc_match:
            desc = re.sub(r'<[^>]+>', '', desc_match.group(1))
            desc = re.sub(r'\s+', ' ', desc).strip()
            if desc:
                proyecto["descripcion"] = desc

        stars = None
        star_matches = re.findall(
            r'octicon-star.*?</svg>\s*([\d,]+)',
            bloque, re.DOTALL
        )
        if star_matches:
            stars = star_matches[-1]

        proyecto["stars"] = stars or "?"

        proyectos.append(proyecto)

    return proyectos


def traducir_descripcion(desc):
    if not desc:
        return "Sin descripción disponible"

    traducciones = {
        " a ": " un ", " an ": " un ", " the ": " el ",
        " for ": " para ", " and ": " y ", " with ": " con ",
        " from ": " desde ", " that ": " que ", " this ": " este ",
        "library": "biblioteca", "framework": "framework",
        "tool": "herramienta", "platform": "plataforma",
        "server": "servidor", "client": "cliente",
        "database": "base de datos", "build": "construir",
        "run": "ejecutar", "fast": "rápido",
        "simple": "simple", "modern": "moderno",
        "lightweight": "ligero", "management": "gestión",
        "development": "desarrollo", "application": "aplicación",
        "support": "soporte", "support for": "soporte para",
        "based": "basado", "using": "usando",
        "written in": "escrito en", "written": "escrito",
        "open-source": "código abierto",
        "open source": "código abierto",
    }

    resultado = desc
    for ing, esp in traducciones.items():
        resultado = resultado.replace(ing, esp)

    if resultado and resultado[0].isalpha() and resultado[0].islower():
        resultado = resultado[0].upper() + resultado[1:]

    return resultado


def generar_ficha(proyecto):
    nombre = proyecto.get("nombre", "?")
    repo_url = proyecto.get("repo_url", "#")
    stars = proyecto.get("stars", "?")
    desc = proyecto.get("descripcion", "")
    desc_es = traducir_descripcion(desc)
    autor = proyecto.get("autor", "?")

    features = [
        "Repositorio de codigo abierto activo",
        f"{stars} estrellas en GitHub",
        f"Tecnologia en tendencia",
    ]

    ficha = f"**{nombre}** ({repo_url})\n\n"
    ficha += f"⭐ **{stars}** estrellas · por {autor}\n\n"
    ficha += f"{desc_es}\n\n"
    ficha += "✨ **Caracteristicas:**\n"
    for f in features:
        ficha += f"* {f}\n"

    return ficha


def _yaml_quote(s):
    """Escapa un string para YAML (comillas dobles)."""
    return json.dumps(s, ensure_ascii=False)


def generar_yaml_item(proyecto, fuente_original="github.com"):
    """Genera un item YAML compatible con el schema Community Content de homedir."""
    nombre = proyecto.get("nombre", "?")
    repo_url = proyecto.get("repo_url", "")
    desc = proyecto.get("descripcion", "")
    desc_es = traducir_descripcion(desc)
    autor = proyecto.get("autor", "?")

    source = "github.com"

    # id: SHA-1 del URL truncado a 12 chars
    item_id = hashlib.sha1(repo_url.encode()).hexdigest()[:12]

    ahora = datetime.now(timezone.utc)
    fecha_iso = ahora.strftime("%Y-%m-%dT%H:%M:%SZ")
    fecha_archivo = ahora.strftime("%Y%m%d")

    lines = [
        f"id: {_yaml_quote(item_id)}",
        f"title: {_yaml_quote(nombre)}",
        f"url: {_yaml_quote(repo_url)}",
        f"summary: >-",
        f"  {desc_es[:320]}",
        f"source: {_yaml_quote(source)}",
        f"created_at: {_yaml_quote(fecha_iso)}",
        f"media_type: article_blog",
        "tags:",
        "  - open-source",
        "  - trending-tech",
    ]
    if autor and autor != "?":
        lines.append(f"author: {_yaml_quote(autor)}")

    yaml_texto = "\n".join(lines) + "\n"
    nombre_archivo = f"{fecha_archivo}-{nombre}-{item_id}.yml"
    return nombre_archivo, yaml_texto


def generar_informe_yaml(proyectos, salida_dir):
    """Genera archivos YAML para cada proyecto en el directorio de salida."""
    os.makedirs(salida_dir, exist_ok=True)
    archivos = []
    for p in proyectos:
        nombre_archivo, contenido = generar_yaml_item(p)
        ruta = os.path.join(salida_dir, nombre_archivo)
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(contenido)
        archivos.append(ruta)
    return archivos


def generar_informe(proyectos, fuentes="GitHub Trending", periodo="diario"):
    ahora = datetime.now()
    fecha = ahora.strftime("%d/%m/%Y %H:%M")

    informe = f"# 📡 Newty - Investigacion {ahora.strftime('%Y-%m-%d')}\n\n"
    informe += f"**Fuente:** {fuentes}  \n"
    informe += f"**Periodo:** {periodo}  \n"
    informe += f"**Generado:** {fecha}  \n"
    informe += f"**Proyectos:** {len(proyectos)}\n\n"
    informe += "---\n\n"

    for p in proyectos:
        informe += generar_ficha(p)

    informe += f"\n*Fin del reporte - {fecha}*\n"
    return informe


def guardar_historial(texto, ruta_historial):
    if not os.path.isabs(ruta_historial):
        ruta_historial = os.path.join(SCRIPT_DIR, ruta_historial)
    os.makedirs(os.path.dirname(ruta_historial), exist_ok=True)

    if os.path.exists(ruta_historial):
        with open(ruta_historial, "r", encoding="utf-8") as f:
            existente = f.read()
        contenido = texto + "\n\n" + existente
    else:
        contenido = (
            "# Newty - Historial de Investigaciones\n\n"
            "Investigaciones automatizadas de proyectos trending en GitHub.\n\n"
            "---\n\n"
        ) + texto

    with open(ruta_historial, "w", encoding="utf-8") as f:
        f.write(contenido)

    return ruta_historial


def generar_html(md_texto):
    html_parts = [
        "<!DOCTYPE html>",
        '<html lang="es">',
        "<head>",
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        "<title>Newty - Investigacion</title>",
        "<style>",
        "body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;"
        "max-width:800px;margin:0 auto;padding:20px;"
        "background:#0d1117;color:#c9d1d9;line-height:1.6}",
        "h1{color:#58a6ff;border-bottom:1px solid #30363d;padding-bottom:10px}",
        "h2{color:#f0f6fc;margin-top:30px}",
        "h3{color:#f0f6fc;margin-top:25px}",
        "a{color:#58a6ff;text-decoration:none}",
        "a:hover{text-decoration:underline}",
        "hr{border:none;border-top:1px solid #30363d;margin:20px 0}",
        ".stars{color:#d29922}",
        "ul{padding-left:20px}",
        "li{margin:5px 0}",
        "footer{margin-top:40px;color:#8b949e;font-size:0.8em;text-align:center}",
        "</style>",
        "</head>",
        "<body>",
    ]

    body = md_texto
    body = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', body)
    # ponytail: auto-link bare URLs, skip ones already inside <a href="...">
    body = re.sub(r'(?<!")(https?://[^\s<>"\)]+)', r'<a href="\1">\1</a>', body)
    body = re.sub(r'^### (.+)$', r'<h3>\1</h3>', body, flags=re.MULTILINE)
    body = re.sub(r'^## (.+)$', r'<h2>\1</h2>', body, flags=re.MULTILINE)
    body = re.sub(r'^# (.+)$', r'<h1>\1</h1>', body, flags=re.MULTILINE)
    body = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', body)
    body = re.sub(r'\* (.+)$', r'<li>\1</li>', body, flags=re.MULTILINE)
    body = re.sub(r'\n{1}', '<br>\n', body)

    html_parts.append(body)
    html_parts.append("</body></html>")
    return "\n".join(html_parts)


def cargar_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return CONFIG_POR_DEFECTO


def main():
    parser = argparse.ArgumentParser(
        description="Newty - Investigacion de proyectos trending"
    )
    parser.add_argument(
        "-c", "--cantidad", type=int, default=None,
        help="Cantidad de proyectos (default: 1)",
    )
    parser.add_argument(
        "--periodo", choices=["diario", "semanal", "mensual"], default=None,
        help="Ventana temporal (default: diario)",
    )
    parser.add_argument(
        "--formato", choices=["md", "yaml"], default=None,
        help="Formato de salida (default: md)",
    )
    parser.add_argument(
        "--no-html", action="store_true",
        help="No generar version HTML",
    )
    args = parser.parse_args()

    config = cargar_config()
    cantidad = args.cantidad or config.get("cantidad", 1)
    periodo = args.periodo or config.get("periodo", "diario")
    formato = args.formato or config.get("formato", "md")

    print(f"🔍 Newty - Investigando GitHub Trending ({periodo})...\n")

    proyectos = scrapear_github_trending(cantidad=cantidad, periodo=periodo)

    if not proyectos:
        print("❌ No se pudieron obtener proyectos. Revisa tu conexion.")
        sys.exit(1)

    print(f"✅ {len(proyectos)} proyectos obtenidos de GitHub Trending\n")

    if formato == "yaml":
        salida_yaml = config.get("salida_yaml", os.path.join(SALIDA_DIR, "yaml"))
        if not os.path.isabs(salida_yaml):
            salida_yaml = os.path.join(SCRIPT_DIR, salida_yaml)
        archivos = generar_informe_yaml(proyectos, salida_yaml)
        print(f"📄 YAML generado: {len(archivos)} archivos en {salida_yaml}")
        for a in archivos:
            print(f"   {os.path.basename(a)}")
        # tambien generar MD para historial
        informe = generar_informe(proyectos, periodo=periodo)
        ruta_historial = config["historial"]
        guardar_historial(informe, ruta_historial)
        print(f"📄 Historial guardado: {ruta_historial}")
    else:
        informe = generar_informe(proyectos, periodo=periodo)
        ruta_historial = config["historial"]
        guardar_historial(informe, ruta_historial)
        print(f"📄 Historial guardado: {ruta_historial}")

        if not args.no_html:
            ruta_html = os.path.join(SALIDA_DIR, "newty.html")
            with open(ruta_html, "w", encoding="utf-8") as f:
                f.write(generar_html(informe))
            print(f"🌐 HTML generado: {ruta_html}")

        print(f"\n{'='*60}")
        print(f"  📡 NEWTY - {len(proyectos)} PROYECTOS ({periodo})")
        print(f"{'='*60}\n")
        print(informe)


if __name__ == "__main__":
    main()
