---
id: computing-software.devops-ci-cd.argo-workflows.sidecar-injection
name: sidecar-injection
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [sidecar-injection, istio, kill-cmd, emissary, service-mesh]
level: advanced
status: docs-checked
description: "Stop mutating-webhook sidecars such as Istio proxies from blocking pod completion using emissary kill-cmd annotations in podMetadata."
sources: ["https://argo-workflows.readthedocs.io/en/latest/sidecar-injection/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Injected sidecars and kill commands
Sidecars added by mutating webhooks (service meshes such as Istio or Anthos) are invisible to the controller, which cannot rewrite their command. Their process runs as protected PID 1, so the wait container may be unable to stop them and pods never finish. The page's blunt advice: avoid Istio with Argo Workflows (issue 1282).

Support: with the `emissary` executor Argo can kill any declared sidecar, but an injected one only via `kubectl exec`.

Kubernetes cannot kill a single container, so Argo mimics termination: SIGTERM to PID 1, wait `terminateGracePeriodSeconds` (30s default), then SIGKILL. `preStop` and `STOPSIGNAL` are unsupported. The default exec is `/bin/sh -c 'kill 1'`, which fails if there is no `/bin/sh`, the process is not PID 1 (common with `runAsNonRoot`), or it ignores `kill 1`.

Override per container with a pod annotation; `%d` is the signal number:

```yaml
spec:
  podMetadata:
    annotations:
      workflows.argoproj.io/kill-cmd-istio-proxy: '["pilot-agent", "request", "POST", "quitquitquit"]'
      workflows.argoproj.io/kill-cmd-vault-agent: '["sh", "-c", "kill -%d 1"]'
```
The suffix after `kill-cmd-` is the sidecar container name, and the value is a JSON array command (see also the linkerd-await example on the page).

## Checked
2026-11-03. Confirmed against the Argo Workflows Sidecar Injection page: the problem statement, support matrix, SIGTERM then grace period then SIGKILL behaviour, unsupported preStop and STOPSIGNAL, default `/bin/sh -c 'kill 1'` and its failure modes, and the annotation override. Nothing removed.
Method: documentation only; no commands were run.
