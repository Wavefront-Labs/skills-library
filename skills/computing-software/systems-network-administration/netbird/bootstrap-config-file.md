---
id: computing-software.systems-network-administration.netbird.bootstrap-config-file
name: bootstrap-config-file
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, default-json, bootstrap, unattended-deployment, kubernetes-init-container]
level: advanced
status: docs-checked
description: "Pre-seed NetBird client config in default.json for unattended deployment: file location, object-typed URLs, setup key handling, Docker and Kubernetes pitfalls."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/peers/bootstrap-via-config-file.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Config file: `/var/lib/netbird/default.json` on Linux and macOS, inside the `netbird-client` volume on Docker (mounted at `/var/lib/netbird/`).

Rules:
- `ManagementURL` and `AdminURL` are objects with `Scheme` and `Host`, not strings; strings stop the daemon from starting.
- Other keys: `WgIface` (default `wt0`), `IFaceBlackList`, `BlockInbound`, `BlockLANAccess`, `RosenpassEnabled`.
- Leave `PrivateKey` empty so each peer generates its own. `PreSharedKey` optional.
- A wrong JSON type in any field fails the whole file. Build the template by bootstrapping one peer on the exact version you will deploy, then clear `PrivateKey`.
- Never store the setup key in the file: use `NB_SETUP_KEY`, `--setup-key` or `--setup-key-file`.

Docker: mount the directory, not the single file. The daemon rewrites `default.json` and creates `active_profile.json`; a single-file bind mount fails with "device or resource busy", even with `:ro`.

Kubernetes: ConfigMaps are read-only, so use an init container to copy the file into an `emptyDir` mounted at `/var/lib/netbird`; take the key from a Secret and enable ephemeral peers on the setup key.

Never copy `default.json` between machines: it holds the private key and a cloned identity cannot coexist with the original. Re-register with a setup key.

Use setup keys only for unattended workloads; enrol people through SSO.

## Checked

2026-11-04: read the bootstrap-via-config-file page in full. Confirmed the file location, object-typed URLs, key list and defaults, setup-key handling, the Docker single-file mount failure (also with `:ro`), the Kubernetes init-container pattern and the cloned-identity warning. Nothing removed.

Method: documentation only; no commands were run.
