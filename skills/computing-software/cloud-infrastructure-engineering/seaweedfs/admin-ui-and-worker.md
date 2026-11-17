---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.admin-ui-and-worker
name: admin-ui-and-worker
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [weed-admin, weed-worker, plugin-worker, job-types]
level: practitioner
status: docs-checked
description: "Start the SeaweedFS Admin UI and maintenance workers: weed admin options, auth and binding rules, worker flags and job types."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/Admin-UI
  - https://github.com/seaweedfs/seaweedfs/wiki/Worker
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# admin ui and worker

```bash
weed admin -master=localhost:9333 -dataDir=/path/to/admin -adminUser=admin -adminPassword=change-me
weed worker -admin=localhost:12535 -jobType=all -workingDir=/path/to/worker
```
`weed admin` options: `-port` (default 12535), `-ip` (default 127.0.0.1), `-port.grpc` (port + 10000, for workers), `-master`, `-filerGroup`, `-dataDir`, `-adminUser`, `-adminPassword` (empty means auth disabled), `-readOnlyUser` / `-readOnlyPassword`, `-urlPrefix`, `-iceberg.port` (8181), `-lance.port` (9101), `-metricsPort`.

Networking: the default bind is loopback; it auto-upgrades to 0.0.0.0 when `-adminPassword` or admin mTLS is configured. `-allowInsecureBind` allows a non-loopback bind without either (unsafe). Port moved from 23646 to 12535 in 4.49; `-port.legacy` keeps the old one for compatibility. OIDC login for the admin UI is Enterprise only.

It auto-discovers filers from the masters and offers topology, volumes, file browser, metrics, S3 user management and the `/plugin` job settings.

Worker: connects over a bidirectional gRPC stream; types `vacuum`, `volume_balance`, `admin_script`, `erasure_coding`, `iceberg_maintenance`. Flags: `-id`, `-jobType` (default all), `-heartbeat` 15s, `-reconnect` 5s, `-maxDetect` 1, `-maxExecute` 4.

Verify: open http://localhost:12535 and see the worker registered.

## Checked

Method: docs-checked 2026-11-09 against the SeaweedFS wiki pages Admin UI and Worker (raw markdown, both read in full).
