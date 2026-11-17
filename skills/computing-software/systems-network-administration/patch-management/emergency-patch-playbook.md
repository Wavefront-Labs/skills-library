---
id: computing-software.systems-network-administration.patch-management.emergency-patch-playbook
name: emergency-patch-playbook
category: computing-software
field: systems-network-administration
product: patch-management
tags: [emergency-patch-playbook, emergency-patching, zero-day, emergency-change, exposure-assessment, out-of-band-update]
level: advanced
status: draft
description: "A ready-to-run playbook for a critical exploited vulnerability: trigger criteria, roles, first-hour steps, exposure scoping, mitigate-then-patch, tracking and close-out."
sources:
  - https://csrc.nist.gov/pubs/sp/800/40/r4/final
  - https://www.cisa.gov/known-exploited-vulnerabilities-catalog
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Emergency patch playbook

NIST SP 800-40r4 calls for an **emergency maintenance plan** separate from routine cycles.
Write it before you need it; this is a template.

## Trigger (any of)
- Vendor or CISA marks a vulnerability **exploited in the wild** (KEV) affecting an asset
  class you run, especially internet-facing or Tier 0 (VPN, firewalls, hypervisors,
  identity, backup, email).
- CVSS ≥ 9 pre-auth RCE on exposed services with public exploit.
- Threat intel or SOC detection of exploitation attempts in your environment.

## Roles
Incident lead (owns timeline), vulnerability analyst, platform owners per asset class,
change manager (emergency CAB), communications, SOC liaison.

## First hour
1. Open an emergency ticket/war room; declare severity and next update time.
2. **Scope exposure**: inventory query for affected product/version; internet exposure
   (ASM, firewall rules, `shodan`-style external scan of your ranges); authenticated scan
   plugin when available.
3. **Decide mitigation now**: vendor workaround, disable feature, block at WAF/IPS,
   restrict access (geo/IP allow-list), take offline if exposed and unpatched Tier 0.
4. Ask SOC to hunt for IOCs from the advisory (logs since disclosure, earlier if 0-day).

## Next 24-72 hours
5. Acquire and validate patch (hash/signature); smoke test on one non-critical instance.
6. Emergency change approval (pre-agreed delegation, e.g. on-call manager + security).
7. Deploy: exposed and Tier 0 first, then internal; snapshots/backups before; verify.
8. Rescan to confirm; track per-asset status in a shared tracker (asset, owner, mitigated,
   patched, verified).
9. If compromise indicators found: switch to incident response (patching does not evict an
   attacker; credentials and persistence must be dealt with).

## Communication
Status updates at fixed intervals to leadership and affected service owners; customer
comms if services degrade.

## Close-out
All in-scope assets patched or under approved exception with compensating control;
post-implementation review within 2 weeks: time to detect, time to mitigate, time to patch,
what slowed you (inventory gaps, approvals, missing access).

## Verify
Tabletop this playbook twice a year with a real recent CVE; measure time to produce the
exposure list.
