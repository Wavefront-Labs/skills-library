---
id: computing-software.messaging-and-integration.celery.celery-daemonize-systemd-and-initd
name: celery-daemonize-systemd-and-initd
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery-daemonizing, celery, systemd, init-d, celerybeat, daemon, pidfile, c-force-root]
level: practitioner
status: docs-checked
description: "Run Celery worker and beat as services with systemd unit files or generic init scripts, with config variables, tmpfiles, troubleshooting and the root check."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/daemonizing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Daemonize Celery with systemd or init scripts

Goal: run the worker (and beat) in the background under a service manager.

systemd (check with `systemctl --version`). `/etc/systemd/system/celery.service`:

```ini
[Service]
Type=forking
User=celery
Group=celery
EnvironmentFile=-/etc/conf.d/celery
WorkingDirectory=/opt/celery
ExecStart=/bin/sh -c '${CELERY_BIN} -A $CELERY_APP multi start $CELERYD_NODES \
    --pidfile=${CELERYD_PID_FILE} --logfile=${CELERYD_LOG_FILE} \
    --loglevel="${CELERYD_LOG_LEVEL}" $CELERYD_OPTS'
ExecStop=/bin/sh -c '${CELERY_BIN} multi stopwait $CELERYD_NODES \
    --pidfile=${CELERYD_PID_FILE} --logfile=${CELERYD_LOG_FILE}'
Restart=always
```

(plus `[Unit]` with `After=network.target` and `[Install]` `WantedBy=multi-user.target`; the page also defines `ExecReload` using `multi restart`). Run `systemctl daemon-reload` after each edit and `systemctl enable celery.service` to start at boot. For RabbitMQ, add `rabbitmq-server.service` to `After=` and `Requires=`. Create directories with `/etc/tmpfiles.d/celery.conf`: `d /run/celery 0755 celery celery -` and `d /var/log/celery 0755 celery celery -`.

`/etc/conf.d/celery`: `CELERYD_NODES="w1"`, `CELERY_BIN="/usr/local/bin/celery"`, `CELERY_APP="proj"`, `CELERYD_OPTS="--time-limit=300 --concurrency=8"`, `CELERYD_PID_FILE="/run/celery/%n.pid"`, `CELERYD_LOG_FILE="/var/log/celery/%n%I.log"`, `CELERYD_LOG_LEVEL="INFO"`. `%I` (child process index) matters with prefork: processes sharing one log file cause race conditions. Beat gets its own `celerybeat.service` (`Type=simple`, `celery -A ${CELERY_APP} beat --pidfile=... --logfile=... --loglevel=...`) and `systemctl enable celerybeat.service`.

Generic init scripts (`extra/generic-init.d/`): `/etc/init.d/celeryd {start|stop|restart|status}` reads `/etc/default/celeryd` (a root-owned sh file; export real env vars). Variables: `CELERYD_NODES`, `CELERY_BIN`, `CELERY_APP`, `CELERYD_CHDIR`, `CELERYD_OPTS` (supports per-node syntax like `-c:worker2 4`), `CELERYD_USER`, `CELERYD_GROUP`, `CELERY_CREATE_DIRS=1`; beat uses `CELERYBEAT_OPTS` etc. Unprivileged users use `celery multi` or `celery worker --detach`.

Troubleshooting: `sh -x /etc/init.d/celeryd start`. If it prints OK then exits silently, run `C_FAKEFORK=1 sh -x /etc/init.d/celeryd start` to see the errors. Celery refuses to run workers as root by default (the worker also appears to start then exit); override with `C_FORCE_ROOT`, but running as root is dangerous because pickle messages can execute arbitrary code.

## Checked

2026-11-07. Confirmed against the Celery 5.7.0 stable docs (userguide/daemonizing.html): the settings, defaults, parameters, code and wording kept in this skill. These are the pages' own claims, not independent tests. Nothing needed removing.

Method: documentation only; no commands were run.
