---
id: computing-software.software-engineering.tauri.tauri-github-pipeline
name: tauri-github-pipeline
category: computing-software
field: software-engineering
product: tauri
tags: [github-pipeline, tauri, github-actions]
level: practitioner
status: docs-checked
description: "Use tauri-action in GitHub Actions to build a Tauri app for Windows, Linux and macOS and publish a GitHub release."
sources:
  - "https://v2.tauri.app/distribute/pipelines/github/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tauri GitHub Actions pipeline

Goal: build and release a Tauri app with `tauri-apps/tauri-action@v1`.

## Setup

Create a workflow in the repo (Actions tab, "New workflow", "Set up a workflow yourself"). If the app is not at the repository root, use the `projectPath` input. Keep the `tauri-action` step at the end, since it runs the build and releases the app.

## Triggers

The example runs on pushes to the `release` branch; the action creates a git tag and release title from the app version. To trigger on a version tag instead:

```yaml
on:
  push:
    tags:
      - 'app-v*'
```

## Workflow steps

The example builds Windows x64, Linux x64, Linux Arm64, macOS x64 and macOS Arm64 using a matrix of `macos-latest` (with `--target aarch64-apple-darwin` or `--target x86_64-apple-darwin`), `ubuntu-22.04`, `ubuntu-22.04-arm` (public repos only) and `windows-latest`:

1. `actions/checkout@v7`.
2. Ubuntu only: `sudo apt-get install -y libwebkit2gtk-4.1-dev libappindicator3-dev librsvg2-dev patchelf xdg-utils`.
3. `actions/setup-node@v6` with `node-version: lts/*`.
4. `dtolnay/rust-toolchain@stable` and `swatinem/rust-cache@v2` (`workspaces: './src-tauri -> target'`).
5. Install frontend dependencies.
6. `tauri-apps/tauri-action@v1` with `GITHUB_TOKEN`, `tagName: app-v__VERSION__`, `releaseName`, `releaseBody`, `releaseDraft: true`, `prerelease: false` and `args: ${{ matrix.args }}`. The job needs `permissions: contents: write`.

## Troubleshooting

"Resource not accessible by integration": the token is read-only by default. In repository settings, Actions, Workflow permissions, select "Read and write permissions".

Windows and macOS signing in the workflow follow their own guides; without an Apple certificate, configure an ad-hoc signing identity. For Arm builds in private repos beware build minutes: the `pguyot/arm-runner-action` emulated-runner approach needs about 1 hour for an uncached fresh project.

## Checked
2026-11-07. Confirmed claim by claim against https://v2.tauri.app/distribute/pipelines/github/ (page text including code blocks and tabs read in full).
Corrected: the page calls the Arm action an emulated runner, not QEMU.
Method: documentation only; no commands were run.
