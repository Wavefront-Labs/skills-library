---
id: computing-software.systems-network-administration.apache-guacamole.sftp-file-transfer
name: sftp-file-transfer
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, sftp, file-transfer, enable-sftp, sftp-hostname, sftp-root-directory, sftp-host-key, guacctl, drag-and-drop]
level: practitioner
status: docs-checked
description: "Enable SFTP file transfer on Guacamole SSH, RDP and VNC connections: enable-sftp, host and credentials, sftp-directory and sftp-root-directory, download/upload blocks, guacctl."
sources:
  - https://guacamole.apache.org/doc/gug/configuring-guacamole.html
  - https://guacamole.apache.org/doc/gug/using-guacamole.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SFTP file transfer

Set `enable-sftp=true` (off by default). Parameters:
| Parameter | Default |
|---|---|
| `sftp-hostname` | the remote desktop host |
| `sftp-port` | 22 |
| `sftp-timeout` | 10 s |
| `sftp-host-key` | none (no verification) |
| `sftp-username`, `sftp-password` | username falls back to the desktop username |
| `sftp-private-key`, `sftp-passphrase`, `sftp-public-key` | optional key auth |
| `sftp-directory` | upload target for drag and drop |
| `sftp-root-directory` | the root directory; what the file browser exposes |
| `sftp-server-alive-interval` | 0 (off); minimum 2 |
| `sftp-disable-download`, `sftp-disable-upload` | false |

For SSH connections the manual lists only `enable-sftp`, `sftp-root-directory` and the two disable flags; the full `sftp-*` list is documented in the RDP section, and the manual says SFTP can serve RDP or VNC connections.

Use in the browser: drag files into the window, or the menu file browser (apache-guacamole.using-guacamole-menu). In SSH sessions, `guacctl -d FILE` downloads (alias `guacget`), and `guacctl -s DIR` sets the upload directory.

RDP alternative without SFTP: virtual drive (apache-guacamole.rdp-drive-redirection).

Verify: the file browser opens at `sftp-root-directory` and an upload lands on the server.

## Checked

2026-11-04. Confirmed against the Guacamole manual pages configuring-guacamole and using-guacamole: SFTP disabled unless enable-sftp is true, every sftp-* parameter and default in the table, the SSH-section subset, independence from RDP drive redirection, drag-and-drop and file browser use, and guacctl -d, -s and the guacget alias. Changed: reworded the RDP and VNC applicability and the root directory default to match the page.

Method: documentation only; no commands were run.
