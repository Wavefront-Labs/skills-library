---
id: computing-software.web-development.dioxus.dioxus-install-cli-and-platform-deps
name: dioxus-install-cli-and-platform-deps
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, dx, dx-doctor, rustup, cargo-binstall, wasm32-unknown-unknown, webview2, install]
level: intro
status: docs-checked
description: "Install Rust, the dx CLI and the per-OS desktop dependencies (WebView2, WebKitGtk, xdotool) needed to build Dioxus apps, and check them with dx doctor."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/getting_started/index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Install Dioxus tooling

Goal: get Rust, the `dx` build tool and OS dependencies ready for a Dioxus project.

## Steps

1. Install Rust (preferably with `rustup`), then add the stable toolchain and, for web apps, the wasm target:

```sh
rustup toolchain install stable
rustup target add wasm32-unknown-unknown
```

2. Install the Dioxus CLI. The prebuilt binary is the recommended route:

```sh
curl -sSL https://dioxus.dev/install.sh | bash
# or
cargo binstall dioxus-cli --force
# or build from source
cargo install dioxus-cli
```

3. Run `dx doctor` to see whether `dx` understands your install; it reports missing toolchains and tools needed for cross-platform development.

## Per-platform dependencies

- macOS: nothing extra (iOS builds need macOS with Xcode, plus the iOS SDK and simulators).
- Windows: needs WebView2, which is present if Edge is installed. Otherwise install it from Microsoft; the docs recommend the tiny evergreen bootstrapper (option 1 of three).
- Linux: WebKitGtk and xdotool are required. On Ubuntu:

```sh
sudo apt update
sudo apt install libwebkit2gtk-4.1-dev \
  build-essential curl wget file libxdo-dev libssl-dev \
  libayatana-appindicator3-dev librsvg2-dev lld
```

  On Fedora also run `sudo dnf install libxdo-devel`. Arch has its own package list (webkit2gtk-4.1, base-devel, xdotool and others) on the page.
- WSL: possible but tricky. Update the kernel and use WSL 2, add `export DISPLAY=:0` to `~/.zshrc`, install Tauri's Linux dependencies, and install a fallback such as `zenity` so file dialogs work.

## Gotchas

- Installing the CLI from source can take up to 10 minutes and needs several dependencies; the docs strongly recommend the prebuilt binaries.
- If installation fails with an OpenSSL error, install the dependencies listed in the openssl crate docs.
- On WSL you may see `libEGL` warnings that cannot be silenced; the app should still render.

## Checked
Checked 2026-11-07 against the 0.7 Getting Started page (read in full). Confirmed: rustup commands, three CLI install routes, 10 minute warning, OpenSSL note, dx doctor, per-OS dependencies, WebView2 option 1, Ubuntu package list, Fedora xdotool, Arch list, WSL steps and libEGL warning. Nothing removed.
Method: documentation only; no commands were run.
