---
id: computing-software.networking-hardware-and-wireless.unbound.remote-control-setup
name: remote-control-setup
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, unbound-control, remote-control, control-enable, unbound-control-setup, certificates]
level: practitioner
status: docs-checked
description: "Enable unbound-control: the remote-control clause, control interface and port, unix sockets, generated certificates and file permissions."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/getting-started/configuration.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound-control.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# remote control setup
Enable under `remote-control:` with `control-enable: yes` (default no).

Options:
- `control-interface`: IP, interface name[@port] or an absolute path for a Unix socket (no certificates needed). Default localhost.
- `control-port`: 8953.
- `control-use-cert`: default yes; may be no only for localhost interfaces; ignored for sockets.
- `server-key-file`, `server-cert-file`, `control-key-file`, `control-cert-file`: defaults `unbound_server.key`, `unbound_server.pem`, `unbound_control.key`, `unbound_control.pem`.

Generate keys with `unbound-control-setup` (self-signed server and client pairs in the run directory, or `-d dir`). Run it as the daemon's user, e.g. `sudo -u unbound unbound-control-setup`; existing private keys are preserved. File permissions decide who may use unbound-control (owner and group by default). Without a configured username, the keys must be readable by the user starting the daemon.

Client: `unbound-control [-hq] [-c cfgfile] [-s server[@port]] command`; pass `-c` if the config is not in the default location. `status` exits 3 if the server is not running.

## Checked
2026-11-04. Confirmed against the unbound.conf manual and unbound-control manual: remote-control options and defaults, Unix socket behaviour, unbound-control-setup usage, key preservation and the status exit code. Nothing removed.
Method: documentation only; no commands were run.
