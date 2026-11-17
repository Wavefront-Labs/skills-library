---
id: computing-software.cloud-infrastructure-engineering.graylog.web-interface-bind-and-journal
name: web-interface-bind-and-journal
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [http-bind-address, message-journal, jvm-heap, preflight, server-conf]
level: practitioner
status: docs-checked
description: "Key server.conf values at install: root_password_sha2, password_secret, http_bind_address, message journal sizing and Graylog heap."
sources:
  - https://go2docs.graylog.org/current/downloading_and_installing_graylog/debian_installation.htm
  - https://go2docs.graylog.org/current/setting_up_graylog/configuration_settings.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# web interface bind and journal

Set these in `/etc/graylog/server/server.conf` so the service starts and the UI is reachable:
- `root_password_sha2`: SHA-256 of the root admin password (hash it without a trailing newline).
- `password_secret`: must equal the Data Node value on every node.
- `http_bind_address`: where the web and API server listens, for example `0.0.0.0:9000` (commented out by default).
- `message_journal_max_age = 72h` and `message_journal_max_size`: recommended 72 hours and a size equal to expected volume over 72 hours, so 30 GB per day means 90gb.

JVM heap in the service defaults file: half of system RAM up to 16 GB, with equal minimum and maximum. The documented form:

```
GRAYLOG_SERVER_JAVA_OPTS="-Xms2g -Xmx2g -server -XX:+UseG1GC -XX:-OmitStackTraceInFastThrow"
```

First login is the preflight with credentials from the log file, not the root password.

## Checked

2026-11-04. Confirmed against the Debian Installation: Single Graylog Node page (root_password_sha2, password_secret, http_bind_address, journal 72h and 90gb example, heap advice and the GRAYLOG_SERVER_JAVA_OPTS line, preflight login) and the Configuration Settings page (server.conf location). Nothing removed.

Method: documentation only; no commands were run.
