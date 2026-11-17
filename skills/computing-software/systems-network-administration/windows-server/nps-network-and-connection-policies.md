---
id: computing-software.systems-network-administration.windows-server.nps-network-and-connection-policies
name: nps-network-and-connection-policies
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, nps, network-policy-server, network-policies, connection-request-policies, peap, eap-tls, nas-port-type, windows-groups-condition, vlan-assignment, policy-order]
level: practitioner
status: docs-checked
description: "Design NPS policy: connection request policies (local vs proxy), network policies with conditions, EAP method settings, RADIUS attributes like VLAN, and ordering."
sources:
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/nps/nps-np-overview
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/nps/nps-np-configure
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/nps/nps-crp-crpolicies
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/nps/nps-best-practices
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NPS connection request and network policies

## Processing order
1. **Connection request policies (CRP)** decide where a request is processed: locally (NPS acts as a RADIUS server) or forwarded to a remote RADIUS server group (NPS acts as a proxy). A request is processed only if it matches at least one CRP; the default policy processes requests locally.
2. **Network policies** are an ordered set of rules: NPS checks the request against the first, then the next, until one matches. The matching policy's conditions, constraints (authentication methods) and settings decide the outcome. With no matching policy the request is rejected unless the account's dial-in properties grant access.

## Wi-Fi example (certificate-based or PEAP)
Network policy "Corp Wi-Fi Users":
- Conditions: **Windows Groups** = a security group of Wi-Fi users; **NAS Port Type** = Wireless - IEEE 802.11. A Called Station ID condition can narrow it to an SSID (the value format is device specific).
- Constraints > Authentication Methods: add the EAP type (for example Protected EAP or Microsoft: Smart Card or other certificate) and choose the NPS server certificate; remove weaker methods you do not need.
- Settings for VLAN assignment: configure the RADIUS attributes **Tunnel-Type**, **Tunnel-Medium-Type**, **Tunnel-Pvt-Group-ID** and **Tunnel-Tag** (the NPS docs list these four).

Microsoft's best practices: use certificate-based methods such as PEAP and EAP rather than password-only authentication.

## Ordering and hygiene
- Order policies so the most specific are evaluated first.
- Access permission: the policy either grants or denies, and can use the user account's Network Access Permission ("Access is determined by User Dial-in properties") or ignore dial-in properties ("Ignore user account dial-in properties").

## Verify
- [ ] A test client authenticates and the event or accounting record shows the expected network policy.
- [ ] The access device receives the VLAN attributes.

## Checked

2026-10-25, against the MicrosoftDocs/windowsserverdocs repository (main, last commit 2026-10-23), the windows-powershell-docs NPS cmdlet pages and the MicrosoftDocs/entra-docs repository. Confirmed CRP versus network policy roles, ordered first-match evaluation, the no-match rejection rule with the dial-in exception, the two dial-in handling options, the four VLAN attributes, and the certificate-based best practice. Removed the unconfirmed SSID regex, Credential Guard and MSCHAPv2 claims, specific attribute values, and reason-code numbers.

Method: documentation only; no commands were run.
