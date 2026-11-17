---
id: computing-software.messaging-and-integration.mosquitto.client-id-policy-options
name: client-id-policy-options
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [allow-zero-length-clientid, auto-id-prefix, use-username-as-clientid, clientid-prefixes]
level: practitioner
status: docs-checked
description: "Control zero-length and auto-generated client ids, tie client ids to usernames and build ids with a prefix."
sources:
  - https://mosquitto.org/man/mosquitto-conf-5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: manage how client identifiers are accepted.

- `allow_zero_length_clientid true|false` (default true): MQTT 3.1.1 and 5 allow a zero length client id and let the broker generate one. With `per_listener_settings` true it applies to the current listener.
- `auto_id_prefix prefix` is a string prefixed to generated client ids to aid log visibility; default `auto-`. It is one of the options controlled per listener when `per_listener_settings` is true.
- `use_username_as_clientid true` replaces the client id a client connected with by its username (default false). This ties authentication to the client id, so one client cannot disconnect another by using the same id. Clients connecting without a username are disconnected as not authorised. Per listener; the page says not to use it together with `clientid_prefixes`.

```
allow_zero_length_clientid false
use_username_as_clientid true
```

The client tools support `-I, --id-prefix`, which builds the client id from the prefix plus the process id, useful where the broker uses `clientid_prefixes`; it cannot be used with `--id`.

## Checked

2026-11-03. Claims, option names, defaults and version notes were compared with the Mosquitto manual pages in `sources` (mosquitto(8), mosquitto.conf(5), mosquitto_pub, mosquitto_sub, mosquitto_rr, mosquitto_ctrl, and the Dynamic Security page where relevant). Removed the clientid_prefixes entry and example and the claim that the global auto_id_prefix is deprecated (not on the page).

Method: documentation only; no commands were run.
