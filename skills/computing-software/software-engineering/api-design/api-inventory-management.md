---
id: computing-software.software-engineering.api-design.api-inventory-management
name: api-inventory-management
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, api-inventory, improper-inventory-management, owasp-api-top-10, shadow-apis, zombie-apis, api-governance]
level: practitioner
status: docs-checked
description: "Keep a live inventory of API hosts, versions and environments (OWASP API9:2023) to find forgotten beta hosts and old versions before attackers do."
sources: ["https://owasp.org/API-Security/editions/2023/en/0xa9-improper-inventory-management/", "https://spec.openapis.org/oas/v3.1.0"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Improper inventory management (OWASP API9:2023)

Old versions (`/v1`), beta hosts, non-production copies with production data and undocumented endpoints are attack surface nobody patches. In OWASP scenario #1 a beta host ran the same reset-password API without the separate rate-limiting component, so a 6-digit reset token could be brute-forced.

## Minimum inventory (one row per API host+version)
- host, and the environment it runs in (production, staging, test, development)
- who should have network access: public, internal or partners
- API version, and the retirement plan for that version
- authentication, errors, redirects, rate limiting, CORS policy and endpoints, documented
- integrated third-party services: their role, what data flows to them and its sensitivity, with a business justification for each sensitive flow

## Keeping it honest
1. Generate, do not hand-write: OWASP recommends generating documentation automatically from open standards and including the documentation build in CI/CD. Publish an OpenAPI file per service and index it in one catalogue. Make the documentation available only to those authorised to use the API.
2. Discover drift: compare gateway access logs against the catalogue.
```bash
# paths seen in traffic but not in the spec
jq -r '.paths|keys[]' openapi.json | sort > spec.txt
awk '{print $7}' access.log | sed 's/[?].*//' | sort -u > seen.txt
comm -13 spec.txt seen.txt
```
(Path parameters need normalising before this comparison is exact.)
3. Retire on a schedule: every version needs a retirement plan; when a newer version adds security improvements, do a risk analysis for the older versions (backport if compatible, otherwise take the old version out and move clients). See the sunset-header skill for signalling.
4. Avoid production data in non-production deployments; if unavoidable, give those endpoints the same security treatment as production.
5. Apply external protection (for example API security tooling) to every exposed version, not just the current production one.

## Gotchas
- Microservices and cloud deployments make it easy to expose API hosts unnecessarily, and attackers find them with DNS enumeration and search engines; do the same enumeration on your own domains.
- Out-of-date or missing documentation is itself a finding (CWE-1059).

Verify: pick three random hostnames from DNS or the cloud account and confirm each has a catalogue entry with an environment, audience and version; any that do not are findings.

## Checked
2026-11-08. Read in full: OWASP API Security Top 10 2023 page API9 (documentation and data-flow blindspots, both scenarios, prevention list). Removed unsupported claims: owner team and data classification columns, separate credentials for non-production, certificate-transparency scanning, and the statement that undocumented fields skip authorization review. The OpenAPI 3.1.0 spec was not re-read for this skill; its use here is only as a document format named by the skill. The shell snippet was not run.
Method: documentation only; no commands were run.
