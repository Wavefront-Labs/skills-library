---
id: computing-software.systems-network-administration.headscale.deb-package-install
name: deb-package-install
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, deb, apt, install, systemd, debian]
level: intro
status: docs-checked
description: "Install Headscale from the official DEB package on Debian 12+ or Ubuntu 22.04+, edit the packaged config, and check the systemd service."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/setup/install/official.md
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Install from the official DEB package

The recommended method on Debian-based systems. Supported: Ubuntu 22.04 or newer and Debian 12 or newer. The packages configure a local user to run headscale, provide a default configuration and ship a systemd service file.

```
HEADSCALE_VERSION="" # e.g. "X.Y.Z" (do not add the "v" prefix)
HEADSCALE_ARCH=""    # e.g. "amd64"
wget --output-document=headscale.deb \
"https://github.com/juanfont/headscale/releases/download/v${HEADSCALE_VERSION}/headscale_${HEADSCALE_VERSION}_linux_${HEADSCALE_ARCH}.deb"

sudo apt install ./headscale.deb
sudo nano /etc/headscale/config.yaml
sudo systemctl restart headscale
sudo systemctl status headscale
```

## Notes

- Take the version (without the "v" prefix) and architecture from the GitHub releases page.
- An up-to-date example config is installed at `/usr/share/doc/headscale/examples/config-example.yaml`.
- Next step: register your first machine (create-users, register-web-auth).

## Verify

`sudo systemctl status headscale` verifies that headscale is running as intended. `headscale configtest` validates the configuration file.

## Checked

2026-11-04. Confirmed against the Headscale official-releases page (DEB steps, supported distributions) and the configuration page (`configtest`). Removed the unsourced advice to compare configs after upgrades, to set server_url and listen_addr before first use, and to read the journal.

Method: documentation only; no commands were run.
