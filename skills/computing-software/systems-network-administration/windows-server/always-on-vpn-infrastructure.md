---
id: computing-software.systems-network-administration.windows-server.always-on-vpn-infrastructure
name: always-on-vpn-infrastructure
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, remote-access, rras, always-on-vpn, ikev2, sstp, device-tunnel, user-tunnel, profilexml, vpnv2-csp]
level: advanced
status: docs-checked
description: "Build Always On VPN on Windows Server: RRAS with IKEv2/SSTP, NPS for RADIUS, certificate templates, user and device tunnels, and ProfileXML via Intune or script."
sources:
  - https://learn.microsoft.com/en-us/windows-server/remote/remote-access/overview-always-on-vpn
  - https://learn.microsoft.com/en-us/windows-server/remote/remote-access/get-started-install-ras-as-vpn
  - https://learn.microsoft.com/en-us/windows-server/remote/remote-access/tutorial-aovpn-deploy-create-certificates
  - https://learn.microsoft.com/en-us/windows-server/remote/remote-access/vpn/vpn-device-tunnel-config
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Always On VPN infrastructure

## Components
- **RRAS** VPN servers in the perimeter (the docs describe load balancing for resilience): IKEv2 (UDP 500/4500)
  with fallback to SSTP (TCP 443) via the automatic protocol type in the user-tunnel profile.
- **NPS** servers (RADIUS) for authorization; EAP types include user certificates, smart cards and Windows Hello for Business.
- **AD CS** templates from the Microsoft tutorial: *VPN User Authentication* (duplicate of User; Enroll and Autoenroll for the VPN Users group),
  *VPN Server Authentication* (duplicate of RAS and IAS Server; add the **IP security IKE intermediate** application policy) and an NPS server authentication template.
- Client profile (ProfileXML) deployed with PowerShell, Configuration Manager, Intune or Windows Configuration Designer.

## RRAS setup (per server)
```powershell
Install-WindowsFeature DirectAccess-VPN -IncludeManagementTools
Install-RemoteAccess -VpnType Vpn
# then in the Routing and Remote Access console: allow IKEv2 only (or SSTP), set an authentication provider (RADIUS for NPS),
# assign a static address pool for connecting clients, and select the server certificate.
```
Set a custom IKEv2 policy (all values below are accepted by the cmdlet; match them in the client profile):
```powershell
Set-VpnServerConfiguration -CustomPolicy -EncryptionMethod AES256 -IntegrityCheckMethod SHA256 `
  -DHGroup Group14 -CipherTransformConstants AES256 -AuthenticationTransformConstants SHA256128 -PfsGroup PFS2048 -SALifeTimeSeconds 28800
```
Clients must use the same custom policy in the ProfileXML cryptography settings.

## Profiles
- **User tunnel**: per-user, EAP with user cert, after logon; full or split tunnel with routes.
- **Device tunnel**: machine certificate, IKEv2 only (no SSTP fallback), before logon; configurable only on domain-joined Windows 10 Enterprise or Education 1709 or later;
  with a Microsoft RAS gateway, enable **Allow machine certificate authentication for IKEv2**; use traffic filters (which block inbound traffic to the client) and host routes to limit reach.
- Trusted Network Detection can be combined with the device tunnel.

## Verify
- [ ] `Get-RemoteAccessConnectionStatistics` on RRAS shows connected users.
- [ ] NPS accounting logs show VPN users authenticating; client `Get-VpnConnection` shows IKEv2.
- [ ] Device tunnel connects at the logon screen.

## Checked
Checked 2026-10-26 against Microsoft windowsserverdocs main, windows-powershell-docs (winserver2025-ps RemoteAccess, NetNat, NetTCPIP), azure-docs vpn-gateway articles, SupportArticles-docs (troubleshoot-always-on-vpn, ms.date 2026-02-12).
Confirmed from overview-always-on-vpn, vpn-device-tunnel-config (ms.date 2023-01-25), get-started-install-ras-as-vpn (ms.date 2025-05-06: Install-WindowsFeature DirectAccess-VPN, IKEv2, static address pool),
tutorial-aovpn-deploy-create-certificates (ms.date 2025-05-08: template names, IP security IKE intermediate) and the Set-VpnServerConfiguration reference (CustomPolicy parameter values AES256, SHA256, Group14, SHA256128, PFS2048).
Removed the PEAP-TLS-only statement, MDM_VPNv2_01, the weak-DH-default claim, the NPS event 6272 check, and the 'Enterprise/Education only' implication for the user tunnel (user tunnel works on all editions).
Method: documentation only; no commands were run.
