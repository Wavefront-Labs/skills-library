---
id: computing-software.cybersecurity-defensive.endpoint-security.lost-device-remote-wipe
name: lost-device-remote-wipe
category: computing-software
field: cybersecurity-defensive
product: endpoint-security
tags: [mobile-device-management, remote-wipe, lost-device, device-lock, activation-lock, retire-vs-wipe, find-my-device, incident-response]
level: practitioner
status: draft
description: "Handle lost and stolen devices: decide lock vs retire vs full wipe, execute via MDM, revoke sessions and keys, and document for breach assessment."
sources: ["Microsoft Learn - Remove devices by using wipe, retire, or manually unenrolling (Intune)", "CompTIA Security+ SY0-701 objective 4.1 (mobile solutions)", "NIST SP 800-124 Rev. 2 Guidelines for Managing the Security of Mobile Devices"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Lost device and remote wipe

**Goal:** when a laptop or phone is lost or stolen, data stays protected, access is cut quickly,
and you can show regulators that no breach notification is needed (or that it is).

## Immediate steps (within an hour of report)
1. **Record**: user, device ID/serial, last check-in time, location/time lost, what data it held, whether it was encrypted and locked.
2. **Revoke access**: sign out all sessions and revoke refresh tokens for the user (Entra `Revoke-MgUserSignInSession`), disable the device object, remove from VPN/Wi-Fi certificate trust (revoke device certificates).
3. **Lock** via MDM (Intune Remote lock, Jamf Lock Computer with PIN, Apple Lost Mode for supervised iOS with message and location).
4. **Decide wipe**:
   | Action | Effect | Use when |
   |---|---|---|
   | Retire / selective wipe | Removes corporate data and management | BYOD; device may be returned to owner |
   | Full wipe | Factory reset | Corporate device stolen or not recovered within agreed time |
   | Lock only | Keeps evidence | Device likely recoverable, or needed for investigation |
   Wipe commands execute when the device next connects; record command status.
5. Rotate secrets that were stored on the device outside managed stores (SSH keys, API tokens).

## Breach assessment
- Full-disk encryption on and device locked at the time: data generally considered protected (check encryption status reports at last check-in).
- Escrowed recovery keys show the device was encrypted; keep the evidence.
- If unencrypted or unlocked with sensitive data: involve privacy/legal.

## Gotchas
- Activation Lock (Apple) / Factory Reset Protection (Android) must be managed by the organisation (bypass codes escrowed), or recovered devices become bricks.
- Wiping destroys forensic evidence if theft is targeted; consult IR before wiping devices of high-risk users.
- Devices that never come online never execute the wipe: encryption is the real control.

## Verify
- [ ] Lost-device runbook tested quarterly with a test device.
- [ ] Each report has a closed record: actions, times, encryption status, assessment outcome.
