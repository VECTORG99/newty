"""Fuente GitLab — extrae proyectos trending via API REST."""

import json
import re
import sys
import urllib.request
import urllib.error


def scrapear_gitlab_trending(cantidad=10):
    """Extrae proyectos trending de GitLab via API REST.

    GitLab bloquea el scraping HTML (302 redirect a login).
    Usa la API publica: /api/v4/projects con order_by=last_activity_at.

    Returns:
        Lista de dicts con keys: nombre, autor, repo_url, descripcion, stars, fuente
    """
    url = f"https://gitlab.com/api/v4/projects?order_by=last_activity_at&sort=desc&per_page=100"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json",
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"  Error al obtener GitLab API: {e}", file=sys.stderr)
        return []

    proyectos = []
    for item in data:
        if not isinstance(item, dict):
            continue

        nombre = item.get("name", "?")
        web_url = item.get("web_url", "")
        if not web_url:
            continue

        # extraer autor del namespace o path_with_namespace
        path = item.get("path_with_namespace", "")
        autor = "?"
        if "/" in path:
            autor = path.split("/")[0]
        else:
            ns = item.get("namespace", {})
            autor = ns.get("path", ns.get("name", "?"))

        desc = (item.get("description") or "").strip()
        desc = desc or f"Proyecto {nombre} en GitLab"

        stars = str(item.get("star_count", 0))

        proyectos.append({
            "nombre": nombre,
            "autor": autor,
            "repo_url": web_url,
            "descripcion": desc[:300],
            "stars": stars,
            "fuente": "GitLab Trending",
        })

    # ponytail: API no soporta order_by=stars, ordenar client-side
    proyectos.sort(key=lambda p: int(p.get("stars", 0)), reverse=True)
    return proyectos[:cantidad]


if __name__ == "__main__":
    # Self-test
    resultados = scrapear_gitlab_trending(cantidad=3)
    print(f"Encontrados {len(resultados)} proyectos de GitLab:")
    for p in resultados:
        print(f"  {p['nombre']} ({p['stars']}*) — {p['repo_url']}")
        print(f"    {p['descripcion'][:80]}")
