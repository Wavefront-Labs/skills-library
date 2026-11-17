---
id: computing-software.software-engineering.tauri.tauri-appimage
name: tauri-appimage
category: computing-software
field: software-engineering
product: tauri
tags: [appimage, tauri, linux-bundle]
level: practitioner
status: docs-checked
description: "Distribute a Tauri app as a Linux AppImage: media support via GStreamer, custom files, glibc baseline and ARM build constraints."
sources:
  - "https://v2.tauri.app/distribute/appimage/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tauri AppImage

An AppImage bundles all dependencies and files the app needs, so it runs on many Linux distributions without installation. Users make it executable (`chmod a+x MyProject.AppImage`) and run it (`./MyProject.AppImage`). The cost is size: from the 2-6 MB range to 70+ MB. Use it when you cannot make a package for the distribution's package manager.

GUI apps on macOS and Linux do not inherit `$PATH` from shell dotfiles; use the `fix-path-env-rs` crate.

## Build baseline

Build on the oldest base system you intend to support that provides WebKitGTK 4.1 (Ubuntu 22.04 and Debian 12 are examples). A newer base can raise the minimum glibc, causing runtime errors like `version 'GLIBC_2.33' not found`. Use Docker or GitHub Actions.

## Multimedia (GStreamer)

If the app plays audio or video, enable `tauri.conf.json > bundle > linux > appimage > bundleMediaFramework`. This grows the bundle and is currently only fully supported on Ubuntu build systems. Make sure the build system has all plugins the app needs at runtime. GStreamer plugins in the `ugly` package may have licensing that makes distribution hard.

## Custom files

For files you do not want in Tauri's `resources`, map AppImage paths to paths relative to `tauri.conf.json`; destination paths must currently begin with `/usr/`:

```json
{
  "bundle": {
    "linux": {
      "appimage": {
        "files": {
          "/usr/share/README.md": "../README.md",
          "/usr/assets": "../assets/"
        }
      }
    }
  }
}
```

## ARM

`linuxdeploy`, the AppImage tooling Tauri uses, does not support cross-compiling ARM AppImages, so build on ARM devices or emulators. GitHub's `ubuntu-22.04-arm` and `ubuntu-24.04-arm` runners need no changes and a typical build takes about 10 minutes. The QEMU-based action workflow is extremely slow; use it only in public repositories.

## Checked
2026-11-07. Confirmed claim by claim against https://v2.tauri.app/distribute/appimage/ (page text including code blocks and tabs read in full).
Corrected: the PATH note covers macOS and Linux GUI apps, not Linux only; removed the public-repos restriction on the ubuntu-*-arm runners (the page says they are publicly available).
Method: documentation only; no commands were run.
