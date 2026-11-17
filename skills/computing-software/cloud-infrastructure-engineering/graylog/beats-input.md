---
id: computing-software.cloud-infrastructure-engineering.graylog.beats-input
name: beats-input
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [beats, filebeat, winlogbeat, logstash-output, beats-input]
level: practitioner
status: docs-checked
description: "Receive Filebeat, Winlogbeat and other Beats data in Graylog: configure the Logstash output over TCP only."
sources:
  - https://go2docs.graylog.org/current/getting_in_log_data/beats_input.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# beats input

The Beats input ingests data from Elastic Beats shippers and does basic parsing. It is a listener input.

Configure Beats to use the **Logstash output** over **TCP**. The Graylog Beats input supports only TCP, not UDP. For most Beats the Logstash output works unchanged; some need custom settings.

Beats include Filebeat (log files), Winlogbeat (Windows Event Logs), Metricbeat, Packetbeat, Auditbeat and community Beats. For easier management of Beats configuration, use Graylog Sidecar.

Input options: Global or Node, Bind Address (for example all interfaces) and Port, plus buffer and worker thread options. Add TLS through the standard input TLS settings if needed.

## Checked

2026-11-04. Confirmed against the Beats input page. Nothing removed.

Method: documentation only; no commands were run.
