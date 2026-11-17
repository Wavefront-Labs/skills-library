---
id: computing-software.cloud-infrastructure-engineering.aws.greengrass-stream-manager-and-local-mqtt
name: greengrass-stream-manager-and-local-mqtt
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, iot, greengrass, stream-manager, local-mqtt, mqtt-bridge, edge-buffering, client-devices]
level: practitioner
status: docs-checked
description: "Buffer and export edge data with Greengrass v2 stream manager (local streams to Kinesis, S3, SiteWise) and connect local devices via the Moquette or EMQX broker and MQTT bridge."
sources: ["https://docs.aws.amazon.com/greengrass/v2/developerguide/manage-data-streams.html", "https://docs.aws.amazon.com/greengrass/v2/developerguide/stream-manager-component.html", "https://docs.aws.amazon.com/greengrass/v2/developerguide/work-with-streams.html", "https://docs.aws.amazon.com/greengrass/v2/developerguide/stream-export-configurations.html", "https://docs.aws.amazon.com/greengrass/v2/developerguide/mqtt-bridge-component.html", "https://docs.aws.amazon.com/greengrass/v2/developerguide/client-device-auth-component.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Greengrass stream manager and local MQTT

## Stream manager
Deploy component `aws.greengrass.StreamManager`; your component uses the Stream Manager SDK:
```python
from stream_manager import (StreamManagerClient, MessageStreamDefinition, StrategyOnFull,
                            ExportDefinition, KinesisConfig, Persistence)
client = StreamManagerClient()
client.create_message_stream(MessageStreamDefinition(
    name="telemetry", max_size=268435456, stream_segment_size=16777216,
    strategy_on_full=StrategyOnFull.OverwriteOldestData, persistence=Persistence.File,
    export_definition=ExportDefinition(kinesis=[KinesisConfig(identifier="toKds",
        kinesis_stream_name="plant-telemetry", batch_size=500)])))
client.append_message("telemetry", json.dumps(reading).encode())
```
- `persistence` defaults to `File` (saved to the file system so data survives restarts); stream manager retries failed exports at
  intervals of up to five minutes with no retry limit.
- Export targets: Kinesis Data Streams, S3 (uploaded from local files, with a multipart threshold) and IoT SiteWise asset
  properties. IoT Analytics channels were discontinued on 2025-12-15; remove any `IoTAnalyticsConfig` exports. HTTP is not a
  listed destination.
- `max_size` defaults to 256 MB (268435456) and `stream_segment_size` to 16 MB; `strategy_on_full` is required:
  `OverwriteOldestData` or `RejectNewData`. Size `max_size` to the longest outage you must survive at your data rate.
- Component recipe needs a dependency on StreamManager. Grant the token exchange role the matching actions:
  `kinesis:PutRecords` (plus `kinesis:ListShards` from stream manager 2.2.1 on for shard-aware export; the Kinesis stream
  must be in the same account and Region as the core device), `iotsitewise:BatchPutAssetPropertyValue`,
  or `s3:PutObject`, `s3:AbortMultipartUpload`, `s3:ListMultipartUploadParts`.
- Stream manager needs at least 70 MB RAM beyond the Greengrass Core software. Components use the Stream Manager SDK
  (Java, Node.js or Python, v1.1.0 or later).

## Local MQTT for client devices
Components:
- `aws.greengrass.clientdevices.Auth`: authenticates and authorizes client devices.
- Broker: `aws.greengrass.clientdevices.mqtt.Moquette` (MQTT 3.1.1) or `aws.greengrass.clientdevices.mqtt.EMQX` (MQTT 5).
- `aws.greengrass.clientdevices.IPDetector` so devices can find the core device's endpoints.
- `aws.greengrass.clientdevices.mqtt.Bridge`: relay topics between local broker, IoT Core and Greengrass IPC:
```json
{"mqttTopicMapping":{
  "toCloud":{"topic":"sensors/+/temp","source":"LocalMqtt","target":"IotCore"},
  "toComponents":{"topic":"sensors/+/temp","source":"LocalMqtt","target":"Pubsub"}}}
```
- Local components subscribe via IPC (`Pubsub`); devices keep working when the internet is down.

## Pattern
Devices -> local broker -> bridge to Pubsub -> processing component (filter/aggregate) -> stream manager -> Kinesis/S3 when online.

## Gotchas
- Disk on the core device fills if streams are oversized; monitor free space.
- Client device certificates must be associated with the core device (`batch-associate-client-device-with-core-device`).
- Bridge loops: when mapping a topic in both directions with an MQTT 5 broker, use the bridge `mqtt5RouteOptions` setting
  `noLocal` to avoid forwarding messages the bridge itself published; otherwise use distinct topic prefixes.

## Verify
- [ ] Unplug the network for 10 minutes; data appears in Kinesis after reconnect, no gaps.
- [ ] A local test device publishes to the broker and the message reaches IoT Core via the bridge.

## Checked

2026-10-27, AWS documentation (current release as read on that date). AWS IoT Greengrass V2 Developer Guide stream manager component and SDK pages (table of contents read for page names), export configurations, MQTT bridge, Moquette, EMQX, IP detector and client device association pages. Fixed: export destinations are Kinesis Data Streams, S3 and IoT SiteWise (the HTTP target was not documented) and IoT Analytics channels were discontinued on 2025-12-15; stream defaults (max_size 256 MB, segment 16 MB, File persistence); added the noLocal bridge option for loop prevention and the kinesis:ListShards permission for newer stream manager versions. Confirmed: component names for Auth, Moquette (MQTT 3.1.1), EMQX (MQTT 5), IPDetector and Bridge, mqttTopicMapping with LocalMqtt, IotCore and Pubsub, batch-associate-client-device-with-core-device, 70 MB RAM, SDK v1.1.0 or later, export IAM actions.
Method: documentation only; no commands were run.
