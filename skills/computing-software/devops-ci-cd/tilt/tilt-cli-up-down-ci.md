---
id: computing-software.devops-ci-cd.tilt.tilt-cli-up-down-ci
name: tilt-cli-up-down-ci
category: computing-software
field: devops-ci-cd
product: tilt
tags: [cli-up-down-ci, tilt, tilt-cli, ci]
level: practitioner
status: docs-checked
description: "Use tilt up, tilt down and tilt ci: Tiltfile args, key flags, what is and is not deleted, and CI exit behaviour."
sources:
  - "https://docs.tilt.dev/cli/tilt_up.html"
  - "https://docs.tilt.dev/cli/tilt_down.html"
  - "https://docs.tilt.dev/cli/tilt_ci.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tilt up, tilt down, tilt ci

All three: `tilt <cmd> [<tilt flags>] [-- <Tiltfile args>]`. Tilt flags are handled by Tilt; Tiltfile args can be anything and are read by `config.parse`.

## tilt up

Starts Tilt and runs the services in the Tiltfile. By default Tiltfile args are the services to start (`tilt up frontend backend`); no args starts all. That default does not apply if the Tiltfile uses `config.parse` or `config.set_enabled_resources`.

On Ctrl+C, Kubernetes and Docker Compose resources keep running (delete with `tilt down`); long-running local resources using `serve_cmd` are terminated.

Flags:

- `-f, --file` Tiltfile path (default `Tiltfile`)
- `--context`, `--namespace` Kubernetes overrides
- `--host` (default localhost, env `TILT_HOST`), `--port` (default 10350, `0` disables, env `TILT_PORT`)
- `--port-forwards=false` disables all port-forwards
- `--update-mode` one of auto, image, container, exec (default auto)
- `--stream` stream logs in the terminal; `--legacy` legacy terminal mode
- `--log-source` all, build or runtime; `--log-resource`; `--log-level` warn or error
- `--output-snapshot-on-exit <path>` writes a snapshot when Tilt exits

## tilt down

Deletes the resources specified in the Tiltfile. Namespaces are not deleted (use `--delete-namespaces`); Docker volumes are not deleted (use `--delete-volumes`); Kubernetes resources annotated `tilt.dev/down-policy: keep` are not deleted. Also takes `-f`, `--context`, `--namespace` and Tiltfile args to delete subsets.

## tilt ci

Batch mode. Exits with failure if any build fails or any server crashes; exits with success when all tasks completed and all servers are healthy. The UI is at localhost:10350 (configurable with `--host`/`--port`). `--timeout` defaults to 30m0s; 0 means no timeout. It shares most `tilt up` flags, including `--output-snapshot-on-exit`.

## Checked

Date: 2026-11-07

Every command, parameter, default, name and figure in this skill was matched line by line against the page text of https://docs.tilt.dev/cli/tilt_up.html, https://docs.tilt.dev/cli/tilt_down.html, https://docs.tilt.dev/cli/tilt_ci.html (read in full, including its code blocks and the page source in the tilt-dev/tilt.build docs repo; linked example-repo files and screenshots were not opened). No change was needed.

Method: documentation only; no commands were run.
