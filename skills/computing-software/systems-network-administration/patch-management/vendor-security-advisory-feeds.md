---
id: computing-software.systems-network-administration.patch-management.vendor-security-advisory-feeds
name: vendor-security-advisory-feeds
category: computing-software
field: systems-network-administration
product: patch-management
tags: [vulnerability-intelligence, security-advisories, msrc, usn, rhsa, dsa, cisa-kev, rss, csaf, patch-management]
level: practitioner
status: docs-checked
description: "Track new vulnerabilities from vendor sources: MSRC Security Update Guide/API, Ubuntu USN, Red Hat RHSA, Debian DSA, appliance vendor PSIRTs and CISA KEV, routed to triage."
sources:
  - https://api.msrc.microsoft.com/cvrf/v3.0/updates
  - https://ubuntu.com/security/notices
  - https://ubuntu.com/security/oval
  - https://security.access.redhat.com/data/csaf/v2/advisories/
  - https://www.debian.org/security/
  - https://security-tracker.debian.org/tracker/data/json
  - https://ftp.suse.com/pub/projects/security/csaf/
  - https://www.cisa.gov/known-exploited-vulnerabilities-catalog
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vendor security advisory feeds

**Goal:** learn about vulnerabilities and fixes affecting your estate within hours of
publication, from authoritative sources, without reading 20 websites daily.

## Sources by platform
| Platform | Source | Machine-readable |
|---|---|---|
| Microsoft | MSRC Security Update Guide (monthly Patch Tuesday, out-of-band) | MSRC CVRF API (`api.msrc.microsoft.com/cvrf/v3.0/updates` lists releases with a `CvrfUrl` each) |
| Ubuntu | Ubuntu Security Notices (USN) | Ubuntu OVAL data (security/oval page) |
| Red Hat / Alma / Rocky | RHSA errata | CSAF at `security.access.redhat.com/data/csaf/v2/advisories/` |
| Debian | DSA (debian-security-announce list, RSS) | Security tracker JSON (`security-tracker.debian.org/tracker/data/json`), OVAL |
| SUSE | SUSE-SU | CSAF (`ftp.suse.com/pub/projects/security/csaf/`) |
| Network/security appliances | Cisco PSIRT, Fortinet PSIRT, Palo Alto, Juniper SIRT | Check each vendor's PSIRT page for RSS, CSAF or API options |
| VMware/Broadcom | Security advisories | Check the vendor page for feed or email options |
| Exploited in the wild | **CISA KEV** catalogue | JSON feed (`known_exploited_vulnerabilities.json`) |

## Pipeline
1. Subscribe only to vendors in your **software inventory**; prune quarterly.
2. Pull machine-readable feeds (CSAF/OVAL/KEV JSON) into the vulnerability management
   tool or a small script that matches products/versions against inventory.
3. Email/RSS for vendors without feeds into a shared triage queue (ticket system), not
   individual inboxes.
4. Add a KEV watcher: new KEV entries matching inventory create high-priority tickets
   immediately.

## Reading an advisory
Extract: affected products and fixed versions, CVSS and the vendor's own severity,
exploitation status (wording differs per vendor), workaround/mitigation, reboot requirement,
known issues. Distro advisories describe backported fixes: compare package
version-release to the advisory's fixed version, not the upstream version.

## Gotchas
- Scanner plugins can lag advisories; for KEV/emergency items, check advisories
  directly.
- Appliance vendors differ in publication cadence and emergency releases; learn each vendor's rhythm.

## Verify
Pick last month's three most severe advisories relevant to you: each produced a triage
ticket within one business day with affected-asset counts attached.

## Checked
Date: 2026-10-27. Documentation read live: MSRC CVRF v3.0 updates endpoint, Red Hat CSAF directory index, Ubuntu OVAL page, Debian security page and tracker JSON, SUSE CSAF directory, CISA KEV feed. Removed unconfirmed claims: Ubuntu OSV, MSRC CSAF, Red Hat VEX path, Cisco openVuln and per-vendor appliance feed types, bi-annual bundle cadence.
Method: documentation only; no commands were run.
