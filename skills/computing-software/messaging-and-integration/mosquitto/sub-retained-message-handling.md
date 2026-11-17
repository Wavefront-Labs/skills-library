---
id: computing-software.messaging-and-integration.mosquitto.sub-retained-message-handling
name: sub-retained-message-handling
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [retained, retain-handling, remove-retained, retained-only]
level: advanced
status: docs-checked
description: "Skip, isolate or delete retained messages with mosquitto_sub -R, --retained-only, --remove-retained and --retain-handling."
sources:
  - https://mosquitto.org/man/mosquitto_sub-1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: handle stale retained messages from the subscriber side.

- `-R`: do not print messages with the retain bit set. They are "stale", since it is unknown when they were published, and a wildcard subscription may deliver many.
- `--retained-only`: print only retained messages; the first non-stale message received makes the client exit.
- `--remove-retained`: for each received retained message, send a message clearing it from the broker (except those filtered by `-T`). It still works with `-R`.
- `--retain-as-published`: sets the subscription's retain-as-published option, so the incoming retain flag is as set by the publisher. Not valid for MQTT v3.1/v3.1.1.
- `--retain-handling always|new|never` (2.1): when existing retained messages are sent. `new` delivers them the first time a subscription is made but not on later ones, useful for a long-running client on a non-clean session which reconnects.

Examples from the page:
```
mosquitto_sub -t '#' --remove-retained --retained-only
mosquitto_sub -t 'bbc/#' -T bbc/bbc1 --remove-retained
```
The first removes all retained messages on the server then exits, assuming you have access; the second removes a whole tree except one topic.

mosquitto_pub clears a single topic by retaining a zero length payload.

Combine `-C` with `-R` or `--retain-handling never` to print only the first fresh messages.

## Checked

2026-11-03. Claims, option names, defaults and version notes were compared with the Mosquitto manual pages in `sources` (mosquitto(8), mosquitto.conf(5), mosquitto_pub, mosquitto_sub, mosquitto_rr, mosquitto_ctrl, and the Dynamic Security page where relevant). Nothing removed.

Method: documentation only; no commands were run.
