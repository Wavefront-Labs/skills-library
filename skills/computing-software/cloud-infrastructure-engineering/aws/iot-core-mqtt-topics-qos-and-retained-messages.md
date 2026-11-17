---
id: computing-software.cloud-infrastructure-engineering.aws.iot-core-mqtt-topics-qos-and-retained-messages
name: iot-core-mqtt-topics-qos-and-retained-messages
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, iot-core, retained-messages, mqtt-qos, topic-design, persistent-sessions, mqtt5]
level: practitioner
status: docs-checked
description: "Use MQTT on AWS IoT Core well: topic namespace design, QoS 0/1 behaviour, persistent sessions, retained messages, MQTT 5 features, limits and policy-scoped topics."
sources: ["https://docs.aws.amazon.com/iot/latest/developerguide/mqtt.html", "https://docs.aws.amazon.com/iot/latest/developerguide/topics.html", "https://docs.aws.amazon.com/iot/latest/developerguide/retained-message-policy-examples.html", "https://docs.aws.amazon.com/general/latest/gr/iot-core.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IoT Core MQTT: topics, QoS and retained messages

## 1. Topic design
- Hierarchical, device-scoped: `dt/<app>/<site>/<thingName>/telemetry` (data),
  `cmd/<app>/<thingName>/req` and `.../res` (commands), with a leading type segment
  (`dt`, `cmd`, `evt`) as a naming convention of your own.
- Put the **thing name** (client ID) in the topic so IoT policies can scope with policy
  variables: `arn:aws:iot:<region>:<acct>:topic/dt/app/*/${iot:Connection.Thing.ThingName}/*`.
- A topic or topic filter can contain at most 7 forward slashes (the three mandatory Basic
  Ingest segments are excluded) and the topic name at most 256 bytes of UTF-8; avoid a
  leading `$` (reserved for AWS IoT Core: shadows, `$aws/rules/...` Basic Ingest).
- Wildcards for subscribers only: `+` single level, `#` multi-level (last).
- **Basic Ingest** (`$aws/rules/<ruleName>/...`) sends a publish straight to a rule instead
  of through the broker, when no device needs to subscribe; see "Reducing messaging costs with
  Basic Ingest" in the guide.

## 2. QoS
- **QoS 0**: at most once, no ack. Cheapest; telemetry where loss is acceptable.
- **QoS 1**: at least once with PUBACK; duplicates possible, handle idempotently.
- QoS 2 is **not supported** by IoT Core.
- Requesting QoS 2 gets no PUBACK or SUBACK. IoT Core retries unacknowledged QoS 1 deliveries to a
  connected client for up to one hour (MQTT 3) or sixteen minutes (MQTT 5).

## 3. Persistent sessions
Connect with `cleanSession=false` (MQTT 3.1.1) or `cleanStart=false` + session expiry
(MQTT 5): IoT Core stores subscriptions and queues QoS 1 messages for an offline device until
the session expires. In MQTT 3 the account-wide expiry defaults to one hour (3,600 s) and can be
raised through the limit-increase process; in MQTT 5 you set a Session Expiry Interval per
session. The timer starts when the broker sees the disconnect, and a session can last up to 30
minutes longer than the limit. Queued messages are limited to 500 per second per account, and
messages queued for a session that expires are discarded but still billed. A persistent session
cannot be resumed across MQTT 3 and MQTT 5.

## 4. Retained messages
Publish with the RETAIN flag: the broker stores the **last** message per topic and sends it
to new subscribers immediately. Use for current configuration/state that late joiners need
(e.g. `cfg/app/<thing>/desired`). Device Shadow is the richer alternative for desired vs
reported state with versioning.
```bash
aws iot-data publish --topic cfg/app/sensor-42/desired --qos 1 --retain \
  --cli-binary-format raw-in-base64-out --payload '{"interval":30}'
aws iot-data list-retained-messages
aws iot-data get-retained-message --topic cfg/app/sensor-42/desired
```
Delete a retained message by publishing an empty (0-byte) payload with RETAIN to the topic. Only
one retained message is kept per topic. A new subscriber receives it only when subscribing to the
exact topic name (a wildcard filter does not deliver it). Limits: 100,000 retained messages per
account by default and 1 retained publish per second per topic. The IoT policy needs
`iot:RetainPublish` (and `iot:GetRetainedMessage` / `iot:ListRetainedMessages` for the APIs).

## 5. MQTT 5 features on IoT Core
User properties, message expiry, request/response (response topic + correlation data),
topic aliases, shared subscriptions (`$share/group/topic`) for load-balanced consumers,
reason codes for better error handling.

## 6. Limits to design around
Payload size 128 KB per publish; 100 publish requests per second per connection (inbound and
outbound, excess discarded); 50 subscriptions per connection and 8 per SUBSCRIBE request; 100
unacknowledged QoS 1 publishes in each direction per client; MQTT 5 topic alias values up to 8;
WebSocket connections last at most 24 hours. These are the default quotas on the AWS General
Reference IoT Core page; request increases early for fleet launches.

## Verify
- [ ] Topic policies scope each device to its own thing-name topics; a device cannot publish to another's topics.
- [ ] Offline device receives queued QoS 1 messages on reconnect within session expiry.
- [ ] Retained config delivered to a newly subscribed client; deletion via empty retained publish works.

## Checked

2026-10-27, AWS documentation (current release as read on that date). AWS IoT Core Developer Guide MQTT page (QoS, persistent sessions, retained messages), topics and retained-message policy pages, AWS General Reference IoT Core quotas page, botocore iot-data model. Fixed: the topic limit is 7 forward slashes (not 8); the persistent-session expiry default is 3,600 s in MQTT 3, adjustable by limit increase, with a per-session interval in MQTT 5 (the skill claimed configurable up to 7 days, which no page states); wildcard subscriptions do not receive retained messages on subscribe; added the retained message limits (100,000 per account default, 1 per second per topic). Confirmed: QoS 2 unsupported, 256-byte topic, 128 KB payload, 100 publishes per second per connection, 50 subscriptions per connection, retained and persistent session behaviour, iot:RetainPublish, iot:GetRetainedMessage, iot:ListRetainedMessages, iot-data publish retain flag. Removed pricing statements and the unsourced lower-of-QoS delivery claim.
Method: documentation only; no commands were run.
