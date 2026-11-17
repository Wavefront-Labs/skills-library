---
id: computing-software.firmware-embedded-development.iot-protocols.paho-reconnect-patterns
name: paho-reconnect-patterns
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [paho-reconnect-patterns, mqtt-client-practice, paho, reconnect, backoff, iot-protocols]
level: practitioner
status: docs-checked
description: "MQTT client reconnect patterns: Make clients resilient across outages."
sources:
  - https://eclipse.dev/paho/files/paho.mqtt.python/html/client.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MQTT client reconnect patterns

**Goal:** Make clients resilient across outages.

## Steps
1. Paho Python reconnects automatically while reconnect_on_failure is true (the default) and a network loop runs; `reconnect_delay_set(min_delay=1, max_delay=120)` sets an exponential backoff that doubles each attempt and resets after a successful CONNACK; the page does not describe jitter, so add random jitter yourself if many clients reconnect together
2. Re-subscribe in on_connect, or check the session-present flag passed to it: it tells you whether the broker still holds the session
3. For a persistent session use clean_session False (MQTT 3.1.1) or clean_start False (MQTT 5.0) and QoS 1 for commands
4. Use loop_start (a thread running loop_forever) or loop_forever, which handles reconnecting; connect_async pairs with loop_start for a non-blocking start; loop_forever raises OSError if the first connection fails unless retry_first_connection is True
5. Bound your own offline publish queue and decide what to drop first
6. Use a stable client id: an empty client id requires clean_session True

## Gotcha
Fleet-wide synchronized reconnects after a broker restart can overload the broker; spread them with jitter on top of the doubling backoff.

## Verify
- [ ] Broker restart: all clients return within the backoff cap
- [ ] Subscriptions restored
- [ ] Queue bounded

## Checked

2026-11-03. Confirmed in the Paho Python client reference: reconnect_on_failure default, reconnect_delay_set defaults and doubling behaviour, loop_start and loop_forever behaviour, retry_first_connection, connect_async, clean_session and clean_start, the session-present flag, and the empty client id rule. Removed: the "1 s to 5 min" range (default max is 120 s) and the statement that Paho applies jitter.
Method: documentation only; no commands were run.
