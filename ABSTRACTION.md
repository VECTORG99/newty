# Newty — Abstracción base

Newty es un extractor de datos de fuentes públicas (GitHub Trending, APIs, RSS) que produce reportes en múltiples formatos. Este documento define el modelo de pensamiento para extenderlo a páginas, bots y otros proyectos.

## Modelo conceptual

```
┌─────────────┐    ┌──────────────┐    ┌──────────────┐
│  Extractor   │ →  │  Transformador │ →  │  Renderizador │
│  (scraper)   │    │  (translate)   │    │  (format)      │
└─────────────┘    └──────────────┘    └──────────────┘
     fetch()           map()              md/yaml/html
```

### 1. Extractor (scraper)
- Fuente: GitHub Trending, API REST, RSS feed, archivo YAML
- Salida: `List<Item>` donde Item es un record con title, url, description, metadata
- Contrato: nunca retorna null, nunca lanza excepción (lista vacía en fallo)
- Scheduling: `@Scheduled(cron="...")` para refresh periódico con caché en memoria

### 2. Transformador (translate)
- EN→ES: diccionario de reemplazo simple (sin dependencias NLP)
- Markup→texto: strip HTML tags, normalizar whitespace
- Sort: ordenar por métrica (estrellas, fecha, relevancia)

### 3. Renderizador (format)
| Formato | Uso |
|---|---|
| Markdown | Reportes, historial, GitHub README |
| YAML | Community Content schema (homedir) |
| HTML | Páginas web, embeds |
| Qute template | Páginas dentro de homedir (Newty_Pages) |
| JSON | API, bots, webhooks |

## Extensiones

### → Páginas (Newty_Pages)
Ver repositorio [`Newty_Pages`](https://github.com/VECTORG99/Newty_Pages):
- ScraperService.java → adaptar Item y parse()
- PageResource.java → endpoint REST + computed UI state
- page.html → template Qute con period toggle + show more/less
- i18n → EN canónico, ES espejo, cero strings hardcodeados

### → Bots (Newty_Bot — futuro)
- Mismo extractor, renderizador → JSON
- Webhook a Discord/Slack/Telegram
- `@Scheduled` para posts automáticos (diario/semanal/mensual)

### → Proyectos standalone (newty.py actual)
- Script CLI: `python newty.py --period weekly --format md`
- Sin dependencias externas (stdlib only)
- Salida: archivos MD + YAML + HTML

## Reglas
1. Cero strings hardcodeados en UI (todo i18n o configuración)
2. Extractor nunca rompe (empty list on failure)
3. Caché en memoria, refresh programado
4. Ordenamiento server-side, template solo renderiza
5. UI state (nextCount, isMax) computado server-side
