---
id: computing-software.messaging-and-integration.mosquitto.sys-topic-interval
name: sys-topic-interval
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [sys-interval, sys-topics, broker-status, dollar-sys]
level: practitioner
status: docs-checked
description: "Set how often the $SYS status tree is updated with sys_interval, disable it with 0, and know the one writable $SYS topic."
sources:
  - https://mosquitto.org/man/mosquitto-conf-5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: control the broker status topics.

`sys_interval seconds` is the number of seconds between updates of the `$SYS` subscription hierarchy. Unset, it defaults to 10. Set 0 to disable publishing `$SYS` completely. It is global and reloaded on the reload signal.

```
sys_interval 10
```

In general it is not possible to grant write access to topics in the `$SYS` tree. The exception is `$SYS/broker/connection/+/state`, which bridge notifications use.

Not covered by the cited page: the contents of the `$SYS` tree and shell quoting when subscribing with mosquitto_sub (quote `$SYS` in single quotes so the shell does not expand it; this is general shell behaviour, not stated on the page).

## Checked

Method: 2026-11-08 docs-only. Read the cited man page in full and compared each claim. Claims checked against mosquitto.conf(5). Removed unsupported claims (static topics, # not matching $SYS, shell quoting as a page claim, Dynamic Security roles); kept interval default, 0 disables, global, reload, and the writable connection state topic.
