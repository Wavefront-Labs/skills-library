---
id: computing-software.digital-privacy-hygiene.device-hardening.flatpak-sandbox-permissions
name: flatpak-sandbox-permissions
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, flatpak-permissions, flatseal, linux-desktop-security, sandbox, portals, filesystem-access, flathub-verified]
level: practitioner
status: docs-checked
description: "Tighten Flatpak app sandboxes with Flatseal or flatpak override: remove home/host filesystem access, devices and session bus holes many Flathub apps ship with."
sources:
  - "https://docs.flatpak.org/en/latest/sandbox-permissions.html"
  - "https://www.privacyguides.org/en/os/linux-overview/#flatpak"
  - "https://github.com/tchx84/Flatseal"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Flatpak sandbox permissions

**Goal:** Flatpak sandboxes apps, but many Flathub manifests grant `--filesystem=home` or
`host`, which makes the sandbox decorative. Review and tighten.

## Inspect
```bash
flatpak list --app
flatpak info --show-permissions org.mozilla.firefox
```
Red flags: `filesystem=host`, `filesystem=home`, `device=all`, `socket=x11`, and access to the
`org.freedesktop.Flatpak` D-Bus interface (lets an app run commands unsandboxed on the host).

## Tighten (GUI: Flatseal)
Flatseal lists each app's permissions with toggles; changes are overrides stored per user.

## Tighten (CLI)
```bash
flatpak override --user --nofilesystem=home org.example.App
flatpak override --user --filesystem=xdg-download org.example.App   # only Downloads
flatpak override --user --nosocket=x11 --socket=wayland org.example.App
flatpak override --user --show org.example.App
flatpak override --user --reset org.example.App   # undo
```
Apps using **portals** (file chooser) still let you open files you pick, without blanket access.

## Choose apps wisely
- Some apps break without broad access (IDEs); accept or use distro packages.

## Gotchas
- Global overrides (`flatpak override --user --nofilesystem=home` without an app id)
  affect every app; useful but test.

## Verify
- [ ] No app retains `filesystem=host` without a reason.
- [ ] Browser restricted to Downloads (if you accept that workflow).

## Checked
2026-11-01. Confirmed against the Flatpak sandbox permissions page and command reference: `flatpak list --app`, `info --show-permissions`, `override` with `--user`, `--nofilesystem`, `--filesystem`, `--nosocket`, `--socket=wayland`, `--show`, `--reset`, and the org.freedesktop.Flatpak interface. Removed: the X11 keylogging claim, Flathub verified publisher advice and the restart note.
Method: documentation only; no commands were run.
