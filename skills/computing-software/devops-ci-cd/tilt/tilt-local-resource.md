---
id: computing-software.devops-ci-cd.tilt.tilt-local-resource
name: tilt-local-resource
category: computing-software
field: devops-ci-cd
product: tilt
tags: [local-resource, tilt, serve-cmd, tiltfile]
level: practitioner
status: docs-checked
description: "Define local commands, servers and tests as Tilt resources with local_resource: deps, parallelism, auto_init, serve_cmd and readiness probes."
sources:
  - "https://docs.tilt.dev/local_resource.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# local_resource

Goal: run non-containerised work (installs, tests, local servers) as a Tilt sidebar resource.

```python
local_resource('yarn', cmd='yarn install', deps=['package.json'])
```

## Triggers and ordering

- `deps` (string or list of paths): changes re-run the command. In `TRIGGER_MODE_MANUAL` it shows a "pending changes" indicator instead. Without `deps` it runs once on `tilt up` and when its definition changes; the "force update" button always runs it.
- `ignore` works as for `docker_build` and `custom_build`.
- `resource_deps` orders initialisation, for example database init after the database is up.
- Local resource commands run serially with other commands to avoid races on files. `allow_parallel=True` lifts that, for example for linters or read-only tests.
- `auto_init=False` skips the run at startup. Combine with `trigger_mode=TRIGGER_MODE_MANUAL` (run only when triggered) or `TRIGGER_MODE_AUTO` (not on `tilt up`, but on dep changes, useful for tests).

## serve_cmd

Without it, the command is a batch job: in progress while running, then red or green by exit code. With `serve_cmd` Tilt first runs `cmd` (if non-empty) and does not kill the previous process until `cmd` succeeds; then it starts `serve_cmd` and counts the resource as updated and running. If `serve_cmd` exits with any code it turns red.

```python
local_resource('local-server', cmd='go build ./cmd/myserver', serve_cmd='./myserver --port=8001', deps=['cmd/myserver'])
local_resource('kube-port-forward', serve_cmd='kubectl port-forward -n openfaas svc/gateway 8080:8080')
```

Environments: `env` applies to `cmd`, `serve_env` to `serve_cmd`.

```python
local_resource('custom-env',
               cmd='go build ./cmd/myserver', env={'CGO_ENABLED': '0'},
               serve_cmd='./myserver', serve_env={'PORT': os.getenv('PORT', default='8001')},
               deps=['cmd/myserver'])
```

## readiness_probe

A probe decides when `serve_cmd` is ready; Tilt waits for success before starting dependent resources for the first time. Without one, it is ready once started. Probe actions: `http_get_action`, `tcp_socket_action`, `exec_action`.

```python
local_resource(
   "probe-example",
   serve_cmd="./myserver --port=8001",
   readiness_probe=probe(
      period_secs=15,
      http_get=http_get_action(port=8001, path="/health")
   )
)
```

## Checked

2026-11-07. Pages read from the tilt-dev/tilt.build source of docs.tilt.dev. Read the local_resource guide in full (deps, ignore, resource_deps, Parallelism, auto_init, serve_cmd, custom environment, readiness_probe sections) and the local_resource docstring in the repo's api/api/__init__.py to confirm that `env` goes to `cmd` and `serve_env` to `serve_cmd`. Confirmed every claim in the skill; nothing removed. Not opened: the linked blog posts and the probe API reference, so probe parameters beyond `period_secs` and `http_get` are not claimed. 

Method: documentation only; no commands were run.
