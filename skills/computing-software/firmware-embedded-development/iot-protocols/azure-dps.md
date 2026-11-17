---
id: computing-software.firmware-embedded-development.iot-protocols.azure-dps
name: azure-dps
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [azure-dps, azure-iot, azure, dps, enrollment-group, attestation, iot-protocols]
level: practitioner
status: docs-checked
description: "Azure Device Provisioning Service: Auto-provision devices to the right IoT hub."
sources:
  - https://learn.microsoft.com/azure/iot-dps/about-iot-dps
  - https://learn.microsoft.com/azure/iot-dps/concepts-service
  - https://learn.microsoft.com/azure/iot-dps/concepts-symmetric-key-attestation
  - https://learn.microsoft.com/azure/iot-dps/how-to-use-allocation-policies
  - https://learn.microsoft.com/azure/iot-dps/concepts-device-reprovision
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure Device Provisioning Service

**Goal:** Auto-provision devices to the right IoT hub.

## Steps
1. Device connects to global endpoint global.azure-devices-provisioning.net with ID scope
2. Attestation: X.509 (individual or group enrollment), TPM (individual enrollment), symmetric key (in a group, a per-device key derived as the HMAC-SHA256 of the registration ID using the group key)
3. Allocation policies (portal names): evenly weighted distribution (the default), lowest latency, static configuration, custom (Azure Function); an enrollment can override the DPS default, and custom cannot be the instance default
4. DPS assigns a linked IoT hub and returns the assigned hub
5. Devices can provision over HTTPS, AMQP, AMQP over WebSockets, MQTT or MQTT over WebSockets
6. Reprovisioning policy on the enrollment handles moved devices: reprovision and migrate data (default for new enrollments), reprovision and reset to initial config, or never reprovision
7. Registration IDs are case-insensitive, up to 128 characters (64 for X.509 because of the certificate common name limit)

## Gotcha
The enrollment-group symmetric key can't be used directly for attestation and is a fleet-wide secret; derive a per-device key (ideally at the factory) and keep the group key off devices.

## Verify
- [ ] Registration returns assigned hub
- [ ] Derived key matches the one DPS recomputes
- [ ] Reprovision policy behaves as chosen after a hub change

## Checked
Confirmed 2026-11-08 against Microsoft Learn pages "About Azure IoT Hub Device Provisioning Service" (protocol list; read from the provisioning section down), "IoT Hub Device Provisioning Service terminology" (global endpoint with ID scope, attestation by enrollment type, ID lengths), "Symmetric key attestation" (derivation, group key not usable directly), "How to use allocation policies" and "IoT Hub Device reprovisioning concepts" (policy names and default). Removed: the claim that devices connect on MQTT port 8883 (no port is stated on these pages) and the disenroll check.
Method: documentation only; no commands were run.
