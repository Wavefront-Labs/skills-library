---
id: computing-software.email-administration.mailcow.mailcow-watchdog-thresholds
name: mailcow-watchdog-thresholds
category: computing-software
field: email-administration
product: mailcow
tags: [watchdog, watchdog-thresholds, service-health, mailq-threshold, auto-restart, admin-notifications]
level: advanced
status: docs-checked
description: "Tune the mailcow watchdog health checks by overriding per-service threshold variables in mailcow.conf."
sources: ["https://docs.mailcow.email/manual-guides/Watchdog/u_e-watchdog-thresholds/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tuning mailcow watchdog thresholds

The watchdog container probes each service and notifies administrators when failures reach a threshold. Defaults come from `docker-compose.yml` and suit most setups: `NGINX_THRESHOLD=5`, `UNBOUND_THRESHOLD=5`, `REDIS_THRESHOLD=5`, `MYSQL_THRESHOLD=5`, `MYSQL_REPLICATION_THRESHOLD=1`, `SOGO_THRESHOLD=3`, `POSTFIX_THRESHOLD=8`, `CLAMD_THRESHOLD=15`, `DOVECOT_THRESHOLD=12`, `DOVECOT_REPL_THRESHOLD=20`, `PHPFPM_THRESHOLD=5`, `RATELIMIT_THRESHOLD=1`, `FAIL2BAN_THRESHOLD=1`, `ACME_THRESHOLD=1`, `RSPAMD_THRESHOLD=5`, `OLEFY_THRESHOLD=5`, `MAILQ_THRESHOLD=20` and `MAILQ_CRIT=30`.

Override by adding the variable, for example `MAILQ_THRESHOLD=10`, to `mailcow.conf` and recreating the containers with `docker compose up -d`.

What each checks: Nginx connection on port 8081; Unbound resolving and DNSSEC validation of external domains; Redis on 6379; MySQL connection and a table query; SOGo on 20000; Postfix by sending a test mail; Clamd connection; PHP-FPM on 9001/9002; olefy on 10005; Dovecot and Rspamd with various tests. For most of these the docs say the watchdog notifies administrators and restarts the container once the threshold is reached. MySQL replication, Dovecot replication, rate limit hits, fail2ban bans and acme-mailcow problems only notify administrators. The mail queue alert fires when the Postfix queue holds more than `MAILQ_CRIT` mails for `MAILQ_THRESHOLD` * (60+-30) seconds.

## Checked

2026-11-04. Confirmed on the Watchdog thresholds page: all default threshold values, the mailcow.conf override with docker compose up -d, and each per-service check (Nginx 8081, Redis 6379, SOGo 20000, PHP-FPM 9001/9002, olefy 10005, Unbound DNSSEC, MySQL table query). Fixed: restart-on-threshold applies only to some services, replication, rate limit, fail2ban and ACME thresholds only notify; corrected the MAILQ_CRIT/MAILQ_THRESHOLD meaning.

Method: documentation only; no commands were run.
