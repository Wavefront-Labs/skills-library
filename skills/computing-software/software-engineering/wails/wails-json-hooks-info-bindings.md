---
id: computing-software.software-engineering.wails.wails-json-hooks-info-bindings
name: wails-json-hooks-info-bindings
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, configuration, build-hooks, bindings]
level: practitioner
status: docs-checked
description: "Configure wails.json build hooks, app info with file associations and URI protocols, and TypeScript model generation prefix, suffix and output type."
sources: [https://wails.io/docs/reference/project-config]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# wails.json hooks, info and bindings

Goal: automate steps around builds, populate app metadata, and shape generated TypeScript.

## Build hooks

`preBuildHooks` and `postBuildHooks` map a key to a command. Keys: `GOOS/GOARCH`, `GOOS/*`, `*/*`. More specific hooks run first (`GOOS/GOARCH` before `GOOS/*` before `*/*`). `${platform}` is replaced by GOOS/GOARCH; in post hooks `${bin}` is the compiled binary path. `runNonNativeBuildHooks` (default false) controls whether hooks for a different OS than the host run.

## info

Populates manifests and version info: `companyName` and `productName` (default: project name), `productVersion` (default 1.0.0), `copyright`, `comments`.

`fileAssociations` entries: `ext` (no leading period), `name`, `description` (Windows only), `iconName` (file in build folder, no extension; icons generated from a .png for macOS and Windows), `role` (macOS only, CFBundleTypeRole, e.g. Editor).

`protocols` entries: `scheme` (e.g. myapp), `description` (Windows only), `role` (macOS only).

## bindings.ts_generation

`prefix` and `suffix` for generated JavaScript entities, and `outputType` of `classes` (default shown) or `interfaces`.

## Gaps
The page does not say how the custom URI protocol is received at runtime.

## Related skills
- computing-software.software-engineering.wails.wails-json-config

## Checked

2026-11-07. Read the whole Project Config reference page (website/docs/reference/project-config.mdx), focusing on preBuildHooks / postBuildHooks (ordering, ${platform}, ${bin}, runNonNativeBuildHooks), the info block (defaults, fileAssociations, protocols) and bindings.ts_generation (prefix, suffix, outputType). Every field, default and platform-only note matched; the Gaps note is correct (the page says nothing about receiving a custom URI protocol at runtime). No claims were trimmed.

Method: documentation only; no commands were run.
