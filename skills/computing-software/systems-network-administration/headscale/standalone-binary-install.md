---
id: computing-software.systems-network-administration.headscale.standalone-binary-install
name: standalone-binary-install
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, binary, useradd, systemd, unix-socket, install]
level: practitioner
status: docs-checked
description: "Install the Headscale standalone binary by hand: download, dedicated system user, config, systemd unit adjustments, and the unix_socket path."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/setup/install/official.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Install the standalone binary (advanced)

Considered advanced: you take care of the local user and the systemd service yourself. If possible, use the DEB packages or a community package instead.

```
sudo wget --output-document=/usr/bin/headscale \
https://github.com/juanfont/headscale/releases/download/v<HEADSCALE VERSION>/headscale_<HEADSCALE VERSION>_linux_<ARCH>
sudo chmod +x /usr/bin/headscale

sudo useradd \
 --create-home \
 --home-dir /var/lib/headscale/ \
 --system \
 --user-group \
 --shell /usr/sbin/nologin \
 headscale

sudo mkdir -p /etc/headscale
sudo nano /etc/headscale/config.yaml
```

## Service unit

Copy headscale's systemd service file (packaging/systemd/headscale.service in the repository) to `/etc/systemd/system/headscale.service`, then adjust `ExecStart`, `WorkingDirectory` and `ReadWritePaths` to your layout. In `/etc/headscale/config.yaml`, override the default `headscale` unix socket with a path that is writable by the `headscale` user or group:

```yaml
unix_socket: /var/run/headscale/headscale.sock
```

```
systemctl daemon-reload
systemctl enable --now headscale
systemctl status headscale
```

## Checked

2026-11-04. Confirmed against the Headscale official-releases page (standalone binaries section: download, chmod, useradd flags, service file parameters, unix_socket, systemctl steps). Removed the Gotchas about home directory defaults and the non-login shell, which the page does not explain, and reworded the DEB advice to what the page says.

Method: documentation only; no commands were run.
