---
id: computing-software.systems-network-administration.patch-management.planning-migrations-off-eol-operating-systems
name: planning-migrations-off-eol-operating-systems
category: computing-software
field: systems-network-administration
product: patch-management
tags: [eol-migration, end-of-life, in-place-upgrade, leapp, do-release-upgrade, os-migration, eol-software]
level: practitioner
status: docs-checked
description: "Plan OS migrations off end-of-life releases: Windows Server in-place upgrade prerequisites, Ubuntu do-release-upgrade path rules, RHEL 8 to 9 Leapp scope, and rebuild vs upgrade."
sources:
  - https://learn.microsoft.com/en-us/windows-server/get-started/perform-in-place-upgrade
  - https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/upgrading_from_rhel_8_to_rhel_9/index
  - https://documentation.ubuntu.com/server/how-to/software/upgrade-your-release/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Planning OS migrations off EOL

**Goal:** no production system running an unsupported OS on the EOL date. Dates and schedule are yours to set; this skill records what the vendor pages say about each upgrade route.

## 1. Inventory and size the problem
Count systems per OS version against each vendor's published lifecycle page; attach app, owner, criticality and dependencies from your own records.

## 2. Choose rebuild or in-place per system
| Path | When |
|---|---|
| Rebuild on new OS and migrate app and data | Required for some roles (see Windows Server below); also the route when automation already builds the server |
| In-place upgrade | Apps that are hard to reinstall; follow the vendor's supported paths |
| Replace or retire | App is commodity or low usage |

## 3. Vendor in-place routes

### Windows Server
- Setup from installation media keeps settings, roles and data. The page's example: Windows Server 2012 R2 to Windows Server 2025. Check the "Supported in-place upgrade paths by version" page for the exact path.
- Prerequisites: full backup with a tested restore, a maintenance window (downtime is required), hardware that meets the target requirements, vendor support for your apps and roles, a valid product key and activation method, and a server that is not clustered (use Cluster-Aware Updating or a cluster OS rolling upgrade for clusters).
- Do not use in-place upgrade for Active Directory Domain Services servers: promote new domain controllers on a clean install and demote the old ones.
- Windows Update route to Windows Server 2025 or later: source servers must be Windows Server 2019 or 2022 with the required cumulative update (the page names KB5078766 for 2022 and KB5078752 for 2019, both 2026-03 or later), and the registry value `AllowWindowsServerFeatureUpdate` (DWORD 1) under `HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AllowWindowsServerFeatureUpdate` enables the offer. Server Core can use SConfig option 6.
- Shut down or migrate VMs running on the server before the upgrade. Check the Setup logs in `%SystemRoot%\Panther` if it fails; SetupDiag helps analyse them.

### Ubuntu
- Upgrade only from one LTS to the next sequential LTS; skipping releases is not possible, so go in stages. LTS to LTS upgrades are offered after the first point release (for example 20.04.1); `-d` forces it earlier but is not recommended for production.
- Before: read the release notes, `sudo apt update` then `sudo apt dist-upgrade -o APT::Get::Always-Include-Phased-Updates=true` until nothing remains (phased packages can block the upgrade), reboot if `/run/reboot-required` exists, check free disk space, back up, and be available because the process is interactive.
- Run `sudo do-release-upgrade`. Third-party repositories and PPAs are disabled during the upgrade and are the most common cause of problems. Config file prompts default to keeping your version; the system counts as upgraded only after the final reboot.

### RHEL
- Red Hat documents an in-place upgrade from RHEL 8 to RHEL 9 using the Leapp utility, which replaces the existing OS. The index page read here is an abstract only; follow the chapters for preupgrade and upgrade steps.

## 4. Test and execute
App owner test plan per system, pilot wave, tested restore as the rollback path, and update monitoring, backup agents and records after each move.

## Gotchas
- Agents (backup, EDR, monitoring) must support the new OS; check before wave one.
- Licensing changes take procurement lead time.

## Verify
Systems remaining on the EOL OS reach zero, or each remaining one has a documented exception, before the date.

## Checked
Date: 2026-11-07. Read in full: Perform an in-place upgrade of Windows Server (prerequisites, AD DS warning, Windows Update route, registry value, verification) and How to upgrade your Ubuntu release (upgrade paths, pre-upgrade checklist, do-release-upgrade flow). Read the RHEL 8 to 9 index page: it is an abstract only, so only the Leapp in-place scope is confirmed. Removed as unconfirmed: the `endoflife.date` API, the 3/6/12/18-month schedule offsets, `leapp preupgrade`, `leapp upgrade` and the `/var/log/leapp/leapp-report.txt` path, the "one major version per run" Leapp rule, and the claim that Windows Server 2025 upgrades from several prior versions beyond the 2012 R2 example (the page links to a separate paths table that was not read).
Method: documentation only; no commands were run.
