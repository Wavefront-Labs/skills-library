---
id: computing-software.cloud-infrastructure-engineering.portainer.stream-portainer-logs-to-syslog
name: stream-portainer-logs-to-syslog
category: computing-software
field: cloud-infrastructure-engineering
product: portainer
tags: [siem, syslog, audit-logs, cli-flags, business-edition]
level: advanced
status: docs-checked
description: "Stream Portainer authentication and activity logs to an external syslog or SIEM with the syslog CLI flags."
sources:
  - https://github.com/portainer/portainer-docs/blob/HEAD/2.39-lts/advanced/siem.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
From Portainer 2.20, authentication and activity logs can stream to an external SIEM in Syslog format. The feature is experimental and Business Edition only, and it is configured with CLI flags when starting the Portainer container, not in the UI.

Flags:

- `--syslog-address`: FQDN or IP of the syslog server.
- `--syslog-port`: defaults to 514.
- `--syslog-protocol`: `udp` (default), `tcp` or `tcp+tls`.
- `--syslog-format`: `rfc3164` or `rfc5424` (default).
- `--syslog-source-hostname`: hostname shown in messages, default `portainer`.
- `--syslog-insecure-skip-verify`: disables TLS server verification for `tcp+tls`; testing only, default false.
- `--syslog-ca-cert`: path to the trusted CA for the syslog server, default `/syslog/certs/ca.pem`.
- `--syslog-cert` and `--syslog-key`: client certificate and key for mTLS to the syslog server, defaults `/syslog/certs/cert.pem` and `/syslog/certs/key.pem`.

Flags go after the image name in the container command, for example `--syslog-address=syslog.mydomain.com --syslog-port=514 --syslog-source-hostname="my-portainer-instance"`.

## Checked

2026-11-04. Checked against the Portainer 2.39 LTS documentation pages in `sources` (portainer-docs on GitHub, fetched this batch): commands, flags, ports, paths, defaults and UI steps. Added the missing `--syslog-cert` and `--syslog-key` flags and the documented example. Removed: the production tcp+tls recommendation, the claim that streamed events match the UI Logs section, and the restart note (none are on the page).

Method: documentation only; no commands were run.
