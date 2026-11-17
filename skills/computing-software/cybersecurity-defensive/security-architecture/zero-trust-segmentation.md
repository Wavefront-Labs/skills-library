---
id: computing-software.cybersecurity-defensive.security-architecture.zero-trust-segmentation
name: zero-trust-segmentation
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [security-architecture, zero-trust, zero-trust-architecture, nist-800-207, microsegmentation, network-segmentation, ztna, identity-aware-proxy, policy-enforcement-point, least-privilege, east-west-traffic, lateral-movement, flow-logs, tiered-administration, paw, mtls, service-mesh, cisa-zero-trust-maturity-model, beyondcorp]
level: advanced
status: draft
description: "Segment an estate around protect surfaces: map flows, define identity-based allow policies, enforce with ZTNA/microsegmentation, and roll out in monitor-then-enforce stages."
sources: ["NIST SP 800-207 Zero Trust Architecture", "CISA Zero Trust Maturity Model v2.0", "NCSC Zero trust architecture design principles", "Google BeyondCorp papers (USENIX ;login:)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Zero-trust segmentation — make lateral movement expensive

**Goal:** replace "inside the network = trusted" with explicit, identity- and
device-aware allow rules around your most valuable systems, so one compromised
laptop or server can reach only what it legitimately needs.

## 1. Pick protect surfaces, not the whole network
List 3–5 protect surfaces to start: identity tier (AD/Entra Connect/IdP, PAM),
backups, payment/customer data stores, CI/CD and secrets, hypervisor/management
plane. For each, record data, applications, assets and owners. Segmenting
everything at once stalls; segmenting the backup and identity tiers first blunts
ransomware.

## 2. Map real flows before writing rules
- Collect 2–4 weeks of flow data: VPC/VNet flow logs, firewall logs, NetFlow/IPFIX,
  or the visibility mode of your microsegmentation tool (agent-based products
  such as Illumio, Akamai Guardicore, or host firewalls via EDR).
- Build a who-talks-to-whom matrix per protect surface: source workload/identity,
  destination, port, process if available. Label each flow *required*, *admin*, or
  *unknown*. Unknown flows go to the owner, not into an allow rule.
- Cover month-end batch jobs and DR tests — a 2-week window misses them; ask owners.

## 3. Write policy in terms of identity and labels
Policy shape: *subject* (user + device posture, or workload identity) → *resource*
→ *action* → *conditions*. Examples:
- `role=web, env=prod` → `role=db, env=prod` on TCP 5432 only; everything else denied.
- Admins reach server management (RDP/SSH/WinRM) only from privileged access
  workstations (PAWs) or a bastion with MFA, never from general workstations.
- Workstation-to-workstation SMB/RDP: deny. It is the main ransomware spread path.
- Users reach internal apps via ZTNA / identity-aware proxy (per-app access with
  device compliance checks), not a flat VPN into a /16.
Use labels (env, app, role) rather than IP addresses so rules survive autoscaling.
For service-to-service, mutual TLS with workload identity (SPIFFE IDs, service mesh
authorisation policies) gives an enforcement point that doesn't depend on IPs.

## 4. Roll out in stages
1. **Visibility** — tool in monitor mode; no blocking.
2. **Test policy** — rules written; tool reports would-be-blocked flows. Fix gaps for
   at least one full business cycle.
3. **Enforce at the protect surface** — default-deny inbound to the segment.
4. **Expand** to the next surface; finally tackle general east-west defaults.
Each step needs a rollback (one switch back to monitor) and an owner on call.

## 5. Tiered administration
Separate admin identities by tier (Tier 0: identity/control plane; Tier 1: servers;
Tier 2: workstations). A Tier 0 credential must never log on to a lower tier host.
Enforce with logon restrictions (GPO "Deny log on" rights, Authentication Policies
and Silos in AD) — segmentation is useless if a domain admin logs on to an infected
helpdesk PC.

## Gotchas
- Shared infrastructure flows (DNS, NTP, AD/Kerberos/LDAP, patching, backup agents,
  monitoring, EDR cloud) are easy to forget and break everything at enforcement.
- Backup systems need inbound from everything — so attackers love them. Make backup
  *management* reachable only from a PAW and keep immutable/offline copies.
- IP-based rules on cloud/Kubernetes go stale within days; use tags/labels or
  Kubernetes NetworkPolicies with a default-deny per namespace.
- "Zero trust" products that only replace the VPN leave east-west traffic flat.
- Exception creep: track every allow rule's owner and review annually.

## Verify
- [ ] Protect surfaces are listed with owners and a mapped flow matrix.
- [ ] Each enforced segment is default-deny with label-based allow rules.
- [ ] Workstation-to-workstation SMB/RDP is blocked and tested from a sample endpoint.
- [ ] Admin protocols to servers succeed only from PAWs/bastion.
- [ ] A red-team or lateral-movement test from a compromised-workstation position is blocked and logged.
- [ ] Rollback to monitor mode is documented and has been exercised.

Related: computing-software.cybersecurity-defensive.network-defence.firewall-and-egress-policy,
computing-software.cybersecurity-defensive.identity-access-management.sso-and-mfa-rollout
