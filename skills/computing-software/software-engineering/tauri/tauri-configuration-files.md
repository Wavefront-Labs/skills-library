---
id: computing-software.software-engineering.tauri.tauri-configuration-files
name: tauri-configuration-files
category: computing-software
field: software-engineering
product: tauri
tags: [configuration-files, tauri]
level: practitioner
status: docs-checked
description: "Work with tauri.conf.json, JSON5 and TOML formats, platform-specific and --config merged configuration, Cargo.toml and package.json in a Tauri app."
sources:
  - "https://v2.tauri.app/develop/configuration-files/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tauri configuration files

Goal: know which file to edit. Main files: `tauri.conf.json`, `Cargo.toml`, `package.json`.

## Tauri config

Defines the web app source, app metadata, bundles, plugin settings and runtime behavior (windows, tray icons, menus). Used by both the runtime and the CLI. All options are in the configuration reference.

**Formats.** Default is JSON. For JSON5 or TOML add the `config-json5` or `config-toml` feature to the `tauri` and `tauri-build` dependencies in `Cargo.toml`, for example `tauri = { version = "2.0.0", features = [ "config-json5" ] }`. The TOML file is `Tauri.toml`; JSON5 content is shown in `tauri.conf.json`. Structure is the same; TOML may use kebab-case (`dev-url`, `before-dev-command`). Field names are case-sensitive.

**Platform-specific files.** `tauri.linux.conf.json`, `tauri.windows.conf.json`, `tauri.macos.conf.json`, `tauri.android.conf.json`, `tauri.ios.conf.json` (or `Tauri.<platform>.toml`) are merged into the main config using JSON Merge Patch (RFC 7396). Objects merge key by key; arrays are replaced whole, including arrays nested in objects, and array elements such as `app.windows` entries are replaced too, so repeat every field you want to keep.

**Extending with `--config`.** The `dev`, `android dev`, `ios dev`, `build`, `android build`, `ios build` and `bundle` commands accept `--config` with a raw JSON string or a JSON file path, merged by the same rule. Example for a beta app: a file `src-tauri/tauri.beta.conf.json` with `productName` "My App Beta" and `identifier` "com.myorg.myappbeta", then `npm run tauri build -- --config src-tauri/tauri.beta.conf.json` (pnpm/yarn/bun: `tauri build --config ...`).

## Cargo.toml

Declares Rust dependencies. Important: `tauri-build` (build-dependencies) and `tauri` (dependencies), generally on the same minor versions as the Tauri CLI. `tauri dev` and `tauri build` manage the `tauri` features automatically from your config. `cargo update` in `src-tauri` pulls the latest Semver-compatible versions; prefix a version with `=` to pin it. Commit `Cargo.lock`.

## package.json

Holds frontend dependencies (`@tauri-apps/api`, `@tauri-apps/cli`) and scripts (`dev`, `build`, `tauri`; the `tauri` script is only needed with npm). Hook scripts into Tauri with `build.beforeDevCommand` and `build.beforeBuildCommand`, for example `yarn dev` and `yarn build`.

## Checked
2026-11-07. Confirmed claim by claim against https://v2.tauri.app/develop/configuration-files/ (page text including code blocks and tabs read in full).
Corrected: the file name `tauri.conf.json5` is not on the page; only `Tauri.toml` is named and JSON5 content appears in a `tauri.conf.json` example.
Method: documentation only; no commands were run.
