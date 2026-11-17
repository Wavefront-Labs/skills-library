---
id: computing-software.messaging-and-integration.rabbitmq.mqtt-plugin
name: mqtt-plugin
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, mqtt-plugin, rmq-mqtt]
level: practitioner
status: docs-checked
description: "Enable the MQTT plugin and understand its mapping of topics to the amq.topic exchange and QoS limits."
sources:
  - https://www.rabbitmq.com/docs/mqtt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MQTT plugin

**Goal:** Accept MQTT devices on RabbitMQ.

## Steps
1. `rabbitmq-plugins enable rabbitmq_mqtt`; default ports 1883 plain, 8883 TLS (`mqtt.listeners.ssl.default`).
2. MQTT topic levels (`/`) are translated to AMQP routing key levels (`.`); topics containing dots do not work as expected.
3. Messages go through the topic exchange `amq.topic` (`mqtt.exchange`); each subscriber gets a queue named `mqtt-subscription-<client ID>qos[0|1]`. Non-clean sessions keep their queues and subscriptions.
4. QoS 0 and 1 are supported. QoS 2 is unsupported: MQTT 3.x publishes are downgraded to QoS 1, and an MQTT 5 client is disconnected with reason code 155.

## Failure modes
- With no credentials the plugin uses `guest`, which only accepts localhost; create real users for remote clients.
- Short-lived clients with non-clean sessions can leave queues and messages behind.

## Verify
- Connect a client and see it in `rabbitmqctl list_connections`.

## Checked

Date: 2026-11-02. Confirmed on the MQTT guide: ports, mapping, queue naming, QoS support, guest behaviour. Removed: "clean_session=false" wording, retained-message version claim (see the guide's Retained Messages section), `list_connections protocol` column.

Method: documentation only; no commands were run.
