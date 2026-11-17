---
id: computing-software.software-engineering.tauri.tauri-webdriver-ci
name: tauri-webdriver-ci
category: computing-software
field: software-engineering
product: tauri
tags: [webdriver-ci, tauri, github-actions, tauri-driver]
level: practitioner
status: docs-checked
description: "Run Tauri WebDriver tests with tauri-driver in GitHub Actions on Linux (xvfb fake display) and Windows (matching Edge Driver)."
sources:
  - "https://v2.tauri.app/develop/tests/webdriver/ci/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WebDriver tests in CI

Goal: run WebdriverIO tests through `tauri-driver` on GitHub Actions. On Linux they run under a fake display; some CI systems such as GitHub Actions also support Windows.

Assumptions: the Tauri app is in `src-tauri`; the WebdriverIO runner is in `e2e-tests` and runs with `yarn test` there.

## Workflow outline (`.github/workflows/webdriver.yml`)

- Trigger `on: [push]`; matrix `platform: [ubuntu-latest, windows-latest]` with `fail-fast: false`.
- `actions/checkout@v4`.
- Linux dependencies: `libwebkit2gtk-4.1-dev`, `libayatana-appindicator3-dev`, plus the two extras `tauri-driver` needs: `webkit2gtk-driver` and `xvfb` (installed with `sudo apt-get update && sudo apt-get install -y ...`).
- Windows: install a matching Edge Driver:
  ```
  cargo install --git https://github.com/chippers/msedgedriver-tool
  & "$HOME/.cargo/bin/msedgedriver-tool.exe"
  $PWD.Path >> $env:GITHUB_PATH
  ```
- Rust: `dtolnay/rust-toolchain@stable`, then `Swatinem/rust-cache@v2` with `workspaces: src-tauri`.
- Run `cargo test` first, to avoid testing a broken application.
- Node: `actions/setup-node@v4` (`node-version: 24`, `cache: 'yarn'`), then `yarn install --frozen-lockfile` in the root and again in `e2e-tests`.
- Install the driver: `cargo install tauri-driver --locked` (its version is independent of other Tauri versions).
- Linux test step: `xvfb-run yarn test` in `e2e-tests`. The fake display server lets the app run headless without code changes.
- Windows test step: `yarn test` in `e2e-tests`, run directly.

## Checked

Checked 2026-11-08 against the Tauri v2 WebDriver CI page: workflow assumptions, matrix, action versions, Linux packages, msedgedriver-tool steps, Rust and Node setup, tauri-driver install and the xvfb-run Linux step. No claims removed.

Method: docs-only read of cited pages, 2026-11-08
