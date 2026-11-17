---
id: computing-software.networking-hardware-and-wireless.kea.dhcp4-lease-storage-memfile
name: dhcp4-lease-storage-memfile
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, kea-dhcp4, memfile, lease-database, csv, persist]
level: practitioner
status: docs-checked
description: "Configure the memfile CSV lease backend for kea-dhcp4: persist, file name, and why periodic lease file cleanup is needed."
sources:
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DHCPv4 memfile lease storage
Smaller deployments store leases in a CSV file, avoiding a database dependency. Configure under `Dhcp4/lease-database`; `type` must be "memfile".

- `persist`: whether new and updated leases are written to the file. Default true. The docs strongly recommend true in normal operation; with false, a restarted server forgets assigned addresses and may hand out ones in use. False is mostly for performance tests.
- `name`: lease file; default `[kea-install-dir]/var/lib/kea/kea-leases4.csv`.
- Since Kea 2.7.9, lease files may only be loaded from the data directory.

Why cleanup matters: updates are appended, not rewritten, and the latest entry per client is the valid one on load. Many entries bloat the file and slow startup and reconfiguration. Lease file cleanup (LFC) keeps only the latest entry per client; set `lfc-interval` according to renewal frequency (more renewals, smaller interval). A too-short interval can start a new cleanup while the last still runs.

## Checked

2026-11-08. Read dhcp4-srv.rst (Kea ARM source, master branch) sections Memfile - Basic Storage for Leases and Why Is Lease File Cleanup Necessary in full. Confirmed persist, name default, the Kea 2.7.9 data-directory rule, append-only file and LFC behaviour. Nothing removed.

Method: documentation only; no commands were run.
