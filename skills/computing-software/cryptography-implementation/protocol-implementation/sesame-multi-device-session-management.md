---
id: computing-software.cryptography-implementation.protocol-implementation.sesame-multi-device-session-management
name: sesame-multi-device-session-management
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [protocol-implementation, cryptography-implementation, sesame, e2ee, multi-device, signal-protocol, session-management, double-ratchet]
level: sme
status: docs-checked
description: "Manage E2EE sessions across multiple devices with Signal's Sesame algorithm: per-device sessions, active session selection, stale device handling and fan-out."
sources: ["https://signal.org/docs/specifications/sesame/", "https://signal.org/docs/specifications/doubleratchet/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sesame multi-device session management

Double Ratchet secures one session between two devices. Real users have several devices, devices get replaced, and
both sides may start sessions simultaneously. Sesame specifies how to keep this consistent.

## Model
- Each user has a set of devices (device IDs) with identity keys; each local device keeps, per remote device, a
  list of sessions with one marked active.
- Each DeviceRecord holds an active session and/or an ordered list of inactive sessions.
- Sending: for each non-stale DeviceRecord of the recipient that has an active session, encrypt the plaintext with
  that active session (a device without one gets a new initiating session). The messages go to the server with a list
  of DeviceIDs; if the server reports old or missing devices, the sender marks those records stale and retries.
- Receiving: a message received on an inactive session makes that session the new active session.
- Simultaneous initiation leaves two sessions; the active/inactive rule converges each device on one session per
  remote device.

## Device changes
- New device for a contact: present as a safety number change or "new device" notice per your UX policy.
- Removed device: mark its record stale; a stale record may be deleted, and the recommended policy is to keep it
  until its stale timestamp is older than MAXLATENCY so delayed messages can still be decrypted.
- Bound the inactive sessions list: Sesame allows deleting sessions from its tail when it grows too large, and
  defines MAXSEND and MAXRECV session lifetimes (MAXRECV greater than MAXSEND + 2 * MAXLATENCY).

## Pitfalls
- Encrypting once with a shared key for all devices gives up the per-session ratcheting that each device pair has.
- Treating server device lists as authoritative without verifying identity keys lets a malicious server add a
  device you did not authorise.

## Verify
- [ ] Tests: simultaneous initiation, device added mid-conversation, stale device list retries, message
  reordering across session switch.

## Checked

2026-11-01. Confirmed against the Sesame specification (DeviceRecord with active and inactive sessions, inactive
session becoming active on receipt, simultaneous initiation convergence, send procedure and retry on old devices,
stale records and MAXLATENCY, tail deletion of inactive sessions, MAXSEND/MAXRECV). Removed: the Signal 409/410
status codes, the example cap of 40 inactive sessions, own-device fan-out, the PreKey-message-from-unknown-session
detail, and the key-transparency remark (not in the sources).
Method: documentation only; no commands were run.
