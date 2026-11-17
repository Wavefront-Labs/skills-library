---
id: computing-software.cloud-infrastructure-engineering.cilium.hubble-cli-install-and-api-access
name: hubble-cli-install-and-api-access
category: computing-software
field: cloud-infrastructure-engineering
product: cilium
tags: [cilium, hubble-cli, hubble-status, port-forward, hubble-server, relay-api]
level: intro
status: docs-checked
description: "Install the Hubble CLI from stable.txt with checksum verification and reach the Relay API using hubble status -P and the HUBBLE_SERVER variable."
sources:
  - https://docs.cilium.io/en/stable/observability/hubble/setup/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Hubble CLI install and API access

## Install (Linux)
```
HUBBLE_VERSION=$(curl -s https://raw.githubusercontent.com/cilium/hubble/main/stable.txt)
HUBBLE_ARCH=amd64
if [ "$(uname -m)" = "aarch64" ]; then HUBBLE_ARCH=arm64; fi
curl -L --fail --remote-name-all https://github.com/cilium/hubble/releases/download/$HUBBLE_VERSION/hubble-linux-${HUBBLE_ARCH}.tar.gz{,.sha256sum}
sha256sum --check hubble-linux-${HUBBLE_ARCH}.tar.gz.sha256sum
sudo tar xzvfC hubble-linux-${HUBBLE_ARCH}.tar.gz /usr/local/bin
rm hubble-linux-${HUBBLE_ARCH}.tar.gz{,.sha256sum}
```
macOS uses `hubble-darwin-*` and `shasum -a 256 -c`. Windows: download hubble-windows-amd64.tar.gz, compare the `certutil -hashfile ... SHA256` output with the .sha256sum file, extract and put hubble.exe on PATH.

## Reach the API
Use the Cilium CLI port-forward (`cilium hubble port-forward`), then `hubble status -P` should print `Healthcheck (via 127.0.0.1:4245): Ok`, flow counts and connected nodes. `hubble observe -P` lists flows.

If you port-forward to a port other than 4245, set `--server` or env `HUBBLE_SERVER` (default `localhost:4245`). With TLS enabled you need extra flags for the API. See `hubble help status`, `hubble help observe` and `hubble config`.

## Checked

2026-11-03. Claims were read against: https://docs.cilium.io/en/stable/observability/hubble/setup/. 

Method: documentation only; no commands were run.
