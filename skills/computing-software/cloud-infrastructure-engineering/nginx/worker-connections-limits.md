---
id: computing-software.cloud-infrastructure-engineering.nginx.worker-connections-limits
name: worker-connections-limits
category: computing-software
field: cloud-infrastructure-engineering
product: nginx
tags: [nginx, worker-connections, worker-processes, worker-rlimit-nofile, file-descriptors]
level: practitioner
status: docs-checked
description: "Sizing nginx workers and connections: worker_processes auto, worker_connections including proxied connections, worker_rlimit_nofile and the stub_status signal."
sources: ["https://nginx.org/en/docs/ngx_core_module.html", "https://nginx.org/en/docs/http/ngx_http_stub_status_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

```nginx
worker_processes auto;            # default 1
worker_rlimit_nofile 65535;       # RLIMIT_NOFILE for workers
events {
    worker_connections 8192;      # default 512
    multi_accept off;             # default off
}
```

- `worker_processes number | auto`: the optimal value depends on CPU cores, disks and load pattern. When in doubt, use the number of CPU cores; `auto` tries to detect it (1.3.8, 1.2.5).
- `worker_connections` is the maximum simultaneous connections per worker. The number includes all connections, for example those with proxied servers, not only client connections. It also cannot exceed the current limit on open files, which `worker_rlimit_nofile` can raise (it changes `RLIMIT_NOFILE` for workers without restarting the main process).
- `multi_accept off`: a worker accepts one new connection at a time; `on` accepts all pending connections at a time. Ignored with kqueue.
- In `stub_status` output, `handled` below `accepts` means a resource limit such as `worker_connections` was reached.

## Checked
Date: 2026-11-03.
Confirmed in the ngx_core_module page: defaults, wording of all directives. Confirmed in the stub_status page: accepts versus handled.
Removed as unconfirmed: the "half the clients" estimate and 2x file descriptor rule, systemd `LimitNOFILE`, the error log messages, the container core-count remark, and the /proc limits verify step.
Method: documentation only; no commands were run.
