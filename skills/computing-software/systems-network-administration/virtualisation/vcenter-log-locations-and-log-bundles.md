---
id: computing-software.systems-network-administration.virtualisation.vcenter-log-locations-and-log-bundles
name: vcenter-log-locations-and-log-bundles
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vcenter-logs, vsphere-monitoring, vsphere-troubleshooting, vpxd, support-bundle, vcsa, vmware, vsphere]
level: practitioner
status: docs-checked
description: "Find the right vCenter Server Appliance log for each symptom (vpxd, sso, vsphere-ui, vmon, vLCM, vAPI), forward them via syslog, and generate a VCSA log bundle."
sources:
  - https://knowledge.broadcom.com/external/article/312194/location-of-vcenter-server-log-files.html
  - https://knowledge.broadcom.com/external/article?legacyId=2109887
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# vCenter (VCSA) logs

All under `/var/log/vmware/<service>/` on the VCSA (Windows vCenter is gone since 6.7).

## Which log for which symptom
| Symptom | Log |
|---|---|
| Tasks fail, host connect/disconnect, inventory errors | `vpxd.log` — the main vCenter log (client connections, tasks and events, vpxa communication); rotated to numbered component-nnn logs |
| Login failures, SSO, identity sources, tokens | SSO/identity service logs |
| vSphere Client UI errors, blank pages | `vsphere-ui` service logs |
| Service won't start | `vmon` service logs, then the service's own log |
| Lifecycle Manager / patch sync | `vmware-updatemgr` service logs |
| REST/vAPI calls (automation) | vAPI endpoint service logs |
| Certificates | certificate-management service logs |
| VAMI, appliance patching | `applmgmt` service logs |
| Postgres DB | vpostgres database logs |
| Content library | content-library service logs |
| Events/alarms | in vpxd.log plus DB (Monitor → Events) |

Search tip: tasks have an **opID**; copy it from the error and grep across logs:
```sh
grep -r "opID=abc123" /var/log/vmware/vpxd/ | head
```

## Log bundle
- vSphere Client: select vCenter → Actions → Export System Logs (include or exclude host logs).
- VAMI: `https://vc:5480` → Actions → Create Support Bundle.
- Generate logs from the vSphere Client (Home > Administration > System Logs) or the VAMI.
Upload to Broadcom with the SR number.

## Syslog forwarding
VAMI → Syslog → remote targets (UDP/TCP/TLS). Forward to the SIEM for audit
(`sso` and `vpxd` events) and retention beyond local rotation.

## Gotchas
- `/storage/log` full stops services; see VCSA disk-full handling.
- Timestamps are UTC; correlate with ESXi logs (also UTC).
- Raised debug log levels fill the disk fast; revert after capture.

## Verify
For the incident, you can name the opID, the service, and the log line with the root error;
syslog target receives a test login event within a minute.

## Checked
2026-10-31: Confirmed `/var/log/vmware/<service>/` as the VCSA log root, `vpxd.log` as the
main vCenter log, numbered rotation and the vSphere Client log export path against
Broadcom KB 312194; the service names against the vCenter services KB 344633
(legacyId 2109887). Replaced the unconfirmed per-service file names with service-level
pointers, and removed the vc-support script path, the 3-target syslog limit and the
config.log.level trivia value.
Method: documentation only; no commands were run.
