---
id: computing-software.software-engineering.tauri.tauri-prerequisites
name: tauri-prerequisites
category: computing-software
field: software-engineering
product: tauri
tags: [prerequisites, tauri]
level: intro
status: docs-checked
description: "Install the system dependencies, Rust, Node.js and optional Android/iOS toolchains needed before building a Tauri app."
sources:
  - "https://v2.tauri.app/start/prerequisites/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tauri prerequisites

Goal: a machine that can build a Tauri app. Order: system dependencies, Rust, Node.js (only for a JavaScript frontend), then mobile targets (only if needed).

## System dependencies

- **Debian/Ubuntu**: `sudo apt update`, then `sudo apt install libwebkit2gtk-4.1-dev build-essential curl wget file libxdo-dev libssl-dev libayatana-appindicator3-dev librsvg2-dev`. Other distributions (Arch, Fedora, Gentoo, OSTree, openSUSE, Alpine) have their own package lists; NixOS instructions live in the NixOS Wiki.
- **macOS**: install Xcode (Mac App Store or Apple Developer site) and launch it once. For desktop-only work, `xcode-select --install` (Command Line Tools) is enough.
- **Windows**: install Microsoft C++ Build Tools with "Desktop development with C++" checked, plus WebView2 (already present on Windows 10 1803 and later; otherwise install the Evergreen Bootstrapper). Building MSI packages needs the VBSCRIPT optional feature enabled; `failed to run light.exe` can signal it is off.

## Rust

- Linux/macOS: `curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh`
- Windows: `winget install --id Rustlang.Rustup`. Make sure the MSVC toolchain is the default; if Rust is already installed, run `rustup default stable-msvc`.
- Restart the terminal afterwards (sometimes the system).

## Node.js

Download the LTS version from the Node.js website and check with `node -v` and `npm -v`. For pnpm or yarn, run `corepack enable`.

## Mobile targets

- **Android**: install Android Studio; set `JAVA_HOME` (Linux: `/opt/android-studio/jbr`); in the SDK Manager install Android SDK Platform, Platform-Tools, NDK (Side by side), Build-Tools and Command-line Tools; set `ANDROID_HOME` and `NDK_HOME`; then run `rustup target add aarch64-linux-android armv7-linux-androideabi i686-linux-android x86_64-linux-android`.
- **iOS** (macOS only, needs full Xcode, not Command Line Tools): `rustup target add aarch64-apple-ios x86_64-apple-ios aarch64-apple-ios-sim`, then install Homebrew and run `brew install cocoapods`.

## Checked

Checked 2026-11-08 against the Tauri v2 prerequisites page: Debian package list, macOS Xcode and Command Line Tools, Windows Build Tools, WebView2 (Windows 10 1803 and later), VBSCRIPT note, rustup commands, MSVC default toolchain, Node LTS and corepack, Android SDK components and variables, rustup targets for Android and iOS, and cocoapods. No claims removed.

Method: docs-only read of cited pages, 2026-11-08
