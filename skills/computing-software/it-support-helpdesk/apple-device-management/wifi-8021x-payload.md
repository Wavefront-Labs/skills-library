---
id: computing-software.it-support-helpdesk.apple-device-management.wifi-8021x-payload
name: wifi-8021x-payload
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, wifi-vpn, wifi-8021x-payload, wifi-payload, eap-tls]
level: practitioner
status: docs-checked
description: "Configure the Wi-Fi payload for WPA Enterprise and 802.1X with EAP-TLS, certificate identity and server trust on Apple devices."
sources:
  - "https://support.apple.com/guide/deployment/connect-to-8021x-networks-depabc994b84/web"
  - "https://support.apple.com/guide/deployment/dynamic-wep-wpa-enterprise-wpa2-settings-dep1c4b37ac2/web"
  - "https://raw.githubusercontent.com/apple/device-management/release/mdm/profiles/com.apple.wifi.managed.yaml"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# wifi-8021x-payload

Goal: auto-join enterprise Wi-Fi without prompts.
- Payload `com.apple.wifi.managed` (macOS 10.7 or later, iOS 4 or later; device and user channel on macOS; more than one allowed). Keys: `SSID_STR`, `AutoJoin` (default true), `EncryptionType` (WEP, WPA, WPA2, WPA3, Any or None; WPA2 allows WPA2 or WPA3 from iOS 16 and macOS 13), `PayloadCertificateUUID` (the client identity certificate payload), and `EAPClientConfiguration`.
- `EAPClientConfiguration`: `AcceptEAPTypes` (13 is EAP-TLS), `PayloadCertificateAnchorUUID` or `TLSTrustedCertificates` for trust, and `TLSTrustedServerNames`, where a wildcard "*" covers one name component and setting names disables dynamic trust.
- On macOS `SetupModes` is `System` or `Loginwindow`. The 802.1X page names the modes User, System, System + User, System + Login Window and Login Window; Apple recommends WPA3 with GCMP-256 at the login window.
- Client identity can come from an AD Certificate (macOS), ACME, PKCS#12 or SCEP payload. The trust certificate does not have to be in the same profile; it can be a standalone profile.
- Shared iPad uses the same EAP credential for every user.
- `CaptiveBypass` is iOS only (default false).
Practice: match EAP type, identity and trusted server names to the RADIUS server settings exactly.
Gotcha: `CaptiveBypass` has no effect on macOS.

## Checked

Date: 2026-11-07
Method: documentation only; no commands were run.
- Read in full: Apple Platform Deployment "Connect to 802.1X networks" and "Dynamic WEP, WPA Enterprise and WPA2 Enterprise settings"; the apple/device-management YAML for `com.apple.wifi.managed`.
- Removed as unconfirmed: "deploy the CA before the Wi-Fi payload" (the page says trust need not be in the same profile), "Add Captive Network and AutoJoin" (CaptiveBypass is iOS only), the SCEP-only identity, the prompt-on-missing-server-names gotcha, guest SSID advice and both Verify steps.
- The original sources were developer.apple.com pages that render with JavaScript and could not be read, so they were replaced.
