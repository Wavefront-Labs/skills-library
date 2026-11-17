---
id: computing-software.systems-network-administration.jellyfin.fallback-and-system-fonts
name: fallback-and-system-fonts
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, fonts, fallback-fonts, ass-subtitles, woff2, subtitle-burn-in]
level: practitioner
status: docs-checked
description: "Fix missing glyphs in burned-in or ASS subtitles by installing server fonts and configuring Jellyfin's fallback font folder."
sources: ["https://jellyfin.org/docs/general/administration/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Fonts for subtitles and cover images

Jellyfin uses fonts in three places.

**Server-side system fonts** are used to burn subtitles into transcoded video and to render cover images. How to install them depends on the operating system, or on the image if you run a container.

**Client-side system fonts** render the client interface and, in some clients, subtitles. They are installed on each device, not on the server.

**Fallback fonts** are loaded by the web client to draw ASS subtitles when no other font can render a glyph, for example CJK characters that would otherwise appear as an empty "tofu" block. Fonts attached to an MKV and client fonts are tried first.

To use them, set the Fallback Fonts setting to a folder on the server containing the fonts. Constraints from the docs:

- Total size is limited to 20 MB, because every font is always preloaded in the browser whether needed or not.
- Lightweight web formats such as woff2 are recommended.
- TrueType (`.ttf`) and OpenType (`.otf`) fonts can be converted to woff2 with the woff2 conversion tool the docs point to.

Google Fonts is suggested as a source for fonts covering most languages.

## Checked

2026-11-03. Confirmed against the Jellyfin Configuration page, Fonts section: server and client system fonts, fallback fonts for ASS subtitles, 20 MB limit, woff2 recommendation, Google Fonts. Removed: unsupported diagnosis advice, an unsupported tool attribution and a burn-in boxes claim.

Method: documentation only; no commands were run.
