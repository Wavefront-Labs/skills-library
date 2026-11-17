---
id: computing-software.cybersecurity-defensive.network-defence.always-on-vpn
name: always-on-vpn
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [always-on-vpn, windows-always-on-vpn, ikev2, device-tunnel, user-tunnel, intune-vpn-profile, vpn-remote-access]
level: advanced
status: docs-checked
description: "Deploy Windows Always On VPN: device and user tunnels, IKEv2 with certificate auth, Intune/ProfileXML configuration, split tunnelling, and RRAS/NPS hardening."
sources: ["https://learn.microsoft.com/en-us/windows-server/remote/remote-access/overview-always-on-vpn", "https://learn.microsoft.com/en-us/windows/security/operating-system-security/network-security/vpn/vpn-profile-options"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows Always On VPN

Native Windows VPN that connects automatically before/after logon. Successor to DirectAccess.

## Tunnels
- **Device tunnel**: establishes connectivity before user sign-in; use it for DC/management access and limit its routes. Check the Always On VPN overview for edition and join requirements.
- **User tunnel**: carries user traffic after sign-in; prefer certificate-based authentication over passwords.

## Server side
- RRAS (or a third-party IKEv2 gateway), NPS for RADIUS auth/authorisation; public certificate on the gateway for IKEv2/SSTP.
- Configure custom IKEv2 cryptography on the server and match it in the client profile (use `Set-VpnServerConfiguration`; check its parameters in Microsoft's reference).
- Restrict which certificates are accepted for VPN authentication and enforce revocation checking so revoked devices cannot connect.

## Client profile (Intune VPN profile or ProfileXML)
```xml
<VPNProfile>
  <AlwaysOn>true</AlwaysOn>
  <DeviceTunnel>false</DeviceTunnel>
  <TrustedNetworkDetection>corp.example.com</TrustedNetworkDetection>
  <NativeProfile><Servers>vpn.example.com</Servers><NativeProtocolType>IKEv2</NativeProtocolType>
    <Authentication><UserMethod>Eap</UserMethod></Authentication>
    <RoutingPolicyType>SplitTunnel</RoutingPolicyType></NativeProfile>
  <Route><Address>10.0.0.0</Address><PrefixSize>8</PrefixSize></Route>
</VPNProfile>
```
## Gotchas
- Force-tunnel vs split-tunnel: split with explicit corporate routes is typical; send M365 direct.
- Device tunnel without route restrictions grants pre-logon network access broadly.

## Verify
- [ ] The device tunnel connects before logon.
- [ ] A revoked certificate cannot connect.
- [ ] Negotiated crypto matches the policy you configured.

## Checked

2026-10-28. Confirmed against: Microsoft Learn Always On VPN overview (IKEv2, device tunnel connects before sign-in) and VPN profile options (AlwaysOn, RoutingPolicyType, SplitTunnel).

Removed as unconfirmed: device-tunnel IKEv2-only and edition claims, SSTP fallback, exact cipher parameter values, Set-VpnAuthProtocol (no such cmdlet page found), Get-NetIPsecMainModeSA check, Conditional Access remark.

Method: documentation only; no commands were run.
