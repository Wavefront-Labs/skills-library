---
id: computing-software.cloud-infrastructure-engineering.graylog.syslog-inputs
name: syslog-inputs
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [syslog, syslog-tcp, syslog-udp, rsyslog, syslog-ng]
level: practitioner
status: docs-checked
description: "Syslog input types in Graylog (TCP, UDP, Kafka, AMQP) and why non-compliant devices should relay via rsyslog or syslog-ng."
sources:
  - https://go2docs.graylog.org/current/getting_in_log_data/syslog_inputs.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# syslog inputs

Syslog input types:
- Syslog TCP: listener input
- Syslog UDP: listener input
- Syslog Kafka: pull input
- Syslog AMQP: pull input

Many devices, especially routers and firewalls, do not send RFC-compliant syslog, causing parse errors or failures. Forwarding through rsyslog or syslog-ng usually parses correctly.

Common options: Global checkbox (run on all nodes) or a specific Node; Title; for AMQP, broker hostname, virtual host, prefetch count and queue name. Each input type has its own settings in the page.

Graylog parses RFC 5424 and RFC 3164 syslog. TCP supports octet counting or termination-character framing; UDP is also supported and the page calls it the recommended way to send log messages in most architectures.

TCP and UDP listeners take a bind address, port, receive buffer size and worker threads (a common start is one per CPU core). TCP adds TLS options (cert file, key file, key password, client authentication optional or required, trusted client certs; `etc/graylog/tls` is the recommended path, readable by the Graylog user), TCP keepalive and maximum message size. Other options: Override source, Encoding (default UTF-8), Force rDNS, Store full message, Expand structured data and Timezone (used only when the sender omits one). The Kafka input has bootstrap servers, topic filter regex, consumer group id and custom Kafka properties.

For setup follow the general input setup instructions, then use Input Diagnosis to check the new input.

## Checked

Method: docs-checked 2026-11-09 against https://go2docs.graylog.org/current/getting_in_log_data/syslog_inputs.html (read in full, Graylog 7.2 docs). The page does not name a wizard, so the earlier "Input Setup Wizard" wording was replaced with the page's own "input setup instructions".
