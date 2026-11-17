---
id: computing-software.cloud-infrastructure-engineering.docker.remote-debugging-delve-debugpy-and-node-inspect-in-compose
name: remote-debugging-delve-debugpy-and-node-inspect-in-compose
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, remote-debugging, delve, debugpy, node-inspect, jdwp, compose-override, vscode-attach, path-mapping, debug-ports]
level: practitioner
status: docs-checked
description: "Attach an IDE debugger to code running in Compose: Delve, debugpy and Node --inspect listeners, safe port publishing and path mappings."
sources: ["https://github.com/go-delve/delve/blob/master/Documentation/usage/dlv_exec.md", "https://github.com/go-delve/delve/blob/master/Documentation/faq.md", "https://github.com/microsoft/debugpy", "https://nodejs.org/en/learn/getting-started/debugging"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Remote debugging in Compose (Delve, debugpy, Node)

**Pattern:** keep debug wiring in `compose.debug.yaml`, start with
`docker compose -f compose.yaml -f compose.debug.yaml up`, and attach from the IDE.

## Rules for every language
- The debugger defaults to loopback (Delve `127.0.0.1:0`, debugpy `localhost`, Node
  `127.0.0.1:9229`). Inside a container, bind it to `0.0.0.0` or the published port reaches nothing.
- Publish debug ports on `127.0.0.1` only (`"127.0.0.1:2345:2345"`). Node's docs warn that anyone
  who can connect to the inspector port may execute arbitrary code, and that binding to a
  public address or 0.0.0.0 removes the restriction.
- Use a debug build stage with the debugger installed.
- While paused at a breakpoint, a Compose `healthcheck` or restart policy may act on the
  stopped process; loosen them in the debug override (not covered by the cited pages).
- The IDE needs a path mapping between the local root and the container root.

## Go (Delve)
```bash
dlv exec --headless --continue --listen :2345 --accept-multiclient /app/server
```
- `--headless` runs the debug server only (JSON-RPC or DAP clients); `--listen` is the address
  (prefix `unix:` for a socket).
- Without `--continue` the program does not start until a client connects and sends
  `continue`. `--continue` starts it immediately and, per the Delve FAQ, is paired with
  `--accept-multiclient`.
- `--only-same-user` (default true) restricts connections to the user that started Delve.
- `--api-version` accepts only 2.
```yaml
# compose.debug.yaml
services:
  api:
    ports: ["127.0.0.1:2345:2345"]
```
Building with optimisations off (`-gcflags="all=-N -l"`) and any seccomp/ptrace container
settings are common practice but were not confirmed on the cited pages.

## Python (debugpy)
```yaml
services:
  web:
    command: ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0"]
    ports: ["127.0.0.1:5678:5678"]
```
- The debugpy README: the hostname in `--listen` is the interface the adapter listens on, and
  `0.0.0.0` listens on all interfaces so another machine (or the host through a published
  port) can attach.
- `--wait-for-client` pauses the program until a client attaches, so the service will not be
  ready until then.
- `--listen` works with `-m module` as well as a script.

## Node.js
```yaml
services:
  api:
    command: ["node", "--inspect=0.0.0.0:9229", "src/index.js"]
    ports: ["127.0.0.1:9229:9229"]
```
- `--inspect=[host:port]` binds the inspector (default `127.0.0.1:9229`).
- `--inspect-brk` breaks before user code starts; `--inspect-wait` waits for a debugger to attach.

## Verify
Start the stack with the debug override, confirm the published port is bound to loopback on the
host, attach the IDE and hit a breakpoint.

## Checked

Checked 2026-11-09 against the Delve `dlv exec` reference and FAQ, the debugpy README and the Node.js debugging guide. Removed because not confirmed by those pages: the Dockerfile and `-gcflags` recipe, `seccomp:unconfined` and `SYS_PTRACE`, all VS Code attach configurations and path mapping keys, the debugpy `--reload` subprocess claim, nodemon, TypeScript source map advice, the entire JVM/JDWP section, and the VS Code debugging source (not read).

Method: docs-checked 2026-11-09 against Delve dlv_exec and FAQ, debugpy README and Node.js debugging guide.
