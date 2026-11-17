---
id: computing-software.cloud-infrastructure-engineering.garage.rpc-secret-sources
name: rpc-secret-sources
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [rpc-secret, rpc-secret-file, garage-rpc-secret, shared-secret]
level: practitioner
status: docs-checked
description: "Provide the cluster RPC secret via config, file or environment variable."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Garage nodes authenticate each other with a shared secret called the RPC secret: a 32-byte hex-encoded random string, generated for example with `openssl rand -hex 32`. All nodes in a cluster must carry the same one.

Ways to supply it:

- `rpc_secret` in `garage.toml`.
- `rpc_secret_file`, a path to a file holding the secret, available since v0.8.2.
- The `GARAGE_RPC_SECRET` environment variable (since v0.8.2).
- The `GARAGE_RPC_SECRET_FILE` environment variable, since v0.8.5 and v0.9.1.

The environment variables override the corresponding config values.

Garage checks that secret files are not world-readable. If the check wrongly flags a file, for example under POSIX ACLs, set `allow_world_readable_secrets = true` or `GARAGE_ALLOW_WORLD_READABLE_SECRETS=true` to bypass it.

The same pattern of value, `_file` variant and environment variable exists for `admin_token` and `metrics_token`.

## Checked

2026-11-07. Read in full (stripped page text, including the inline code blocks; no linked include files were opened): Configuration file format. Confirmed on the configuration page: 32-byte hex secret, `openssl rand -hex 32`, `rpc_secret_file` and `GARAGE_RPC_SECRET` since v0.8.2, `GARAGE_RPC_SECRET_FILE` since v0.8.5 and v0.9.1, environment override, world-readable check and its bypass, and the same pattern for admin and metrics tokens. Removed: the paragraph about an encryption page and Secret Handshake (that page is not cited and was not read).

Method: documentation only; no commands were run.
