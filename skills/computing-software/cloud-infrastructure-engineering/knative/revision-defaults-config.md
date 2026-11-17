---
id: computing-software.cloud-infrastructure-engineering.knative.revision-defaults-config
name: revision-defaults-config
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [config-defaults, revision-timeout-seconds, timeout-seconds, idle-timeout, container-concurrency-max-limit]
level: practitioner
status: docs-checked
description: "Tune default request timeouts, resource requests and limits, and concurrency caps for all Revisions."
sources:
  - https://knative.dev/docs/serving/configuration/config-defaults/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: set cluster-wide defaults that Revisions inherit when they specify nothing.

The `config-defaults` ConfigMap in `knative-serving` holds them. View with `kubectl get configmap -n knative-serving config-defaults -oyaml`.

Timeouts (global key, per-revision spec key, default):
- `revision-timeout-seconds`, `timeoutSeconds`, 300 (5 minutes): per-request timeout.
- `max-revision-timeout-seconds`, no per-revision key, 600: the cap for `revision-timeout-seconds`, which must be at most this value. If you raise it, also raise the activator's `terminationGracePeriodSeconds` so in-flight requests are not disrupted.
- `revision-response-start-timeout-seconds`, `responseStartTimeoutSeconds`, 300.
- `revision-idle-timeout-seconds`, `idleTimeoutSeconds`, 0 meaning infinite.

Resources (the page lists the resource names `cpu`, `memory` and `ephemeral-storage` as the per-revision keys, but its per-Revision examples set `resources.requests` or `resources.limits` on the container; it also says these keys are "not enabled by default" even though its example ConfigMap lists the values, so treat the values as the defaults used when the key is set):
- Requests: `revision-cpu-request` 400m, `revision-memory-request` 100M, `revision-ephemeral-storage-request` 500M.
- Limits: `revision-cpu-limit` 1000m, `revision-memory-limit` 200M, `revision-ephemeral-storage-limit` 750M.

Other keys:
- `container-name-template`: default `user-container`.
- `container-concurrency`: default 0, per-revision `containerConcurrency`.
- `container-concurrency-max-limit`: default 1000; must be greater than 1, and the `container-concurrency` default must be at or below it. A user can still choose `containerConcurrency: 0` unless `allow-container-concurrency-zero` is `"false"`.
- `allow-container-concurrency-zero`: default true.
- `enable-service-links`: default for the PodSpec `enableServiceLinks` field when the user omits it; a tri-state flag with values true, false or default. The page's default is `"false"` and it suggests `false` in environments with a large number of Services.

Per-revision values override these defaults for that Revision only. With the Operator, the page shows `container-concurrency-max-limit` set under `spec.config.defaults` of the `KnativeServing` resource; its other keys show only the ConfigMap form.

## Checked

2026-11-04. Confirmed against the Configuring the Defaults ConfigMap page (knative/docs source): the `config-defaults` ConfigMap in `knative-serving`, the view command, every key and default listed (timeouts 300, 600, 300, 0 infinite; resource requests 400m, 100M, 500M; limits 1000m, 200M, 750M; `user-container`; concurrency 0, 1000, true), the per-revision spec keys `timeoutSeconds`, `responseStartTimeoutSeconds`, `idleTimeoutSeconds`, `containerConcurrency`, the activator `terminationGracePeriodSeconds` advice, and the tri-state `enable-service-links`. Page-internal tension recorded in the skill: the page says the resource keys are not enabled by default yet shows default values, and names annotation keys while its examples use container resources. Added the missing `enable-service-links` default and the concurrency constraints, and narrowed the Operator sentence to what the page shows.

Method: documentation only; no commands were run.
