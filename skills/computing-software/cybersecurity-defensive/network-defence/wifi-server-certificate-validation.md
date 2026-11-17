---
id: computing-software.cybersecurity-defensive.network-defence.wifi-server-certificate-validation
name: wifi-server-certificate-validation
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [server-certificate-validation, wifi-certificate-validation, 802-1x-supplicant, peap, eap-tls, evil-twin, wireless-security]
level: practitioner
status: draft
description: "Make Wi-Fi clients validate the RADIUS server certificate: trusted CA and server name pinning in Windows, macOS, iOS, Android profiles, preventing evil-twin credential capture."
sources: ["https://learn.microsoft.com/en-us/mem/intune/configuration/wi-fi-settings-windows", "https://support.apple.com/guide/deployment/wi-fi-payload-settings-dep0b82d4f5/web", "https://source.android.com/docs/security/features/wifi-enterprise", "https://csrc.nist.gov/pubs/sp/800/153/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Server certificate validation on Wi-Fi clients

With PEAP/EAP-TTLS (and even EAP-TLS), a client that does not validate the RADIUS server certificate
will hand credentials or a challenge-response to any rogue AP with the same SSID (evil twin, e.g.
hostapd-wpe). PEAP-MSCHAPv2 responses captured this way are crackable.

## What "validated" means
1. Server certificate chains to a **specific** trusted root (your private RADIUS CA), not any public CA.
2. Server name matches an expected value (`radius.corp.example.com`).
3. User is **not** allowed to accept unknown certificates when prompted.

## Platform configuration (push via MDM, never manual)
| Platform | Setting |
|---|---|
| Windows (Intune Wi-Fi profile / GPO) | Trusted root CA certificate selected, "Certificate server names" = RADIUS FQDN, "Notifications before connecting: Don't ask user to authorize new servers or trusted CAs" |
| macOS/iOS (Wi-Fi payload) | `PayloadCertificateAnchorUUID` = root CA payload, `TLSTrustedServerNames` = radius FQDN; certificate trust in the profile |
| Android 11+ | Must set CA certificate and domain; "Do not validate" option removed for new configs; Android Enterprise Wi-Fi config with `domainSuffixMatch` |
| Linux (NetworkManager) | `802-1x.ca-cert` and `802-1x.domain-suffix-match` |

## Server side
- Dedicated private CA for RADIUS certs, long enough validity to avoid frequent client updates, but plan renewals: pushing the new chain before rotating.
- Move to EAP-TLS (certificate client auth) so no reusable password is exposed even if validation fails.

## Gotchas
- BYOD devices onboarded manually almost always skip validation - use an onboarding tool (SecureW2, ClearPass Onboard, ISE BYOD) or EAP-TLS.
- Wildcard or public-CA server certificates make pinning weaker; anyone can buy a public cert for their domain.

## Verify
- [ ] Rogue AP test (authorised, lab) with a self-signed cert: managed clients refuse to connect without prompting.
- [ ] Profiles in MDM include CA and server names for all platforms.
