---
id: computing-software.systems-network-administration.healthchecks.docker-runtime-options
name: docker-runtime-options
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, gunicorn-workers, listen-ipv6, gunicorn-port, container-tuning]
level: practitioner
status: docs-checked
description: "Tune the Healthchecks container: GUNICORN_WORKERS, GUNICORN_PORT, GUNICORN_DISABLE_LOGGING and LISTEN_IPV6, including why IPv6 is off by default."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/self_hosted_docker.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/docker/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Gunicorn settings (version 5.0 and later), set in the container environment (for example `docker/.env`):

- `GUNICORN_WORKERS`: number of worker processes; reduce (the docs example is `2`) to save memory.
- `GUNICORN_PORT`: HTTP listening port.
- `GUNICORN_DISABLE_LOGGING=1`: disable access logs to container stdout.

IPv6: by default the web server listens on IPv4 only. Set `LISTEN_IPV6=1` to listen on IPv6 as well. It is off by default because on an IPv4-only system the server crashes on startup when it tries to open an IPv6 socket.

SMTP listener: set `SMTPD_PORT` to enable it (see self-hosted-email-receiving).

Other container-related facts:
- Images run migrations on startup and start `sendalerts`, `sendreports` and `smtpd` in the background.
- Static files are served by whitenoise.
- Many secrets accept a `_FILE` variant (for example `SECRET_KEY_FILE`) whose file contents take precedence.

## Checked

2026-11-04. Confirmed against the Healthchecks Docker documentation, docker README and server configuration page: GUNICORN_WORKERS, GUNICORN_PORT, GUNICORN_DISABLE_LOGGING, LISTEN_IPV6 and the reason it is off, SMTPD_PORT, automatic background commands, whitenoise, and _FILE precedence. Removed the claim that hc/local_settings.py overrides environment variables, which these pages do not state.

Method: documentation only; no commands were run.
