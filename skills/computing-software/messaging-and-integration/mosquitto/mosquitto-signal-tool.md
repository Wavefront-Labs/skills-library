---
id: computing-software.messaging-and-integration.mosquitto.mosquitto-signal-tool
name: mosquitto-signal-tool
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [mosquitto-signal, config-reload, log-rotate, tree-print]
level: intro
status: docs-checked
description: "Send named signals such as config-reload, log-rotate and shutdown to local brokers with mosquitto_signal, including on Windows."
sources:
  - https://mosquitto.org/man/mosquitto_signal-1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: signal Mosquitto brokers by name instead of raw kill signals.

Synopsis: `mosquitto_signal { -a | -p pid } signal`.

- `-a` sends the signal to all processes matching the name `mosquitto` (only those you have permission to signal).
- `-p pid` sends to one process id; it always attempts to send and does not check that it is a mosquitto process.

Named signals and their POSIX equivalents:
- `config-reload`: reload the configuration file (SIGHUP)
- `log-rotate`: close and reopen the log when `log_dest file` is used (SIGHUP)
- `shutdown`: make the broker quit (SIGINT)
- `tree-print`: print the subscription and retain trees to stdout, for debugging only (SIGUSR2)
- `xtreport`: write internal state to `/tmp/xtmosquitto.kcg.<pid>.<iteration>` on POSIX or `xtmosquitto.kcg.<pid>.<iteration>` on Windows; debugging only, and the broker only acts on it when support is compiled in, which is not the case by default (SIGRTMIN)

```
mosquitto_signal -a config-reload
mosquitto_signal -p 1234 log-rotate
```

The tool works only for brokers on the local computer. On POSIX it replaces `kill(1)` with the added ability to use named signals and signal several brokers at once. On Windows it is the only means of sending signals to a broker.

Note that SIGHUP and SIGUSR2 are shared by several named signals.

## Checked

2026-11-08. Confirmed against the mosquitto_signal man page: -a and -p behaviour, all five named signals with their POSIX equivalents, the xtreport file paths and compile-time caveat, local-only scope and Windows use. Claims unchanged.

Method: documentation only; no commands were run.
