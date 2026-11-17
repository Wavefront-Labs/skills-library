---
id: computing-software.software-engineering.tauri.tauri-debian-package
name: tauri-debian-package
category: computing-software
field: software-engineering
product: tauri
tags: [debian-package, tauri, deb]
level: practitioner
status: docs-checked
description: "Ship a Tauri app as a Debian package: glibc baseline, custom files, and manual ARMv7 and ARM64 cross-compilation steps."
sources:
  - "https://v2.tauri.app/distribute/debian/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tauri Debian package

The stock Debian package defines icons, generates a Desktop file and depends on `libwebkit2gtk-4.1-0` and `libgtk-3-0`, plus `libappindicator3-1` if the app uses the system tray.

## Build baseline

glibc often breaks compatibility with older systems, so build on the oldest base system you intend to support that provides WebKitGTK 4.1. Ubuntu 22.04 and Debian 12 are suitable baselines (both provide `libwebkit2gtk-4.1-dev`). A newer base can raise the minimum glibc and cause errors like `version 'GLIBC_2.33' not found`. Use a Docker container or GitHub Actions.

GUI apps on macOS and Linux do not inherit `$PATH` from shell dotfiles; use the `fix-path-env-rs` crate.

## Custom files and dependencies

Extra system dependencies go under `tauri.conf.json > bundle > linux > deb`. To add files, map package path to a path relative to `tauri.conf.json`:

```json
{
  "bundle": {
    "linux": {
      "deb": {
        "files": {
          "/usr/share/README.md": "../README.md",
          "/usr/share/assets": "../assets/"
        }
      }
    }
  }
}
```

## Cross-compile for ARM (Debian/Ubuntu host)

1. `rustup target add armv7-unknown-linux-gnueabihf` or `aarch64-unknown-linux-gnu`.
2. `sudo apt install gcc-arm-linux-gnueabihf` or `gcc-aarch64-linux-gnu`.
3. In `.cargo/config.toml` set `[target.<triple>] linker = "arm-linux-gnueabihf-gcc"` or `"aarch64-linux-gnu-gcc"`.
4. `sudo dpkg --add-architecture armhf` or `arm64`.
5. On non-Debian distros edit `/etc/apt/sources.list`: add `deb [arch=armhf,arm64] http://ports.ubuntu.com/ubuntu-ports <codename> ...` lines and add `[arch=amd64]` to the existing lines.
6. `sudo apt-get update && sudo apt-get upgrade -y`.
7. `sudo apt install libwebkit2gtk-4.1-dev:armhf` (or `:arm64`).
8. If OpenSSL headers are missing, install `libssl-dev:armhf`/`:arm64` or add `openssl-sys = {version = "0.9", features = ["vendored"]}`.
9. `export PKG_CONFIG_SYSROOT_DIR=/usr/arm-linux-gnueabihf/` (or `/usr/aarch64-linux-gnu/`).
10. `cargo tauri build --target armv7-unknown-linux-gnueabihf` (or `aarch64-unknown-linux-gnu`).

## Checked
2026-11-07. Confirmed claim by claim against https://v2.tauri.app/distribute/debian/ (page text including code blocks and tabs read in full).
Method: documentation only; no commands were run.
