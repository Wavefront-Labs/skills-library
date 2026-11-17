---
id: engineering-technology.agricultural-and-biosystems-engineering.precision-agriculture-systems.edge-gateway-and-iot-data-pipeline
name: edge-gateway-and-iot-data-pipeline
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: precision-agriculture-systems
tags: [agricultural-and-biosystems-engineering, precision-agriculture-systems, iot-gateway, mqtt, edge-computing, time-series-database, store-and-forward, node-red, grafana, device-authentication, farm-iot]
level: advanced
status: verified
description: "Build an edge gateway and data pipeline for farm IoT: MQTT ingest, buffering, time sync, TLS and device identity, time-series storage, dashboards, alerts and updates."
sources:
  - "OASIS MQTT Version 3.1.1 (https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html)"
  - "Eclipse Mosquitto (https://mosquitto.org)"
  - "Grafana (https://grafana.com/docs/)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Edge gateway and data pipeline

**Goal:** sensor data that flows reliably from the field to storage and dashboards, survives outages and is secure.

## Architecture
1. Devices (LoRaWAN nodes, Modbus sensors, controllers) send to an edge gateway at the farm.
2. The gateway decodes payloads, adds metadata (device ID, location, units), buffers locally, and forwards via MQTT or HTTPS over cellular, fibre or satellite to a cloud or farm server.
3. A broker (such as Mosquitto or a managed MQTT service) receives the messages; a consumer writes them to a time-series database (for example InfluxDB or TimescaleDB); dashboards and alerts read from there (for example Grafana). Flow-based tools such as Node-RED are convenient for the gateway logic.

## Design rules
- Use a consistent schema: UTC timestamps in ISO 8601, a stable device ID, measurement name, value and unit; keep calibration offsets separate from raw values so you can reprocess later.
- Store-and-forward: the gateway keeps a local queue (disk, not RAM only) so the link outage does not lose data; use MQTT QoS 1 (at-least-once delivery, so duplicates are possible: OASIS MQTT 3.1.1 section 4.3.2) with persistent sessions where available, and make the consumer idempotent against duplicates.
- Time: sync the gateway clock using NTP or GNSS; device timestamps drift.
- Security: TLS for all links, unique credentials or certificates per device or per gateway, no default passwords, closed inbound ports, regular updates, and a way to revoke a compromised device. Separate the control network from the guest network. Keep secrets out of source repositories.
- Monitoring: heartbeat messages from each node and gateway, and an alert when one is missing; track battery and signal quality as data.
- Local control: do not make safety or irrigation control depend on the internet link; run the critical logic at the edge with local fallback.
- Retention and downsampling: raw data for a defined period, aggregates (hourly, daily) afterwards.

## Operations
Backups of the database and configuration; documented procedure for replacing a gateway; remote update with rollback; capacity and cost review of the cloud components.

## Verify
- [ ] Unplug the backhaul for an hour and confirm no data are lost on reconnection.
- [ ] A missing-device alert fires within the expected time.
- Unconfirmed: product choices; any equivalent tools work.
