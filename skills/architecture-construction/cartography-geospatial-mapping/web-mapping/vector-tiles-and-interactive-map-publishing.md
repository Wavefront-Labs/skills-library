---
id: architecture-construction.cartography-geospatial-mapping.web-mapping.vector-tiles-and-interactive-map-publishing
name: vector-tiles-and-interactive-map-publishing
category: architecture-construction
field: cartography-geospatial-mapping
product: web-mapping
tags: [web-mapping, web-gis, interactive-map, slippy-map, vector-tiles, mvt, mbtiles, pmtiles, raster-tiles, xyz-tiles, tippecanoe, maplibre, maplibre-gl-js, leaflet, openlayers, mapbox-style-spec, style-json, geojson, zoom-levels, simplification, feature-dropping, popups, attribution, osm, openstreetmap, tile-server, cdn, cors, web-mercator, epsg-3857, arcgis-online, story-maps]
level: practitioner
status: docs-checked
description: "Publish a fast interactive web map: GeoJSON vs vector tiles, PMTiles with tippecanoe, zoom-dependent MapLibre styling, popups, attribution, and range-request and CORS hosting."
sources: ["https://raw.githubusercontent.com/felt/tippecanoe/main/README.md", "https://docs.protomaps.com/pmtiles/maplibre", "https://docs.protomaps.com/pmtiles/", "https://operations.osmfoundation.org/policies/tiles/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vector tiles and interactive map publishing

**Goal:** an interactive map that loads quickly on a phone, stays legible at every zoom,
and credits its data — by sending the browser only what it needs at each zoom level.

## 1. Choose the delivery format
- **GeoJSON straight to the browser**: fine for small, simple datasets. Large files download and parse slowly.
- **Vector tiles (MVT)**: data cut into z/x/y tiles, simplified per zoom. The default for
  anything large. Styled client-side, so one tileset can serve many map designs.
- **Raster tiles**: for imagery, hillshade, or complex cartography that must look identical
  everywhere.
- Packaging: **PMTiles** (single file, served by HTTP range requests from static
  hosting/object storage — no tile server needed) or MBTiles (SQLite; needs a server).

## 2. Build tiles with tippecanoe
```bash
tippecanoe -o parcels.pmtiles -l parcels -zg \
  --drop-densest-as-needed --extend-zooms-if-still-dropping \
  --coalesce-densest-as-needed parcels.geojson
```
- Input in **WGS 84 lon/lat** (EPSG:4326 GeoJSON); tiles are in Web Mercator.
- `-zg` guesses a max zoom from data density; or set `-Z`/`-z` explicitly
  (e.g. `-Z4 -z14`).
- Keep only needed attributes (`-y name -y use`) — tile size limits (~500 KB default
  per tile) are hit by attributes as much as geometry.
- Point data at low zooms: cluster or drop (`-r1` / `--cluster-distance`). *Flag names
  differ between tippecanoe versions/forks; check `tippecanoe --help`.*

## 3. Style with MapLibre
Minimal page structure:
```js
import maplibregl from 'maplibre-gl';
import { Protocol } from 'pmtiles';
maplibregl.addProtocol('pmtiles', new Protocol().tile);
const map = new maplibregl.Map({ container: 'map', style: 'style.json',
  center: [-1.5, 53.8], zoom: 11 });
```
In `style.json`, add a `vector` source `pmtiles://<URL>/parcels.pmtiles` and layers with
zoom-dependent paint using expressions, e.g.
`"line-width": ["interpolate", ["linear"], ["zoom"], 10, 0.3, 16, 2]`.
Apply cartographic hierarchy (see map-design): muted basemap, strong thematic layer.
Set `minzoom` on detailed layers so they don't render at overview zooms.

## 4. Interaction
- Popups on click (`map.on('click', 'parcels-fill', e => ...)`) showing a few
  formatted fields — not a raw attribute dump.
- Hover highlight via `feature-state`.
- Mobile: use generous tap targets, avoid hover-only information, test on a real phone.
- Legend and a short explanatory panel; story maps for narrative sequences.

## 5. Basemap and attribution
- Use a basemap provider whose terms allow your use; the standard OpenStreetMap tile
  servers are **not** for heavy or commercial production use (per OSM tile usage policy).
  Self-host OSM-derived tiles or use a commercial provider.
- Always show **attribution** ("© OpenStreetMap contributors" plus data sources) — it's
  a licence condition of OSM data.

## 6. Hosting
- PMTiles on static hosting/object storage: the host must support **HTTP range
  requests** and send **CORS** headers allowing your site's origin.
- Put a CDN in front; set cache headers; version filenames when data changes.
- Don't expose private attributes — anything in the tiles is downloadable by anyone.

## Gotchas
- Polygons with slivers/gaps at low zoom come from tile simplification; see the tippecanoe README on
  simplification options for your version.
- Coordinates ordered lat,lon in GeoJSON (must be lon,lat) put features in the wrong place.

## Verify
- [ ] Largest tile under the size limit; map loads in a few seconds on mobile data.
- [ ] Features visible and legible at minimum and maximum zoom.
- [ ] Popups readable on a phone; legend present.
- [ ] Attribution shown for basemap and data.
- [ ] Hosting returns 206 Partial Content and CORS headers for the tileset.

## Checked
2026-11-01. Confirmed in the tippecanoe README: `-zg`, `-y`/`--include`, `--drop-densest-as-needed`,
`--extend-zooms-if-still-dropping`, `--coalesce-densest-as-needed`, `-r1` with `--cluster-distance`, and the 500K tile size limit.
Confirmed on docs.protomaps.com: PMTiles readers use HTTP Range Requests, the MapLibre `addProtocol("pmtiles", ...)` plugin, and
the need for a Range- and CORS-capable server. Confirmed on the OSM tile usage policy: heavy use of the standard servers may be blocked.
Removed the unconfirmed size thresholds, the shared-borders flags and the ODbL note.
Method: documentation only; no commands were run.
