---
id: computing-software.messaging-and-integration.mosquitto.client-v5-properties
name: client-v5-properties
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [mqtt5-properties, property-option, user-property]
level: advanced
status: docs-checked
description: "Attach MQTT v5 properties with -D command identifier value in the Mosquitto client tools."
sources:
  - https://mosquitto.org/man/mosquitto_pub-1.html
  - https://mosquitto.org/man/mosquitto_sub-1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: send MQTT v5 properties from the command line.

`-D, --property` has two forms:

```
-D command identifier value
-D command identifier name value
```

`command` is one of CONNECT, PUBLISH, PUBACK, PUBREC, PUBCOMP, SUBSCRIBE, UNSUBSCRIBE, DISCONNECT, AUTH or WILL. `identifier` is the spec property name with `-` as word separator, e.g. `payload-format-indicator`. `name` is only used for `user-property`, as the first string of the pair; `value` is the second. Using `-D` makes the client an MQTT v5 client.

Properties documented for mosquitto_pub:
- CONNECT: authentication-data, authentication-method, maximum-packet-size, receive-maximum, request-problem-information, request-response-information, session-expiry-interval (use `-x` instead), topic-alias-maximum, user-property.
- PUBLISH: content-type, correlation-data, message-expiry-interval, payload-format-indicator, response-topic, topic-alias, user-property.
- DISCONNECT: session-expiry-interval, user-property.
- WILL: content-type, correlation-data, message-expiry-interval, payload-format-indicator, response-topic, user-property, will-delay-interval.

```
mosquitto_pub -t a/b -m hello -D PUBLISH user-property source sensor1 -D PUBLISH message-expiry-interval 60
```

Binary data properties (authentication-data, correlation-data) are treated as strings.

mosquitto_sub accepts the same `-D` option with the same command list. Its documented properties are the CONNECT, DISCONNECT and WILL ones above plus `user-property` for SUBSCRIBE and UNSUBSCRIBE (it has no PUBLISH properties).

## Checked

2026-11-08. Confirmed against the mosquitto_pub and mosquitto_sub man pages: both -D forms, the command list, identifier naming, the pub property lists and the binary-data note. Replaced a closing claim that mosquitto_rr and mosquitto_ctrl pages share the command set (not read) with what the sub page lists.

Method: documentation only; no commands were run.
