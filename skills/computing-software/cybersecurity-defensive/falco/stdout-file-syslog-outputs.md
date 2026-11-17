---
id: computing-software.cybersecurity-defensive.falco.stdout-file-syslog-outputs
name: stdout-file-syslog-outputs
category: computing-software
field: cybersecurity-defensive
product: falco
tags: [stdout-output, file-output, syslog-output, keep-alive, unbuffered]
level: intro
status: docs-checked
description: "Configure Falco stdout, file and syslog alert channels, buffering with -U, keep_alive, SIGUSR1 reopen and the syslog facility."
sources:
  - https://falco.org/docs/concepts/outputs/channels/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each channel is enabled in `falco.yaml`.

```yaml
stdout_output:
  enabled: true
file_output:
  enabled: true
  keep_alive: false
  filename: ./events.txt
syslog_output:
  enabled: true
```

**Stdout** prints one line per alert and suits Fluentd or Logstash collecting container logs. When tailing with `kubectl logs -f`, alerts can seem delayed by 15 minutes or more because of output buffering, not a Falco fault. Force flushing for every event with `-U` or `--unbuffered`, at the cost of higher CPU.

**File** appends alerts. With `keep_alive: false` (default) the file is opened, written and closed for each alert. With `true` it stays open and output is buffered until close, unless `--unbuffered` is used. Falco never rotates or truncates the file. Since Falco 0.10.0 it closes and reopens the file on `SIGUSR1`, which a logrotate config can use.

**Syslog** sends each alert with facility `LOG_USER`, and the rule priority becomes the syslog priority. The final format depends on your syslog daemon.

Gotcha: Falco never rotates the file itself, so rotation needs an external tool such as logrotate; with `keep_alive: true` signal `SIGUSR1` so Falco reopens the file.

## Checked

2026-11-08. Read the Output Channels page in full. Corrected the rotation gotcha: Falco does not rotate files and SIGUSR1 matters with keep_alive true.

Method: documentation only; no commands were run.
