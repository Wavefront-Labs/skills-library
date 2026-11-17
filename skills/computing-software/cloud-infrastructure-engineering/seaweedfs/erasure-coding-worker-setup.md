---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.erasure-coding-worker-setup
name: erasure-coding-worker-setup
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [warm-storage, reed-solomon-10-4, worker, erasure-coding, reed-solomon, ec-shards]
level: advanced
status: docs-checked
description: "Seal warm volumes into RS(10,4) erasure coding with the erasure_coding plugin worker: benefits, limits and how to start admin plus worker."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/Erasure-Coding-for-warm-storage
  - https://github.com/seaweedfs/seaweedfs/wiki/Volume-Management
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# erasure coding worker setup

Open source SeaweedFS uses Reed-Solomon 10+4 (custom ratios are Enterprise). A 30GB volume becomes 14 shards; up to 4 can be lost at about 1.4x storage, versus 5x replication for similar safety. Shards are placed rack-aware and disk-aware, and there is no minimum server count.

Enable it with the `erasure_coding` plugin worker:
```bash
weed admin -master=localhost:9333
weed worker -admin=localhost:12535
```
(`ec.encode` in the old maintenance script is replaced by this worker.)

Layout: 1GB blocks, with 1MB blocks for volumes under 10GB and edge cases, so most small-file reads cost one disk read. The volume server loads no index into memory, giving fast startup.

Downsides:
- Reading missing shards is slower; rebuilding one moves the whole volume's data.
- Deletion is supported, updates are not.
- Compaction needs conversion back to a normal volume first.

Shell tools: `ec.balance`, `ec.rebuild`, `ec.decode`, `ec.scrub`.

Verify: after the job runs, the volume shows as EC shards in the Admin UI or volume listing.

## Checked

Method: docs-checked 2026-11-09 against the SeaweedFS wiki pages Erasure Coding for warm storage (read in full) and Volume Management (first 48 lines read).
