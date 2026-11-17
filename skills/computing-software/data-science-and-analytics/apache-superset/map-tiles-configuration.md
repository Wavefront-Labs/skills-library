---
id: computing-software.data-science-and-analytics.apache-superset.map-tiles-configuration
name: map-tiles-configuration
category: computing-software
field: data-science-and-analytics
product: apache-superset
tags: [map-tiles, deckgl, mapbox, tile-prefix, connect-src]
level: practitioner
status: docs-checked
description: "Configure map tile sources for Superset deck.gl charts: DECKGL_BASE_MAP, tile:// URLs, MAPBOX_API_KEY, CORS_OPTIONS and Talisman connect-src."
sources:
  - https://github.com/apache/superset/blob/master/docs/admin_docs/configuration/map-tiles.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: choose the base map behind geospatial charts.

Superset uses OSM and Mapbox tiles by default. OSM is free; you still need to set `MAPBOX_API_KEY` to use Mapbox maps.

Set tiles with `DECKGL_BASE_MAP` in `superset_config.py` or `superset_config_docker.py`. Each entry is `[url, label]`.

A custom tile server needs the `tile://` prefix:

```python
DECKGL_BASE_MAP = [
    ['tile://https://your_personal_url/{z}/{x}/{y}.png', 'MyTile']
]
```

OpenStreetMap tile URLs are added without the prefix:

```python
DECKGL_BASE_MAP = [
    ['https://c.tile.openstreetmap.org/{z}/{x}/{y}.png', 'OpenStreetMap']
]
```

The docs also show Yandex Tiles API as a custom provider (a `tile://` URL with `apikey`, `x`, `y`, `z`, layer and projection parameters).

The defaults are two OSM entries (Streets and Topography, `tile.openstreetmap.org` and `tile.osm.ch`) plus Mapbox styles `mapbox://styles/mapbox/...` (streets-v9, dark-v9, light-v9, satellite-streets-v9, satellite-v9, outdoors-v9). You can keep only Mapbox or only OSM by removing the others.

Setting `DECKGL_BASE_MAP` overwrites the defaults.

After defining tiles, register the tile hosts in:
- `CORS_OPTIONS` (with `ENABLE_CORS = True`), under `"origins"`.
- The `connect-src` list of the `content_security_policy` in `TALISMAN_CONFIG` and `TALISMAN_CONFIG_DEV`. The docs' example keeps `'self'`, `https://api.mapbox.com` and `https://events.mapbox.com` there alongside the tile hosts.

## Checked

2026-11-08: read map-tiles.mdx in full. Removed claims not on the page: tile service terms, air-gapped hosting advice, browser console debugging, "leave key empty" advice.
Method: documentation only; no commands were run.
