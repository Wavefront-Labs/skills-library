---
id: computing-software.cybersecurity-defensive.nessus.nessus-upgrade-and-migration
name: nessus-upgrade-and-migration
category: computing-software
field: cybersecurity-defensive
product: nessus
tags: [nessus, nessus-upgrade, nessus-manager, migration, tenable-vulnerability-management, nessus-agents, nessus-deployment]
level: practitioner
status: draft
description: "Upgrade Nessus scanners and agents safely, and migrate Nessus Manager agents and scan data to Tenable Vulnerability Management using the migration process."
sources: ["https://docs.tenable.com/nessus/Content/UpgradeNessus.htm", "https://docs.tenable.com/nessus/Content/MigrateToTenableio.htm", "https://docs.tenable.com/nessus-agent/Content/UpdateAgentSoftware.htm"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Nessus upgrades and migration from Nessus Manager

## Upgrading a scanner
1. Check release notes and OS support; back up first:
   `nessuscli backup --create nessus-backup-$(date +%F)` (10.x) or stop service and copy the data dir.
2. Upgrade in place: install the new package over the old (`dnf install ./Nessus-10.x.rpm`,
   `dpkg -i`, Windows MSI). Configuration, scans and plugins persist.
3. Or let automatic software updates handle it (Settings > Software Update > Update all components).
4. Linked scanners managed by Tenable VM/SC: enable automatic updates from the manager side or
   upgrade during a window; plugin compatibility requires reasonably current versions.
Restore: `nessuscli backup --restore <file>` on a fresh install of the same or newer version.

## Agents
- Nessus Manager / Tenable VM agent update plans (Settings > Agents > Software Update, or agent
  profiles pinning versions). Pilot on a group first; agents update themselves.
- Very old agents may need manual reinstall when jumping major versions.

## Migrating Nessus Manager to Tenable VM
- Tenable's migration (Settings > Advanced / Migration in Nessus Manager 8.11+) relinks agents to
  Tenable VM, optionally migrating scan history.
- Steps: link Nessus Manager to Tenable VM with a linking key; choose agent groups to migrate;
  monitor progress; old scans are imported as history. Once agents check in to Tenable VM, rebuild
  agent scans and schedules there.
- Plan for licence counts in Tenable VM before migration (agents count as assets).

## Gotchas
- Downgrades are not supported; take the backup.
- Large plugin recompilation after upgrade delays scans; schedule upgrades outside scan windows.
- Agents behind proxies need the proxy configured to reach `sensor.cloud.tenable.com` post-migration.

## Verify
Settings > About shows the new version; a test scan runs; after migration, agent counts in Tenable
VM match Nessus Manager and agents report recent check-ins.
