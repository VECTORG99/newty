# Newty

Newty extrae proyectos open source trending desde **GitHub Trending** y los expone en múltiples formatos: Markdown, YAML, HTML. Es a la vez una herramienta standalone y un **modelo conceptual** para construir páginas web, bots y otros proyectos que necesiten contenido curado automáticamente.

## Alcance

| Artefacto | Repo | Uso |
|---|---|---|
| **newty.py** | este repo | CLI standalone — sin dependencias, stdlib Python 3 |
| **Newty_Pages** | [VECTORG99/Newty_Pages](https://github.com/VECTORG99/Newty_Pages) | Esqueleto para páginas Quarkus + Qute + i18n |
| **ABSTRACTION.md** | este repo | Modelo 3-capas: Extractor → Transformador → Renderizador |

### Modelo conceptual (3 capas)

```
Extractor (scraper) → Transformador (translate/sort) → Renderizador (format)
     fetch()                  map()                       md / yaml / html / qute
```

- **Extractor**: obtiene datos de una fuente pública (GitHub Trending, API, RSS). Nunca retorna null, nunca lanza.
- **Transformador**: traduce EN→ES, ordena por métrica, normaliza texto.
- **Renderizador**: emite Markdown, YAML (homedir schema), HTML, Qute template, o JSON.

### Extensiones posibles

- **Páginas web**: usar `Newty_Pages` como esqueleto para integrar en homedir u otra app Quarkus
- **Bots**: mismo extractor, renderizar a JSON → webhook Discord/Slack/Telegram
- **Proyectos standalone**: este script CLI, sin dependencias

## Finalidad

- **Dar visibilidad** a proyectos open source emergentes
- **Alimentar plataformas comunitarias** como [homedir](https://github.com/os-santiago/homedir) con contenido curado automáticamente
- **Servir como modelo** reutilizable para scraping + traducción + renderizado

## Características

- **Multi-periodo** — Diario, semanal, mensual
- **Salida dual Markdown + YAML** — Markdown para compartir; YAML compatible con schema Community Content de homedir
- **HTML con estilo dark mode**
- **Historial completo** — Cada ejecución se acumula en `salida/investigaciones.md`
- **Sin dependencias externas** — Solo stdlib de Python 3
- **Configurable** — Cantidad, periodo, formato vía CLI o `config.json`

## Instalación

```bash
git clone https://github.com/VECTORG99/newty.git
cd newty
python3 newty.py --help
```

## Uso

```bash
# Diario, 1 proyecto (default)
python3 newty.py

# Semanal, 5 proyectos
python3 newty.py -c 5 --periodo semanal

# Mensual, 10 proyectos
python3 newty.py --periodo mensual -c 10

# Salida YAML para homedir
python3 newty.py -c 5 --formato yaml

# Solo markdown, sin HTML
python3 newty.py -c 3 --no-html
```

### Ejemplo de salida

```markdown
**proyecto** (https://github.com/autor/proyecto)

⭐ **1,234** estrellas · por autor

Descripción traducida al español del proyecto.

✨ **Características:**
* Funcionalidad destacada del proyecto
* Tecnología en tendencia
```

## Estructura

```
newty/
├── newty.py                  # Script principal
├── config.json               # Configuración
├── ABSTRACTION.md            # Modelo conceptual para extensiones
├── salida/
│   ├── investigaciones.md    # Historial acumulativo
│   ├── newty.html            # Último reporte en HTML
│   └── yaml/                 # YAML para homedir (Community Content schema)
└── README.md
```

## Configuración

Edita `config.json`:

| Opción | Descripción | Default |
|---|---|---|
| `cantidad` | Número de proyectos | `1` |
| `idioma` | Filtrar por lenguaje | `""` (todos) |
| `historial` | Ruta del archivo de historial | `salida/investigaciones.md` |
| `periodo` | diario, semanal, mensual | `"diario"` |
| `formato` | md, yaml | `"md"` |
| `salida_yaml` | Directorio de salida YAML | `"salida/yaml/"` |

## Integración con homedir

Los archivos YAML generados en `salida/yaml/` siguen el schema [Community Content de homedir](https://github.com/os-santiago/homedir):

```bash
python3 newty.py -c 5 --periodo semanal --formato yaml
# Archivos .yml en salida/yaml/ listos para desplegar en homedir
```

## Licencia

MIT
