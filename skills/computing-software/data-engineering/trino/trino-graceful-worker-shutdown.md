---
id: computing-software.data-engineering.trino.trino-graceful-worker-shutdown
name: trino-graceful-worker-shutdown
category: computing-software
field: data-engineering
product: trino
tags: [graceful-shutdown, worker, shutting-down, grace-period, system-information]
level: practitioner
status: docs-checked
description: "Drain a Trino worker without failing queries using the graceful shutdown API, including the access control it requires."
sources: ["https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/admin/graceful-shutdown.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trino graceful worker shutdown

Trino has a graceful shutdown API that works only on workers. Call it with an HTTP PUT of the JSON string `"SHUTTING_DOWN"` to `/v1/info/state` on the worker:

```bash
curl -v -X PUT -d '"SHUTTING_DOWN"' -H 'Content-type: application/json' \
  -H 'X-Trino-User: authorizeduser' http://worker:8081/v1/info/state
```

With basic auth, use `-u 'authorizeduser:password'` against the HTTPS URL. A good call logs `Shutdown requested` at INFO in the worker log.

Shutdown sequence:
1. The worker enters the `SHUTTING_DOWN` state.
2. It sleeps for `shutdown.grace-period` (default 2 minutes); after this the coordinator knows and stops sending it tasks.
3. It blocks until all active tasks complete.
4. It sleeps for the grace period again so the coordinator sees the tasks finished.
5. The application shuts down.

Things to check first:
- On a secured cluster, provide the authorization header or satisfy whatever security is enabled.
- With TLS, the worker certificate must be CA signed or trusted by the caller; `--insecure` works but is not recommended.
- The default system access control does not allow graceful shutdown. Use `allow-all`, `file` system access control with system information rules, or Apache Ranger. The configuration must be present on every worker.
- The user needs permission to write system information (in Ranger: System Information - Write System Information).

## Checked

2026-11-04. Read against the Trino docs page `admin/graceful-shutdown.md` (GitHub source of the public docs): property names, defaults, allowed values, error messages, examples and behaviour described above match it. Nothing needed removing.
Method: documentation only; no commands were run.
