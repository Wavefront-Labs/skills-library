---
id: computing-software.cloud-infrastructure-engineering.garage.lmdb-map-size-limit
name: lmdb-map-size-limit
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [lmdb-map-size, metadata-size-limit, virtual-memory, 32-bit]
level: advanced
status: docs-checked
description: "Raise or inspect lmdb_map_size, the ceiling on how large the LMDB metadata database can grow."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`lmdb_map_size` sets the size of the virtual memory region LMDB uses to map the database file. In practice it is the maximum size the metadata database can reach. It is not bound by the machine's physical RAM.

If you leave it out, Garage defaults to 1GiB on 32-bit machines and 1TiB on 64-bit machines. The full example in the page writes it as `lmdb_map_size = "1T"`.

The configuration page's LMDB engine notes add two relevant constraints:

- LMDB can technically be used on 32-bit systems, but this limits a node to very small databases, so it is not recommended.
- LMDB keys are limited to 511 bytes, which gives a 479-byte limit on S3 object keys and K2V sort keys.

Remember that metadata snapshots need up to four times the database size, so a larger database also demands more room in `metadata_snapshots_dir`.

## Checked

2026-11-04. Read the Configuration file format page in full. Confirmed the meaning of lmdb_map_size, the 1GiB and 1TiB defaults, the example value, the 32-bit remark, the 511 and 479 byte key limits and the four-times snapshot space. Removed the advice paragraph on when to raise the value and the claim that the setting applies only with the lmdb engine, neither of which the page states.
Method: documentation only; no commands were run.
