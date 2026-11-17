---
id: computing-software.systems-network-administration.patch-management.rapid-exposure-assessment-new-cve
name: rapid-exposure-assessment-new-cve
category: computing-software
field: systems-network-administration
product: patch-management
tags: [emergency-patching, zero-day, exposure-assessment, cisa-kev, attack-surface, asset-inventory, threat-hunting, patch-management]
level: advanced
status: docs-checked
description: "Answer 'are we exposed?' within hours of a critical CVE: affected versions, inventory and scanner queries, internet exposure, exploitation checks, and the response decision."
sources:
  - https://csrc.nist.gov/pubs/sp/800/40/r4/final
  - https://www.cisa.gov/known-exploited-vulnerabilities-catalog
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rapid exposure assessment for a new critical CVE

**Goal:** within the first few hours of a headline vulnerability, a defensible answer: which
assets are affected, which are exposed, whether we see exploitation, and what we do now.

## Hour 0-1: understand the vulnerability
From the vendor advisory (not news articles): affected products **and exact version
ranges**, required configuration (feature enabled? port reachable? authentication
needed?), fixed versions, workaround, exploitation status, KEV listing.

## Hour 1-3: find affected assets
1. **Inventory query** for product and version (software inventory, CMDB, osquery, EDR
   software inventory): for example the osquery Windows `programs` table, which has `name` and `version` columns: `SELECT name, version FROM programs WHERE name LIKE '%<product>%'`.
2. **Scanner**: run the vendor's or scanner's new plugin as an ad-hoc scan against relevant
   ranges; authenticated checks are more accurate than banner checks.
3. **Embedded copies**: libraries (log4j-style) live inside other products; ask vendors,
   search file systems for the component (`find / -name '<lib>*.jar'`), check SBOMs.
4. **Cloud/SaaS**: check provider bulletins for managed services you use.

## Hour 2-4: exposure and exploitation
- Which affected assets are **internet-facing** (external attack surface scan, firewall
  NAT rules, cloud security groups)?
- Hunt for exploitation indicators published by the vendor/CISA in proxy, WAF, EDR and
  web logs since the vulnerability's earliest known exploitation date.
- If exploitation is found, switch to incident response.

## Decide
| Situation | Response |
|---|---|
| Internet-facing + exploited in the wild | Emergency change: patch or mitigate within hours, isolate if neither possible |
| Internal + KEV or PoC public | Emergency plan timeline (days) |
| Not reachable / feature disabled | Routine cycle, document reasoning |
Record everything in one ticket: affected list, exposure, decisions, timestamps.

## Gotchas
- "Not in inventory" is not "not present": inventory gaps are discovered in exactly these
  moments; note them as findings.
- Vendor version ranges are revised in the first days; re-check advisories.

## Verify
Executive summary within 4 hours: count affected/exposed/remediated, actions and next
update time; a follow-up rescan confirms the affected list matched reality.

## Checked
Date: 2026-10-27. Documentation: osquery `programs` table spec (columns name, version), CISA KEV feed, NIST SP 800-40 Rev. 4 page. The remaining content is a time-boxed process with example hour ranges, not vendor facts.
Method: documentation only; no commands were run.
