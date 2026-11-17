---
id: computing-software.messaging-and-integration.mosquitto.rr-request-response
name: rr-request-response
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [mosquitto-rr, request-response, response-topic, latency]
level: practitioner
status: docs-checked
description: "Send a request and wait for the response with mosquitto_rr, using -t, -e and a payload option, plus --latency."
sources:
  - https://mosquitto.org/man/mosquitto_rr-1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: do one MQTT request/response exchange from the shell.

`mosquitto_rr [options] -e response-topic -t message-topic... {payload-options}`. It publishes a request and waits for a response. MQTT v5 is the default, using the Request-Response feature. The important options are `-t`, `-e` and one of `-f`, `-m`, `-n`, `-s`.

```
mosquitto_rr -t request-topic -e response-topic -m message
```

- `-e`: the response topic; the client subscribes to it to wait for the response.
- `-t`: request topic, repeatable.
- Payload: `-m` message, `-f` file, `-s` stdin as one message, `-n` null message.
- `-W seconds`: timeout; the client disconnects after this long, counted from connection.
- `--latency` (2.1): prints the time between starting to publish the request and the response arriving, including broker and client processing and network latency. Using an identical request and response topic measures message delivery latency. `--nodelay` is applied automatically.
- Output options: `-F` format (same sequences as mosquitto_sub), `-N`, `--pretty`, `-R`, `-v`, `-d`, `--quiet`.
- `-q`, `-c`, `-x`, `-k`, `-i`, `-I`, `-V`, `-D`, wills, TLS and `--retain-handling` behave as in the other client tools.

## Checked

2026-11-03. Claims, option names, defaults and version notes were compared with the Mosquitto manual pages in `sources` (mosquitto(8), mosquitto.conf(5), mosquitto_pub, mosquitto_sub, mosquitto_rr, mosquitto_ctrl, and the Dynamic Security page where relevant). Nothing removed.

Method: documentation only; no commands were run.
