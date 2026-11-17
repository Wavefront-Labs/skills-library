---
id: computing-software.systems-network-administration.apache-guacamole.rdp-drive-redirection
name: rdp-drive-redirection
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, rdp, drive-redirection, enable-drive, drive-path, file-transfer, tsclient, disable-download, disable-upload, static-channels]
level: practitioner
status: draft
description: "Enable RDP file transfer in Guacamole through a virtual drive: enable-drive, drive-path on the guacd host, create-drive-path, drive-name, download/upload blocks and static channels."
sources:
  - https://guacamole.apache.org/doc/gug/configuring-guacamole.html
  - https://guacamole.apache.org/doc/gug/using-guacamole.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# RDP drive redirection

Parameters:
- `enable-drive=true`: turn on the virtual drive (off by default).
- `drive-path`: required; a directory on the Guacamole (guacd) server, not on the RDP host. guacd's user must be able to read and write it.
- `create-drive-path=true`: creates only the final directory; parents must exist.
- `drive-name`: name under Computer / My Computer and as the `\\tsclient` share.
- `disable-download` / `disable-upload` (default false): block transfers to/from the browser.
- `static-channels`: comma-separated static channel names exposed as pipes; max 7 characters each.

Usage in the browser: drag and drop files, or use the menu's file browser; files saved to the drive's **Download** folder on the remote side are sent to the browser automatically (apache-guacamole.using-guacamole-menu).

Gotchas:
- Static channels (drive/RDPDR, sound) fail with `Cannot create static channel "NAME": failed to load "guac-common-svc"` if a source-built FreeRDP has its plugins in the wrong place; put them in the `freerdp2/` directory next to `libfreerdp2.so`.
- Uploads through a proxy fail unless the body size limit is raised (apache-guacamole.nginx-reverse-proxy).
- Exposing `drive-path` via quickconnect can reveal any directory guacd can read (apache-guacamole.quickconnect).
- Use per-user paths with tokens, e.g. `/path/to/drives/${GUAC_USERNAME}` (apache-guacamole.parameter-tokens).

Verify: the remote Explorer shows the drive; an uploaded file appears under `drive-path`.
