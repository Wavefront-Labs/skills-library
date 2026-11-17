---
id: computing-software.systems-network-administration.windows-server.nps-8021x-eap-tls
name: nps-8021x-eap-tls
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, nps, network-policy-server, 8021x, eap-tls, wired-autoconfig, wlansvc, computer-certificates, wired-network-policy, wireless-network-policy]
level: advanced
status: docs-checked
description: "Deploy certificate-based 802.1X (EAP-TLS) for wired and wireless with NPS: computer/user cert autoenrollment, GPO wired/wireless profiles, NPS policy, and switch config basics."
sources:
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/nps/nps-manage-cert-requirements
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/nps/nps-np-configure
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/nps/nps-best-practices
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/nps/nps-radius-clients-configure
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# 802.1X with EAP-TLS and NPS

## Certificates
- **NPS server certificate**: see nps-server-certificate-for-peap-eap-tls (Server Authentication EKU, non-blank subject, DNS name in the SAN). Clients must trust its CA.
- **Client certificates**: Client Authentication purpose (1.3.6.1.5.5.7.3.2). Computer certificates carry the client FQDN (DNS name) in the SAN; user certificates carry the UPN.
- Use certificate autoenrollment from your AD CS templates so client and server certificates renew without manual steps.

## Client configuration
Configure wired or wireless 802.1X profiles (Group Policy or MDM) with the EAP method for certificates, server certificate validation against your trusted root CA and, where available, the NPS server names. Skipping server validation lets clients authenticate to a rogue RADIUS server. Follow the Microsoft wired and wireless access deployment guides for the exact GPO paths.

## NPS policy
Create the connection request policy and network policy for 802.1X switches or wireless access points using the NPS "Configure 802.1X" procedure: conditions such as Windows Groups and NAS Port Type (Ethernet or Wireless), and the EAP type that uses the NPS server certificate. Add VLAN attributes if the switch assigns VLANs (Tunnel-Type, Tunnel-Medium-Type, Tunnel-Pvt-Group-ID, Tunnel-Tag).

## Switch side
Configure the switch or access point as an NPS RADIUS client (same shared secret, UDP 1812/1813) and enable 802.1X on access ports only, not uplinks or server ports. Fallback VLAN and MAB behaviour is vendor specific: check the switch vendor's documentation.

## Verify
- [ ] A test device authenticates through the intended network policy (NPS logs the policy name).
- [ ] Revoking a client certificate (with CRL publishing) blocks that device.

## Checked

2026-10-25, against the MicrosoftDocs/windowsserverdocs repository (main, last commit 2026-10-23), the windows-powershell-docs NPS cmdlet pages and the MicrosoftDocs/entra-docs repository. Confirmed certificate purposes and SAN requirements for NPS and client certificates, the 802.1X NPS policy procedure, VLAN attribute names, RADIUS client ports and the best practice to use certificate-based methods. Removed the unconfirmed template names, GPO tree paths, netsh interface commands, and event numbers; vendor-specific switch features are pointed to vendor documentation.

Method: documentation only; no commands were run.
