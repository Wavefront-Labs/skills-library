---
id: computing-software.firmware-embedded-development.iot-protocols.ota-update-design
name: ota-update-design
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [ota-update-design, iot-ota, ota, firmware-update, delta-update, signing, iot-protocols]
level: practitioner
status: docs-checked
description: "IoT OTA update design: Design an update system with the RFC 9019 / SUIT architecture in mind."
sources:
  - https://datatracker.ietf.org/doc/html/rfc9019
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IoT OTA update design

**Goal:** Design an update system following the RFC 9019 firmware update architecture (IETF SUIT working group; informational).

## Steps
1. Name the roles: author (creates the image), device operator, network operator, trust provisioning authority (distributes trust anchors and authorisation policies), status tracker (client and server: announces new versions, reports device characteristics, can trigger the update), firmware server (stores images and manifests), firmware consumer (on-device: parses and verifies the manifest and stores the image) and bootloader. Authors do not upload to the firmware server or start updates directly; they make images available to device operators.
2. Authenticate and integrity-protect the image through a manifest (metadata about the image, protected against modification, identifying the author). Authentication and integrity protection MUST be used; confidentiality protection of the image is optional. Asymmetric cryptography is the common choice, symmetric credentials suit very constrained devices.
3. The device needs: an Internet stack for downloads (with congestion and flow control, fragmentation and reassembly, and ways to resume interrupted or corrupted transfers), the ability to write the image to persistent storage, a manifest parser that verifies a signature or MAC, the ability to unpack, decompress or decrypt the image, and a status tracker.
4. Decide how devices learn of updates: client polling, server push (quick response, but the device must stay reachable through NATs and firewalls) or a hybrid where the server notifies and the device pulls.
5. The architecture does not assume a transport (HTTP, CoAP, MQTT, BLE and others all work). If images are broadcast, security must be applied to the manifest and image rather than the link, and one manifest must not be acceptable to the wrong device.
6. An image may be a differential update; if so a dependency resolution step is needed before installation, since the base must be present.
7. Plan robustness: install so the update does not break the device, test it, and provide a recovery strategy when an update fails. Updates are energy-intensive on battery devices (radio plus flash writes).

## Gotcha
An update that fails mid-write with no recovery strategy can leave devices unusable; design the recovery path (for example keeping a known-good image) before shipping.

## Verify
- [ ] A tampered image or manifest is rejected
- [ ] A power failure mid-download recovers
- [ ] The status tracker shows which devices updated and which are pending

## Checked
2026-11-09. Read RFC 9019 sections 1 to 3: roles, manifest requirements, device components, update-notification modes, transport neutrality, broadcast constraints, differential update dependency note, robustness and energy concerns. Removed: specific algorithms (Ed25519, ECDSA P-256, SHA-256), anti-rollback counter, staged-rollout percentages, CoAP block-wise advice, the SUIT manifest RFC number (unconfirmed; RFC 9019 cites only an Internet-Draft) and the MCUboot source (the fetched page confirmed none of the retained claims).
Method: documentation only; no commands were run.
