---
id: computing-software.firmware-embedded-development.iot-protocols.azure-iot-hub-twins-methods
name: azure-iot-hub-twins-methods
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [azure-iot-hub-twins-methods, azure-iot, azure, device-twin, direct-method, c2d, iot-protocols]
level: practitioner
status: docs-checked
description: "Azure IoT Hub twins and direct methods: Use twins and methods for configuration and commands."
sources:
  - https://learn.microsoft.com/azure/iot-hub/iot-hub-devguide-device-twins
  - https://learn.microsoft.com/azure/iot-hub/iot-hub-devguide-direct-methods
  - https://learn.microsoft.com/azure/iot-hub/iot-hub-mqtt-support
  - https://learn.microsoft.com/azure/iot-hub/iot-hub-devguide-messages-d2c
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure IoT Hub twins and direct methods

**Goal:** Use twins and methods for configuration and commands.

## Steps
1. Device twin JSON: tags (service only), properties.desired, properties.reported
2. Twin size limits: 8 KB for tags, 32 KB each for properties/desired and properties/reported; keys up to 1 KB, string values up to 4 KB, depth up to 10; operations that exceed a limit are rejected
3. Direct methods are synchronous request/response, HTTPS from the cloud side; timeout defaults to 30 s and is settable from 5 to 300 s; request and response payload up to 128 KB
4. Cloud-to-device messages for async commands
5. MQTT: a device subscribes to $iothub/twin/res/# then sends an empty message to $iothub/twin/GET/?$rid={request id}; telemetry goes to devices/{device-id}/messages/events/
6. Message routing endpoints include the built-in messages/events endpoint, Storage containers, Service Bus queues and topics, and Event Hubs
7. Twin change notifications need a route with data source twinChangeEvents; none exists by default
8. On connect a device subscribes to desired-property notifications, then retrieves the full desired document, and ignores notifications with a $version at or below that document's

## Gotcha
Twins are for last-known state and configuration; reported properties suit "last value" data, while device-to-cloud messages suit time-series telemetry. Treating twin properties as a telemetry channel risks throttling and size limits.

## Verify
- [ ] Desired property change triggers callback
- [ ] Method returns 200
- [ ] Routing endpoint receives telemetry

## Checked
Confirmed 2026-11-08 against Microsoft Learn pages "Understand and use device twins in IoT Hub" (read in full), "Understand and invoke direct methods from IoT Hub" (first 40 lines: lifecycle, timeout, payload size), "IoT Hub MQTT support" (twin and telemetry topics, partial read via search) and "IoT Hub message routing" (endpoint list). Removed: the "8 KB for each properties section" figure (the page says 32 KB), and the SAS token expiry step, which none of these pages state.
Method: documentation only; no commands were run.
