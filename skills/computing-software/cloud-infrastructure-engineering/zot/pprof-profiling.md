---
id: computing-software.cloud-infrastructure-engineering.zot.pprof-profiling
name: pprof-profiling
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, pprof, cpu-profile, go-tool-pprof, execution-trace, performance-profiling]
level: advanced
status: docs-checked
description: "Collect CPU, heap, goroutine and trace profiles from a running Zot at /v2/_zot/pprof/ and analyse them with go tool pprof and go tool trace."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/pprofiling.md
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/authn-authz.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Endpoints: `/v2/_zot/pprof/` lists profiles with record counts; `/v2/_zot/pprof/<profile-type>[?params]` exports one. If authentication is enabled, only an admin user can use them (needs `adminPolicy`).

Profile types: `allocs`, `block`, `cmdline`, `goroutine` (add `debug=2` for panic format), `heap` (add `gc` to run GC first), `mutex`, `profile` (CPU, `seconds`), `threadcreate`, `trace` (`seconds`).

Collect a 30-second CPU profile (default is 30):

```
curl -s http://localhost:8080/v2/_zot/pprof/profile?seconds=30 > cpu.prof
```

Redirect to a file or use `curl -O`, otherwise curl fails with "Failure writing output to destination".

Analyse:

```
go tool pprof -http=:9090 cpu.prof     # web UI, Flame Graph view recommended
go tool pprof -png cpu.prof            # image
go tool pprof cpu.prof                 # interactive, then: top
```

Execution trace:

```
curl -s -v http://localhost:8080/v2/_zot/pprof/trace?seconds=30 > trace.prof
go tool trace trace.prof
go tool trace -pprof=net trace.prof    # net, sync, syscall or sched
```

## Checked

2026-11-04. Read against the zot profiling article and authn-authz article (admin-only routes). Removed: the statement that the endpoints need no configuration and are always enabled, which the page does not make.

Method: documentation only; no commands were run.
