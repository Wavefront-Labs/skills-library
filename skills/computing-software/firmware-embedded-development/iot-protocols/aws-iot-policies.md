---
id: computing-software.firmware-embedded-development.iot-protocols.aws-iot-policies
name: aws-iot-policies
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [aws-iot-policies, aws-iot-core, aws-iot, iot-policy, thing-name, policy-variables, iot-protocols]
level: practitioner
status: docs-checked
description: "AWS IoT policies and authentication: Write least-privilege IoT policies."
sources:
  - https://docs.aws.amazon.com/iot/latest/developerguide/iot-policies.html
  - https://docs.aws.amazon.com/iot/latest/developerguide/protocols.html
  - https://docs.aws.amazon.com/iot/latest/developerguide/thing-policy-variables.html
  - https://docs.aws.amazon.com/iot/latest/developerguide/pub-sub-policy.html
  - https://docs.aws.amazon.com/general/latest/gr/iot-core.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS IoT policies and authentication

**Goal:** Write least-privilege IoT policies.

## Steps
1. MQTT with an X.509 client certificate connects on port 8883, or on port 443 with ALPN protocol name x-amzn-mqtt-ca
2. Policy actions iot:Connect, iot:Publish, iot:Subscribe, iot:Receive with resource ARNs
3. Use policy variables: arn:aws:iot:REGION:ACCOUNT:topic/dev/${iot:Connection.Thing.ThingName}/*
4. Restrict Connect to client ID equal to thing name: client/${iot:Connection.Thing.ThingName}
5. Subscribe uses topicfilter ARN, publish and receive use topic ARN
6. Quotas (AWS General Reference, AWS IoT Core service quotas): MQTT payload 128 KB, client ID 128 bytes of UTF-8, 8 subscriptions per SUBSCRIBE request, 50 subscriptions per connection (adjustable)
7. Thing policy variables only resolve for MQTT and MQTT over WebSocket; with a certificate attached to several things, the MQTT client ID must exactly match the thing name
8. Policy changes can take 6 to 8 minutes to become effective because AWS IoT caches policy documents

## Gotcha
Policies using * on topic resources let any device read all others; use thing-name variables.

## Verify
- [ ] Device cannot publish to a neighbour topic
- [ ] Connect with wrong client ID is refused
- [ ] IoT policy simulator clean

## Checked
Confirmed 2026-11-08 against AWS IoT Core Developer Guide pages "Device communication protocols", "AWS IoT Core policies", "Thing policy variables", "Publish/Subscribe policy examples" and the AWS General Reference AWS IoT Core quotas page. Removed: the "ats" endpoint remark (not stated on the pages read) and the "confirm quotas" hedge.
Method: documentation only; no commands were run.
