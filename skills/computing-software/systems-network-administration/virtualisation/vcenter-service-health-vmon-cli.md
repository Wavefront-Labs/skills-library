---
id: computing-software.systems-network-administration.virtualisation.vcenter-service-health-vmon-cli
name: vcenter-service-health-vmon-cli
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vmon-cli, service-control, vcsa, vpxd, vcenter-services, storage-log-full, vdt, vsphere-troubleshooting, vmware, vcenter]
level: practitioner
status: docs-checked
description: "Troubleshoot vCenter appliance services: service-control and vmon-cli, partition-full causes, vpxd startup failures, VDT checks and safe restarts."
sources:
  - https://knowledge.broadcom.com/external/article?legacyId=2109887
  - https://knowledge.broadcom.com/external/article?legacyId=90561
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vCenter service health with service-control and vmon-cli

**Goal:** bring a misbehaving VCSA back (UI errors, "no healthy upstream", vpxd down)
by fixing the actual cause, not rebooting blindly.

## Inspect services
```sh
service-control --status --all            # running vs stopped
vmon-cli --list ; vmon-cli --status vpxd  # vMon-managed services, last failure reason
service-control --start --all             # start whatever should run
service-control --stop vsphere-ui && service-control --start vsphere-ui
```
"no healthy upstream" in the browser = envoy proxy cannot reach the UI or vpxd service:
check `vsphere-ui` and `vpxd` status.

## Common causes
| Symptom | Check |
|---|---|
| Services won't start | `df -h`: `/storage/log`, `/storage/db`, `/storage/seat` (stats/events), `/` full |
| vpxd crashes at start | `/var/log/vmware/vpxd/vpxd.log` last lines; DB issues; certificate errors |
| Login fails for all | STS certificate expired, time skew, identity source unreachable |
| UI slow | Memory pressure (`top`), oversized stats retention, many plug-ins |

Partition full fixes: purge old logs/support bundles in `/storage/log`; for
`/storage/seat` reduce event/task retention or clean via the KB procedure; grow disks
(edit VMDK, then `/usr/lib/applmgmt/support/scripts/autogrow.sh`).

## Certificate pre-checks
Expired STS signing or machine SSL certificates are a classic cause of vpxd startup and
login failures; run the certificate-management checks from the KB workflow before any
deeper fix and before upgrades.

## Gotchas
- Restarting all services takes 10+ minutes; HA and running VMs are unaffected but
  backups, DRS and provisioning pause.
- Root password expired: SSH logs in to a forced-change prompt; service accounts and
  scripts fail. Set password expiry consciously (`chage -l root`).
- Snapshot the VCSA before deeper fixes (DB edits are support-led only).

## Verify
`service-control --status` shows all expected services running; the UI loads; VAMI health
is green.

## Checked
2026-10-31: Confirmed service-control --list/--status --all/--start/--stop syntax and the
VAMI at https://<vCenter>:5480 Services page against Broadcom KB 344633 (legacyId 2109887);
the STS/machine SSL certificate replacement workflow and the ELM offline-snapshot rule
against Broadcom KB 322249 (legacyId 90561). Replaced the unconfirmed VDT tool paragraph
with the documented certificate pre-check workflow.
Method: documentation only; no commands were run.
