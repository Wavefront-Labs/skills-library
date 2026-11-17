---
id: computing-software.web-development.ghost.ghost-theme-responsive-images
name: ghost-theme-responsive-images
category: computing-software
field: web-development
product: ghost
tags: [ghost, theme, responsive-images, img-url, srcset, webp, package-json]
level: practitioner
status: docs-checked
description: "Define image sizes in package.json and use img_url size and format to build responsive srcsets and WebP output in Ghost themes."
sources:
  - https://github.com/TryGhost/docs/blob/main/themes/responsive-images.mdx
  - https://github.com/TryGhost/docs/blob/main/themes/helpers/data/img_url.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: serve right-sized feature images from a theme.

Define sizes in `package.json` under `config.image_sizes`, each with a `width`, for example `"m": {"width": 600}` (the page shows Casper's `xxs` 30, `xs` 100, `s` 300, `m` 600, `l` 1000, `xl` 2000). Ghost generates copies at those sizes and works like a cache, so sizes can change any time. Keep to no more than about 10 sizes so media storage does not grow out of control.

Use them with the helper: `{{img_url feature_image size="m"}}`.

Build a srcset:
```handlebars
<img srcset="{{img_url feature_image size="s"}} 300w,
             {{img_url feature_image size="m"}} 600w,
             {{img_url feature_image size="l"}} 1000w"
     sizes="(max-width: 1000px) 400px, 700px"
     src="{{img_url feature_image size="m"}}" alt="{{title}}">
```

Format conversion: add `format="webp"` (this works only together with `size`). The docs say converting PNG, GIF or JPEG to WebP can cut size by about 25 percent without visible loss; the helper accepts `webp`, `avif`, `png`, `jpg`, `jpeg` and `gif`. AVIF compresses better but is not supported in all browsers and does not support animation yet. Conversion changes the file type but the extension stays the same (an AVIF image keeps `.jpg`). The page recommends a `<picture>` tag with AVIF and WebP `<source>` elements and an original-format `<img>` fallback. `absolute="true"` forces an absolute URL but is almost never needed.

Content images added in posts are compressed and resized automatically; this feature covers feature images and theme images.

Compatibility: sizes are generated on the first request for each image at a size, and regenerated when an image, the size config or the theme changes. Dynamic sizes do not work with externally hosted images (except inserted Unsplash images); with a third-party storage adapter the URL comes from the external source.

## Checked

Date: 2026-11-07. Read in full (GitHub blob text, 125 and 46 lines, code samples inline, no imported snippets): themes/responsive-images.mdx and themes/helpers/data/img_url.mdx. The size cap, format-needs-size rule, format list, WebP saving and content-image statements match. The srcset example is shortened from the page's Casper example (the page also uses `xl` 2000w). Removed the Verify step. Added config key, AVIF, extension, picture and compatibility notes.
Method: documentation only; no commands were run.
