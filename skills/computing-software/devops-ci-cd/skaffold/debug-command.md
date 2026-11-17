---
id: computing-software.devops-ci-cd.skaffold.debug-command
name: debug-command
category: computing-software
field: devops-ci-cd
product: skaffold
tags: [debug, delve, jdwp, debugpy, runtimetype]
level: advanced
status: docs-checked
description: "Run containers under language debuggers with skaffold debug and the runtime-specific requirements."
sources:
  - "https://skaffold.dev/docs/workflows/debug/"
  - "https://skaffold.dev/docs/references/yaml/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`skaffold debug` acts like `dev`, but reconfigures containers in pods to run under a debugger and exposes the debug ports so they can be port-forwarded. Unlike `dev`, it disables image rebuilding, redeploying and file syncing by default, because saving files would end debug sessions; re-enable with `--auto-build`, `--auto-deploy` and `--auto-sync`.

Supported runtimes (runtime ID, debugger):

- Go 1.13+ (`go`): Delve, headless, port 56268.
- NodeJS (`nodejs`): Node inspector via `--inspect`, port 9229.
- Java and JVM languages (`jvm`): JDWP via `JAVA_TOOL_OPTIONS`, port 5005.
- Python 3.5-3.10 (`python`): `debugpy` or `pydevd`, port 5678. The page says 3.11 support is in progress.
- .NET Core: `vsdbg`, VS Code only.

By default `skaffold debug` forwards the `user` and `debug` port classes (see the port-forwarding skill); connect your IDE to the forwarded debug port. Skaffold detects the runtime from the built image. Override it on the artifact:

```yaml
artifacts:
- image: app
  runtimeType: go
```

`runtimeType` must be one of `go`, `nodejs`, `jvm`, `python` or `netcore` (the schema values). The debug page's own .NET heading says `dotnet`, so the pages disagree; use `netcore`, which is the value the config schema lists.

Detection and build notes from the docs:

- Go: recognised by `GODEBUG`, `GOGC`, `GOMAXPROCS` or `GOTRACEBACK`, by `KO_DATA_PATH` (ko images), or by launching with `dlv`. Build with `-gcflags='all=-N -l'`; Docker builds get a `SKAFFOLD_GO_GCFLAGS` build argument for that (`ARG SKAFFOLD_GO_GCFLAGS` then `go build -gcflags="${SKAFFOLD_GO_GCFLAGS}"`). The ko builder adds the flags automatically. Avoid `-trimpath`. Alpine-based `golang` images lack the C compiler this needs.
- JVM: recognised by `JAVA_VERSION` or `JAVA_TOOL_OPTIONS`, or a command line that invokes `java`.
- NodeJS: recognised by `NODE_VERSION`, `NODEJS_VERSION` or `NODE_ENV`, or a command line invoking `node` or `npm`.
- Python: recognised by standard `PYTHON*` variables or a command invoking `python`, `python2` or `python3`.
- .NET: build with `--configuration Debug`.

Go and Python containers must invoke the binary or launcher directly. Skaffold cannot debug them through user shell scripts or shell constructs such as `exec` or `eval` (`CMD gunicorn app:app` works; `CMD exec gunicorn app:app` does not). If an image is not recognised, `debug` warns "not configured for debugging".

Other behaviour: debug only configures images built by Skaffold; it rewrites replica counts to 1; it raises HTTP probe timeouts to 600 seconds (skip with the `debug.cloud.google.com/probe-timeouts: skip` annotation). It supports only the `kubectl`, `kustomize` and `helm` deployers (Helm v3.1.0 or later). Containers start in run-on-start mode, so breakpoints in the startup path are unlikely to be hit.

## Checked

2026-11-04. Read the whole Skaffold "Debugging With Skaffold" page and the `Artifact.runtimeType` description in the v4beta14 schema. Confirmed all items above. The default forwarding of user and debug ports is confirmed on the Port Forwarding page. Removed: the claim that Python/Node need no flags and must run the interpreter directly (the page gives that constraint for Go and Python only, and says Skaffold adds a node wrapper). Conflict: the .NET runtime ID is `netcore` in the page's runtime list and the schema but `dotnet` in the page's .NET headings.
Method: documentation only; no commands were run.
