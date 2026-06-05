# 📡 Newty

**Newty** es un script automatizado que investiga los proyectos más trending de **GitHub Trending** y genera fichas informativas en español con enlaces directos a los repositorios. Ideal para compartir con amigos y mantenerte al día con las tecnologías emergentes.

## 🚀 Características

- 🔍 **Scraping de GitHub Trending** — Extrae los repositorios más populares del momento
- 🌐 **Salida dual** — Genera automáticamente Markdown (historial acumulativo) y HTML (para compartir)
- 📜 **Historial completo** — Cada ejecución se acumula en `salida/investigaciones.md`, manteniendo las investigaciones anteriores
- 🎨 **HTML con estilo dark mode** — Visualmente atractivo, listo para abrir en el navegador
- 🔌 **Sin dependencias externas** — Funciona solo con la librería estándar de Python 3
- ⚙️ **Configurable** — Define la cantidad de proyectos por investigación

## 📦 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/VECTORG99/newty.git
cd newty

# No requiere instalar dependencias (usa solo la stdlib de Python)
python3 newty.py --help
```

## 🧑‍💻 Uso

```bash
# Ejecutar con 10 proyectos (por defecto)
python3 newty.py

# Especificar cantidad de proyectos
python3 newty.py -c 5

# Modo completo (preparado para futuras fuentes)
python3 newty.py --modo completo

# Omitir generación de HTML
python3 newty.py --no-html
```

### Ejemplo de salida

```markdown
### 1. **headroom**
https://github.com/chopratejas/headroom

⭐ **3,142** estrellas · por chopratejas

Compress tool outputs, logs, files, and RAG chunks before they reach the LLM.

✨ **Características destacadas:**
* Repositorio de código abierto activo
* Tecnología en tendencia en GitHub
* [Ver repositorio](https://github.com/chopratejas/headroom)
```

## 📁 Estructura del proyecto

```
newty/
├── newty.py                  # Script principal
├── config.json               # Configuración
├── fuentes/                  # Extracts por fuente (futuro)
│   ├── github.py
│   └── otras.py
├── salida/
│   ├── investigaciones.md    # Historial acumulativo en Markdown
│   └── newty.html            # Última investigación en HTML
├── .gitignore
└── README.md
```

## ⚙️ Configuración

Edita `config.json`:

```json
{
  "cantidad": 10,
  "idioma": "",
  "historial": "salida/investigaciones.md"
}
```

| Opción      | Descripción                                  | Default                      |
|-------------|----------------------------------------------|------------------------------|
| `cantidad`  | Número de proyectos por investigación        | `10`                         |
| `idioma`    | Filtrar por lenguaje de programación         | `""` (todos)                 |
| `historial` | Ruta del archivo de historial                | `salida/investigaciones.md`  |

## 🗺️ Roadmap

- [ ] **Mejorar la traducción** — Integrar API de traducción (DeepL, Google Translate) para descripciones más naturales
- [ ] **Más fuentes** — Agregar Product Hunt, Hacker News, Reddit, y otros
- [ ] **Publicación automatizada** — Compartir directamente a Telegram, WhatsApp, o Discord
- [ ] **Modo web** — Interfaz web para visualizar el historial
- [ ] **Estadísticas** — Analytics de tecnologías más repetidas en el tiempo

## 🤝 Contribuir

1. Crea un fork del proyecto
2. Crea tu rama (`git checkout -b feature/nueva-funcionalidad`)
3. Haz commit de tus cambios (`git commit -m 'feat: agrega nueva funcionalidad'`)
4. Haz push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

MIT
