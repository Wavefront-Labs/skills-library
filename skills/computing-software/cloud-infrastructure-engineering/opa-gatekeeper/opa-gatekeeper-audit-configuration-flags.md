---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-audit-configuration-flags
name: opa-gatekeeper-audit-configuration-flags
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, audit, flags, audit-interval, chunk-size, from-cache, ramdisk, violations-limit]
level: advanced
status: docs-checked
description: "Tune Gatekeeper audit with constraint-violations-limit, audit-chunk-size, audit-interval, audit-from-cache and the RAM disk cache option."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/audit.md", "https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/performance-tuning.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper audit configuration flags

Audit settings (controller flags):
- `--constraint-violations-limit=N` (default 20): violations stored per constraint status. It only affects the status model; exporting violations is configured separately and both work at once.
- `--audit-chunk-size=N` (default 500, 0 = unlimited): lists API objects in pages. Smaller values reduce audit pod memory but increase API server requests.
- `--audit-interval=N` (default 60 seconds; 0 disables the interval).
- `--audit-from-cache=true`: audit the informer cache instead of requesting each resource from the API every cycle. Resources must first be replicated into the cache (see the Replicating data section).
- From v3.7.0 audit writes its API server cache to node disk by default to save memory. If high IOPS is a concern, use a tmpfs RAM disk with Helm `--set audit.writeToRAMDisk=true`, or mount an `emptyDir` with `medium: Memory`; this raises the pod memory footprint.

Choose the interval so that no more than one audit runs at a time; overlapping audits raise RAM and CPU use, add API server load, and a newer run can pre-empt the status report of an earlier one, leaving constraints without violation results in status.

## Checked

2026-11-04. Confirmed against audit.md (Configuring Audit) and performance-tuning.md (audit interval overlap). Removed or corrected: nothing.

Method: documentation only; no commands were run.
