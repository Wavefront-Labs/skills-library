---
id: computing-software.systems-network-administration.healthchecks.self-hosted-email-receiving
name: self-hosted-email-receiving
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, smtpd-listener, smtpd-port, ping-email-domain, email-based-pings]
level: advanced
status: docs-checked
description: "Run the Healthchecks smtpd listener to accept email pings: manage.py smtpd, the SMTPD_PORT Docker variable, PING_EMAIL_DOMAIN and exposing the port."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/self_hosted.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/self_hosted_docker.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/self_hosted_configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Email pings arrive at `<uuid>@<domain>` addresses, which needs the SMTP listener on your instance.

From source:

```
./manage.py smtpd --port 2525
```

Test with curl against `smtp://127.0.0.1:2525`, using a check's UUID in the recipient address on your ping domain.

Domain: `PING_EMAIL_DOMAIN` (default `localhost`) is the domain used to generate ping email addresses.
Docker:
- The `smtpd` command runs in the official images, but only if `SMTPD_PORT` is set. If unset, the listener does not run.
- Expose the port under `ports` for the `web` service in `docker-compose.yml`; startup logic is in `run.sh`.

Checks can then classify emails with keyword filtering (see email-pinging).

## Checked

2026-11-04. Confirmed against the Healthchecks self-hosted page, Docker documentation and server configuration page: smtpd with --port 2525, the curl test, PING_EMAIL_DOMAIN default, SMTPD_PORT conditional start, exposing the port under the web service ports and the run.sh logic, and keyword filtering from the Management API page. Nothing removed.

Method: documentation only; no commands were run.
