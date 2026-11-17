---
id: computing-software.systems-network-administration.virtualisation.proxmox-ceph-major-upgrade
name: proxmox-ceph-major-upgrade
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [ceph-upgrade, pveceph, ceph, pve-upgrade, rolling-upgrade, noout, proxmox]
level: advanced
status: docs-checked
description: "Upgrade Ceph on Proxmox VE 8 from Reef to Squid: repository switch, noout, restart order for mon, mgr, OSD and CephFS MDS, require-osd-release and known issues."
sources:
  - https://pve.proxmox.com/wiki/Ceph_Reef_to_Squid
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ceph major upgrade on Proxmox VE (Reef to Squid)

Proxmox publishes one wiki page per hop (the Reef to Squid page lists "Ceph Quincy to Reef"
and "Ceph Pacific to Quincy" under See Also); follow the page for your hop. This skill
follows Reef (18.2+) to Squid (19.2+) on Proxmox VE 8. Read the upstream Ceph release notes first.

## Assumptions
- All nodes on the latest Proxmox VE 8.2 or higher, with pve-manager 8.2.8 or newer and
  Ceph packages 18.2.4-pve3 or newer. Check with `pveversion --verbose`.
- The cluster is healthy and working.
- Quincy (17.2+) to Squid directly is possible, but Proxmox primarily tests and recommends
  going to Reef first. If you skip, test on a non-production setup, and make sure no
  FileStore based OSD is left (FileStore support was removed in Ceph 18.2 Reef).
- Commands starting with `ceph` need to run only once, on any node of the Ceph cluster.

## Steps
1. On each node change the repository (the page uses sed):
   ```sh
   sed -i 's/reef/squid/' /etc/apt/sources.list.d/ceph.list
   ```
   Enterprise: `deb https://enterprise.proxmox.com/debian/ceph-squid bookworm enterprise`.
   Without a subscription: `deb http://download.proxmox.com/debian/ceph-squid bookworm no-subscription`.
2. Optional but recommended: `ceph osd set noout` (or the OSD tab, Manage Global Flags).
3. On each node: `apt update` then `apt full-upgrade` (or install updates in the GUI). The
   daemons keep running the old Reef binaries until restarted. If the enterprise repository
   gives 401 Unauthorized, check pve-manager is 8.2.8 or newer, run
   `pvesubscription update --force` and retry.
4. Restart monitors one node at a time: `systemctl restart ceph-mon.target`. Wait and check
   `ceph -s` shows HEALTH_OK or HEALTH_WARN with only "noout flag(s) set". When all are up,
   `ceph mon dump | grep min_mon_release` should report `min_mon_release 19 (squid)`.
5. Restart managers on all nodes if they did not restart with the monitors:
   `systemctl restart ceph-mgr.target`, then confirm with `ceph -s`. The page notes
   managers can become unresponsive after the first monitor restart; carry on with the
   monitors, then restart the managers.
6. Restart OSDs one node at a time (to avoid losing data redundancy):
   `systemctl restart ceph-osd.target`, checking `ceph status` between nodes. Afterwards the
   warning "all OSDs are running squid or later but require_osd_release < squid" can appear.
7. Once every OSD reports a Ceph 19.2 version: `ceph osd require-osd-release squid`.
8. CephFS, for each file system (`ceph fs ls`): note and disable standby-replay
   (`ceph fs set <fs_name> allow_standby_replay false`); if more than one MDS, note
   `max_mds` and set it to 1 and wait for non-zero ranks to go away; stop standby MDS
   daemons with `systemctl stop ceph-mds.target`; confirm one MDS on rank 0 with
   `ceph status`; restart the remaining MDS with `systemctl restart ceph-mds.target`; start
   the standbys with `systemctl start ceph-mds.target`; restore `max_mds` and
   `allow_standby_replay` to the noted values.
9. `ceph osd unset noout` (or the OSD tab, Manage Global Flags).

## Known issue named on the page
iSCSI users: upstream Ceph hit a bug upgrading from 19.1.1 to 19.2.0 (tracker issue
68215); read it before upgrading to 19.2.0.

## Verify
`ceph -s` shows HEALTH_OK, `ceph mon dump | grep min_mon_release` reports squid, and the
require_osd_release warning is gone.

## Checked
Date: 2026-11-07. Read the whole Proxmox wiki page "Ceph Reef to Squid" (revision shown
as oldid 12611). Every command and version above is on it. Removed as not on the page:
the claim that Ceph supports upgrading only one or two releases, `ceph versions`,
`ceph mon stat`, `ceph osd ok-to-stop`, the PGs active+clean pre-flight, the claims that
skipping require-osd-release breaks later upgrades and that all-OSD restarts pause I/O,
the librbd client-restart gotcha and the `ceph osd dump` verify. The
`pve-docs/chapter-pveceph.html` source was dropped because it was not used. The telemetry
section of the page was left out as optional.
Method: documentation only; no commands were run.
