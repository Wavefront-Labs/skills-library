---
id: computing-software.collaboration-platform-administration.nextcloud.preview-providers-and-external-binaries
name: preview-providers-and-external-binaries
category: computing-software
field: collaboration-platform-administration
product: nextcloud
tags: [previews, enabledpreviewproviders, ffmpeg, imagemagick, libreoffice]
level: advanced
status: docs-checked
description: "Know which Nextcloud preview providers are on by default, which need ffmpeg, LibreOffice or ImageMagick delegates, and why AVIF may need a second provider."
sources:
  - https://docs.nextcloud.com/server/latest/admin_manual/configuration_files/previews_configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: get thumbnails for the file types you care about without enabling risky providers.

By default Nextcloud previews images and text documents. Providers for many other types (documents in various Office formats, many video formats) are disabled by default for security and performance reasons. They remain available but are discouraged and considered unsupported. The full enabled and disabled lists are under the `enabledPreviewProviders` parameter.

Providers that depend on external software:
- Video, `OC\Preview\Movie` and `OC\Preview\MKV`: need `ffmpeg`.
- Office, `OC\Preview\OpenDocument` and `OC\Preview\MSOfficeDoc`: need LibreOffice.
- ImageMagick formats such as `OC\Preview\Illustrator`, `SVG` and `TIFF`: need ImageMagick support. Installing the `imagick` PHP extension alone is not enough; ImageMagick must carry the delegate for the format.
- `OC\Preview\JP2` needs the OpenJPEG delegate.
- `OC\Preview\HEIC` and `OC\Preview\AVIFImagick` need an HEIF delegate, usually libheif.

A provider whose delegate is missing is never registered, so those files keep their mimetype icon instead of a broken preview.

AVIF: `OC\Preview\AVIF` is enabled by default but decodes with GD, which handles AVIF only if PHP was built against a libgd that supports it. Where it was not, also enable `OC\Preview\AVIFImagick`. GD is asked first and ImageMagick is asked if GD returns nothing.

Set providers in `config/config.php` via `enabledPreviewProviders`. After any preview parameter change, run `preview:cleanup` to remove previews made under obsolete settings.

Check: upload a sample of each file type and confirm a thumbnail, not a generic icon.

## Checked

2026-11-03. Confirmed against these Nextcloud admin manual pages:
- https://docs.nextcloud.com/server/latest/admin_manual/configuration_files/previews_configuration.html
Removed or reworded: claims the pages did not state (see the Check line and any softened wording).
Method: documentation only; no commands were run.
