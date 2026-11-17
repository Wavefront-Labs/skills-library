---
id: computing-software.digital-forensics-incident-response.incident-response-process.vlan-and-segment-isolation-of-compromised-enclaves
name: vlan-and-segment-isolation-of-compromised-enclaves
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [vlan-isolation, network-containment, segmentation, quarantine-vlan, containment, dfir]
level: practitioner
status: draft
description: "Contain a compromised network enclave by VLAN or segment isolation: quarantine VLANs, ACLs at the boundary, keeping management and forensic access, and verifying the cut."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r2/final", "https://www.cisa.gov/sites/default/files/publications/Federal_Government_Cybersecurity_Incident_and_Vulnerability_Response_Playbooks_508C.pdf", "https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/sec/b_179_sec_9300_cg/configuring_ipv4_acls.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# VLAN and segment isolation of compromised enclaves

When many hosts in one zone are compromised, or hosts cannot run an EDR agent (OT, appliances, legacy servers), isolate the segment at the network rather than host by host.

## Options, least to most disruptive
1. **Boundary ACL / firewall rule** on the routed interface or firewall zone: deny the enclave outbound to internet and to other internal zones, allow only responder subnets and required management. Fastest and reversible.
2. **Quarantine VLAN**: move switch ports (or use NAC/802.1X dynamic VLAN assignment) into a VLAN that routes only to a remediation network.
3. **Private VLAN / port isolation** inside the enclave to stop host-to-host lateral movement while keeping uplink.
4. **Physical disconnect** of the uplink: last resort, kills remote forensic access.

## Example boundary ACL (Cisco IOS-XE style)
```
ip access-list extended QUARANTINE-ENCLAVE
 remark allow IR jump hosts and EDR cloud
 permit ip 10.20.0.0 0.0.255.255 host 10.99.1.10
 permit tcp 10.20.0.0 0.0.255.255 host 10.99.1.20 eq 443
 deny   ip 10.20.0.0 0.0.255.255 any log
interface Vlan120
 ip access-group QUARANTINE-ENCLAVE in
```
In cloud, the equivalent is replacing security groups / NSGs with a quarantine group that only allows the forensic subnet.

## Procedure
1. Get the authority per the delegation table; tell service owners what will break.
2. Capture before cutting: start a packet capture or flow export at the boundary so attacker reaction is recorded.
3. Decide timing with the coordinated-remediation plan; isolating one segment early can tip the attacker off elsewhere.
4. Apply the change through an emergency change record; keep the exact config diff in the case.
5. Keep out-of-band management (iLO/iDRAC network, console servers) reachable from the IR network only.

## Gotchas
- Dual-homed hosts, VPN concentrators and hypervisor management networks bypass VLAN boundaries; check them.
- DHCP, DNS and NTP stop if you deny all; decide whether isolated hosts still need them.
- The ACL `log` keyword on a busy interface can spike CPU; use flow export instead if volume is high.

## Verify
From an isolated host, attempts to reach the internet and another internal zone fail and appear in the deny log, while the IR jump host can still connect.
