---
id: computing-software.firmware-embedded-development.iot-protocols.aws-iot-device-shadow
name: aws-iot-device-shadow
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [aws-iot-device-shadow, aws-iot-core, aws-iot, device-shadow, desired, reported, delta, iot-protocols]
level: practitioner
status: docs-checked
description: "AWS IoT Device Shadow: desired, reported and delta state, named vs classic shadows, offline behaviour and out-of-order delta handling."
sources:
  - https://docs.aws.amazon.com/iot/latest/developerguide/iot-device-shadows.html
  - https://docs.aws.amazon.com/iot/latest/developerguide/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS IoT Device Shadow

**Goal:** Share device state between a device and apps even when the device is offline.

## Steps
1. A thing has no shadow until one is created explicitly (console, reserved MQTT topics, Device Shadow REST API, or the AWS CLI).
2. Every shadow has a reserved MQTT topic and HTTP URL supporting get, update and delete.
3. The JSON document has a state property with desired (written by apps), reported (written by the device) and delta (computed by AWS IoT as the difference). Documents carry a version and timestamp.
4. Rule of thumb from the page: devices write only to reported; apps and other cloud services write only to desired.
5. Flow: an app updates desired, AWS IoT publishes the change to the device, the device updates itself and publishes reported.
6. If the device is offline, apps can still read and write the shadow; on reconnect the device receives the current state and publishes its update.
7. A thing can have several named shadows and at most one unnamed (classic) shadow. Named shadows split state into groups and allow per-group access policies. Choose one type and stick with it, since the APIs differ.
8. Delta messages can arrive out of order. State in them is cumulative, so discard any message with a version older than the one you track.
9. To shrink delta messages, use a rule that selects only needed fields from the shadow update/delta topic and republishes them.
10. For devices often offline that need deltas after reconnect, use the persistent session feature.

## Gotcha
Update permission must be limited to trusted apps and devices; otherwise keys in the shadow state can change unexpectedly.

## Verify
- [ ] Device receives a delta set while it was offline, after reconnect
- [ ] Device reports state and the delta clears
- [ ] An older-version delta is ignored

## Checked

2026-11-08. Confirmed on the AWS Device Shadow page: creation methods, get/update/delete, desired/reported/delta, writer roles, offline behaviour, named vs unnamed, message-order example, rule-based trimming, persistent sessions. Removed as unsupported by the page: the full topic list (accepted, rejected, delta, documents suffixes are on a linked page), the 8 KB size limit, and the "persistent delta loop" gotcha (replaced with the page's permission warning). The service root URL is a landing page and was not relied on.
Method: documentation only; no commands were run.
