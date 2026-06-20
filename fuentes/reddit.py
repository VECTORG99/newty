"""Fuente Reddit — extrae proyectos con links a GitHub/GitLab.

NOTA: La API publica de Reddit bloquea solicitudes sin autenticacion
desde algunos entornos. Si todos los subreddits fallan con 403,
considera usar una VPN o configurar OAuth2.
"""

import json
import re
import sys
import urllib.request
import urllib.error

REDDIT_PERIOD_MAP = {
    "diario": "day",
    "semanal": "week",
    "mensual": "month",
}

DEFAULT_SUBREDDITS = [
    "opensource",
    "programming",
    "github",
    "selfhosted",
    "coolgithubprojects",
]


def _extraer_urls_repo(texto):
    """Extrae URLs de GitHub/GitLab de un texto."""
    urls = set()
    for match in re.finditer(
        r"https?://(?:www\.)?(github|gitlab)\.com/([a-zA-Z0-9._-]+)/([a-zA-Z0-9._-]+)",
        texto or "",
    ):
        platform = match.group(1)
        owner = match.group(2)
        repo = match.group(3)
        url = f"https://{platform}.com/{owner}/{repo}"
        urls.add((url, owner, repo, platform))
    return urls


def scrapear_reddit(periodo="diario", cantidad=10, subreddits=None):
    """Extrae proyectos mencionados en Reddit con links a GitHub/GitLab.

    Args:
        periodo: "diario", "semanal", "mensual"
        cantidad: max proyectos a devolver
        subreddits: lista de subreddits (default: opensource, programming, etc.)

    Returns:
        Lista de dicts con keys: nombre, autor, repo_url, descripcion, stars, fuente
    """
    if subreddits is None:
        subreddits = DEFAULT_SUBREDDITS

    reddit_period = REDDIT_PERIOD_MAP.get(periodo, "day")
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json",
    }

    proyectos = []
    urls_vistas = set()

    for sub in subreddits:
        url = f"https://www.reddit.com/r/{sub}/top.json?t={reddit_period}&limit=25"
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            print(f"  ⚠ Reddit r/{sub}: {e}", file=sys.stderr)
            continue

        posts = data.get("data", {}).get("children", [])
        for child in posts:
            post = child.get("data", {})
            title = post.get("title", "")
            selftext = post.get("selftext", "")
            texto_completo = f"{title}\n{selftext}"

            urls_encontradas = _extraer_urls_repo(texto_completo)
            for url_repo, owner, repo, platform in urls_encontradas:
                if url_repo in urls_vistas:
                    continue
                urls_vistas.add(url_repo)

                # si el titulo es descriptivo, usarlo; sino usar selftext
                desc = title.strip() or selftext.strip()[:200]
                # limpiar el titulo para que no sea solo un link
                desc = re.sub(r"https?://\S+", "", desc).strip()
                desc = desc or f"Proyecto {repo} mencionado en r/{sub}"

                proyectos.append({
                    "nombre": repo,
                    "autor": owner,
                    "repo_url": url_repo,
                    "descripcion": desc[:300],
                    "stars": "?",
                    "fuente": f"Reddit r/{sub}",
                })

                if len(proyectos) >= cantidad:
                    break

            if len(proyectos) >= cantidad:
                break

        if len(proyectos) >= cantidad:
            break

    return proyectos[:cantidad]


if __name__ == "__main__":
    # Self-test
    resultados = scrapear_reddit(periodo="semanal", cantidad=3)
    print(f"Encontrados {len(resultados)} proyectos de Reddit:")
    for p in resultados:
        print(f"  {p['nombre']} — {p['repo_url']} — {p['fuente']}")
        print(f"    {p['descripcion'][:80]}")
