---
id: computing-software.cybersecurity-defensive.wazuh.journald-collection
name: journald-collection
category: computing-software
field: cybersecurity-defensive
product: wazuh
tags: [journald, filter, only-future-events, systemd-unit, docker-log-driver]
level: practitioner
status: docs-checked
description: "Collect systemd journal logs with Wazuh using a journald localfile, regex field filters, only-future-events behaviour and the Docker journald driver."
sources:
  - https://documentation.wazuh.com/current/user-manual/capabilities/log-data-collection/journald.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The logcollector reads journald and the agent forwards events. The default block in `/var/ossec/etc/ossec.conf` is a `<localfile>` with `<location>journald</location>` and `<log_format>journald</log_format>`, which forwards everything.

Filter with `<filter field="...">regex</filter>` inside `<localfile>`. Examples: `_SYSTEMD_UNIT` with `^ssh.service$`, and `PRIORITY` with `[0-6]` (logs above priority 6 are ignored). A log matching two or more filters in one block is sent once.

Only future events are collected by default; disable `only-future-events` to also collect events produced while the log collector was stopped.

Logs are rebuilt in syslog format from `_HOSTNAME`, `SYSLOG_IDENTIFIER`, `MESSAGE` and `SYSLOG_PID` or `_PID`. Put custom decoders in `/var/ossec/etc/decoders/local_decoder.xml` and rules in `/var/ossec/etc/rules/local_rules.xml`.

Examples on the page: CRON rules 111800 (group), 111801 (command executed, level 8), 111802 (level 12, started outside system startup); Docker rules 111700 (group), 111701 (container launched, level 8), 111702 (container shut down, level 12).

Docker setup: run containers with `--log-driver=journald` and verify with `docker inspect -f '{{.HostConfig.LogConfig.Type}}' <name>`.

Restart `wazuh-agent` on the endpoint and `wazuh-manager` on the server. Alerts land in `/var/ossec/logs/alerts/alerts.log` and `alerts.json`.

## Checked

2026-11-08. Read the whole journald log collection page. Confirmed: default localfile block, filter fields and regexes, [0-6] priority note, duplicate-once note, only-future-events, syslog-format fields, decoder and rule file paths, rule IDs 111800-111802 and 111700-111702 with levels, docker log-driver command and inspect check, restarts, alert file paths.
Method: documentation only; no commands were run.
