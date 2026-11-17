---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.volume-ttl-expiring-files
name: volume-ttl-expiring-files
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [expire, assign, ttl, expiry, volume-ttl]
level: practitioner
status: docs-checked
description: "Store files with a TTL: assign with ttl=, upload with ttl=, TTL units, volume vs file TTL, and how expired volumes are reclaimed cheaply."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/Store-file-with-a-Time-To-Live
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# volume ttl expiring files

```bash
curl "http://localhost:9333/dir/assign?ttl=3m"
curl -F "file=@x.go" "http://127.0.0.1:8080/5,01637037d6?ttl=3m"
```
Units: m, h, d, w, M, y (e.g. 3m, 4h, 5d, 6w, 7M, 8y).

Reads before expiry work as normal; afterwards the file returns 404.

Two TTLs: the one on assign picks a volume with a matching TTL; the one on upload is stored with the file. They need not match as long as the volume TTL is larger than the file TTL. This lets you keep few volume TTL variants.

Design: TTL is attached to the volume as well as each file. Volumes are checked periodically (every 5-10 seconds by default). Volume servers track each volume's largest expiration time and stop reporting expired volumes to the master; the master then treats them as dead and stops assigning writes to them, and after about 10% of the TTL time (at most 10 minutes) the volume server deletes the expired volume, so space is reclaimed by dropping whole volumes. Writes with ttl=3m reuse the same TTL volumes until they are full (new ones are created) or there is no write activity for 3 minutes (then they are stopped and deleted).

Deployment: TTL volumes can grow to the maximum volume size (default 30GB, set at the cluster level), so reduce it when disk space is tight. The page recommends not mixing TTL and non-TTL volumes in one cluster.

S3: TTL can also be set via LifecycleConfiguration.

Verify: read the fid after the TTL elapses and expect an HTTP not found response.

## Checked

2026-11-08. Confirmed against the Store file with a Time To Live wiki page. Removed the filer `?ttl=1d` and `fs.configure` per-path TTL claims, which the page does not state; added the deletion timing, deployment advice and S3 lifecycle note.

Method: documentation only; no commands were run.
