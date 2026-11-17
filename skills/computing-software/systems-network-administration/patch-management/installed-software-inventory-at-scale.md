---
id: computing-software.systems-network-administration.patch-management.installed-software-inventory-at-scale
name: installed-software-inventory-at-scale
category: computing-software
field: systems-network-administration
product: patch-management
tags: [software-inventory, asset-inventory, installed-software-query, osquery, uninstall-registry, dpkg-query, rpm-qa, patch-management]
level: practitioner
status: draft
description: "Build a software inventory for patching: query installed software on Windows (registry, not Win32_Product), Linux packages, osquery fleet queries, and normalising versions."
sources:
  - https://csrc.nist.gov/pubs/sp/800/40/r4/final
  - https://osquery.readthedocs.io/en/stable/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Installed-software inventory at scale

**Goal:** know every installed product and version on every system, because NIST SP
800-40r4 starts patch planning with software inventory: you cannot patch or even assess
what you don't know is there.

## Windows
Read the **Uninstall registry keys**, not `Win32_Product` (which is slow and triggers MSI
self-repair on every package):
```powershell
$paths = 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*',
         'HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*'
Get-ItemProperty $paths | Where DisplayName |
  Select DisplayName, DisplayVersion, Publisher, InstallDate |
  Export-Csv "$env:COMPUTERNAME-sw.csv" -NoTypeInformation
Get-AppxPackage -AllUsers | Select Name, Version          # Store/MSIX apps
Get-HotFix | Sort InstalledOn                             # installed updates (partial view)
```
Per-user installs (HKCU, `%LOCALAPPDATA%` apps like some browsers and Teams) are missed by
machine-level queries: include user hives or use an agent.

## Linux
```sh
dpkg-query -W -f='${Package}\t${Version}\n'        # Debian/Ubuntu
rpm -qa --qf '%{NAME}\t%{VERSION}-%{RELEASE}\t%{ARCH}\n'   # RHEL family
snap list ; flatpak list                              # other package systems
pip list --format=freeze ; npm ls -g --depth=0        # language runtimes on servers
```
Software outside package managers (tarballs in `/opt`, vendored JARs) needs file scans.

## Fleet query with osquery
```sql
SELECT name, version, source FROM programs;          -- Windows
SELECT name, version FROM deb_packages;              -- Debian/Ubuntu
SELECT name, version, release FROM rpm_packages;
SELECT name, version FROM chrome_extensions;
```
Run via a fleet manager (FleetDM, Kolide) on a schedule, centralise results.

## Normalise
Map names to products (CPE or vendor/product pairs) and keep version strings comparable
(epoch:version-release on Linux). Backported fixes mean distro versions must be compared
against distro advisories, not upstream version numbers.

## Verify
Inventory covers ≥ 98% of assets in the CMDB/asset list; spot-check five machines against
their local package list; a known-vulnerable package query returns the expected hosts.
