---
id: computing-software.systems-network-administration.windows-server.rd-gateway-certificates-and-policies
name: rd-gateway-certificates-and-policies
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, remote-desktop-services, rds, rd-gateway, cap, rap, rdg-certificate, udp-transport, nps]
level: practitioner
status: docs-checked
description: "Publish RDS through RD Gateway: certificate, connection and resource authorization policies, UDP 3391, central NPS for MFA, and gateway troubleshooting."
sources:
  - https://learn.microsoft.com/en-us/windows-server/remote/remote-desktop-services/rds-plan-access-from-anywhere
  - https://learn.microsoft.com/en-us/windows-server/remote/remote-desktop-services/rds-rdweb-gateway-ha
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/remote/ports-used-by-rds
  - https://learn.microsoft.com/en-us/powershell/module/remotedesktop/add-rdserver
  - https://learn.microsoft.com/en-us/powershell/module/remotedesktop/set-rdcertificate
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RD Gateway with certificates and CAP/RAP

## Install and certificate
```powershell
Add-RDServer -Server rdgw01 -Role RDS-GATEWAY -ConnectionBroker rdcb01 -GatewayExternalFqdn remote.example.com
Set-RDCertificate -Role RDGateway -ImportPath '<vol>:\certs\remote.pfx' -Password $pw -ConnectionBroker rdcb01 -Force
```
- The gateway must have a certificate that the client device recognizes (trusted, matching the external FQDN).
- Ports: TCP 443 (HTTP over SSL) and UDP 3391 (RDP over UDP); both can be configured in the RD Gateway Manager console.
  Firewalls with directional UDP analysis need UDP Send Receive.

## Policies
- **CAP** (connection authorization policy): who may use the gateway.
- **RAP** (resource authorization policy): which internal hosts they may reach. Avoid "allow any network resource".
Create and review both in RD Gateway Manager; the exact settings differ by Windows Server release (this skill does not
state property names that could not be confirmed).

## MFA
RD Gateway can use the RADIUS protocol to integrate multi-factor authentication solutions such as Azure MFA, and NPS
traffic needs UDP 1812 and 1813 between the gateway and NPS.

## Farm
Put multiple gateways (and RD Web servers) behind a load balancer so long-lived connections are distributed evenly, and
give every gateway the same certificate.

## Troubleshoot
- Gateway unreachable: check DNS, the firewall ports above and the certificate name.
- Users succeed via the gateway but not to the host: check RAP membership and that the internal name matches the RAP
  entry.

## Verify
- [ ] External client connects through the gateway; RAP denies hosts that are not listed.

## Checked

Checked 2026-10-26 against learn.microsoft.com / MicrosoftDocs/windowsserverdocs, windows-powershell-docs and SupportArticles-docs main branches, last commits 2026-10-23. Confirmed: Add-RDServer with -Role RDS-GATEWAY and -GatewayExternalFqdn, Set-RDCertificate -Role RDGateway, the ports (TCP 443 for HTTP over SSL, UDP 3391 for RDP over UDP, UDP 1812 and 1813 for NPS) from the Ports used by RDS article, the need for a certificate the client recognizes and RADIUS-based MFA support from the plan access article, and load balancing of RD Web and RD Gateway servers. Removed as unconfirmed: the RDS PowerShell provider (GatewayServer path) commands and their parameters, the RADIUS 60 second timeout, UDP source affinity, the gateway event IDs, CRL reachability and the RAP naming claim. CAP and RAP property details are not documented in a public repository, so the skill defers to RD Gateway Manager.

Method: documentation only; no commands were run.
