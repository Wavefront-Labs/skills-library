---
id: computing-software.messaging-and-integration.mosquitto.sub-json-output
name: sub-json-output
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [json-output, pretty, format-j, mosquitto-sub]
level: practitioner
status: docs-checked
description: "Emit each message as JSON from mosquitto_sub with %j or %J and pretty print it with --pretty."
sources:
  - https://mosquitto.org/man/mosquitto_sub-1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pipe messages into JSON tooling.

Two helper format sequences print the message parameters and timestamp as a JSON object:

- `%j`: the payload is quoted and escaped. Example from the page:
`{"tst":"2020-05-06T22:12:00.000000+0100","topic":"greeting","qos":0,"retain":0,"payload":"hello world"}`
- `%J`: the payload is not quoted or escaped, so it must itself be valid JSON:
`{"tst":"2020-05-06T22:12:00.000000+0100","topic":"foo","qos":0,"retain":0,"payload":{"temperature":27.0,"humidity":57}}`

If the payload is not valid JSON with `%J`, the error `Error: Message payload is not valid JSON on topic <topic>` is printed to stderr.

```
mosquitto_sub -t sensors/# -F %J
mosquitto_sub -t sensors/# -F %j --pretty
```

`--pretty` formats `%j` and `%J` output in a more human readable way; the default is unformatted.

Related output options: `--message-rate` (2.1) prints a count of messages received at one second intervals instead of the messages, and other output formatting options are not valid then. `-w/--watch` (2.1) prints each topic on a fixed terminal line and requires ANSI escape support; use single-line payloads.

`-N` omits the end-of-line character so payloads from several messages stream unmodified to another application.

## Checked

2026-11-08. Confirmed against the mosquitto_sub man page: %j and %J definitions and examples, the invalid-JSON error, --pretty, --message-rate and --watch (both marked 2.1) and -N. Claims unchanged.

Method: documentation only; no commands were run.
