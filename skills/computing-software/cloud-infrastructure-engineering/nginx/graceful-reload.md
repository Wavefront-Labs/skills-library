---
id: computing-software.cloud-infrastructure-engineering.nginx.graceful-reload
name: graceful-reload
category: computing-software
field: cloud-infrastructure-engineering
product: nginx
tags: [nginx, nginx-reload, reload, hup, graceful, signal]
level: intro
status: docs-checked
description: "Reloading nginx configuration without dropping connections with nginx -s reload or HUP, and what happens to old and new workers."
sources: ["https://nginx.org/en/docs/control.html", "https://nginx.org/en/docs/switches.html", "https://nginx.org/en/docs/ngx_core_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`nginx -s reload` sends `HUP` to the master process. On `HUP` the master:

1. checks the syntax of the configuration and tries to apply it, that is, open log files and new listen sockets;
2. if that fails, rolls back and keeps working with the old configuration;
3. if it succeeds, starts new worker processes and asks the old workers to shut down gracefully.

Old workers close their listen sockets and keep serving existing clients; after all clients are served they exit. During this window `ps` shows `nginx: worker process is shutting down` for the old workers.

`worker_shutdown_timeout time;` (main context, 1.11.11) sets a timeout for the graceful shutdown of workers; when it expires nginx tries to close all connections still open so the worker can exit.

`HUP` also covers keeping up with a changed time zone (FreeBSD and Linux only). A new executable is not picked up by `HUP`; see the USR2 upgrade skill.

```bash
nginx -t && nginx -s reload
```

## Checked

2026-11-03. Confirmed against the nginx "Controlling nginx" page (HUP behaviour and process listing), "Command-line parameters" (`-s reload`) and `ngx_core_module` (`worker_shutdown_timeout`). Removed: the `worker_shutdown_timeout 30s` figure, claims about systemd, memory exhaustion, which master settings a reload cannot change, and the Verify step.
Method: documentation only; no commands were run.
