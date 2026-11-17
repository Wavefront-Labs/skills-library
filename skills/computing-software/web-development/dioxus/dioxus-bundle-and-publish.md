---
id: computing-software.web-development.dioxus.dioxus-bundle-and-publish
name: dioxus-bundle-and-publish
category: computing-software
field: web-development
product: dioxus
tags: [dioxus, dx-bundle, bundle, github-pages, windows-subsystem, resources, macos, windows, deb]
level: practitioner
status: docs-checked
description: "Publish a Dioxus app: dx bundle for GitHub Pages or desktop installers, windows_subsystem gating, [bundle] resources, identifier, icon, category and per-OS bundle settings."
sources:
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/guides/deploy/index.md
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/guides/deploy/config.md
  - https://github.com/DioxusLabs/docsite/blob/main/docs-src/0.7/src/guides/tools/configure.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Bundling and publishing

Goal: ship a web build to GitHub Pages or build a desktop installer.

## Web: GitHub Pages

1. In `Dioxus.toml` set `base_path` to the repo name under `[web.app]`.
2. Make sure Pages publishes static files from the `docs` directory.
3. Build and relocate:

```sh
dx bundle --out-dir docs
mv docs/public/* docs
cp docs/index.html docs/404.html
```

The 404 copy makes client-side routing work. Then commit and push.

## Desktop installer

Install the CLI (`cargo install dioxus-cli`), then:

```sh
dx bundle --release
```

(add `--features bundle` if you use the gate below). Output lands in `dist/bundle/`.

On Windows, `#![windows_subsystem = "windows"]` hides the terminal window but also removes all logs, so use it only when bundling. Gate it:

```toml
[features]
bundle = []
```

```rust
#![cfg_attr(feature = "bundle", windows_subsystem = "windows")]
```

## Assets and [bundle] options

Assets from `manganis`/`asset!` are bundled automatically; or list files (globs allowed) in `Dioxus.toml`:

```toml
[bundle]
resources = ["main.css", "header.svg", "**/*.png"]
```

Dioxus uses tauri-bundler. Other `[bundle]` keys: `identifier` (e.g. `com.dioxuslabs`), `publisher`, `icon` (square 16, 24, 32, 64 or 256 pixels; PNG 32-bit RGBA; include `.icns` for macOS, `.ico` for Windows, `.png` for Linux), `copyright`, `category` (one of a fixed list such as `Utility`, `Productivity`), `short_description`, `long_description` and `external_bin` (sidecar binaries; the target triple is appended to the filename automatically).

Per-OS tables: `[bundle.macos]` (`frameworks`, `minimum_system_version` default `10.13`, `signing_identity`, `entitlements`, `hardened_runtime`) and `[bundle.windows]` (`digest_algorithm`, `certificate_thumbprint`, `timestamp_url`, `tsp`, `icon_path`, `webview_install_mode` with `EmbedBootstrapper`, `DownloadBootstrapper`, `OfflineInstaller`, `FixedRuntime` or `Skip`). The config page also lists Debian and WiX/NSIS settings as Rust structs.

## Gotcha

`Skip` for `webview_install_mode` makes the app fail if WebView2 is not already installed. CSS may behave differently per platform, so test each.

## Checked
Checked 2026-11-07 against the 0.7 Publishing page, the bundling config page and the Configure Project page (all read in full). Confirmed: GitHub Pages steps, dx bundle --release and dist/bundle/, windows_subsystem feature gate, [bundle] keys including icon rules, category list, external_bin triple, macOS default 10.13, Windows webview_install_mode values and the Skip warning, tauri-bundler. Nothing removed.
Method: documentation only; no commands were run.
