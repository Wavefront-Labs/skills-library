---
id: computing-software.messaging-and-integration.dapr.component-updates-and-hot-reload
name: component-updates-and-hot-reload
category: computing-software
field: messaging-and-integration
product: dapr
tags: [components, hot-reload, hotreload, ignoreerrors, rollout-restart, preview-features, kubernetes]
level: practitioner
status: docs-checked
description: "Update deployed Dapr components: apply YAML and restart sidecars, or enable the HotReload preview gate, with ignoreErrors behaviour and the actor state and workflow exceptions."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/components/component-updates.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dapr does not pick up component changes by itself unless the `HotReload` feature gate is on.

Kubernetes without hot reload, two steps:

1. Apply the new component YAML to the namespace.
2. Unless HotReload is on, perform a rollout restart of the deployments that use it (the page links the kubectl cheatsheet).

Self-hosted without hot reload: stop and restart the `daprd` process.

Hot reload is a preview feature enabled through the `HotReload` feature gate. Once on, creating, updating or deleting a component manifest takes effect in the running sidecar without restarting it or the pod.

Caveats from the page:

- An updated component is closed first, then re-initialized with the new configuration, so it is unavailable for a short period.
- If initialization fails, the sidecar follows `spec.ignoreErrors` of the component, the same as at boot: `false` (default) shuts the sidecar down gracefully; `true` keeps it running with neither the old nor the new component registered.
- Everything is supported except actor state stores and workflow backends. Changes to those are ignored and need a restart.

## Checked

2026-11-08. Restart steps for Kubernetes and self-hosted, HotReload behaviour, close-then-reinitialize caveat, ignoreErrors semantics and the actor state store and workflow backend exclusions confirmed on the Updating components page. Changed: dropped the Configuration features entry detail, the exact kubectl command and the production advice, none of which the page states.

Method: documentation only; every cited page read in full; no commands were run.
