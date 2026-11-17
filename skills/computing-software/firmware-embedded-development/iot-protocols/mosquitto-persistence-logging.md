---
id: computing-software.firmware-embedded-development.iot-protocols.mosquitto-persistence-logging
name: mosquitto-persistence-logging
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [mosquitto-persistence-logging, mosquitto-broker, mosquitto, persistence, log-dest, iot-protocols]
level: practitioner
status: docs-checked
description: "Mosquitto persistence and logging: Keep state across restarts and make the broker observable."
sources:
  - https://mosquitto.org/man/mosquitto-conf-5.html
  - https://mosquitto.org/man/mosquitto-8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mosquitto persistence and logging

**Goal:** Keep state across restarts and make the broker observable.

## Steps
1. Set `persistence true` and `persistence_location` to a directory the mosquitto user can write (data goes to mosquitto.db there); autosave_interval defaults to 1800 s, 0 saves only on exit or SIGUSR1; the manual recommends plugin-based persistence over the built-in one
2. Built-in persistence stores connection, subscription and message data; it is written on exit, at autosave_interval, or when the broker receives SIGUSR1
3. Set `log_dest file <path>` (only one file destination allowed) and `log_type` values such as error, warning, notice, information (these four are the default)
4. Set `connection_messages true` to log client connects and disconnects
5. Subscribe to `$SYS/broker/#`, for example clients/connected, messages/received and heap/current
6. sys_interval sets the seconds between $SYS updates (default 10; 0 disables $SYS)
7. Rotate the log file, then send SIGHUP: the file is closed and reopened

## Gotcha
The persistence database is written periodically, not per message, so a crash can lose changes since the last save; autosave_on_changes true saves by change count instead of time.

## Verify
- [ ] Retained message survives restart
- [ ] $SYS stats update
- [ ] Logs rotate without restart

## Checked

2026-11-03. Confirmed in the mosquitto.conf(5) and mosquitto(8) man pages: persistence, persistence_location, persistence_file default, autosave_interval default and 0 behaviour, autosave_on_changes, SIGUSR1 and SIGHUP behaviour, log_dest file rules, log_type defaults, connection_messages, sys_interval default and 0, and the $SYS topics clients/connected, messages/received and heap/current. Removed: the exact list "retained messages, subscriptions of persistent sessions, queued messages" (the manual says connection, subscription and message data), the example /var paths, and the claim about systemctl.
Method: documentation only; no commands were run.
