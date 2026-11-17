---
id: computing-software.email-administration.mailcow.mailcow-logging-drivers-and-rotation
name: mailcow-logging-drivers-and-rotation
category: computing-software
field: email-administration
product: mailcow
tags: [logging, docker-logging-driver, syslog, gelf, redis-log-keys, logrotate, rsyslog, override-compose]
level: practitioner
status: docs-checked
description: "Send mailcow container logs to syslog or Graylog via compose override or daemon.json, and rotate the resulting file with logrotate."
sources: ["https://docs.mailcow.email/post_installation/firststeps-logging/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# mailcow logging drivers and log rotation

Containers write to stdout and are transient; every line reaches the Docker daemon unfiltered, with the default `json` logging driver. Some application logs are also filtered into Redis keys (10000 lines are kept for the web UI) and streamed to a Redis channel that netfilter-mailcow reads to ban clients after failed authentication. Because of this you can change Docker's logging driver without losing the UI log view or the bans. System messages such as cron are not kept in the Redis keys.

Per service: in `docker-compose.override.yml` add a `logging:` block under a service, for example `driver: "gelf"` with `gelf-address: "udp://graylog:12201"`, or `driver: "syslog"` with `syslog-address: "udp://127.0.0.1:514"` and `syslog-facility: "local3"`. Repeat for postfix-mailcow, dovecot-mailcow, rspamd-mailcow and others.

Globally: set `log-driver` and `log-opts` in `/etc/docker/daemon.json`, restart Docker, then `docker compose down` and `up -d` to recreate containers.

Rsyslog: enable `imudp` on port 514 in `/etc/rsyslog.conf` and create `/etc/rsyslog.d/docker.conf` containing `local3.* /var/log/mailcow.log` followed by `& stop`.

Rotation: create `/etc/logrotate.d/mailcow` for `/var/log/mailcow.log` with `rotate 7`, `daily`, `compress`, `delaycompress`, `missingok`, `notifempty` and `copytruncate`, needed because the Docker daemon keeps the file open. A commented `postrotate` block that restarts rsyslog is the alternative.

## Checked

2026-11-09. Confirmed on the logging page: json default driver, Redis keys with 10000 lines and the failed-auth channel, system messages excluded, gelf and syslog override examples, rsyslog imudp and docker.conf, daemon.json and recreate commands, and the logrotate file with copytruncate and the commented postrotate alternative. No changes needed.

Method: docs-checked 2026-11-09 against the full logging page (firststeps-logging.en.md in mailcow-dockerized-docs).
