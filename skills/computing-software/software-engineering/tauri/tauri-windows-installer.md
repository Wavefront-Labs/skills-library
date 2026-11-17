---
id: computing-software.software-engineering.tauri.tauri-windows-installer
name: tauri-windows-installer
category: computing-software
field: software-engineering
product: tauri
tags: [windows-installer, tauri, nsis-wix]
level: advanced
status: docs-checked
description: "Build and customise Tauri Windows installers (MSI via WiX, setup.exe via NSIS), WebView2 install modes, cross-compiling and install modes."
sources:
  - "https://v2.tauri.app/distribute/windows-installer/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tauri Windows installer

Goal: produce `.msi` (WiX Toolset v3, Windows only) or `-setup.exe` (NSIS) installers with `tauri build`.

## Targets

- 32-bit: `rustup target add i686-pc-windows-msvc`, then `tauri build --target i686-pc-windows-msvc`.
- ARM64: install the "C++ ARM64 build tools" in Visual Studio Installer, `rustup target add aarch64-pc-windows-msvc`, then `--target aarch64-pc-windows-msvc`. The NSIS installer itself stays x86 under emulation; the app is native ARM64.
- Cross-compile from Linux or macOS (NSIS only, last resort, less tested): install NSIS (`sudo apt install nsis` or `brew install nsis`), LLVM and LLD (`sudo apt install lld llvm` or `brew install llvm`), `rustup target add x86_64-pc-windows-msvc`, `cargo install --locked cargo-xwin`, then `tauri build --runner cargo-xwin --target x86_64-pc-windows-msvc`. Output is in `target/x86_64-pc-windows-msvc/release/bundle/nsis/`. Signing needs an external tool.
- MSI packages need the VBSCRIPT optional Windows feature; "failed to run light.exe" can mean it is disabled.

## WebView2 install modes

Set `bundle > windows > webviewInstallMode > type`:

| type | Internet | Extra size |
| :-- | :-- | :-- |
| `downloadBootstrapper` (default) | yes | 0MB |
| `embedBootstrapper` | yes | ~1.8MB (better Windows 7 `.msi` support) |
| `offlineInstaller` | no | ~127MB |
| `fixedRuntime` (with `path`; the page's table calls it fixedVersion) | no | ~180MB |
| `skip` | no | 0MB, app will not work without the runtime |

For a minimum runtime, set `bundle > windows > minimumWebview2Version`, for example `"110.0.1531.0"`.

## WiX

Custom template: `bundle > windows > wix > template`. Extend with fragments: save a `.wxs` in `src-tauri/windows/fragments` and set `wix > fragmentPaths` plus `componentRefs` (also `componentGroupRefs`, `featureGroupRefs`, `featureRefs`, `mergeRefs`). Set `wix > language` to a string, an array (one installer per language) or an object with `localePath` to a `.wxl` file. FIPS: set `TAURI_BUNDLER_WIX_FIPS_COMPLIANT=true`.

## NSIS

Hooks `NSIS_HOOK_PREINSTALL`, `NSIS_HOOK_POSTINSTALL`, `NSIS_HOOK_PREUNINSTALL`, `NSIS_HOOK_POSTUNINSTALL` go in a `.nsh` file referenced by `nsis > installerHooks`. `nsis > installMode` is `perMachine` or `both` (default: current user only, no admin). Other keys: `languages`, `displayLanguageSelector`, `template`.

## Checked

Checked 2026-11-08 against the cited Tauri v2 Windows Installer page: build targets, cross-compile steps, WebView2 table and keys, WiX and NSIS keys, hooks and install modes. Added the VBSCRIPT note and the fixedRuntime/fixedVersion naming. No claims removed.

Method: docs-only read of cited pages, 2026-11-08
