---
id: computing-software.networking-hardware-and-wireless.strongswan.windows-and-apple-client-interop
name: windows-and-apple-client-interop
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, windows-client, ios, macos, interop, modp2048]
level: practitioner
status: docs-checked
description: "Make Windows, iOS and macOS built-in IKEv2 clients work with a strongSwan gateway: Windows modp2048 registry value, auth methods, Apple default proposals and optional PFS."
sources:
  - https://docs.strongswan.org/docs/latest/interop/windowsClients.html
  - https://docs.strongswan.org/docs/latest/interop/ios.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# windows and apple client interop
**Windows 7 and newer** support IKEv2 and MOBIKE through Agile VPN, but not IKE redirection (RFC 5685) or multiple authentication rounds (RFC 4739).

By default Windows 7 to 11 propose only the weak modp1024 group. To enable modp2048 set the DWORD `NegotiateDH2048_AES256` under `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Rasman\Parameters`: 0 disables AES-256-CBC and MODP-2048 (default), 1 enables, 2 enforces (Windows 11 then proposes `aes256-sha1-sha256-sha384-modp2048`). ESP proposals still include weak algorithms (single DES, NULL, SHA1 only); `Set-VpnConnectionIPsecConfiguration` adds AES-GCM and ECP groups, at least on Windows 10.

strongSwan authenticates Windows clients with X.509 machine certificates (RSA signatures), user certificates via EAP-TLS (needs the eap-tls and eap-identity plugins), or passwords via EAP-MSCHAPv2. Certificates must meet the documented Windows requirements.

**iOS 9+ and macOS 10.11+** support IKEv2 through Settings, a configuration profile, or an app with the NetworkExtension entitlement. Windows gateway configs work with small changes. Default strongSwan proposals work with recent releases; explicit ones, valid at least since iOS 14, are `ike=aes256-sha256-modp2048` and `esp=aes256-sha256`.

**PFS:** only iOS sends an ESP proposal with a DH group (and a second without); macOS sends only one without. To support both, make the group optional: `esp=aes256-sha256-modp2048-modpnone` (default since 6.0.2). Prefer modp2048 or ecp256 over modp1536, which may fail due to an unfixed bug.

## Checked
2026-11-04. Confirmed against the Windows and Apple client pages: supported features, the NegotiateDH2048_AES256 registry values, authentication options, iOS and macOS proposals and the PFS behaviour.

Method: documentation only; no commands were run.
