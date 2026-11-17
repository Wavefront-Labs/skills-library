---
id: computing-software.messaging-and-integration.mosquitto.log-destinations
name: log-destinations
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [log-dest, logging, syslog, log-facility]
level: practitioner
status: docs-checked
description: "Choose where Mosquitto logs with log_dest (stdout, stderr, syslog, topic, file, dlt, android) and rotate the file on HUP."
sources:
  - https://mosquitto.org/man/mosquitto-conf-5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: direct broker logs to the right place.

`log_dest destinations` may be specified multiple times. Destinations:
- `stdout`, `stderr`: console. Default is stderr.
- `syslog`: userspace syslog facility.
- `topic`: logs to `$SYS/broker/log/<severity>` with severity E, W, N, I or M (error, warning, notice, information, message). Message severity is used by the subscribe and unsubscribe log types and publishes to `$SYS/broker/log/M/subscribe` and `$SYS/broker/log/M/unsubscribe`. Debug is never logged to topics.
- `file`: needs a path, e.g. `log_dest file /path/to/mosquitto.log`. The file is closed and reopened on a HUP signal. Only a single file destination may be configured.
- `dlt`: automotive Diagnostic Log and Trace, requires DLT support compiled in.
- `android`: Android only, outputs to the logd daemon.
- `none` disables logging.

On Windows, a broker running as a service defaults to `log_dest none`, with no stdout or stderr logging.

`log_facility local facility`: for syslog (not Windows) the default facility is daemon; give an integer such as `log_facility 5` for local5.

`log_dest` is reloaded on the reload signal; the page makes no such statement for `log_facility`.

## Checked

2026-11-08. Confirmed against mosquitto.conf(5): log_dest destinations, topic severities, single file destination, dlt and android notes, Windows service default, and log_facility. Replaced a closing sentence that claimed the whole option group and SIGRTMIN rotation were documented there; the page marks log_dest as reloaded and does not mention SIGRTMIN.

Method: documentation only; no commands were run.
