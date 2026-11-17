---
id: computing-software.firmware-embedded-development.iot-protocols.chirpstack-setup
name: chirpstack-setup
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [chirpstack-setup, lorawan-network-servers, chirpstack, gateway-bridge, device-profile, mqtt, iot-protocols]
level: practitioner
status: docs-checked
description: "ChirpStack setup: Stand up ChirpStack v4 and add a device."
sources:
  - https://www.chirpstack.io/docs/getting-started/docker.html
  - https://www.chirpstack.io/docs/guides/connect-device.html
  - https://www.chirpstack.io/docs/chirpstack/integrations/mqtt.html
  - https://www.chirpstack.io/docs/chirpstack/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ChirpStack setup

**Goal:** Stand up ChirpStack v4 and add a device.

## Steps
1. Clone https://github.com/chirpstack/chirpstack-docker, follow its README for configuration (EU868 is configured by default) and run docker compose up; the first run may log errors while the database initialises
2. The example environment includes a Gateway Bridge listening for UDP packet-forwarder data on port 1700 and one with the Basics Station backend on port 3001
3. For a gateway running the MQTT Forwarder or Gateway Bridge, make its topic-prefix or topic setting match the ChirpStack region
4. In chirpstack.toml, enabled_regions lists the region names to enable; each must match the name of a [[regions]] entry (for example in region_eu868.toml); the API and UI bind to 0.0.0.0:8080 by default
5. Log in at http://localhost:8080 with admin / admin by default and change the password
6. Create a device-profile (activation type, LoRaWAN version, regional parameters revision), an Application, then a Device with its DevEUI; OTAA devices need root-keys unless an external join-server is used
7. MQTT integration: events on application/APPLICATION_ID/device/DEV_EUI/event/EVENT, downlinks on application/APPLICATION_ID/device/DEV_EUI/command/down; APPLICATION_ID is not the AppEUI/JoinEUI

## Gotcha
A gateway's topic or topic-prefix must match the ChirpStack region; the docs call this out for the MQTT Forwarder and Gateway Bridge. A MIC error in the Device data tab means the root or session keys are wrong.

## Verify
- [ ] Gateway LoRaWAN frames tab shows JoinRequest then JoinAccept for an OTAA device
- [ ] Device data tab shows Join and Up events
- [ ] mosquitto_sub on the event/up topic shows the uplink

## Checked
Confirmed 2026-11-08 against the ChirpStack "Quickstart Docker Compose", "Connecting a device" and "MQTT" pages (all read in full) and the configuration reference (searched, not read in full: postgresql and redis sections, enabled_regions, API bind 0.0.0.0:8080, region_eu868.toml example heading). Removed as unconfirmed: the component list as a whole (Mosquitto and Redis appear in config but the compose contents were not listed), HTTP and InfluxDB integrations, and the claim that a topic mismatch gives "connected but no uplinks".
Method: documentation only; no commands were run.
