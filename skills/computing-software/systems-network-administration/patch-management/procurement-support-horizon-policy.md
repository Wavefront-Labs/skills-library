---
id: computing-software.systems-network-administration.patch-management.procurement-support-horizon-policy
name: procurement-support-horizon-policy
category: computing-software
field: systems-network-administration
product: patch-management
tags: [support-horizon, procurement-policy, eol-software, lifecycle-management, patch-management]
level: practitioner
status: draft
description: "Set a procurement support horizon policy: minimum remaining vendor support at purchase, contract clauses for security fixes, and review gates that stop buying soon-to-be-EOL tech."
sources:
  - https://learn.microsoft.com/en-us/lifecycle/
  - https://endoflife.date/docs/api
  - https://csrc.nist.gov/pubs/sp/800/161/r1/upd1/final
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Procurement support horizon policy

Most EOL problems are bought, not grown: a product purchased with 18 months of support left, or a vendor with no published lifecycle.

## Policy statements (example)
- Hardware and software must have **at least N years of vendor security support remaining at purchase** (common: 3 years for software, 5 for servers/network gear, matched to depreciation period).
- Vendor must publish a lifecycle policy (dates for end of sale, end of standard support, end of security fixes) or state it contractually.
- Embedded OS/components (appliances, OT, medical/lab devices) must declare their OS and its support date; vendor commits to security updates for the product's supported life.
- Products already announced end-of-sale need an exception.

## Contract clauses
- Security patches for critical/high vulnerabilities within X days of disclosure for the support term.
- Notice of end-of-life at least 12-24 months ahead.
- SBOM delivery and vulnerability disclosure process (aligns with NIST SP 800-161 supply chain practices).
- Right to apply OS patches without voiding support (common pain with vendor appliances).

## Review gate
Add to the purchase/architecture review checklist: product, version, support end date (source link), years remaining vs policy, owner, planned refresh date. Record in CMDB at purchase so EOL tracking starts on day one.

## Lookups
- Microsoft Lifecycle site, Red Hat/Ubuntu/SUSE lifecycle pages, Cisco EoL bulletins, Dell/HPE/Lenovo product support lifecycles.
- `curl -s https://endoflife.date/api/<product>.json | jq '.[0]'` for quick checks on common software.

## Gotchas
- "Extended support" that excludes security fixes does not count.
- Cloud/SaaS components still have version lifecycles (managed DB engine versions, Kubernetes minors); include them.

## Verify
Purchases in the last year sampled: each has a recorded support date meeting policy or an approved exception.
