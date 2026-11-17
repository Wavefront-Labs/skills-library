---
id: computing-software.collaboration-platform-administration.vikunja.desktop-app-install
name: desktop-app-install
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, electron-desktop, flatpak, desktop-cors, port-45735]
level: intro
status: docs-checked
description: "Install the Vikunja Electron desktop app on Windows or Linux, via Flathub or package files, and allow its localhost origin through CORS on a self-hosted server."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/desktop.mdx
  - https://raw.githubusercontent.com/go-vikunja/vikunja/main/config-raw.json
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The desktop app is an Electron application for Linux and Windows.

Install: download from the desktop download page. Windows: the `.exe` or `.msi`. Linux: builds exist for Alpine, AppImage, Arch Linux, Debian-based systems, FreeBSD, Fedora and Snap. Install it as you would any package of that type.

Flatpak:

```
flatpak install flathub io.vikunja.Vikunja
```

Self-hosted servers: enable CORS for at least the host `http://127.0.0.1:45735` so the desktop app can talk to your instance. The default of `cors.enable` is true, and by default it is enabled only for requests from the desktop application running on localhost. `service.publicurl` is required when `cors.enable` is true.

For end-user features (signing in, quick-entry window, system tray, command-line flags) see the Desktop App help page and the desktop README on GitHub.

## Checked

2026-11-04. Confirmed against the Vikunja Desktop Packages page (setup/desktop) and config-raw.json: Electron app for Linux and Windows, .exe and .msi, the Linux package types, Flathub command, CORS host 127.0.0.1:45735, cors.enable default and service.publicurl requirement. Removed: the OIDC redirect advice, which neither page states.

Method: documentation only; no commands were run.
