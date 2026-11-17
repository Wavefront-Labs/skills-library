---
id: computing-software.cloud-infrastructure-engineering.graylog.sidecar-architecture
name: sidecar-architecture
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [sidecar, collector-configuration, sidecar-tags, filebeat, api-token]
level: practitioner
status: docs-checked
description: "How Graylog Sidecar works: agent, tags, collector configurations, collectors and API token enrolment."
sources:
  - https://go2docs.graylog.org/current/getting_in_log_data/graylog_sidecar.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# sidecar architecture

Sidecar is a lightweight service on each host that centrally manages collector processes (Filebeat, Winlogbeat, Auditbeat and others).

Architecture: the Graylog node holds collector configurations. Each Sidecar daemon periodically fetches its configurations through the Graylog REST API, and on first run or on change generates the collector's backend config.

Building blocks:
- **Agent**: runs as a Windows service or Linux daemon, authenticates with an API token.
- **Tags**: labels set in `sidecar.yml` (environment, role, OS, location). Configurations assigned to a tag go to every agent with it.
- **Collector configurations**: templates created in Graylog describing inputs, processors and outputs.
- **Collectors**: the binaries. Linux Sidecar includes Filebeat and Auditbeat; Windows includes Filebeat and Winlogbeat.

Example from docs: tags production and webservers pull a Filebeat config reading NGINX logs and sending to a Beats input.

Operation details:
- An agent applies any configuration that shares at least one tag with its tag list. On a change Sidecar regenerates the config files and restarts only the affected collectors.
- Agents poll the REST API every `update_interval` seconds (default 10) and send heartbeats and collector health.
- Token, tags and `server_url` go in `/etc/graylog/sidecar/sidecar.yml`; `node_id` and `node_name` are generated (the name defaults to the hostname or container name) and appear under System > Sidecars.
- Sidecar can also manage other existing collectors such as Sysmon, NXLog or Packetbeat.
- Unlike the Forwarder, which collects and ships logs itself to a Forwarder input using input profiles, Sidecar only controls external collectors.

## Checked

Method: docs-checked 2026-11-09 against https://go2docs.graylog.org/current/getting_in_log_data/graylog_sidecar.html (read in full, Graylog 7.2 docs).
