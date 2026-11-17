---
id: computing-software.web-development.directus.image-transform-params
name: image-transform-params
category: computing-software
field: web-development
product: directus
tags: [image-transform, asset-query-params, focal-point, transform-size-limits]
level: practitioner
status: docs-checked
description: "Resize and reformat Directus images with width, height, quality, fit, format and withoutEnlargement on /assets, within the transformation size limits."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/guides/05.files/5.transform.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Pass parameters to the `assets` endpoint; a missing processed asset is generated, stored and returned.

```http
GET /assets/<file-id>?width=300&height=300&quality=50&fit=contain
```

- `width`, `height`: pixels
- `quality`: 1 to 100 (Sharp's default for the format if omitted)
- `withoutEnlargement`: disable upscaling
- `format`: auto (default; webp or avif if the browser supports it, else jpg), jpg, png, webp, tiff
- `fit`: `cover` (default), `contain` (letterbox), `inside`, `outside`

With `width`/`height`, cropping uses the file's `focal_point_x` and `focal_point_y`; default is the centre.

SDK: `directus.request(readAssetRaw(FILE_ID, { width: 300, height: 300, quality: 50, fit: 'contain' }))`. GraphQL is not supported.

Limits: `ASSETS_TRANSFORM_IMAGE_MAX_DIMENSION` caps the source image size and `ASSETS_TRANSFORM_IMAGE_MAX_OUTPUT_DIMENSION` caps any produced size at every step of a chain. Violations raise `ILLEGAL_ASSET_TRANSFORMATION`.

## Checked

2026-11-04: parameter list with quality range, format and fit values, focal point behaviour, REST and SDK examples, GraphQL not supported, and the two dimension limit variables confirmed against the Directus Transform Files page. Removed a Verify line the page does not state.

Method: documentation only; no commands were run.
