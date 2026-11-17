---
id: computing-software.it-support-helpdesk.apple-device-management.acme-device-attestation
name: acme-device-attestation
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, certificates, acme-device-attestation, acme, attestation]
level: practitioner
status: docs-checked
description: "Use the ACME Certificate payload with hardware-bound keys and Managed Device Attestation, and know which key type and size combinations Apple allows."
sources:
  - "https://support.apple.com/guide/deployment/depb95c66a07/web"
  - "https://support.apple.com/guide/deployment/dep28afbde6a/web"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# acme-device-attestation

Goal: issue certificates whose private key is bound to one device, with the device's properties attested to the CA.

- Payload identifier `com.apple.security.acme`. Works on iOS, iPadOS, Shared iPad device, macOS device and user channels, tvOS, watchOS 10 and visionOS 1.1, with User Enrolment, Device Enrolment and Automated Device Enrolment. More than one ACME payload may be delivered to a device.
- ACME is the modern alternative to SCEP, and ACME is required when you use Managed Device Attestation.
- Required settings: Client identifier, URL (the ACME server address including `https://`), `HardwareBound`, Key type and Key size. Optional: Extended Key Usage (array of dotted OIDs), Subject, Subject Alternative Name Type, Usage Flags (bit 0x01 digital signature, bit 0x10 key agreement) and `Attest`.
- Key rules: with `HardwareBound` set, the Secure Enclave generates the key pair, the private key cannot be exported, `KeyType` must be `ECSECPrimeRandom` and `KeySize` must be 256 or 384. `RSA` keys need `KeySize` from 1024 to 4096 in multiples of 8 and `HardwareBound` false. `ECSECPrimeRandom` accepts 192, 256, 384 or 521 (521, not 512).
- `Attest` true makes the device send attestations about the device and key to the ACME server; it requires `HardwareBound` true. The CA can validate the attested properties (for example the serial number) and cross-check its device inventory.
- Managed Device Attestation needs iOS 16, iPadOS 16.1, macOS 14 or tvOS 16 or later, on iPhone, iPad and Apple TV with the A11 Bionic chip or later and on Macs with Apple silicon.
- On a Mac, hardware-bound keys can be used for authentication with the MDM service, Microsoft Exchange, Kerberos, 802.1X networks, the built-in VPN client and built-in network relay.
- Setting names above are those Apple's page shows; each MDM service implements them differently, so check your vendor's documentation for how they are exposed.

Gotchas:
- Hardware-bound keys are removed when a device is erased or restored, so profiles that depend on them stop working until the profile is applied again.
- A failed attestation still gets a response, but some values or the whole attestation are omitted and the device gives no reason; treat that as a lower trust score, not a diagnosable error.
- User Enrolment omits serial number and UDID from attestation to protect privacy.

Verify:
- The payload meets the key rules above (hardware-bound means `ECSECPrimeRandom` with 256 or 384; `Attest` means hardware-bound).
- The CA's ACME service is configured to request attestation, and the issued certificate's properties match the device.

## Checked

Date: 2026-11-07. Read in full: Apple Platform Deployment pages "Automated Certificate Management Environment (ACME) device management payload settings for Apple devices" (supported identifier, OS and enrolment lists, every settings-table row) and "Managed Device Attestation for Apple devices" (hardware, OS minimums, ACME section, failed attestations, User Enrolment note). Removed as unconfirmed: the keys `DirectoryURL` and `ClientIdentifier` (the page names the settings Client identifier and URL), the claim that attestation fails on virtual machines, the "confirm" placeholders, the SCEP fallback advice and the developer.apple.com link (JavaScript page, unreadable). Verify steps were rewritten to checkable rules.
Method: documentation only; no commands were run.
