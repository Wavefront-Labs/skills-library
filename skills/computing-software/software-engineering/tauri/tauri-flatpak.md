---
id: computing-software.software-engineering.tauri.tauri-flatpak
name: tauri-flatpak
category: computing-software
field: software-engineering
product: tauri
tags: [flatpak, tauri, flathub]
level: advanced
status: docs-checked
description: "Package a Tauri app as a Flatpak from its .deb, test it locally with flatpak-builder, and submit it to Flathub."
sources:
  - "https://v2.tauri.app/distribute/flatpak/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tauri Flatpak

Goal: build a Flatpak from your Tauri `.deb` and publish to Flathub (closed-source flow).

## Prerequisites

Install `flatpak` and `flatpak-builder` (for example `sudo apt install flatpak flatpak-builder`), then the runtime:

```shell
flatpak install flathub org.gnome.Platform//46 org.gnome.Sdk//46
```

Build the `.deb` of your app and create an AppStream MetaInfo file.

## Manifest (flatpak-builder.yaml)

Key fields: `id: <identifier>`, `runtime: org.gnome.Platform`, `runtime-version: '47'`, `sdk: org.gnome.Sdk`, `command: <main_binary_name>`. `finish-args`: `--socket=wayland`, `--socket=fallback-x11`, `--device=dri` (OpenGL, not always needed), `--share=ipc`; tray icon apps also need `--talk-name=org.kde.StatusNotifierWatcher` and `--filesystem=xdg-run/tray-icon:create`. Optional `--env=WEBKIT_DISABLE_COMPOSITING_MODE=1` may solve black webviews on Wayland.

A `simple` module lists sources (the metainfo file and the `.deb`, remote ones with `sha256`, `only-arches: [x86_64]`) and build commands: extract with `ar -x *.deb --output deb-extract` and `tar -C deb-extract -xf deb-extract/data.tar.gz`; `install -Dm755` the binary into `/app/bin`; copy extra resources to `/app/lib/<product_name>`; `sed` the `Icon=` line of the desktop file to `<identifier>` and install it to `/app/share/applications/<identifier>.desktop`; install the 128x128, 32x32 and `256x256@2` icons as `<identifier>.png`; install the metainfo to `/app/share/metainfo/<identifier>.metainfo.xml`. The GNOME 46 runtime includes the standard Tauri app dependencies.

Tray icon without opening `$XDG_RUNTIME_DIR`: call `.temp_dir_path(app.path().app_cache_dir().unwrap())` on `TrayIconBuilder`.

## Build and test

```shell
flatpak-builder --force-clean --user --disable-cache --repo flatpak-repo flatpak flatpak-builder.yaml
flatpak run <your flatpak id>
flatpak -y --user update <your flatpak id>
```

For extra libraries, build them from source inside the Flatpak rather than including local `.so` files.

## Submit to Flathub

Fork `flathub/flathub`, clone with `--branch=new-pr`, create a branch, add your manifest, push, and open a pull request against `new-pr`. After review and approval you get an invitation to edit your app's repository.

## Checked
2026-11-07. Confirmed claim by claim against https://v2.tauri.app/distribute/flatpak/ (page text including code blocks and tabs read in full).
Method: documentation only; no commands were run.
