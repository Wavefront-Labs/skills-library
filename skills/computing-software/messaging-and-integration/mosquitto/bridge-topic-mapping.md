---
id: computing-software.messaging-and-integration.mosquitto.bridge-topic-mapping
name: bridge-topic-mapping
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [bridge-topic, topic-remapping, local-prefix, remote-prefix, topic]
level: advanced
status: docs-checked
description: "Share topics between brokers with the bridge topic option, direction, QoS and local/remote prefix remapping."
sources:
  - https://mosquitto.org/man/mosquitto-conf-5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: choose which topics cross a bridge and how they are renamed.

Syntax: `topic pattern [[[ out | in | both ] qos-level] local-prefix remote-prefix]`. May be repeated per bridge. The pattern may use wildcards and may be double-quoted if it contains a space. Direction defaults to `out`; QoS defaults to 0.

Prefixes remap topics. For incoming topics the bridge prepends the remote prefix to the pattern for the remote subscription, then on receipt removes the remote prefix and adds the local prefix. Outgoing is the reverse. An empty prefix is written `""`.

Valid combinations (pattern / local prefix / remote prefix):
- pattern, `L/`, `R/`: local `L/pattern`, remote `R/pattern`
- pattern, `L/`, `""`: local `L/pattern`, remote `pattern`
- pattern, `""`, `R/`: local `pattern`, remote `R/pattern`
- pattern, `""`, `""`: valid, no remapping
- an empty pattern `""` with prefixes `local` and `remote`: valid, remaps the single topic `local` to `remote`
- empty pattern with `local` and `""`, empty pattern with `""` and `remote`, and all three empty: invalid

Remap a whole tree:
```
topic # both 2 local/topic/ remote/topic/
```

Warning from the docs: loops are possible; high CPU usage on a broker may mean two brokers forever forward each other the same messages.

`bridge_attempt_unsubscribe` (default true) sends an unsubscribe to the remote broker for `out` topics, so switching a topic from in to out stops incoming messages.

## Checked

Method: 2026-11-08 docs-only. Read the cited man page in full and compared each claim. Claims checked against mosquitto.conf(5). Added the valid no-remapping row from the page table; other claims unchanged.
