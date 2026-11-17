---
id: computing-software.collaboration-platform-administration.matrix-synapse.workers-systemd-and-synctl-management
name: workers-systemd-and-synctl-management
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, workers, systemd, synctl, matrix-synapse-target, hardening, pid-file, poetry]
level: advanced
status: docs-checked
description: "Run Synapse and its workers under systemd with matrix-synapse.target and the worker@ template, or with synctl -a and -w, plus the daemonize caveat."
sources:
  - https://element-hq.github.io/synapse/latest/systemd-with-workers/
  - https://element-hq.github.io/synapse/latest/synctl_workers.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The docs recommend systemd where available. Their setup provides a `matrix-synapse` service for the main process, a `matrix-synapse-worker@` template for workers, and a `matrix-synapse.target` that groups them. Worker configs are expected in `/etc/matrix-synapse/workers/<worker_name>.yaml` (edit the `*.service` files to use another location). The main process needs no separate file. Systemd handles daemonizing, so no config may set `daemonize` or `worker_daemonize`.

Set-up order: copy the `*.service` and `*.target` files to `/etc/systemd/system`, run `systemctl daemon-reload`, enable `matrix-synapse.service`, enable `matrix-synapse-worker@<worker_name>.service` for each worker, then start and enable the target:

```sh
systemctl start matrix-synapse.target
systemctl enable matrix-synapse.target
systemctl restart matrix-synapse-worker@generic_worker.service
```

The last line restarts one worker without touching the main process. For optional sandboxing, copy `override-hardened.conf` from `contrib/systemd` into `matrix-synapse.service.d/` and the worker variant into `matrix-synapse-worker@.service.d/`, reload systemd and restart; compare with `systemd-analyze security matrix-synapse.service`.

With synctl, the main process needs its own extra config containing `worker_app: synapse.app.homeserver`, and each worker needs a `worker_pid_file`. Operate on every worker file in a directory with `-a`, or one worker with `-w`:

```sh
synctl -a $CONFIG/workers start
synctl -w $CONFIG/workers/worker1.yaml restart
```

Always restart all workers when restarting or upgrading Synapse unless you know it is safe not to; for example, restarting without the synchrotrons may break typing notifications.

For a Poetry source install, start workers with `poetry run synapse_worker --config-path [your homeserver.yaml] --config-path [your worker.yaml]`.

## Checked

Method: docs-checked 2026-11-09 against docs/systemd-with-workers/README.md and docs/synctl_workers.md (read in full) plus docs/workers.md (Poetry section), Synapse develop branch, raw markdown.
