---
id: computing-software.software-engineering.tauri.tauri-environment-variables
name: tauri-environment-variables
category: computing-software
field: software-engineering
product: tauri
tags: [environment-variables, tauri, cli, signing]
level: practitioner
status: docs-checked
description: "Reference of environment variables read by the Tauri CLI for CI, signing, notarization and mobile paths, and those set for hook commands."
sources:
  - "https://v2.tauri.app/reference/environment-variables/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tauri environment variables

Goal: configure the CLI and bundler through the environment. If both an environment variable and the equivalent CLI flag are given, the flag wins.

## CLI inputs

- `CI`: run in CI mode with no user interaction.
- `TAURI_CLI_CONFIG_DEPTH`: levels to traverse to find the Tauri config file.
- `TAURI_CLI_PORT`: port for the CLI built-in dev server.
- `TAURI_CLI_WATCHER_IGNORE_FILENAME`: name of a `.gitignore`-style file controlling what `dev` watches.
- `TAURI_CLI_NO_DEV_SERVER_WAIT`: do not wait for the frontend dev server before building.
- `TAURI_LINUX_AYATANA_APPINDICATOR`: `true` or `1` forces `libayatana-appindicator` for the Linux tray.
- `TAURI_BUNDLER_WIX_FIPS_COMPLIANT`: WiX `FipsCompliant` option.
- `TAURI_BUNDLER_TOOLS_GITHUB_MIRROR` and `TAURI_BUNDLER_TOOLS_GITHUB_MIRROR_TEMPLATE`: GitHub mirror (or URL template such as `https://mirror.example.com/<owner>/<repo>/releases/download/<version>/<asset>`) for bundler downloads.
- `TAURI_SKIP_SIDECAR_SIGNATURE_CHECK`: skip signing sidecars.
- `TAURI_WEBVIEW_AUTOMATION`: webview automation (Linux only).
- `TAURI_ANDROID_PROJECT_PATH` / `TAURI_IOS_PROJECT_PATH`: usually `<project>/src-tauri/gen/android` and `.../gen/ios`.

## Signing

- `TAURI_SIGNING_PRIVATE_KEY` (string or file path) and `TAURI_SIGNING_PRIVATE_KEY_PASSWORD`: sign app bundles.
- `TAURI_SIGNING_RPM_KEY` (ASCII-armored GPG private key) and `TAURI_SIGNING_RPM_KEY_PASSPHRASE`: sign the RPM bundle.
- `TAURI_WINDOWS_SIGNTOOL_PATH`: path to `signtool.exe`.

## Apple

- `APPLE_CERTIFICATE`: base64 of the `.p12`, from `openssl base64 -A -in MyCertificate.p12 -out MyCertificate-base64.txt`; `APPLE_CERTIFICATE_PASSWORD` is its export password.
- `APPLE_SIGNING_IDENTITY`: overrides `bundle > macOS > signingIdentity`; if neither is set it is inferred from `APPLE_CERTIFICATE`.
- Notarization with an Apple ID: `APPLE_ID`, `APPLE_PASSWORD` (app-specific password; `@keychain:` or `@env:` prefixes allowed) and `APPLE_TEAM_ID` must all be set.
- Notarization with a JWT: `APPLE_API_KEY`, `APPLE_API_ISSUER` (required with the key), `API_PRIVATE_KEYS_DIR`, `APPLE_API_KEY_PATH` (the `.p8` file; required for iOS).
- `APPLE_PROVIDER_SHORT_NAME`: team to notarize with when the Apple ID has several; overrides `bundle > macOS > providerShortName`.
- `APPLE_DEVELOPMENT_TEAM`: iOS code signing team; overrides `bundle > iOS > developmentTeam`.

## Hook command variables

Set for each hook command such as `beforeDevCommand` and `beforeBuildCommand`:

- `TAURI_ENV_DEBUG`: `true` for `dev` or `build --debug`, else `false`.
- `TAURI_ENV_TARGET_TRIPLE`, `TAURI_ENV_ARCH` (`x86_64`, `aarch64`), `TAURI_ENV_PLATFORM` (`windows`, `darwin`, `linux`), `TAURI_ENV_PLATFORM_VERSION`, `TAURI_ENV_FAMILY` (`unix` or `windows`).

## Checked
2026-11-07. Confirmed claim by claim against https://v2.tauri.app/reference/environment-variables/ (page text including code blocks and tabs read in full).
Method: documentation only; no commands were run.
