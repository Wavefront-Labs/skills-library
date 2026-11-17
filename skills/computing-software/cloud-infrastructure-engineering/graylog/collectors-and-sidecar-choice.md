---
id: computing-software.cloud-infrastructure-engineering.graylog.collectors-and-sidecar-choice
name: collectors-and-sidecar-choice
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [graylog-collector, collector-sources, sidecar-vs-collector, control-channel]
level: intro
status: docs-checked
description: "Graylog Collector versus Sidecar: how the collector gets sources from the Graylog UI over two HTTPS connections."
sources:
  - https://go2docs.graylog.org/current/getting_in_log_data/collectors.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# collectors and sidecar choice

Graylog Collector (a preview feature in Graylog 7.2) and Graylog Sidecar are separate features. They share no configuration, enrollment or management. Sidecar manages third-party collectors such as Filebeat and NXLog that you install alongside it; Graylog Collector collects and sends logs itself.

Graylog Collector has two jobs per host:
1. Collect log data and send it to Graylog. You define sources in the Graylog interface and the server delivers them; sources can read files, the systemd journal, the Windows Event Log or macOS unified logging.
2. Report on itself: health, host metadata, applied configuration, and its own diagnostic logs, so a failing collector can be diagnosed in the UI.

Each collector keeps two HTTPS connections to Graylog, a control channel and a data channel. After enrollment the host needs no local configuration.

## Checked

2026-11-04. Confirmed against the Collectors page. Added that Graylog Collector is a preview feature in 7.2.

Method: documentation only; no commands were run.
