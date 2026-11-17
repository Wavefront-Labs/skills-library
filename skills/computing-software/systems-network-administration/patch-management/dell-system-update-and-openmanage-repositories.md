---
id: computing-software.systems-network-administration.patch-management.dell-system-update-and-openmanage-repositories
name: dell-system-update-and-openmanage-repositories
category: computing-software
field: systems-network-administration
product: patch-management
tags: [dell-system-update, openmanage, firmware-updates, idrac, bios-update, repository-manager]
level: practitioner
status: draft
description: "Update Dell PowerEdge firmware and drivers with Dell System Update, iDRAC repository updates and OpenManage Enterprise catalogs, with staging, reboot handling and verification."
sources:
  - https://www.dell.com/support/kbdoc/en-us/000130590/dell-emc-system-update-dsu
  - https://www.dell.com/support/manuals/en-us/dell-openmanage-enterprise/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dell firmware: DSU, iDRAC and OpenManage Enterprise

## Methods
| Tool | Where it runs | Best for |
|---|---|---|
| **Dell System Update (DSU)** | in the host OS (Linux/Windows) | per-server or scripted updates incl. drivers |
| **iDRAC "Update from repository"** | out of band | OS-agnostic, hypervisors, staged until reboot |
| **OpenManage Enterprise (OME)** | central appliance | fleet baselines, compliance reports, scheduled jobs |
| Repository Manager | admin PC | build custom catalogs/repos for air-gapped sites |
| vLCM HSM (OMEVV) | vCenter | ESXi clusters (see vLCM hardware support managers) |

## DSU (in OS)
```sh
dsu --inventory                    # what's installed
dsu --preview                      # what would update from the default catalog
dsu --non-interactive --apply-upgrades --reboot=no
dsu --source-type=REPOSITORY --source-location=http://repo.corp.example/dell --non-interactive
```
Exit codes tell you if a reboot is required (check documentation for the code list) so
orchestration can schedule it.

## iDRAC repository update
iDRAC → Maintenance → System Update → Network share/HTTP(S) → catalog `Catalog.xml`.
Scripted via racadm:
```sh
racadm -r idrac01 -u admin -p '...' update -f Catalog.xml -l http://repo.corp.example/dell -t HTTP -a FALSE
racadm -r idrac01 jobqueue view
```
`-a FALSE` stages updates; they apply at next reboot (fits patch-window reboots).

## OME baselines
Create a catalog (online Dell catalog or Repository Manager share), a **baseline** for a
device group, run compliance, then an update job with "stage for next reboot" or immediate.
Export the compliance report for audit.

## Order and gotchas
- Typical order: iDRAC → BIOS → storage controller (PERC) → NIC → drives → others; DSU/OME
  handle dependencies, manual updates must follow the release notes.
- PERC and drive firmware can need a full power cycle.
- Clustered hosts: one node at a time, workloads drained first.
- Check release notes for "Urgent" criticality (security or data integrity).

## Verify
OME compliance shows baseline compliant; `racadm swinventory` or DSU inventory shows target
versions; hardware logs (Lifecycle Log) list successful update jobs.
