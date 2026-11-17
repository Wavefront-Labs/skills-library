---
id: computing-software.systems-network-administration.immich.custom-map-styles
name: custom-map-styles
category: computing-software
field: systems-network-administration
product: immich
tags: [map, style-json, maptiler, dark-theme, tiles]
level: practitioner
status: docs-checked
description: "Replace Immich's default map tiles with a custom style.json for light and dark themes, including building one in MapTiler."
sources:
  - https://docs.immich.app/guides/custom-map-styles
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: change how maps look, or use a different tile provider.

The default styles are published as `style.json` documents you can use as a base:

- Light: `https://tiles.immich.cloud/v1/style/light.json`
- Dark: `https://tiles.immich.cloud/v1/style/dark.json`

Apply a style:

1. In Immich go to Administration, Settings, Map & GPS Settings and expand Map Settings.
2. Paste the URL of your JSON style into Light Style, Dark Style, or both. Different styles per theme help the map match Immich's light or dark mode.
3. Save, then reload the map.

Build one with MapTiler (no hand-written JSON):

1. Create a free account at `cloud.maptiler.com`.
2. Either choose New Map, pick a starter map and Customize, or pick a Standard Map and customise it.
3. In the editor change colours, remove visible layers or add layers such as administrative, topo or hydro.
4. Click Save at the top right and give the map a unique name.
5. Click Publish. This deploys it to production so it is reachable over the internet. MapTiler warns that changing the map changes it across all apps using it; that is fine for a new map.
6. Open the map's details page and copy the link under "Use vector style". It already contains your personal API key.

Paste that link into the Immich settings above. The link contains your personal MapTiler API key.

## Checked

2026-11-09. Confirmed against the Immich docs (https://docs.immich.app/) by reading guides/custom-map-styles in full. The default light and dark style URLs were fetched (HTTP 200, JSON) and match the map defaults in install/config-file.
Reworded: the secret-handling remark, to what the page states.
Method: documentation only; no commands were run.
