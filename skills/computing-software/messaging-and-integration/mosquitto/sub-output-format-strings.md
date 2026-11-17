---
id: computing-software.messaging-and-integration.mosquitto.sub-output-format-strings
name: sub-output-format-strings
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [mosquitto-sub, output-format, format-string]
level: practitioner
status: docs-checked
description: "Customise mosquitto_sub output with -F format strings using % parameters, @ strftime codes and \ escapes."
sources:
  - https://mosquitto.org/man/mosquitto_sub-1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: print exactly the message fields you need.

Default output is the payload only; `-v` prints `topic payload` separated by a space; `-F format` overrides `-v` but not `-N` (which omits the trailing newline). Three characters start a sequence: `%` (message parameter or helper), `@` (passed to strftime with `@` replaced by `%`, plus `@N` for nanoseconds) and `\`.

Common parameters: `%t` topic, `%p` payload raw bytes, `%q` QoS, `%r` retained flag, `%m` message id, `%l` payload length, `%x`/`%X` payload as hex lower/upper, `%I` ISO-8601 date and time, `%U` Unix timestamp with nanoseconds, `%%` a literal percent. MQTT v5 ones: `%A` topic alias, `%C` content-type, `%D` correlation-data, `%E` message-expiry-interval, `%F` payload-format-indicator, `%P` user properties as key:value, `%R` response-topic, `%S` subscription-identifier. `%f` and `%d` read the payload as a 4 or 8 byte IEEE 754 float.

Flags and widths: `0` zero pads, `-` left aligns, `%10t` sets a minimum width, `%.20t` a maximum, `%.2x` splits hex into bytes separated by spaces, and `%.2:x` uses `:`.

Escapes: `\\`, `\0` (null, handy with xargs), `\a`, `\e` (ANSI colours), `\n`, `\r`.

```
mosquitto_sub -F '@Y-@m-@dT@H:@M:@S@z : %t : %x' -t '#'
mosquitto_sub -F '\e[92m%t \e[96m%p\e[0m' -q 2 -t '#'
```

## Checked

2026-11-08. Confirmed against the mosquitto_sub man page output format section: default, -v and -F precedence, the three sequence-start characters, parameters, flags, widths, hex splitting, escapes and examples. Claims unchanged.

Method: documentation only; no commands were run.
