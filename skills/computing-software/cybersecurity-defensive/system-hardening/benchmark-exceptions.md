---
id: computing-software.cybersecurity-defensive.system-hardening.benchmark-exceptions
name: benchmark-exceptions
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [benchmark-exceptions, cis-benchmarks, stig, hardening-deviations, risk-acceptance, compensating-controls]
level: practitioner
status: draft
description: "Document deviations from CIS Benchmark or STIG settings: exception records, compensating controls, approvals, expiry, encoding in scanners, and audit evidence."
sources: ["https://www.cisecurity.org/cis-benchmarks", "https://public.cyber.mil/stigs/", "https://csrc.nist.gov/pubs/sp/800/70/r4/final", "https://www.pcisecuritystandards.org/document_library/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Benchmark deviation documentation

No real estate applies 100% of a CIS Benchmark or STIG. The difference between a hardened estate and a
non-compliant one is whether every deviation is deliberate, justified and tracked.

## Exception record (one per rule per scope)
| Field | Example |
|---|---|
| Rule ID | CIS Ubuntu 22.04 L1 1.1.2.3 "noexec on /tmp" / STIG V-238xxx |
| Scope | Group "build-agents" (hosts by tag), not "all servers" |
| Reason | Build tooling executes binaries from /tmp; vendor confirms |
| Risk | Malware staged in /tmp can execute |
| Compensating controls | EDR with execution blocking from temp paths, AppArmor profile for agent |
| Owner / approver | Platform lead / CISO delegate |
| Created / expiry | 2026-10-01 / 2027-04-01 |
| Ticket for remediation | PLAT-412 (move tool temp dir to dedicated volume) |

## Process
1. Engineering requests exception with evidence (failing app test, vendor statement).
2. Security reviews risk and compensating controls; approver signs according to severity (L1 vs L2, CAT I vs
   CAT II/III; CAT I STIG findings need higher authority).
3. Encode the exception in tooling so scans show "accepted" not "fail":
   - CIS-CAT Pro / OpenSCAP: **tailoring file** (XCCDF tailoring) deselecting the rule for that profile and
     scope, with the exception ID in the description.
   - STIG Viewer checklists: status "Not a Finding" only if compliant; use "Open" with comments or mark as
     accepted via POA&M rather than misreporting.
   - Ansible/Puppet roles: variable to skip the rule with a comment referencing the exception.
   - Cloud CSPM: suppression with expiry date and reason.
4. Review on expiry; renew only with fresh justification.

## Reporting
Compliance percentage computed both "raw" and "with approved exceptions", count of exceptions by severity,
exceptions past expiry (should be zero). Auditors (PCI DSS 2.2, FedRAMP, ISO 27001) expect this list with
approvals.

## Gotchas
- Blanket exceptions ("all of section 5 for all servers") are rejected by auditors and hide real gaps.
- A tailoring file that disables rules without records is an undocumented exception.
- Re-check exceptions after OS upgrades; the original reason may no longer apply.

## Verify
Every failing rule in the latest scan is either remediated or matches an unexpired exception record; tailoring
files reference exception IDs.
