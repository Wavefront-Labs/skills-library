---
id: computing-software.messaging-and-integration.mosquitto.reload-and-signals
name: reload-and-signals
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [sighup, sigusr1, sigusr2, config-reload]
level: practitioner
status: docs-checked
description: "Reload configuration, certificates and logs with SIGHUP, save persistence with SIGUSR1 and rotate logs with SIGRTMIN."
sources:
  - https://mosquitto.org/man/mosquitto-8.html
  - https://mosquitto.org/man/mosquitto-conf-5.html
  - https://mosquitto.org/man/mosquitto_signal-1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: use POSIX signals to operate a running broker.

Send signals with e.g. `kill -HUP <process id of mosquitto>`:
- `SIGHUP`: reload configuration file data, assuming `-c` was given at startup. Not all parameters can be reloaded without a restart (each option states whether it is reloaded). TLS certificates are reloaded, and the logs are closed and reopened.
- `SIGRTMIN`: close and reopen the logs to support log rotation.
- `SIGUSR1`: write the persistence database to disk; only acted on if persistence is enabled.
- `SIGUSR2`: print the current subscription tree and where retained messages exist. Described as a testing feature that may be removed at any time.

Options documented as not reloaded include `port`, `bind_address`, `bind_interface`, `plugin`, `pid_file`, `user`, `listener_allow_anonymous` and other listener-level settings such as `auto_id_prefix`, `max_connections` and `max_qos`. Reloaded options include `password_file`, `acl_file`, `psk_file`, logging options and the queue and inflight limits.

Effect of reloading authentication files: already connected clients are not affected by new password or PSK data; reloading `acl_file` affects existing subscriptions after reload.

Setting `log_dest file` allows HUP to close and reopen the file.

On Windows, signals can only be sent with `mosquitto_signal`.

## Checked

2026-11-08. Confirmed against mosquitto(8) Signals and the per-option reload notes in mosquitto.conf(5): SIGHUP, SIGRTMIN, SIGUSR1 and SIGUSR2 behaviour, reloaded versus not-reloaded options, and connected clients not affected by password or PSK reloads. Removed listener from the not-reloaded list (not stated per option) and added three listener options the page does mark as not reloaded. The Windows mosquitto_signal remark comes from that tool page.

Method: documentation only; no commands were run.
