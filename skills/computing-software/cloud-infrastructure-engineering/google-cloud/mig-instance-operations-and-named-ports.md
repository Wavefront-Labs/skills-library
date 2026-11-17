---
id: computing-software.cloud-infrastructure-engineering.google-cloud.mig-instance-operations-and-named-ports
name: mig-instance-operations-and-named-ports
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, managed-instance-groups, abandon-instances, recreate-instances, mig-resize, named-ports, resize-requests, load-balancing]
level: practitioner
status: docs-checked
description: "Day-2 MIG operations: resize, recreate, delete or abandon specific VMs for debugging, resize requests, and named ports that wire MIGs to load balancer backends."
sources: ["https://cloud.google.com/compute/docs/instance-groups/working-with-managed-instances", "https://cloud.google.com/compute/docs/instance-groups/creating-groups-of-managed-instances#assign_named_ports", "https://cloud.google.com/compute/docs/instance-groups/about-resize-requests-mig", "https://cloud.google.com/sdk/gcloud/reference/compute/instance-groups/managed"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MIG instance operations and named ports

## 1. Resize
```bash
M="--region=europe-west2"     # or --zone for zonal MIGs
gcloud compute instance-groups managed resize web-mig $M --size=12
```
With an autoscaler attached, the autoscaler controls the group size — change
`--min-num-replicas` instead. For Flex-start or reservation-bound VMs, use a **resize request**
(`--requested-run-duration` must be between 10 minutes and seven days):
```bash
gcloud compute instance-groups managed resize-requests create web-mig --resize-request=train-8 \
  --resize-by=8 --zone=<Z> --requested-run-duration=24h
```

## 2. Fix or inspect one VM
| Need | Command | Effect |
|---|---|---|
| Rebuild a sick VM from the template | `recreate-instances web-mig $M --instances=web-mig-x1z9` | VM is recreated from the group's template |
| Remove one and shrink | `delete-instances web-mig $M --instances=...` | target size −1 |
| Pull a VM out for forensics | `abandon-instances web-mig $M --instances=...` | VM is not rebooted or deleted, target and current size drop by 1 |
| Apply pending template now | `update-instances web-mig $M --instances=... --minimal-action=replace` | targeted rollout |
After abandoning, the VM still exists and bills; delete it after the investigation.

## 3. Named ports
Backend services refer to a **port name**, not a number; the instance group maps it.
```bash
gcloud compute instance-groups set-named-ports web-mig $M --named-ports=http:8080,admin:9090
gcloud compute backend-services update web-bes --global --port-name=http
gcloud compute instance-groups get-named-ports web-mig $M
```
`set-named-ports` **replaces** the whole list — always pass every pair.

## Gotchas
- A VM you stop by hand in a MIG might be recreated; abandon it, or remove autohealing (`gcloud compute instance-groups managed update --clear-autohealing`), to debug.
- In a stateful MIG, preserved items (instance names, disks, metadata, IPs) persist when the MIG recreates a VM.
- A port name that the backend service uses but the instance group does not define leaves the backends without a usable port; check `get-named-ports` first.
- Resize requests schedule Flex-start VM creation on a best-effort basis based on availability.

## Verify
- [ ] `gcloud compute instance-groups managed describe web-mig $M --format='value(targetSize,status.isStable)'` matches expectation.
- [ ] `gcloud compute backend-services get-health web-bes --global` shows HEALTHY on the named port.

## Checked

Checked 2026-10-27 against Working with managed instances, About resize requests, and the gcloud reference for resize-requests create, set-named-ports, abandon-instances, delete-instances, recreate-instances and managed update. Fixed: resize requests are for Flex-start or reservation-bound VMs with a run duration of 10 minutes to seven days and also accept --region, abandon does not reboot or delete the VM, and --clear-autohealing is the flag that removes autohealing. Removed the unconfirmed all-or-nothing and zonal-only claims.

Method: documentation only; no commands were run.
