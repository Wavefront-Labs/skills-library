---
id: computing-software.networking-hardware-and-wireless.wifi-80211.wifi-passpoint-profile-lifecycle
name: wifi-passpoint-profile-lifecycle
category: computing-software
field: networking-hardware-and-wireless
product: wifi-80211
tags: [passpoint-profile-provisioning, passpoint-revocation, wifi-mdm-profiles]
level: practitioner
status: draft
description: "Deliver Passpoint or WPA-Enterprise Wi-Fi profiles to managed clients via MDM and revoke credentials cleanly."
sources:
  - https://www.wi-fi.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Profile lifecycle

- Deliver profiles with MDM (Apple Wi-Fi payload, Android/Windows management, Intune/Jamf) including the trusted CA and server names, so clients validate the RADIUS server.
- Certificates: issue per-device client certificates (via SCEP/ACME/internal CA) with a short enough lifetime and an automated renewal path.
- Revocation: disable the device in the identity store and use CRL/OCSP at the RADIUS server for EAP-TLS.
- Retire profiles when SSIDs change; stale profiles cause unexpected auto-joins.

## Verify
- [ ] A revoked certificate fails authentication on the next attempt.
