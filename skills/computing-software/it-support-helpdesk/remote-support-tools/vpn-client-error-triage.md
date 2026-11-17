---
id: computing-software.it-support-helpdesk.remote-support-tools.vpn-client-error-triage
name: vpn-client-error-triage
category: computing-software
field: it-support-helpdesk
product: remote-support-tools
tags: [it-support-helpdesk, remote-support-tools, vpn-client-errors, vpn, globalprotect, cisco-secure-client, ikev2, always-on-vpn, vpn-certificate, vpn-protocols-ports, vpn-client-logs]
level: practitioner
status: draft
description: "Triage VPN client errors by layer: decode common GlobalProtect, Cisco Secure Client and Windows RAS error codes, collect the right logs, and know what to escalate."
sources:
  - "https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/troubleshoot-always-on-vpn"
  - "https://learn.microsoft.com/en-us/windows/win32/rras/routing-and-remote-access-error-codes"
  - "https://docs.paloaltonetworks.com/globalprotect"
  - "https://www.cisco.com/c/en/us/support/docs/security/anyconnect-secure-mobility-client/212972-anyconnect-vpn-client-troubleshooting-gu.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vpn-client-error-triage

## Layer the problem
1. **Internet**: does a browser reach a public site? Captive portal (hotel, train) must be
   cleared first.
2. **Reach the gateway**: `Test-NetConnection vpn.example.com -Port 443`; for IKEv2, UDP
   500/4500 must pass (cannot be tested with Test-NetConnection).
3. **Authenticate**: password/MFA, certificate, or device posture.
4. **After connect**: routes, DNS, and MTU (see vpn-mtu-and-fragmentation-problems).

## Windows built-in / Always On VPN codes
| Code | Meaning | Usual fix |
|---|---|---|
| 809 | No response from server | UDP 500/4500 blocked or NAT-T issue; try another network |
| 691 | Access denied, bad credentials | Password, account locked, or not in the VPN group |
| 812 | Rejected by server policy (NPS) | Group membership or auth method mismatch |
| 13801 | IKE auth credentials unacceptable | Client cert missing/expired or server cert name/EKU wrong |
| 13806 | No valid machine certificate | Device tunnel cert not issued; check Intune SCEP/PKCS profile |

Logs: Application log, source RasClient (event 20227 gives the code); `Get-VpnConnection`.

## Vendor clients
- **GlobalProtect**: "Gateway not responding" (network or gateway down), certificate not
  trusted (root CA missing), HIP check failed (posture). Collect via Troubleshooting tab >
  Collect Logs (PanGPS.log, PanGPA.log).
- **Cisco Secure Client (AnyConnect)**: "VPN establishment capability for a remote user is
  disabled" when starting the VPN inside an RDP session (profile setting); "Login failed"
  (auth). Collect a DART bundle.
- **FortiClient**: 98% hang during connect is usually DNS/route push; collect diagnostic
  logs from the client.

## Escalate with
User, time, public IP, client version, error text, logs. Gateway-side failures need the
network/security team with these details.

## Gotchas
- Clock skew breaks certificate auth; check time first.
- Two VPN/ZTNA clients installed fight over routes and DNS.
- Hotel networks often block UDP; an SSL/TLS fallback profile saves the trip.

## Verify
Client connects, internal name resolves (`Resolve-DnsName intranet.example.com`), an
internal resource opens, and the ticket records code, cause and fix.
