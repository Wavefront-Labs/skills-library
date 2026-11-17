---
id: computing-software.it-support-helpdesk.remote-support-tools.vpn-mfa-with-radius-and-nps
name: vpn-mfa-with-radius-and-nps
category: computing-software
field: it-support-helpdesk
product: remote-support-tools
tags: [it-support-helpdesk, remote-support-tools, radius-nps, vpn-mfa, nps-extension, radius, network-policy-server, vpn-authentication]
level: practitioner
status: docs-checked
description: "Add MFA to VPN logins through RADIUS and NPS with the Entra MFA NPS extension, and troubleshoot timeouts, rejected logins and missing push prompts."
sources:
  - "https://learn.microsoft.com/en-us/entra/identity/authentication/howto-mfa-nps-extension"
  - "https://learn.microsoft.com/en-us/entra/identity/authentication/howto-mfa-nps-extension-vpn"
  - "https://learn.microsoft.com/en-us/windows-server/networking/technologies/nps/nps-top"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vpn-mfa-with-radius-and-nps

## Flow
VPN server (RADIUS client) sends an Access-Request to the NPS server where the NPS extension
is installed. If the NPS connection request and network policy conditions are met, the
extension requests secondary authentication from Entra MFA, which returns the result to the
extension, and NPS answers the VPN server.

## Setup essentials
- NPS: install the role on a server other than the VPN server; add the VPN as a RADIUS
  client with a long, complex shared secret; create a network policy for the VPN users.
- Install the **NPS extension for Microsoft Entra MFA** on the NPS server (not on the VPN
  server) and run the included Graph PowerShell script, which creates a self-signed
  certificate and associates it with the service principal. Run it on each NPS server that
  has the extension.
- On-premises users must be synced to Entra and enabled for MFA.
- **VPN server RADIUS timeout: at least 60 seconds** (Microsoft suggests raising to 90 or
  120 if discarded requests still appear in the logs), so the user has time to approve.
- Once installed, the NPS server requires MFA for all RADIUS clients it serves. To mix,
  Microsoft describes two NPS servers with the extension on only one, or the
  `REQUIRE_USER_MATCH` string value in `HKLM\SOFTWARE\Microsoft\AzureMfa` for users not
  enrolled; read the VPN article for its exact semantics first.

## Troubleshooting
- Logs: Security log on the RADIUS server or the Network Policy and Access Services custom
  view in Event Viewer: Event ID 6272 is a granted connection, 6273 a denied one. Extension
  logs: Applications and Services Logs > Microsoft > AzureMfa.
- Login worked before moving to central RADIUS but now fails: suspect RADIUS misconfiguration
  or an invalid user name or password. Using an alternate UPN suffix in the user name can fail;
  use the same account name for best results.
- Code-based methods: TOTP is supported by the extension, but some VPN clients (for example
  the Windows built-in one) do not support it; check the client first.
- NPS does not support Authenticator number matching; see the NPS extension FAQ for the
  TOTP workaround and the extension version caveat.
- The extension article lists which methods work with PAP; check it before choosing the
  authentication protocol.

## Verify
A test user gets one MFA prompt and connects; the RADIUS server's Security log shows 6272.

## Checked
2026-11-01. Confirmed against the Microsoft Learn pages "Integrate your existing NPS
infrastructure with Microsoft Entra multifactor authentication", "Integrate your VPN
infrastructure with Azure MFA by using NPS extension" and the NPS overview: flow, install
location, certificate script, 60 s timeout (and 90/120), events 6272/6273, AzureMfa log
path, TOTP/number matching caveats, REQUIRE_USER_MATCH. Removed: MSCHAPv2/PAP
push-versus-OTP table rows, 5-10 s default timeouts, Entra sign-in log "NPS extension"
label, single-NPS and licensing advice, retries explanation.
Method: documentation only; no commands were run.
