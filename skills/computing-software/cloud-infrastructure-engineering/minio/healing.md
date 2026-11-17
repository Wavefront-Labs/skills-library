---
id: computing-software.cloud-infrastructure-engineering.minio.healing
name: healing
category: computing-software
field: cloud-infrastructure-engineering
product: minio
tags: [minio, healing, object-healing, bit-rot, get-heal, mc-admin-heal, parity-shard, heal-metrics]
level: practitioner
status: docs-checked
description: "Know when MinIO heals damaged objects: on GET and HEAD, via the scanner at one in 1024 objects per pass, and by manual mc admin heal, with bit rot check caveats."
sources: ["https://github.com/minio/docs/blob/main/source/operations/concepts/healing.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MinIO object healing

Healing restores an object that is damaged, corrupted or partially lost, for example through drive errors, OS or filesystem failure, or bit rot. Success depends on the erasure set size, how many drives still hold intact shards, and the parity setting. The number of drives with intact shards must be at least the number of data shards (example: with 5 data and 3 parity on 8 drives, five intact drives must be online).

## When healing runs
1. **On read.** Every `GET` or `HEAD` checks the object's data shards. If all are intact MinIO serves them without looking at parity. If any are missing or damaged, MinIO uses parity shards to heal before serving. Each lost data shard needs an intact parity shard. Missing parity shards are restored too, if enough others remain. For versioned buckets the check also happens on `PUT`.
2. **Through the scanner.** On each scan pass a hash of the object name selects one in every 1,024 objects; objects found with lost shards are healed. By default the scanner does **not** check for bit rot because that is expensive and multi-disk bit rot risk is low.
3. **Manually.** `mc admin heal` starts a full-system heal. The docs call it very resource intensive, rarely needed, and advise consulting MinIO engineers first.

## Monitoring
Healing metrics are documented under the v2 metrics reference; see `computing-software.cloud-infrastructure-engineering.minio.prometheus-metrics`.

Related: `computing-software.cloud-infrastructure-engineering.minio.scanner`, `computing-software.cloud-infrastructure-engineering.minio.erasure-coding`.

## Checked
2026-11-03. Confirmed against the MinIO docs source: Object Healing page (healing.rst). Removed: nothing; every claim was confirmed.
Method: documentation only; no commands were run.
