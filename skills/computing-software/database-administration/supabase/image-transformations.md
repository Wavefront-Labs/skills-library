---
id: computing-software.database-administration.supabase.image-transformations
name: image-transformations
category: computing-software
field: database-administration
product: supabase
tags: [storage, image-transformations, resize, webp, imgproxy]
level: practitioner
status: docs-checked
description: "Supabase Storage image transformations: width, height, resize modes, quality, format, size limits, supported formats, billing and self-hosted imgproxy."
sources:
  - https://supabase.com/docs/guides/storage/serving/image-transformations
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: serve resized images from Storage.

Availability: Pro plan and above. Toggle **Enable Image Transformations** in Storage > Settings; disabling stops all transformation requests.

Parameters:
- `width`, `height`: integers 1 to 2500. Giving only one resizes and crops keeping the aspect ratio.
- `resize`: `cover` (default, crops overflow), `contain` (fits inside), `fill` (ignores aspect ratio).
- `quality`: 20 to 100, default 80.
- `format`: `origin` skips automatic WebP delivery (supabase-js v2.2.0+).

Limits: source image 25MB, resolution 50MP.

Formats: source and result PNG, JPEG, WebP, AVIF, GIF, ICO, SVG, BMP, TIFF; HEIC is source only. Storage returns the best format the client supports; currently only WebP.

Signed URLs embed the transform options in the token, so they cannot be changed after signing.

Billing: charged per origin image only for usage beyond the plan's quota; the count resets at the start of each billing cycle. See Supabase's pricing page for current quota and rates.

Self-hosting uses imgproxy, preconfigured in the official Docker Compose stack. For a custom setup, run imgproxy on an internal network with `IMGPROXY_ENABLE_WEBP_DETECTION=true` and `IMGPROXY_JPEG_PROGRESSIVE=true` (image `darthsim/imgproxy`; not reachable from the public internet), and set `ENABLE_IMAGE_TRANSFORMATION=true` and `IMGPROXY_URL` on the storage-api service.

## Checked

2026-11-04: Read the Storage Image Transformations page in full. Confirmed availability, the toggle, parameters, limits, formats, WebP behaviour, signed-URL note and self-hosting variables. Removed the dollar figure and quota number (prices change; see the vendor's pricing page).
Method: documentation only; no commands were run.
