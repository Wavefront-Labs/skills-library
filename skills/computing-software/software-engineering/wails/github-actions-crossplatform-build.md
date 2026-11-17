---
id: computing-software.software-engineering.wails.github-actions-crossplatform-build
name: github-actions-crossplatform-build
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, github-actions, ci, cross-platform, wails-build-action, release]
level: practitioner
status: docs-checked
description: "Build a Wails app for Linux, Windows and macOS in GitHub Actions on new tags using the dAppServer wails-build-action matrix."
sources: [https://wails.io/docs/guides/crossplatform-build]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: produce one build per operating system using GitHub Actions (the page says an application build is needed for each OS).

The page points to the community action https://github.com/dAppServer/wails-build-action (steps can be copied from its `action.yml` if it does not fit).

## Workflow (on any new tag)
```yaml
name: Wails build

on:
  push:
    tags:
      - '*'

env:
  # Build failures from OOM are common otherwise
  NODE_OPTIONS: "--max-old-space-size=4096"

jobs:
  build:
    strategy:
      fail-fast: false
      matrix:
        build:
          - name: 'App'
            platform:  'linux/amd64'
            os: 'ubuntu-latest'
          - name: 'App'
            platform:  'windows/amd64'
            os: 'windows-latest'
          - name: 'App'
            platform:  'darwin/universal'
            os: 'macos-latest'

    runs-on: ${{ matrix.build.os }}
    steps:
      - name: Checkout
        uses: actions/checkout@v2
        with:
          submodules: recursive

      - name: Build wails
        uses: dAppServer/wails-build-action@v2.2
        id: build
        with:
          build-name: ${{ matrix.build.name }}
          build-platform: ${{ matrix.build.platform }}
          package: false
          go-version: '1.20'
```

`fail-fast: false` stops one platform's failure cancelling the others. The page says the build is then uploaded to Actions artifacts.

## Extensions suggested by the page
Dependency caching, code signing, uploading to S3/Supabase etc., secrets as env vars, and env vars as build variables (for example a version taken from the Git tag).

Related: `computing-software.software-engineering.wails.mac-app-store-submission`.

## Checked

Date: 2026-11-07

Confirmed against the Wails v2 documentation source (wailsapp/wails, website/versioned_docs/version-v2.17.0), each cited page read in full: "Crossplatform build with Github Actions" guide.

Corrected or removed: Removed "Wails builds natively per platform"; the page says only that a build is needed for each operating system.

Method: documentation only; no commands were run.
