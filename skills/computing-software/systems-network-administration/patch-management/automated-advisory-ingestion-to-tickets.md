---
id: computing-software.systems-network-administration.patch-management.automated-advisory-ingestion-to-tickets
name: automated-advisory-ingestion-to-tickets
category: computing-software
field: systems-network-administration
product: patch-management
tags: [advisory-ingestion, vulnerability-intelligence, csaf, ticketing-automation, patch-management]
level: practitioner
status: docs-checked
description: "Pull vendor advisories (CSAF, RSS, MSRC API, KEV) automatically, filter them against your inventory, and open deduplicated tickets for the right owner team."
sources:
  - https://docs.oasis-open.org/csaf/csaf/v2.0/csaf-v2.0.html
  - https://github.com/gocsaf/csaf/blob/main/docs/csaf_downloader.md
  - https://api.msrc.microsoft.com/cvrf/v3.0/updates
  - https://security.access.redhat.com/data/csaf/v2/advisories/
  - https://www.cisa.gov/known-exploited-vulnerabilities-catalog
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Automated advisory ingestion into tickets

**Goal:** a new advisory for a product you run becomes a ticket in the owning team's queue within an hour, with no ticket for products you do not run.

## Sources and formats
| Source | Format | Endpoint |
|---|---|---|
| CSAF 2.0 providers (for example Red Hat and SUSE) | JSON | providers publish `/.well-known/csaf/provider-metadata.json`; Red Hat's CSAF is under `security.access.redhat.com/data/csaf/v2/advisories/` |
| Microsoft MSRC | CVRF API (send `Accept: application/json` for JSON; XML is the default) | `https://api.msrc.microsoft.com/cvrf/v3.0/updates` |
| CISA KEV | JSON | known_exploited_vulnerabilities.json |
| Others | RSS/Atom | vendor PSIRT pages |

Fetch CSAF with `csaf_downloader` from the open-source gocsaf/csaf project (options `-d` directory, `-t`/`--time_range`; the range accepts a relative duration or an RFC 3339 date):
```sh
csaf_downloader -d ./csaf --time_range 2026-10-01 redhat.com cisco.com
```

## Pipeline
1. **Fetch** on a schedule (hourly), store raw documents with the fetch time.
2. **Parse** product identifiers: CSAF `product_tree` gives CPEs/purls and product names; extract CVE, severity, fixed versions, remediation URL.
3. **Match** against inventory (CPE/purl/product mapping table). No match -> archive, no ticket.
4. **Dedup** on `(vendor advisory id)`; append new CVEs to the existing ticket on revisions instead of opening another.
5. **Route** to the owner team from the CMDB; set priority from KEV/EPSS/CVSS and asset criticality.
6. **Close loop**: link ticket to the patch change; scanner confirmation closes it.

Create the ticket through your ticketing system's documented API (for example ServiceNow's Table API); check its field names and authentication method in that product's documentation.

## Gotchas
- Advisory revisions (v1.1, v2.0) change affected versions; re-match on each revision.
- Product name mismatches cause silent misses. Report "advisories for vendors we run that matched zero assets" weekly and fix the mapping.
- Rate limits: honour vendor caching headers and published limits.

## Verify
Inject a known past advisory for a product you run; a ticket appears for the right group with the right asset count, and re-ingesting creates no duplicate.

## Checked
Date: 2026-10-27. Documentation: gocsaf/csaf docs (csaf_downloader options, provider-setup path `/.well-known/csaf/provider-metadata.json`), live MSRC CVRF v3.0 API (JSON requires an Accept header), Red Hat and SUSE CSAF directories, KEV feed. Removed the unconfirmed Cisco, Siemens and Oracle CSAF claims and the ServiceNow sample call.
Method: documentation only; no commands were run.
