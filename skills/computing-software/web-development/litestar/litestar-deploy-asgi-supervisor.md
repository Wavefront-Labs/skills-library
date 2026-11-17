---
id: computing-software.web-development.litestar.litestar-deploy-asgi-supervisor
name: litestar-deploy-asgi-supervisor
category: computing-software
field: web-development
product: litestar
tags: [litestar, deployment, uvicorn, gunicorn, supervisor, hypercorn, granian, asgi-server]
level: practitioner
status: docs-checked
description: "Run a Litestar app with Uvicorn, Hypercorn, Daphne or Granian, understand why Gunicorn workers are legacy, and keep it running under Supervisor."
sources: [https://docs.litestar.dev/latest/topics/deployment/manually-with-asgi-server.html, https://docs.litestar.dev/latest/topics/deployment/supervisor.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar deployment: ASGI server and Supervisor

Goal: start the app with an ASGI server, then keep it alive with Supervisor.

## Method

1. Running an ASGI server by hand is usually only ideal for development and testing. For production the page recommends a container (Docker, Kubernetes) or a process manager (Supervisor, systemd).
2. Servers and install:
   - Uvicorn (`pip install uvicorn`): HTTP/1.1 and WebSocket. Run `uvicorn app:app`; expect `Uvicorn running on http://127.0.0.1:8000`.
   - Hypercorn (`pip install hypercorn`): HTTP/1.1, HTTP/2, WebSocket. Run `hypercorn app:app`.
   - Daphne (`pip install daphne`): HTTP/1.1, HTTP/2, WebSocket. Run `daphne app:app`.
   - Granian (`pip install granian`): Rust-based, HTTP/1.1, HTTP/2, WebSocket. Run `granian --interface asgi app:app`.
3. Gunicorn with Uvicorn workers is legacy: Uvicorn 0.30.0+ has a native multiprocess manager meant to replace Gunicorn. For new deployments use Uvicorn directly.
4. Supervisor service definition, placed at `/etc/supervisor/conf.d/exampleapp.conf`:

```ini
[program:exampleapp]
directory=/opt/exampleapp/src
command=/opt/exampleapp/venv/bin/litestar app.py
redirect_stderr=true
stdout_logfile=/var/log/exampleapp.log
stdout_logfile_backups=10
autostart=true
autorestart=true
```

   (`directory` is where the service runs; `autostart` starts it with Supervisor; `autorestart` restarts it after an unexpected exit.)
5. Load and control it:

```shell
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start exampleapp
sudo supervisorctl status exampleapp
sudo supervisorctl tail -f exampleapp
```

   `stop` and `restart` work the same way.
6. Optional: a shell function in a file under `/etc/profile.d/` wraps these as `exampleapp start|stop|restart|status|watch`; activate it with `source` on that file. An `update` case can stop the service, `git fetch --all` and `git reset --hard origin/master`, relink the Supervisor config, run `supervisorctl reread` and `update`, reinstall requirements, then offer to start the service.

## Verify

After `supervisorctl start exampleapp`, `supervisorctl status exampleapp` should show the service running, and the app is reachable at `http://0.0.0.0:8000` by default per the page.

## Checked

2026-11-07. Read the full cited page(s) (topics/deployment/manually-with-asgi-server.html, topics/deployment/supervisor.html) and the example files they include, and confirmed the claims in this skill against that text. Nothing needed removing.

Method: documentation only; no commands were run.
