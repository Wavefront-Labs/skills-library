---
id: computing-software.cloud-infrastructure-engineering.garage.k2v-api-enablement
name: k2v-api-enablement
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [k2v, k2v-api, k2v-client, small-values]
level: advanced
status: docs-checked
description: "Turn on the optional K2V key-value API with a k2v feature build and a [k2v_api] section."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/k2v/
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
K2V (since v0.7.2) is an optional alternative storage API for efficiently storing many small values in buckets, whereas S3 targets large blobs. Release builds include it from v0.8.0; earlier versions had separate builds whose tag ended in `-k2v`. When compiling yourself, enable the Cargo feature `k2v`.

Enable it by adding to the configuration:

```
[k2v_api]
api_bind_addr = "<ip>:<port>"
```

Choose a port not used by the S3 API, the admin API or the RPC server.

Authentication uses AWS v4 signatures like S3, and the region for signatures is always the one set for the S3 API in the config.

Tooling: an early-stage Rust client library (`k2v-client`, from the Garage git repository in `Cargo.toml`) and a CLI built with `cargo build --features cli --bin k2v-cli` inside `garage/src/k2v-client`; `k2v-cli --help` documents it.

With the LMDB database engine, K2V sort keys are limited to 479 bytes (the configuration page ties this to the 511 byte LMDB key limit).

Precompiled builds of older versions with k2v are on the download page under Extra builds, and the page links the K2V specification, which also contains a high-level overview of the design.

## Checked

2026-11-04. Read the K2V and Configuration file format pages in full. Confirmed the version history, the feature flag, the [k2v_api] section, the signature rule, the client library and CLI build lines and the LMDB key limit. Reworded the limit to apply to LMDB only.
Method: documentation only; no commands were run.
