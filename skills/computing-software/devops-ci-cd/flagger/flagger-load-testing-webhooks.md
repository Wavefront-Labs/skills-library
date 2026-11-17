---
id: computing-software.devops-ci-cd.flagger.flagger-load-testing-webhooks
name: flagger-load-testing-webhooks
category: computing-software
field: devops-ci-cd
product: flagger
tags: [load-testing, loadtester, k6, ngrinder]
level: practitioner
status: docs-checked
description: "Generate traffic for Flagger canary analysis with the loadtester webhook, nGrinder delegation or a k6 webhook for workloads without constant traffic."
sources:
  - https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/usage/webhooks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Workloads without steady traffic need generated load, otherwise metrics have nothing to measure. A `rollout` webhook to the Flagger loadtester runs a command against the canary service address, as in the canary example: `cmd: "hey -z 1m -q 10 -c 2 http://podinfo-canary.test:9898/"`.

The loadtester can delegate to nGrinder with `metadata.type: ngrinder`, plus `server`, `clone` (id of an existing test), `username`, base64 `passwd` and `pollInterval` (default 1s). It sends a clone_and_start request when analysis starts, polls status, and avoids duplicate requests in later loops.

Third-party option: the Grafana `flagger-k6-webhook`, used for example as a `pre-rollout` hook with a k6 script in `metadata.script` and `timeout: 5m`, load testing a service before any traffic reaches it (thresholds in the k6 script, such as `http_req_duration: ['p(95)<50']`, decide pass or fail).

If Flagger runs outside the mesh, see the FAQ on how it can start the load test.

## Checked

2026-11-03. Confirmed against the Flagger documentation: https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/usage/webhooks.md.

No wrong claims found; nothing needed removing.

Method: documentation only; no commands were run.
