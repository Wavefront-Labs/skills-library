---
id: computing-software.systems-network-administration.apache-guacamole.rdp-audio-printing
name: rdp-audio-printing
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, rdp, audio, microphone, audio-input, printing, virtual-printer, ghostscript, printer-name, device-redirection]
level: practitioner
status: draft
description: "RDP sound, microphone and printer redirection in Guacamole: disable-audio, enable-audio-input, enable-printing with GhostScript on guacd, printer-name, and clipboard channel messages."
sources:
  - https://guacamole.apache.org/doc/gug/configuring-guacamole.html
  - https://guacamole.apache.org/doc/gug/troubleshooting.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# RDP audio, microphone, printing

| Parameter | Default | Effect |
|---|---|---|
| `disable-audio` | audio on | `true` mutes |
| `enable-audio-input` | off | microphone via the AUDIO_INPUT channel |
| `enable-printing` | off | virtual printer that delivers PDFs to the browser |
| `printer-name` | - | name shown in Devices and Printers; ignored if printing is off |
| `console-audio` | - | audio in the console session; only with `console=true` |

Printing requirements:
- GhostScript (`gs`) must be installed on the guacd host.
- Output is a PDF downloaded in the browser.

Dependencies and failures:
- Sound (RDPSND) and printing (RDPDR) use static channels; guacd logs `Cannot create static channel` if the FreeRDP plugin cannot load (see apache-guacamole.rdp-drive-redirection).
- `Support for the CLIPRDR channel could not be loaded` means clipboard redirection is unavailable; the reason is logged.
- `Server requested unsupported clipboard data type` is informational.

Disable clipboard in either direction with `disable-copy` / `disable-paste` (apache-guacamole.clipboard-and-terminal-display).

Verify: print from a remote app to the Guacamole printer and a PDF downloads.
