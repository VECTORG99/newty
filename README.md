# Newty

Newty investiga y expone los mejores proyectos open source del momento desde **GitHub Trending, Reddit y GitLab**. Genera fichas informativas en espanol para compartir con la comunidad y dar visibilidad a proyectos open source emergentes.

Proyecto complementario a [homedir](https://github.com/os-santiago/homedir), la plataforma de comunidad DevRel/OpenSource de OS Santiago.

## Finalidad

- **Dar visibilidad** a proyectos open source con potencial, grandes y pequenos
- **Apoyar a la comunidad** open source redirigiendo trafico y atencion a sus repositorios
- **Alimentar plataformas comunitarias** como homedir con contenido curado automaticamente
- **Mantenerte al dia** con las tecnologias emergentes en GitHub, Reddit y GitLab

## Caracteristicas

- **Multi-fuente** — GitHub Trending, Reddit (posts con links a repos), GitLab Trending
- **Multi-periodo** — Diario, semanal, mensual. Descubre que es tendencia esta semana o este mes
- **Salida dual Markdown + YAML** — Markdown para compartir en Discord/comunidad; YAML compatible con el schema Community Content de homedir
- **HTML con estilo dark mode** — Listo para abrir en el navegador
- **Historial completo** — Cada ejecucion se acumula en `salida/investigaciones.md`
- **Sin dependencias externas** — Solo usa la libreria estandar de Python 3
- **Configurable** — Cantidad, periodo, fuentes, formato

## Instalacion

```bash
git clone https://github.com/VECTORG99/newty.git
cd newty
python3 newty.py --help
```

## Uso

```bash
# Ejecutar con defaults: GitHub Trending, diario, 1 proyecto
python3 newty.py

# Con multiples fuentes y periodo
python3 newty.py -c 5 --periodo semanal --fuentes github reddit

# Periodo mensual, solo Reddit
python3 newty.py --periodo mensual --fuentes reddit -c 10

# Salida YAML para homedir
python3 newty.py -c 5 --fuentes github --formato yaml

# Formato markdown sin HTML
python3 newty.py -c 3 --no-html
```

### Ejemplo de salida

```markdown
**proyecto** (https://github.com/autor/proyecto)

⭐ **1,234** estrellas · por autor

Descripcion traducida al espanol del proyecto.

✨ **Caracteristicas:**
* Funcionalidad destacada del proyecto
* Otra caracteristica relevante
* Tecnologia en tendencia
```

## Estructura del proyecto

```
newty/
├── newty.py                  # Script principal (orquestador multi-fuente)
├── config.json               # Configuracion
├── fuentes/                  # Extractores por fuente
│   ├── reddit.py             # Extractor de Reddit
│   └── gitlab.py             # Extractor de GitLab
├── salida/
│   ├── investigaciones.md    # Historial acumulativo en Markdown
│   ├── newty.html            # Ultima investigacion en HTML
│   └── yaml/                 # YAML para homedir (Community Content schema)
├── .gitignore
└── README.md
```

## Configuracion

Edita `config.json`:

```json
{
  "cantidad": 1,
  "idioma": "",
  "historial": "salida/investigaciones.md",
  "periodo": "diario",
  "fuentes": ["github"],
  "formato": "md",
  "salida_yaml": "salida/yaml/"
}
```

| Opcion        | Descripcion                                  | Default                      |
|---------------|----------------------------------------------|------------------------------|
| `cantidad`    | Numero de proyectos por investigacion        | `1`                          |
| `idioma`      | Filtrar por lenguaje de programacion         | `""` (todos)                 |
| `historial`   | Ruta del archivo de historial                | `salida/investigaciones.md`  |
| `periodo`     | Ventana temporal: diario, semanal, mensual   | `"diario"`                   |
| `fuentes`     | Fuentes: github, reddit, gitlab (o varias)   | `["github"]`                 |
| `formato`     | Formato de salida: md, yaml                  | `"md"`                       |
| `salida_yaml` | Directorio de salida YAML                    | `"salida/yaml/"`             |

## Integracion con homedir

Newty puede generar salida YAML compatible con el schema [Community Content de homedir](https://github.com/os-santiago/homedir). Los archivos `.yml` generados en `salida/yaml/` siguen la misma estructura que usa el curator de homedir (`tools/community-curator/`).

Para usar Newty como alimentador de homedir:

```bash
# Generar fichas YAML para homedir
python3 newty.py -c 5 --fuentes github reddit --periodo semanal --formato yaml

# Los archivos YAML quedan en salida/yaml/
# Copiarlos o desplegarlos al content dir de homedir:
# /work/data/community/content/
```

Cada archivo YAML contiene: `id`, `title`, `url`, `summary`, `source`, `created_at`, `media_type`, `tags`, y opcionalmente `author`.

## Licencia

MIT
