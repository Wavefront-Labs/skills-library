---
id: computing-software.systems-network-administration.patch-management.vendor-workarounds-and-mitigations
name: vendor-workarounds-and-mitigations
category: computing-software
field: systems-network-administration
product: patch-management
tags: [risk-response, vendor-workaround, mitigation, compensating-controls, temporary-mitigation, nist-sp-800-40, patch-management]
level: practitioner
status: draft
description: "Apply NIST SP 800-40r4 risk responses when a patch can't go in yet: vendor workarounds, feature disablement, network restrictions, WAF/IPS rules, tracking and removing them later."
sources:
  - https://csrc.nist.gov/pubs/sp/800/40/r4/final
  - https://www.cisa.gov/known-exploited-vulnerabilities-catalog
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Vendor workarounds and mitigations

**Goal:** reduce exposure to a vulnerability quickly when patching is not yet possible,
then remove the stopgap once the real fix is in.

## Risk responses (NIST SP 800-40r4)
- **Accept** (documented, time-bound),
- **Mitigate** (patch, or reduce likelihood/impact by other means),
- **Transfer** (insurance, outsourcing; rarely relevant to a single CVE),
- **Avoid** (remove the software or the exposure).
Workarounds are a form of mitigation; patching remains the goal.

## Typical mitigations
| Type | Example |
|---|---|
| Vendor workaround | Registry key or config change from the advisory (disable a vulnerable feature or protocol) |
| Disable/uninstall | Remove unused component (print spooler on DCs, legacy SMBv1, unused web modules) |
| Network restriction | Block the port at host firewall/ACL, restrict management interfaces to admin networks, take an appliance's VPN portal offline |
| Virtual patching | WAF rule or IPS signature for the exploit pattern |
| Hardening | Attack surface reduction rules, application allow-listing, least privilege |
| Detection | Temporary detection rule/hunt query for exploitation attempts |

## Procedure
1. Read the vendor advisory's workaround section and its stated side effects.
2. Assess scope: which assets, business impact of the workaround.
3. Apply via configuration management (GPO, Ansible) as an **emergency or standard
   change**, so it is consistent and reversible.
4. Verify it works: rescan, or test the specific condition (port closed, feature off).
5. Record it: ticket with CVE, assets, mitigation, owner, **expiry/review date**.
6. When the patch is deployed, remove workarounds that degrade function, and close the record.

## Gotchas
- Workarounds can be undone by later patches or config drift; re-verify after each cycle.
- Some vendor "mitigations" only cover one attack vector; read carefully and keep pushing
  for the patch.
- Scanners may still flag the CVE (version-based detection); note the mitigation in the
  scanner as an exception with expiry rather than ignoring it.

## Verify
Each active mitigation has a ticket, an owner and a review date; spot-check that the
control is still in place on a sample of assets.
