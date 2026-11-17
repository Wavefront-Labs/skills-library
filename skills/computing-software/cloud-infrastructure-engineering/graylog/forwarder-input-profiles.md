---
id: computing-software.cloud-infrastructure-engineering.graylog.forwarder-input-profiles
name: forwarder-input-profiles
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [forwarder, input-profiles, remote-site, forwarder-ports, tls]
level: practitioner
status: docs-checked
description: "Graylog Forwarder: Linux or container-only shipper that runs input profiles and sends logs over TLS to a forwarder input."
sources:
  - https://go2docs.graylog.org/current/getting_in_log_data/forwarder.html
  - https://go2docs.graylog.org/current/setting_up_graylog/default_file_locations.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# forwarder input profiles

The Forwarder collects logs at remote sites or distributed environments and sends them securely to your Graylog cluster. It runs as a service on Linux or in a container. **It cannot be installed on Windows**; send Windows logs to a Forwarder via a Sidecar collector.

The Forwarder is available with Cloud, Security and Enterprise licenses only.

Parts:
- **Forwarder on host**: runs the inputs defined by assigned input profiles (many of the same input types as the server, such as Syslog and Beats).
- **Forwarder input** in the cluster: receives the logs. Port 13301 carries log data, port 13302 carries configuration updates.
- **Control layer** in Graylog: administrators create tokens, input profiles and settings; the Forwarder retrieves and applies them.

Example profile named Remote Site A includes a Syslog UDP input on port 5140 and a Beats input.

Files: `/etc/graylog/forwarder/forwarder.conf`, journal `/var/lib/graylog-forwarder/data`, log `/var/log/graylog-forwarder/forwarder.log`.

## Checked

2026-11-04. Confirmed against the Forwarder page. Added the license note.

Method: documentation only; no commands were run.
