---
id: computing-software.systems-network-administration.network-design.network-segmentation-strategy
name: network-segmentation-strategy
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, network-segmentation, segmentation, microsegmentation, macrosegmentation, security-zones, trust-zones, zero-trust, east-west-traffic, flow-matrix, default-deny, firewall-zones, dmz, management-network, out-of-band, oob, jump-host, paw, guest-network, iot-segmentation, ot-segmentation, pci-dss, cde, scope-reduction, 802-1x, nac, dynamic-vlan, trustsec, sgt, security-groups, nsx, networkpolicy, netflow, lateral-movement, ransomware-containment]
level: advanced
status: gated
description: "Plan segmentation: zones by trust and blast radius, a flow matrix from NetFlow/logs, default-deny between zones, isolated management and shared services, then microsegmentation."
sources:
  - https://www.nist.gov/publications/zero-trust-architecture
  - https://www.cisa.gov/zero-trust-maturity-model
  - https://www.pcisecuritystandards.org/document_library/
  - https://kubernetes.io/docs/concepts/services-networking/network-policies/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network segmentation strategy — decide who may talk to whom, then make everything else impossible

**Goal:** limit how far an attacker (or a broken device, or a broadcast storm) can spread,
and shrink audit scope, without breaking the business. This is the vendor-neutral policy;
device configuration is in vendor skills such as
`computing-software.systems-network-administration.cisco-networking.acl-and-security-configuration`.
Address plans for the zones: `...network-design.ip-addressing-and-subnetting`.

## 1. Define zones by trust and blast radius
A zone is a set of systems with the same trust level and the same allowed flows. A typical
starting set:

| Zone | Contents | Default stance |
|---|---|---|
| Users | wired/Wi-Fi corporate endpoints | outbound to apps/internet; no inbound from other zones |
| Guest | visitor Wi-Fi | internet only; nothing internal |
| Servers / apps | split prod vs non-prod | only published service ports in |
| Data | databases, file stores | only from their app tier |
| Shared services | AD/DNS/NTP/DHCP, monitoring | many in, narrowly scoped ports |
| Backup | backup servers, repositories | **pulls** from others; nothing may initiate into it |
| Management | switch/firewall/hypervisor/BMC interfaces | only from jump hosts/PAWs |
| IoT / OT / printers | cameras, HVAC, badge readers, printers | to their controller only |
| Regulated (e.g. PCI CDE) | card data systems | minimal, documented flows |

Split further where a compromise of one system must not reach its peers (e.g. separate
Tier 0 identity systems from general servers).

## 2. Build the flow matrix from evidence
1. Turn on flow visibility before enforcing: NetFlow/IPFIX/sFlow from core switches,
   firewall logs, cloud VPC flow logs, or host-level tools.
2. Collect at least one full business cycle (month-end, payroll, backups, patching).
3. Write a matrix: source zone × destination zone → protocol/port → business owner →
   justification. Every cell without a justified flow is **deny**.
4. Flag surprises (servers browsing the internet, workstations talking to each other on
   SMB/RDP) as findings, not as rules to copy.

## 3. Enforce at the boundaries
- Put a **stateful firewall** (or cloud security groups / NSG) between zones. Stateless
  switch ACLs are acceptable inside a zone or for crude filtering, not as the main control.
- **Default deny** between zones, explicit allows by matrix row, logging on denies.
- Inter-zone traffic must actually traverse the firewall: put zone gateways on the
  firewall (or VRFs routed through it), not on a core switch that routes between VLANs
  directly. Check firewall throughput for east-west volume (backups, vMotion, storage
  are better kept on dedicated, non-routed networks).
- Rule hygiene: no `any` service rules between zones; each rule has an owner and a review
  date; remove rules with zero hits after a review period.

## 4. Treat shared services as the danger they are
Shared services and backup touch every zone, so they are lateral-movement highways:
- AD/DNS: allow only the ports clients need; administer from the management zone only.
- Backup: backup servers initiate connections to clients; clients cannot reach the
  repository. Repositories have separate credentials and immutable copies
  (see `computing-software.systems-network-administration.backup-and-recovery.backup-strategy-3-2-1-rule`).
- Monitoring/patching servers with credentials everywhere: harden and isolate them as Tier 0.

## 5. Management plane
- Device management interfaces, hypervisor management and BMC/iLO/iDRAC live in a
  dedicated management zone (ideally out-of-band), reachable only from jump hosts or
  privileged access workstations with MFA.
- Never expose BMCs or management interfaces to user VLANs or the internet.

## 6. Go finer where it pays: microsegmentation
When zones are still too big (a flat server VLAN of hundreds), enforce per workload:
- host firewalls managed centrally (managed centrally);
- hypervisor distributed firewalls or cloud security groups referencing
  other groups instead of IP ranges;
- Kubernetes `NetworkPolicy` with a default-deny policy per namespace (needs a network plugin that
  enforces it);
- identity-based access at the edge: 802.1X/NAC assigning VLANs or security group tags
  (SGT) by user/device identity.
Roll out in monitor mode first, then enforce one application at a time.

## 7. Prove the segmentation
- Test from each zone with a scanner (a port scanner such as nmap) to confirm only matrix
  flows are open. Repeat after every major change; PCI DSS requires periodic segmentation
  testing to validate scope reduction (gated: unconfirmed, source is paywalled or blocked).
- Run a tabletop: "a user laptop is compromised; list everything it can reach."

## Verify
- [ ] Every system is assigned to exactly one zone, recorded in IPAM/CMDB.
- [ ] Flow matrix built from observed traffic over a full business cycle; each allow has an owner.
- [ ] Inter-zone traffic provably passes a stateful control with default deny.
- [ ] Management interfaces reachable only from the management zone.
- [ ] Backup repositories cannot be reached from client zones.
- [ ] Scan results from each zone match the matrix.

## Checked

- Date: 2026-10-28
- Confirmed: Kubernetes network-policies page: policies need a network plugin that supports NetworkPolicy; NIST zero trust architecture page (SP 800-207) exists as the cited background.
- Removed: nmap flags, NSX DFW and GPO/nftables examples, named CNI plugins.
- Gated: the PCI DSS periodic segmentation testing requirement (PCI document library page returned almost no text).
Method: documentation only; no commands were run.
