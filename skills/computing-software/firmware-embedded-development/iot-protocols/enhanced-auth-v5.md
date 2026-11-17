---
id: computing-software.firmware-embedded-development.iot-protocols.enhanced-auth-v5
name: enhanced-auth-v5
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [enhanced-auth-v5, mqtt-security, mqtt5, enhanced-auth, authentication-method, iot-protocols]
level: practitioner
status: docs-checked
description: "MQTT 5 enhanced authentication: Use challenge-response auth such as SCRAM in MQTT 5."
sources:
  - https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MQTT 5 enhanced authentication

**Goal:** Use challenge-response auth such as SCRAM in MQTT 5.

## Steps
1. CONNECT includes Authentication Method (e.g. SCRAM-SHA-256) and Authentication Data
2. Broker replies with AUTH packet reason 0x18 Continue authentication
3. Loop until CONNACK 0
4. Client may send AUTH 0x19 to re-authenticate on a live connection
5. Both ends must support the method; unknown method gives 0x8C Bad authentication method

## Gotcha
Both ends must support the chosen method; a server that does not returns 0x8C Bad authentication method.

## Verify
- [ ] Wrong credentials fail with 0x86 or 0x87
- [ ] Re-auth works without dropping session

## Checked

2026-11-03. Confirmed in the OASIS MQTT 5.0 specification: Authentication Method and Authentication Data properties, AUTH reason codes 0x18 Continue authentication and 0x19 Re-authenticate, 0x8C Bad authentication method, 0x86 Bad User Name or Password, 0x87 Not authorized, SCRAM as an example of challenge/response. Removed: the Mosquitto configuration source (page unreachable) and the client-library support claim.
Method: documentation only; no commands were run.
