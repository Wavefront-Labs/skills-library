---
id: computing-software.cybersecurity-defensive.network-defence.nac-posture-assessment
name: nac-posture-assessment
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [posture-assessment, nac, cisco-ise-posture, endpoint-compliance, remediation-vlan, intune-compliance-nac, network-access-control]
level: advanced
status: draft
description: "Add posture assessment to NAC: compliance conditions, agent vs agentless checks, MDM/EDR compliance integration, quarantine and remediation, and avoiding mass lockouts."
sources: ["https://www.cisco.com/c/en/us/td/docs/security/ise/3-3/admin_guide/b_ise_admin_3_3/b_ISE_admin_33_compliance.html", "https://docs.fortinet.com/product/fortinac", "https://learn.microsoft.com/en-us/mem/intune/protect/network-access-control-integrate"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NAC posture assessment

Authentication says who/what the device is; posture says whether it is healthy enough to get full access.

## Checks
- AV/EDR installed, running, signatures current.
- OS patch level / minimum build; disk encryption on; firewall on.
- Managed device (MDM enrolled, compliant in Intune/Jamf).

## Sources of posture
| Method | Notes |
|---|---|
| NAC agent (Cisco Secure Client ISE posture module, FortiClient) | Rich checks and remediation; agent to manage |
| Temporal/dissolvable agent | Guest/BYOD one-off checks |
| MDM compliance API (Intune, Jamf, Workspace ONE) | NAC queries device compliance; no extra agent. ISE MDM integration / Intune compliance retrieval (Intune's newer Compliance Retrieval service uses device IDs, not MAC/serial alone) |
| EDR signals | Some NACs pull EDR health/risk |

## Flow (ISE-style)
1. 802.1X auth succeeds -> posture status Unknown -> limited access (redirect ACL to the posture portal/agent provisioning, plus remediation servers: WSUS, AV update, MDM).
2. Agent assesses -> Compliant -> RADIUS CoA re-authorisation -> full access authorisation profile.
3. NonCompliant -> remediation VLAN/dACL with only remediation servers reachable; user notified.
4. Periodic reassessment (e.g. every 4-24 h) catches drift.

## Rollout
- Monitor-only (posture evaluated, no enforcement) for weeks; fix systemic non-compliance first.
- Grace periods for patch checks; exclude critical devices (medical, OT) via profiling-based policies.

## Gotchas
- Posture checks that fail because the agent cannot reach its server look like non-compliance; ensure the limited-access ACL allows the posture servers and DNS.
- Strict checks rolled out at once lock out large parts of the workforce on Monday morning.

## Verify
- [ ] Non-compliant test device lands in remediation, regains access after fixing, via CoA.
- [ ] Monitoring dashboard: compliant percentage by site.
