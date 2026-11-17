---
id: computing-software.messaging-and-integration.mosquitto.dynsec-acl-types
name: dynsec-acl-types
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [acl-types, subscribe-literal, subscribe-pattern, pattern-substitution, subscribeliteral]
level: advanced
status: docs-checked
description: "Choose between publishClientSend, publishClientReceive, subscribeLiteral/Pattern and unsubscribeLiteral/Pattern ACL types."
sources:
  - https://mosquitto.org/documentation/dynamic-security/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick the correct ACL type for a rule.

Each ACL has a topic, a priority, and allow or deny. Types:

- `publishClientSend`: may a device publish to this topic. Wildcards allowed, so `topic/#` covers `topic` and below.
- `publishClientReceive`: may a device receive a message published on this topic.
- `subscribeLiteral` and `unsubscribeLiteral`: compare the ACL topic filter literally with the filter in SUBSCRIBE/UNSUBSCRIBE. A deny on `#` stops subscribing to `#` only, but still allows `topic/#`.
- `subscribePattern` and `unsubscribePattern`: wildcard comparison of the ACL filter and the requested topic. A deny on `#` blocks subscribing to any topic at all.

Pattern substitution works in publishClientSend, publishClientReceive, subscribePattern and unsubscribePattern: `%c` is replaced with the client id and `%u` with the username, and must be the only item in its topic level, so `topic/%count` is not a pattern. The ACL `room/%c/temperature` lets a client with id `kitchen` use only `room/kitchen/temperature`. A client with no username never matches a `%u` pattern.

```
mosquitto_ctrl <options> dynsec addRoleACL sensorrole publishClientSend room/%c/temperature allow 5
```

## Checked

2026-11-08. Confirmed against the Dynamic Security plugin documentation page (and the mosquitto_ctrl_dynsec man page for the init synopsis). ACL types, literal versus pattern behaviour, %c and %u substitution rules and the example all match. Claims unchanged.

Method: documentation only; no commands were run.
