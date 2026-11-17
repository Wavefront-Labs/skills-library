---
id: computing-software.it-support-helpdesk.apple-device-management.scep-payload
name: scep-payload
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, scep, scep-payload, certificates, pki]
level: practitioner
status: docs-checked
description: "Request per-device certificates over SCEP with the com.apple.security.scep payload: exact key names, defaults, key usage values and retry behaviour."
sources:
  - "https://raw.githubusercontent.com/apple/device-management/release/mdm/profiles/com.apple.security.scep.yaml"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# scep-payload

Goal: automate a client certificate request from a SCEP server (for example for Wi-Fi or VPN).
- Payload type `com.apple.security.scep`; the settings sit in a `PayloadContent` dictionary. Available on iOS 4, macOS 10.7, tvOS 9, visionOS 1 and watchOS 3 and later; allowed with User Enrolment on iOS and macOS.
- Keys: `URL` (required), `Name` (a string the SCEP server understands, used to pick between CA certificates), `Subject` (array of OID/value pairs, for example `[ [ ["C", "US"] ], [ ["CN", "foo"] ] ]`), `Challenge` (a preshared secret), `CAFingerprint`, `SubjectAltName` (`rfc822Name`, `dNSName`, `uniformResourceIdentifier`, `ntPrincipalName`).
- Note the key names with spaces: `Key Type` (always `RSA`) and `Key Usage` (bitmask: `1` signing, `4` encryption, default `0`; some CAs such as Windows CA support only one of them). `Keysize` is 1024, 2048 or 4096, default 1024.
- `Retries` (default 3) is how often the device retries after a `PENDING` response; `RetryDelay` (default 10 seconds) is the wait between retries, with the first retry immediate. Both from macOS 10.10.
- macOS: `KeyIsExtractable` (default true; false blocks exporting the private key, from 10.13.4) and `AllowAllAppsAccess` (default false).
Practice: test with one device and check the CA's own logs for the request; choose a `Keysize` your CA and clients accept rather than the 1024 default.
Gotcha: `Retries` and `RetryDelay` only apply to `PENDING` responses; check your CA's own documentation for challenge lifetime.
Verify: the profile shows as installed on the device and the CA's own records show a certificate issued for the `Subject` you set (CA behaviour is outside Apple documentation).

## Checked

Date: 2026-11-07. Read in full: apple/device-management `com.apple.security.scep.yaml` (every key, default, range and OS minimum). Removed: NDES/Intune dynamic challenge claims, the ordering rule "trust, SCEP, then Wi-Fi", the `com.apple.security.root` ordering requirement, "renewal handled by the CA profile", the System keychain Verify the NDES expiry claim and the original Verify steps, none of which the page states. Corrected `KeyType` and `KeyUsage` to the real key names `Key Type` and `Key Usage`, and dropped them from a plain key list.
Method: documentation only; no commands were run.
