---
id: computing-software.web-development.node-express.process-management-pm2-systemd-cluster
name: process-management-pm2-systemd-cluster
category: computing-software
field: web-development
product: node-express
tags: [express, pm2, node-cluster, systemd, process-manager, zero-downtime-reload, containers, web-development]
level: practitioner
status: docs-checked
description: "Running Node/Express in production: PM2 cluster mode and reloads, systemd units, one-process-per-container, node:cluster, memory limits and signal handling."
sources:
  - https://github.com/Unitech/pm2
  - https://nodejs.org/api/cluster.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html
  - https://github.com/nodejs/docker-node/blob/main/docs/BestPractices.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Process management and clustering

**Goal:** restart on crash, use all CPU cores where appropriate, and deploy without dropped requests.

## 1. Pick by platform
| Platform | Supervisor | Multi-core |
|---|---|---|
| VM / bare metal | systemd or PM2 | PM2 cluster or node:cluster |
| Docker / Kubernetes | the orchestrator | more replicas, one Node process per container |
| PaaS (Render, Fly, Heroku) | platform | platform instances |

Inside Kubernetes pods prefer one Node process per container and let the orchestrator supervise it rather than adding PM2.

## 2. PM2
```js
// ecosystem.config.cjs
module.exports = { apps: [{
  name: "api", script: "dist/server.js",
  instances: "max", exec_mode: "cluster",
  max_memory_restart: "512M",
  env: { NODE_ENV: "production", PORT: 3000 },
  kill_timeout: 10000, listen_timeout: 8000,
}] };
```
```bash
pm2 start ecosystem.config.cjs
pm2 reload api            # graceful reload for HTTP/HTTPS apps, without downtime in cluster mode (restart = all at once)
pm2 startup && pm2 save   # survive reboots
pm2 install pm2-logrotate
```

## 3. systemd
```ini
# /etc/systemd/system/api.service
[Service]
User=api
WorkingDirectory=/srv/api
Environment=NODE_ENV=production
EnvironmentFile=/etc/api.env
ExecStart=/usr/bin/node dist/server.js
Restart=on-failure
RestartSec=2
KillSignal=SIGTERM
TimeoutStopSec=20
LimitNOFILE=65536
NoNewPrivileges=true
[Install]
WantedBy=multi-user.target
```
`systemctl daemon-reload && systemctl enable --now api`; logs via `journalctl -u api -f`.

## 4. node:cluster directly
```js
import cluster from "node:cluster";
import { availableParallelism } from "node:os";
if (cluster.isPrimary) {
  for (let i = 0; i < availableParallelism(); i++) cluster.fork();
  cluster.on("exit", (w, code) => { if (code !== 0) cluster.fork(); });
} else { startServer(); }
```
Workers share no memory: in-process sessions, caches, rate-limit counters and WebSocket rooms need Redis (and sticky sessions for Socket.IO long-polling).

## 5. Containers
- Run `node` directly (`CMD ["node", "dist/server.js"]`), not `npm start` (npm swallows exit signals such as SIGTERM and SIGINT). Use `--init`/tini if you spawn children.
- Handle SIGTERM: stop accepting, drain, close DB, exit.
- Set the V8 heap below the container memory limit with `--max-old-space-size` (it is allowed in `NODE_OPTIONS`), leaving room for buffers and native memory.

## Verify
- [ ] `kill -9` the process: supervisor restarts it within seconds.
- [ ] Load test during `pm2 reload` / rolling deploy shows no 5xx.
- [ ] Container receives SIGTERM and exits cleanly within the grace period (`docker stop` returns within the grace period).

## Checked

2026-10-25 against the PM2 repository (Unitech/pm2 main: README, CLI and option schema), the systemd man page sources, the Node.js cluster, os and CLI docs and the docker-node best practices. Confirmed: PM2 option schema: instances, exec_mode (cluster or fork), max_memory_restart, env, kill_timeout (default 1600 ms) and listen_timeout; "max" is a documented instances value; reload, startup, save and pm2-logrotate exist; PM2 reload is for HTTP/HTTPS apps and lets apps reload without downtime; systemd directives Restart=on-failure, RestartSec, EnvironmentFile, TimeoutStopSec, KillSignal, LimitNOFILE and NoNewPrivileges exist; Node cluster isPrimary, os.availableParallelism and NODE_OPTIONS allowing --max-old-space-size; docker-node: exec-form CMD stops npm swallowing SIGTERM and SIGINT, --init wraps Node in tini.

Method: documentation only; no commands were run.
