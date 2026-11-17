---
id: computing-software.systems-network-administration.apache-guacamole.rdp-display-settings
name: rdp-display-settings
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, rdp, display-settings, color-depth, resize-method, display-update, dpi, force-lossless, disable-gfx, resolution]
level: practitioner
status: draft
description: "Guacamole RDP display parameters: color-depth, width/height, dpi, resize-method display-update or reconnect, force-lossless and disable-gfx (new in 1.6.0)."
sources:
  - https://guacamole.apache.org/doc/gug/configuring-guacamole.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# RDP display settings

| Parameter | Values / default |
|---|---|
| `color-depth` | 8, 16 or 24 bpp; otherwise the server decides |
| `width`, `height` | pixels; default is the browser display size |
| `dpi` | optional; if unset Guacamole estimates from size and resolution |
| `resize-method` | `display-update` (RDP 8.1+ Display Update channel) or `reconnect`; unset means no action on browser resize |
| `force-lossless` | `true` disables lossy compression; default uses lossy when heuristics favour it |
| `disable-gfx` | GFX (Graphics Pipeline Extension) is on by default (new in 1.6.0); `true` falls back to basic graphics |

Guidance:
- Dynamic resizing: choose `display-update` for modern Windows; `reconnect` restarts the session on resize.
- Fixed `width`/`height` override the browser size, so the display will not follow window resizes.
- Blurry text over slow links is lossy compression; try `force-lossless=true`, or lower `color-depth` for bandwidth.
- Invalid values such as non-integer width log `Invalid PARAMETER` in guacd (apache-guacamole.troubleshooting-guacd-errors).
- If graphics glitch after upgrading to 1.6.0, test `disable-gfx=true` to isolate the new pipeline (a diagnostic step, not a documented fix).

Related: performance flags in apache-guacamole.rdp-performance-flags.

Verify: after changing `resize-method`, resize the browser window and the remote desktop follows (or reconnects).
