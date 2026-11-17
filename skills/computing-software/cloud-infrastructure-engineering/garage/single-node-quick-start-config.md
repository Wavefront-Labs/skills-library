---
id: computing-software.cloud-infrastructure-engineering.garage.single-node-quick-start-config
name: single-node-quick-start-config
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [quick-start, single-node, garage-toml, rpc-secret]
level: intro
status: docs-checked
description: "Write a minimal garage.toml for a one-node test Garage and point the CLI at it with GARAGE_CONFIG_FILE."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/quick-start/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Quick Start builds the simplest deployment: one node, no redundancy, explicitly not for production. The generated garage.toml sets `metadata_dir = "/tmp/meta"`, `data_dir = "/tmp/data"`, `db_engine = "sqlite"`, `replication_factor = 1`, `rpc_bind_addr = "[::]:3901"`, `rpc_public_addr = "127.0.0.1:3901"` and an `rpc_secret` made with `openssl rand -hex 32`.

Three sections follow. `[s3_api]` uses `s3_region = "garage"`, `api_bind_addr = "[::]:3900"` and `root_domain = ".s3.garage.localhost"`. `[s3_web]` uses `bind_addr = "[::]:3902"`, `root_domain = ".web.garage.localhost"` and `index = "index.html"`. `[admin]` uses `api_bind_addr = "[::]:3903"` plus an `admin_token` and a `metrics_token`, each from `openssl rand -base64 32`.

By default Garage reads `/etc/garage.toml`. When the file lives elsewhere, run `export GARAGE_CONFIG_FILE=$(pwd)/garage.toml`.

The guide warns that `/tmp` is erased on reboot, so data on this server is not persistent; move both directories to local disk if you want persistence. The `rpc_secret` is a 32-byte hex string, and in a multi-node cluster every node must use the same value.

Check the node with `garage status`, which lists ID, hostname, address, tags, zone, capacity, free data space and version for healthy nodes.

From v2.3.0, `garage server --single-node --default-bucket` configures a one-node cluster and a default key and bucket automatically, using `GARAGE_DEFAULT_ACCESS_KEY`, `GARAGE_DEFAULT_SECRET_KEY` and `GARAGE_DEFAULT_BUCKET`; older versions need the manual layout steps.

## Checked

2026-11-07. Read in full (stripped page text, including the inline code blocks; no linked include files were opened): Quick Start. Confirmed on the Quick Start: every value of the generated `garage.toml`, `GARAGE_CONFIG_FILE`, the `/tmp` warning, the shared-secret note, and the `garage status` output. Added: the `--single-node` and `--default-bucket` flags and the v2.3.0 boundary.

Method: documentation only; no commands were run.
