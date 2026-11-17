---
id: computing-software.systems-network-administration.linux.build-flatpaks-with-flatpak-builder
name: build-flatpaks-with-flatpak-builder
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, flatpak, flatpak-builder, flatpak-manifest, flathub, sandbox-permissions, ostree]
level: advanced
status: docs-checked
description: "Package an application as a Flatpak with flatpak-builder: manifest modules and sources, runtimes/SDKs, finish-args permissions, local repo export and test installs."
sources:
  - https://docs.flatpak.org/en/latest/flatpak-builder.html
  - https://docs.flatpak.org/en/latest/manifests.html
  - https://docs.flatpak.org/en/latest/sandbox-permissions.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Building flatpaks with flatpak-builder

## Prereqs
```bash
dnf install flatpak-builder   |  apt install flatpak-builder
flatpak remote-add --if-not-exists --user flathub https://dl.flathub.org/repo/flathub.flatpakrepo
flatpak install --user flathub org.freedesktop.Platform//<BRANCH> org.freedesktop.Sdk//<BRANCH>
```
## Manifest (com.example.MyTool.yml)
```yaml
id: com.example.MyTool
runtime: org.freedesktop.Platform
runtime-version: '<BRANCH>'          # a currently supported runtime branch
sdk: org.freedesktop.Sdk
command: mytool
finish-args:
  - --share=network
  - --socket=wayland
  - --socket=fallback-x11
  - --filesystem=xdg-documents:ro
modules:
  - name: mytool
    buildsystem: meson          # autotools, cmake, cmake-ninja, simple, qmake
    sources:
      - type: archive
        url: https://example.com/mytool-1.4.tar.xz
        sha256: 9f8a...
      - type: patch
        path: fix-paths.patch
```
## Build, test, export
```bash
flatpak-builder --user --install --force-clean build-dir com.example.MyTool.yml
flatpak run com.example.MyTool
flatpak-builder --repo=repo --force-clean build-dir com.example.MyTool.yml   # export to a local OSTree repo
flatpak build-bundle repo mytool.flatpak com.example.MyTool                 # single-file bundle
flatpak run --command=sh com.example.MyTool                                 # debug inside the sandbox
```
Builds run offline after the download stage — every source must be declared in the manifest
(`--disable-download` makes flatpak-builder fail instead of touching the network).

## Permissions
Ask for the minimum: avoid `--filesystem=home`/`host`; prefer portals (file chooser) over filesystem access.

## Gotchas
- Runtime branches go end-of-life; move `runtime-version` to a supported branch before yours does.
- Paths are under `/app`, not `/usr` — hardcoded `/usr/share` paths need patching.
- Sign repos (`--gpg-sign`) when publishing your own remote.

## Verify
- [ ] `flatpak run` works; `flatpak info --show-permissions com.example.MyTool` lists only intended permissions.

## Checked

2026-10-28

Confirmed: flatpak-builder manual and command reference (buildsystem values, --install, --force-clean, --repo, --gpg-sign, --disable-download, sources in the manifest), flatpak manifests page (modules, sources, finish-args), sandbox-permissions page, first-build page (install into /app, build-bundle), flatpak command reference (build-export, override, info).

Removed or corrected: The pinned 24.08 runtime branch (replaced by a placeholder), the pip and node generator tool names, the claim that Flathub reviewers reject broad permissions, and the 'yearly' runtime bump.

Method: documentation only; no commands were run.
