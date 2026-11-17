---
id: computing-software.messaging-and-integration.mosquitto.sub-filtering-and-stopping
name: sub-filtering-and-stopping
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [sub-filter, count, timeout, random-filter]
level: practitioner
status: docs-checked
description: "Stop or thin out mosquitto_sub output with -C, -W, -T, -E and --random-filter."
sources:
  - https://mosquitto.org/man/mosquitto_sub-1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: bound a subscription in scripts.

- `-C count`: disconnect and exit immediately after that many messages, useful when a script needs a single status value. Combine with `-R` or `--retain-handling never` to count only fresh messages, or with `-T` to filter topics.
- `-W seconds`: stop processing and disconnect after this many seconds; the timeout starts just after connecting.
- `-T, --filter-out topic`: suppress printing of topics matching the filter; repeatable. Example: `mosquitto_sub -t bbc/# -T bbc/radio3`.
- `-E`: exit as soon as all subscriptions are acknowledged by the broker. With `-c` it initialises a durable session.
- `--random-filter chance`: print on average that percentage of messages; a float between 0.1 and 100.0.
- `-q 0|1|2`: QoS for incoming messages (default 0), applied to all topics of that client instance.
- `-t topic`: repeat to subscribe to several topics.

```
mosquitto_sub -t status/boiler -C 1 -W 10
```

Exit status: zero on success; if the broker refuses the connection the exit code is the CONNACK reason code, and the sub page lists code 27 as timed out waiting for message.

`-C` and `-W` pair well: the first ends on count, the second ends on time.

## Checked

2026-11-08. Confirmed against the mosquitto_sub man page: -C, -W, -T, -E, --random-filter, -q and -t. Corrected the exit-status line, which attributed the CONNACK and code 27 text to the pub page; the sub page lists both itself.

Method: documentation only; no commands were run.
