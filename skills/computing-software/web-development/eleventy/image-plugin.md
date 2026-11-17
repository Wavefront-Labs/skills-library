---
id: computing-software.web-development.eleventy.image-plugin
name: image-plugin
category: computing-software
field: web-development
product: eleventy
tags: [image, eleventy-img, sharp, html-transform, srcset, avif, webp]
level: practitioner
status: docs-checked
description: "Optimize images at build time with @11ty/eleventy-img: HTML transform plugin, per-image eleventy: attributes, widths, formats, caching and build cost."
sources:
  - https://www.11ty.dev/docs/plugins/image/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`npm install @11ty/eleventy-img` (v7 needs Node 22+ and is ESM). Uses sharp; inputs include jpeg, png, webp, gif, tiff, avif, svg. No upscaling of raster images.

**HTML transform** (Eleventy v3.0.0+, Image v4.0.1+): processes every `<img>` and `<picture>` in output.

```js
import { eleventyImageTransformPlugin } from "@11ty/eleventy-img";
eleventyConfig.addPlugin(eleventyImageTransformPlugin, {
  formats: ["avif", "webp", "jpeg"],
  widths: ["auto"],
  htmlOptions: { imgAttributes: { loading: "lazy", decoding: "async" } },
});
```

Relative `src` writes beside the template output; absolute `src` goes to the default `img` directory (or `urlPath`). `sizes` is required with multiple widths and has no default (auto with `loading="lazy"` in v6+).

**Per-image attributes:** `eleventy:widths="200,600"`, `eleventy:formats="webp"`, `eleventy:ignore`, `eleventy:optional` (`keep` or `placeholder`), `eleventy:output`, `eleventy:pictureattr:NAME`.

**Options:** `widths` (`["auto"]` default), `formats` (`["webp","jpeg"]` default; also png, svg, avif, gif, auto, passthrough in v7), `svgShortCircuit`, `outputDir`, `urlPath`, `filenameFormat`, `urlFormat`, `statsOnly`, `dryRun`, `failOnError`, `useCache`, `sharpOptions`, `transform`, `returnType: "html"`, `cacheOptions` for remote images.

**Performance:** cost grows with unique images, remote images, formats (avif costs extra), widths and source size. In serve mode `transformOnRequest` processes images when the browser asks. Memory and disk caches skip unchanged work. Concurrency: `Image.concurrency`.

## Checked

2026-11-04. Confirmed against the Eleventy Image page: install and Node 22+ ESM requirement for v7, sharp and input types, no raster upscaling, HTML transform plugin and sample config, relative and absolute src resolution, sizes rules (sizes=auto with lazy in v6), the eleventy: attributes, option defaults and formats, svgShortCircuit, outputDir, urlPath, filenameFormat, urlFormat, statsOnly, dryRun, failOnError, useCache, sharpOptions, transform, returnType, cacheOptions, build cost factors, transformOnRequest, caches and Image.concurrency. Corrected the HTML transform version gate from 3.0.0-alpha.5.

Method: documentation only; no commands were run.
