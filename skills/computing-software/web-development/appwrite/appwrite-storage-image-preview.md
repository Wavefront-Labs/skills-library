---
id: computing-software.web-development.appwrite.appwrite-storage-image-preview
name: appwrite-storage-image-preview
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, storage, images, getfilepreview, transformations]
level: practitioner
status: docs-checked
description: "Resize, crop, round, rotate and re-encode stored images on the fly with getFilePreview parameters."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/storage/images/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: serve optimized images without storing variants.

Call `storage.getFilePreview` (the preview endpoint) with the bucket and file ID plus optional parameters:
- `width` and `height`: integers 0 to 4000 pixels; the image is resized keeping the aspect ratio.
- `gravity`: crop anchor, one of `center`, `top-left`, `top`, `top-right`, `left`, `right`, `bottom-left`, `bottom`, `bottom-right`.
- `quality`: 0 to 100, where 100 is highest.
- `borderWidth`: 0 to 100 pixels and `borderColor`: hex color without the leading `#`.
- `borderRadius`: pixels, 0 to 4000.
- `opacity`: float 0 to 1 (0 is transparent); only works with output formats that support alpha channels such as `png`.
- `rotation`: -360 to 360 degrees.
- `background`: hex color without the leading `#`; only works with output formats that support alpha channels such as `png`.
- `output`: `jpg`, `jpeg`, `png`, `gif`, `webp`, `avif` or `heic`; defaults to the original image's format.

Transformed images are cached by Appwrite and your browser, so repeated use of the same transformation has minimal performance impact. The docs frame this as a way to change resolution, format and compression for network transfer and responsive layouts.

Gotcha: pass hex colors without the leading `#`, and use an alpha-capable output such as `png` when you need `opacity` or `background`.

## Checked

Date: 2026-11-07. Read in full on the appwrite/website docs source (Markdoc): products/storage/images. Code tabs for non-JavaScript SDKs were collapsed when read and Markdoc partials (shared include files) were not opened; all prose and the JavaScript examples were read. Corrections: Removed "0 keeps the original proportion", the Cloud metering plan note (not on the page), opacity/background restricted wording corrected to formats with alpha channels like png, output formats corrected (jpg, jpeg, png, gif, webp, avif, heic), borderRadius range corrected to 0-4000, Gotcha reworded; removed the invented Verify; added caching note.

Method: documentation only; no commands were run.
