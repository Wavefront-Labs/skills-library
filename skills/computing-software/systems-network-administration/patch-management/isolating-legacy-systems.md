---
id: computing-software.systems-network-administration.patch-management.isolating-legacy-systems
name: isolating-legacy-systems
category: computing-software
field: systems-network-administration
product: patch-management
tags: [legacy-isolation, eol-software, network-segmentation, compensating-controls, virtual-patching, application-allowlisting]
level: advanced
status: draft
description: "Contain unpatchable legacy and EOL systems: segmentation, allowlist firewalling, removing internet and broad admin access, virtual patching, monitoring and documented exceptions."
sources:
  - https://csrc.nist.gov/pubs/sp/800/40/r4/final
  - https://csrc.nist.gov/pubs/sp/800/82/r3/final
  - https://www.cisa.gov/resources-tools/resources/secure-by-design
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Isolating legacy systems

**Goal:** an EOL machine that cannot be patched or replaced yet (lab instrument PC, OT controller, legacy app server) cannot be used as an entry point or pivot.

## Controls, strongest first
1. **Segment.** Dedicated VLAN/VRF or microsegment; default-deny firewall with explicit allow rules for the exact peers and ports it needs (both directions). No internet egress; if updates of app data are needed, use a proxy allowlist.
2. **Reduce trust.** Remove from the main domain where feasible, or restrict which accounts can log on; no shared admin credentials; separate local admin passwords (LAPS).
3. **Access via jump host only.** RDP/SSH allowed only from a hardened bastion with MFA and session recording.
4. **Harden the host.** Disable unneeded services (SMBv1 exposure, remote registry), application allowlisting, remove email and browsing.
5. **Virtual patching.** IPS signatures for known CVEs at the segment boundary; WAF for legacy web apps.
6. **Monitor.** Forward logs; alert on any new outbound connection or new listening port; network detection on the segment.
7. **Backups** of the system and its configuration so rebuild is possible.

## Paperwork
Risk exception per system: reason it cannot be patched, controls in place, owner, review date, replacement plan. Review at least quarterly.

## Gotchas
- "Temporarily" isolated systems often get firewall rule creep; audit rule hits and remove unused rules.
- Removable media is a common bypass; control USB on the legacy host.

## Verify
A scan from the general network reaches no ports on the isolated host except via the jump host, and outbound internet attempts are blocked and logged.
