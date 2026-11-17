---
id: computing-software.systems-network-administration.patch-management.distro-security-trackers
name: distro-security-trackers
category: computing-software
field: systems-network-administration
product: patch-management
tags: [debian-security-tracker, ubuntu-cve-tracker, rhsa, red-hat-cve, vulnerability-intelligence, linux-patching]
level: practitioner
status: docs-checked
description: "Answer whether a CVE is fixed on your distro using the Debian Security Tracker, Ubuntu CVE tracker and Red Hat CVE pages, including not-affected and will-not-fix."
sources:
  - https://security-tracker.debian.org/tracker/
  - https://ubuntu.com/security/cves/about
  - https://access.redhat.com/security/security-updates/cve
  - https://www.suse.com/security/cve/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Distribution security trackers

Upstream "fixed in 3.0.8" is irrelevant on enterprise distros: fixes are **backported** into
the shipped version. The distro tracker tells you which package build fixes it.

## Debian
`https://security-tracker.debian.org/tracker/CVE-2024-XXXX`
- Table per release and source package (for example bookworm, trixie, forky/sid), with a status such as `fixed` (with the package version), `<no-dsa>` (minor issue, may be fixed in a point update), `<postponed>` or `<end-of-life>`; the Security Tracker documentation lists the full set.
- DSA/DLA advisories list fixed versions. Local check: `debsecan --suite bookworm --only-fixed`.

## Ubuntu
`https://ubuntu.com/security/CVE-2024-XXXX`
- Status per release: `Needs evaluation`, `Not affected`, `Vulnerable`, `Vulnerable, work in progress`, `Vulnerable, fix deferred`, `Fixed` (with the package version), `Ignored`, `Not in release`.
- Ubuntu exports its CVE data as OVAL for scanners.

## Red Hat (and rebuilds)
`https://access.redhat.com/security/cve/CVE-2024-XXXX`
- Per product: `Affected`, `Under investigation`, `Fixed` (with the RHSA errata), `Not affected`, `Will not fix`. Red Hat's scores reflect how the vulnerability affects Red Hat products, so they can differ from NVD's CVSS.
- Local: `dnf updateinfo info --cve CVE-2024-XXXX`, `dnf upgrade --cve CVE-2024-XXXX`,
  `rpm -q --changelog openssl | grep CVE-2024-XXXX`.

## SUSE
`https://www.suse.com/security/cve/CVE-2024-XXXX.html`; local `zypper list-patches --cve=CVE-2024-XXXX`.

## Using statuses
- `Not affected` / `Will not fix` (low severity): document as risk acceptance or close the
  scanner finding with the tracker link as evidence.
- Scanner reports vulnerable version but tracker shows fixed build installed: false
  positive from version-only detection; fix the scanner config (OVAL-based checks).

## Verify
For each critical CVE in scope you can cite the distro status page, fixed package version,
and installed version per host.

## Checked
Date: 2026-10-27. Documentation checked: Debian Security Tracker documentation and a live CVE page (`fixed`, `<no-dsa>`, `<postponed>`, `<end-of-life>`, releases listed), debsecan manual (`--suite`, `--only-fixed`), Ubuntu CVE "about" page (status definitions, OVAL export) and a live CVE page, Red Hat CVE page FAQ (Affected, Under investigation, Will not fix, Red Hat scores), DNF command reference (`--cve`, `--security`, `updateinfo`), SUSE CVE page URL form and the zypper manual (`list-patches --cve`). Removed the Ubuntu `Released/Needed/Deferred` labels and `pro fix`, the Red Hat `Fix deferred` and `Out of support scope` states and the Alma/Rocky advisory-ID claim, which were not confirmed.

Method: documentation only; no commands were run.
