# Newty

Newty es un script automatizado que investiga los proyectos mas trending de **GitHub Trending** y genera fichas informativas en espanol con enlaces directos a los repositorios. Ideal para compartir con amigos y mantenerte al dia con las tecnologias emergentes.

## Caracteristicas

- **Scraping de GitHub Trending** — Extrae los repositorios mas populares del momento
- **Salida dual** — Genera Markdown (historial acumulativo) y HTML (para compartir)
- **Historial completo** — Cada ejecucion se acumula en `salida/investigaciones.md`
- **HTML con estilo dark mode** — Listo para abrir en el navegador
- **Sin dependencias externas** — Solo usa la libreria estandar de Python 3
- **Configurable** — Define la cantidad de proyectos por investigacion

## Instalacion

```bash
git clone https://github.com/VECTORG99/newty.git
cd newty
python3 newty.py --help
```

## Uso

```bash
# Ejecutar con 1 proyecto (por defecto)
python3 newty.py

# Especificar cantidad de proyectos
python3 newty.py -c 5

# Modo completo (preparado para futuras fuentes)
python3 newty.py --modo completo

# Omitir generacion de HTML
python3 newty.py --no-html
```

### Ejemplo de salida

```markdown
### 1. **headroom**
https://github.com/chopratejas/headroom

3,142 estrellas · por chopratejas

Compress tool outputs, logs, files, and RAG chunks before they reach the LLM.

Caracteristicas:
* Repositorio de codigo abierto activo
* Tecnologia en tendencia en GitHub
* Ver repositorio
```

## Estructura del proyecto

```
newty/
├── newty.py                  # Script principal
├── config.json               # Configuracion
├── fuentes/                  # Extractores por fuente (futuro)
├── salida/
│   ├── investigaciones.md    # Historial acumulativo en Markdown
│   └── newty.html            # Ultima investigacion en HTML
├── .gitignore
└── README.md
```

## Configuracion

Edita `config.json`:

```json
{
  "cantidad": 1,
  "idioma": "",
  "historial": "salida/investigaciones.md"
}
```

| Opcion      | Descripcion                                  | Default                      |
|-------------|----------------------------------------------|------------------------------|
| `cantidad`  | Numero de proyectos por investigacion        | `1`                          |
| `idioma`    | Filtrar por lenguaje de programacion         | `""` (todos)                 |
| `historial` | Ruta del archivo de historial                | `salida/investigaciones.md`  |

## Licencia

MIT
