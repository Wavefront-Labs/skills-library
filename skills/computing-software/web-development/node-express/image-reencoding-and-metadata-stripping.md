---
id: computing-software.web-development.node-express.image-reencoding-and-metadata-stripping
name: image-reencoding-and-metadata-stripping
category: computing-software
field: web-development
product: node-express
tags: [file-upload-security, secure-file-upload, image-reencoding, exif-stripping, sharp, gps-metadata, polyglot-files, image-processing]
level: practitioner
status: docs-checked
description: "Re-encoding uploaded images with sharp to neutralise polyglots and strip EXIF/GPS metadata, with orientation handling and safe output formats."
sources:
  - https://sharp.pixelplumbing.com/api-output#keepmetadata
  - https://sharp.pixelplumbing.com/api-operation#rotate
  - https://sharp.pixelplumbing.com/api-constructor
  - https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Image re-encoding and metadata stripping

**Goal:** stored user images contain only pixels - no hidden scripts/polyglot payloads, and no GPS location or camera serial numbers leaking users' privacy.

## 1. Re-encode everything
```js
import sharp from 'sharp';
const out = await sharp(inputBuffer, { limitInputPixels: 40_000_000 })   // keep failOn at its default 'warning' for untrusted input
  .rotate()                                   // apply EXIF orientation before it's stripped
  .resize({ width: 2048, height: 2048, fit: 'inside', withoutEnlargement: true })
  .webp({ quality: 82 })                       // or .jpeg({ quality: 85, mozjpeg: true })
  .toBuffer();
```
- sharp **drops metadata by default** on output (EXIF, XMP, IPTC, GPS) unless you call `keepMetadata()`/`withMetadata()`. Don't add `withMetadata()` "to keep orientation" - use `.rotate()` instead; it bakes orientation into pixels.
- ICC profiles are not kept unless you call `keepIccProfile()` (sharp 0.33+); `withMetadata()` also adds a web-friendly sRGB profile where appropriate.
- Re-encoding writes a new file from decoded pixels instead of storing the uploaded bytes; check that appended data does not survive (see Verify).
- Pick output format yourself (WebP/AVIF/JPEG/PNG); never store the original bytes as the served file. Keep the original in a private bucket only if you must (legal, re-processing).

## 2. Animated images
Multi-frame input (GIF, WebP): sharp reads one page by default; the `pages` input option (-1 for all) controls how many frames are loaded, so cap it to limit CPU.

## 3. Other languages
- Python Pillow: `ImageOps.exif_transpose()` applies the EXIF orientation; save to a new file and check that no EXIF remains.

## 4. Where to run
In a background job/worker with resource limits; image parsers are attack surface (OWASP cites ImageTragick): keep libvips/ImageMagick patched and run with least privilege.

## Verify
- [ ] `exiftool output.webp` shows no GPS/Make/Model/Serial fields.
- [ ] A phone photo taken in portrait displays upright after processing.
- [ ] A JPEG with appended `<script>` produces output without the appended bytes (size and hexdump check).

## Checked

2026-10-25 against the sharp docs (lovell/sharp main) and the OWASP File Upload cheat sheet. Confirmed: sharp removes all metadata by default, including EXIF orientation; keepMetadata, withMetadata and keepIccProfile (0.33+) exist; withMetadata also adds an sRGB profile; rotate() with no angle calls autoOrient to apply EXIF orientation; failOn defaults to warning and sharp advises keeping it for untrusted input; limitInputPixels default is 268402689; pages input option defaults to 1 and -1 loads all pages or frames; OWASP File Upload: validate file signature, store outside the webroot, keep libraries current, CDR for applicable types, ImageTragick as an example.

Method: documentation only; no commands were run.
