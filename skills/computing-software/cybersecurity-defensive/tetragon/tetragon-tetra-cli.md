---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-tetra-cli
name: tetragon-tetra-cli
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [tetra-cli]
level: intro
status: docs-checked
description: "Install the tetra client for Tetragon from release archives or Homebrew and connect it to a TLS-protected agent."
sources:
  - "https://tetragon.io/docs/installation/tetra-cli/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Install and use the tetra CLI

Goal: get the `tetra` client that talks to the Tetragon agent.

## Autodetect script

Needs a Go toolchain, `curl` and `sha256sum`. It downloads the archive and its SHA 256 digest, checks them, installs and cleans up:

```shell
GOOS=$(go env GOOS)
GOARCH=$(go env GOARCH)
curl -L --remote-name-all https://github.com/cilium/tetragon/releases/latest/download/tetra-${GOOS}-${GOARCH}.tar.gz{,.sha256sum}
sha256sum --check tetra-${GOOS}-${GOARCH}.tar.gz.sha256sum
sudo tar -C /usr/local/bin -xzvf tetra-${GOOS}-${GOARCH}.tar.gz
rm tetra-${GOOS}-${GOARCH}.tar.gz{,.sha256sum}
```

## Quick install (needs only curl)

Replace the OS and architecture as needed (linux, darwin or windows; amd64 or arm64):

```shell
curl -L https://github.com/cilium/tetragon/releases/latest/download/tetra-linux-amd64.tar.gz | tar -xz
sudo mv tetra /usr/local/bin
```

On Windows, download `tetra-windows-amd64.tar.gz` (or arm64) with `curl -LO`, extract with `tar -xzf`, and move the binary into a directory in your PATH.

## Homebrew

```shell
brew install tetra
```

The formula fetches precompiled binaries; `--build-from-source` builds with a Go dependency.

## Specific release

Set `OS`, `ARCH` and `TAG` (for example `linux`, `amd64`, `v0.9.0`) and download `https://github.com/cilium/tetragon/releases/download/${TAG}/tetra-${OS}-${ARCH}.tar.gz`.

## TLS-protected server

```shell
tetra \
  --server-address tetragon.example.com:54321 \
  --tls-ca-cert-files ca.crt \
  --tls-cert-file client.crt \
  --tls-key-file client.key \
  getevents
```

## Checked

2026-11-08. Read the tetra CLI installation page in full (raw docs markdown). Checked install methods and the TLS example against it; no claims removed.

Method: documentation only; no commands were run.
