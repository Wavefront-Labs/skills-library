---
id: computing-software.messaging-and-integration.mosquitto.wildcard-subscriptions
name: wildcard-subscriptions
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [wildcard, topic-filter, plus-wildcard, hash-wildcard]
level: intro
status: docs-checked
description: "Match topics with + and # in Mosquitto subscriptions, including the $SYS exception and shell quoting."
sources:
  - https://mosquitto.org/man/mosquitto-8.html
  - https://mosquitto.org/man/mosquitto_sub-1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: write valid topic filters.

`+` matches a single level of hierarchy. For topic `a/b/c/d` these match: `a/b/c/d`, `+/b/c/d`, `a/+/c/d`, `a/+/+/d`, `+/+/+/+`. These do not match: `a/b/c`, `b/+/c/d`, `+/+/+`.

`#` matches all subsequent levels. For `a/b/c/d` these match: `a/b/c/d`, `#`, `a/#`, `a/b/#`, `a/b/c/#`, `+/b/c/#`.

Rules:
- Wildcards must be used on their own: `a/b+/c` is not valid.
- `#` must be the final character of a subscription.
- The `$SYS` hierarchy does not match `#`; subscribe to `$SYS/#` to see it.

Shell tip: quote or escape the `$`, e.g. `mosquitto_sub -v -t '$SYS/#'`.

mosquitto_sub examples from its page:
```
mosquitto_sub -t sensors/machines/+/temperature/+
mosquitto_sub -t 'bbc/#' -T bbc/bbc1 --remove-retained
```

Unsubscribing cannot punch holes in a wildcard: after `mosquitto_sub -t sensors/# -U sensors/+/temperature -v`, messages matching `sensors/+/temperature` are still delivered.

Overlapping subscriptions such as `foo/#` and `foo/+/baz` should deliver a matching message once; `allow_duplicate_messages` (deprecated, default true) can disable the tracking that ensures this.

## Checked

2026-11-08. Confirmed against the mosquitto(8) wildcard section (match and non-match lists, standalone wildcards, # last, $SYS exception, shell quoting), the mosquitto_sub -U note and the mosquitto.conf(5) allow_duplicate_messages entry (deprecated, default true). Claims unchanged.

Method: documentation only; no commands were run.
