---
id: computing-software.systems-network-administration.keepalived.logging-options
name: logging-options
category: computing-software
field: systems-network-administration
product: keepalived
tags: [systems-network-administration, keepalived, logging, syslog, log-facility, log-detail, log-console, troubleshooting]
level: practitioner
status: docs-checked
description: "Control Keepalived logging with -l console logging, -D detailed messages and -S syslog facility LOG_LOCAL0 to LOG_LOCAL7 (default LOG_DAEMON)."
sources:
  - https://keepalived.readthedocs.io/en/latest/programs_synopsis.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Logging options

By default Keepalived logs to syslog.

- `-l`, `--log-console`: send messages to the local console instead of syslog.
- `-D`, `--log-detail`: enable detailed log messages.
- `-S`, `--log-facility=[0-7]`: choose syslog facility LOG_LOCAL0 to LOG_LOCAL7. Default is LOG_DAEMON.
- `-d`, `--dump-conf`: dump the parsed configuration to the logs.

To separate Keepalived output from other daemon logs, pick a LOG_LOCALn facility with `-S` and route that facility in your syslog configuration (the syslog side is not covered by the page). For interactive troubleshooting combine `-n` (foreground) with `-l` and `-D`.

SMTP and syslog are also the channels the daemon uses for administrative notifications and daemon messages.

Verify: after starting with the chosen options, messages appear under the expected facility or on the console.

## Checked

2026-11-04. Confirmed -l, -D, -S (LOG_LOCAL0 to 7, default LOG_DAEMON) and -d on the programs synopsis page, and that SMTP and syslog are the notification and daemon-message channels on the Software Design page. The -n with -l and -D combination is advice, not a documented requirement.

Method: documentation only; no commands were run.
