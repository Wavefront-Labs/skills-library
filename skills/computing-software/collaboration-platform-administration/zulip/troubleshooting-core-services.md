---
id: computing-software.collaboration-platform-administration.zulip.troubleshooting-core-services
name: troubleshooting-core-services
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [nginx-failure, allowed-hosts, rabbitmq-restart, amqp-connection-error]
level: practitioner
status: docs-checked
description: "Fix common Zulip core service failures: nginx not starting from SSL errors, Invalid HTTP_HOST and ALLOWED_HOSTS noise, and RabbitMQ AMQPConnectionError with broken DNS."
sources: ["https://zulip.readthedocs.io/en/latest/production/troubleshooting.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Troubleshooting Zulip's supporting services

Zulip depends on PostgreSQL, RabbitMQ, nginx, Redis and memcached. If one is missing or misbehaving, Zulip does not work. Common cases:

**Browser says no web server is running.** nginx probably failed to start, typically from incorrect SSL configuration or missing certificates. Fix the certificate setup, then run `service nginx restart`.

**Port-scan noise in `/var/log/zulip/server.log`.** Lines like `Invalid HTTP_HOST header: '10.2.3.4'. You may need to add '10.2.3.4' to ALLOWED_HOSTS` come from unauthorised hosts probing. Django compares the request's Host header with `ALLOWED_HOSTS` and rejects and logs mismatches, protecting against Host header poisoning.
**AMQPConnectionError or rabbitmqctl errors.** RabbitMQ is usually not running. Try `service rabbitmq-server restart`. If it will not start, the likely culprit is a virtual machine with broken DNS configuration, often corrected by setting up `/etc/hosts` properly.

If you need help, post in the community production help channel with the full traceback from `errors.log` or the install log, in code blocks, and state your Zulip version or the versions you are upgrading between.

## Checked

2026-11-03: commands, paths, flags, settings and figures read against the Zulip documentation page production/troubleshooting.html (zulip.readthedocs.io, latest). Removed: the harmlessness claim for ALLOWED_HOSTS noise and the invented general-approach steps.

Method: documentation only; no commands were run.
