---
id: computing-software.web-development.web-performance.image-cdns-and-on-the-fly-resizing
name: image-cdns-and-on-the-fly-resizing
category: computing-software
field: web-development
product: web-performance
tags: [image-optimization, image-cdn, responsive-images, avif, cloudinary, imgix]
level: practitioner
status: docs-checked
description: "Using image CDNs to resize, crop and convert images on the fly: URL parameters, auto format, security keys, caching and billing, and LCP effects."
sources:
  - https://web.dev/articles/image-cdns
  - https://developers.cloudflare.com/images/optimization/transformations/
  - https://cloudinary.com/documentation/image_transformations
  - https://docs.imgix.com/en-US/apis/rendering/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Image CDNs and on-the-fly resizing

An image CDN transforms, optimizes and delivers images; the URL says which image to load plus parameters such as size, format and quality. Unlike a build-time script, it creates versions as they are needed. web.dev (a 2019 article) says switching can yield a 40-80% saving in image file size.

## 1. URL patterns
- Cloudinary: `https://res.cloudinary.com/<cloud_name>/image/upload/<public_id>.<extension>`, with transformation segments before the public ID, for example `c_crop,h_200,w_300` or `f_auto` (best format for the requesting browser, such as webp or avif).
- imgix: parameters are added to the image URL's query string (resize, crop, compress, change format).
- Cloudflare: transformations are requested through a specially formatted URL on your zone, or through Workers; they must be enabled for the zone first.
- web.dev: the most important transformations for performance are size, pixel density, format and compression. "Auto" modes choose using signals such as client hints, the Save-Data header, User-Agent and the Network Information API (for example AVIF to Chrome, WebP to Edge, JPEG to a very old browser).
- The returned format can differ from the URL's file extension; the `Content-Type` header is authoritative, which matters if the file is saved to disk.

## 2. Security, cost and caching
- web.dev: a security key stops other people creating new versions of your images; without a valid key a changed URL cannot generate a new version.
- Cloudflare: by default only source images from the same zone are accepted; define allowed source origins explicitly. Each unique combination of source image and parameters is cached and billed separately; the first request for each unique version in a calendar month counts as one transformation, whatever the cache status. A cache hit is served from the edge without contacting the origin.
- imgix: strips most metadata (EXIF, geolocation) by default; `iptc=allow` keeps IPTC/XMP. Maximum canvas is 8192 by 8192 px (larger images are resized to fit first); input files should stay under 100 MB (soft limit 500 MB).
- Third-party CDNs are typically priced by usage tiers; self-managed options named by web.dev are Thumbor, Imaginary and Imagor.

## 3. LCP considerations (web.dev)
- A cross-origin image CDN adds connection setup; prefer one that proxies through your primary origin, and using your own domain also makes switching CDNs easier because no URLs change.
- Use `fetchpriority="high"` on the LCP image, and `rel=preload` if it is not discoverable in the initial HTML.
- If you cannot proxy and the browser will not know the image until late, connect to the CDN origin early (preconnect).

## Verify
- [ ] The CDN serves a modern format to supporting browsers, a URL with altered parameters and no valid key is refused (if keys are enabled), and the LCP image request starts early.

## Checked
2026-11-09. Read web.dev "Use image CDNs" in full, the Cloudflare transformations overview, the imgix Rendering API overview and the opening and URL sections of Cloudinary's image transformations page (searched for `f_auto` and the delivery URL format; not read end to end). Removed (not on those pages): `q_auto`, `g_auto`, `c_fill`, the imgix `auto=format` and `s=` signing parameters, the Cloudflare `/cdn-cgi/image/` URL, the fixed-width srcset advice, `Vary: Accept` advice, upscaling and ICC notes, SSRF framing, Bunny, Fastly, Akamai and imgproxy claims, and the framework image components.
Method: documentation only; no commands were run.
