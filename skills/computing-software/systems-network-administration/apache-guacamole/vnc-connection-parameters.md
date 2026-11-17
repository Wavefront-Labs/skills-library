---
id: computing-software.systems-network-administration.apache-guacamole.vnc-connection-parameters
name: vnc-connection-parameters
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, vnc, vnc-parameters, color-depth, swap-red-blue, cursor, encodings, read-only, compress-level, quality-level, clipboard-encoding]
level: practitioner
status: docs-checked
description: "Guacamole VNC connection parameters: hostname/port, credentials, color-depth, swap-red-blue, cursor, encodings, read-only, compression and quality levels, clipboard-encoding."
sources:
  - https://guacamole.apache.org/doc/gug/configuring-guacamole.html
  - https://guacamole.apache.org/doc/gug/adhoc-connections.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VNC parameters

Network and auth:
- `hostname` (required), `port` (usually 5900 plus display number; display `:1` is 5901; VNC has no default in quickconnect URIs)
- `autoretry`: retries before returning an error
- `username`, `password`: optional

Display:
| Parameter | Values |
|---|---|
| `color-depth` | 8, 16, 24 or 32 |
| `swap-red-blue` | `true` fixes swapped colours |
| `cursor` | `remote` renders the pointer remotely (local shows a small dot) |
| `encodings` | space-delimited list; default any supported |
| `read-only` | `true` ignores all input |
| `disable-server-input` | `true` asks the server to disable its local keyboard/mouse |
| `disable-display-resize` | stops sending browser size changes to the server |
| `force-lossless` | lossless only |
| `compress-level` | 0 (none) to 9 for tight/zlib; server has the final say |
| `quality-level` | 0 to 9 JPEG quality for tight |

Clipboard: `clipboard-encoding` defaults to `ISO8859-1`; alternatives `UTF-8`, `UTF-16`, `CP1252`. Only ISO 8859-1 is guaranteed by the VNC standard, so change it only if the server supports otherwise.

Authentication: the VNC standard defines only password authentication; Guacamole also supports username plus password, and which scheme works depends on the libvncclient version guacd is built against (MSLogonII needs a recent one).

Reverse connections, repeaters and audio: apache-guacamole.vnc-reverse-repeater-audio.

Verify: connect to port 5900 + display and colours look right.

## Checked

2026-11-04. Confirmed against the Guacamole manual pages configuring-guacamole and adhoc-connections: hostname, port (5900 plus display number), autoretry, username and password, color-depth values, swap-red-blue, cursor remote, encodings (space-delimited, any supported by default), read-only, disable-server-input, disable-display-resize, force-lossless, compress-level and quality-level ranges, and clipboard-encoding values with ISO 8859-1 as the only guaranteed encoding. Changed: removed the guacd error-message explanations, which these pages do not contain, and added the authentication note from the page.

Method: documentation only; no commands were run.
