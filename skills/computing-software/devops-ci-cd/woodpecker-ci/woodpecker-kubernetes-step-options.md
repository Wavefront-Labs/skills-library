---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-kubernetes-step-options
name: woodpecker-kubernetes-step-options
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [backend-options, resources, security-context]
level: sme
status: docs-checked
description: "Set per-step Kubernetes resources, security context and service account in Woodpecker backend_options."
sources: ["https://woodpecker-ci.org/docs/administration/configuration/backends/kubernetes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker Kubernetes step options

Per-step settings live under `backend_options.kubernetes`. Always set `resources` for efficient scheduling:

```yaml
steps:
  - name: build
    image: alpine
    backend_options:
      kubernetes:
        resources:
          requests: { memory: 200Mi, cpu: 100m }
          limits: { memory: 400Mi, cpu: 1000m }
```

Use LimitRanges for per-namespace defaults.

`securityContext` mixes Pod and container fields in one object; container-only fields go to the container:

```yaml
backend_options:
  kubernetes:
    securityContext:
      runAsUser: 999
      allowPrivilegeEscalation: false
      capabilities:
        drop: [ALL]
```

You can also set `seccompProfile`, `apparmorProfile` and `fsGroupChangePolicy` (the last needs Kubernetes v1.30 or newer). Capabilities can only be dropped.

Other options: `runtimeClassName`, `hostUsers: false` (needs Kubernetes v1.25+ with the feature gate), `annotations`, `labels`, and `workspaceVolume: false` for service Pods.

Some are blocked by default and need an agent flag: `serviceAccountName` needs `WOODPECKER_BACKEND_K8S_SERVICE_ACCOUNT_NAME_ALLOW_FROM_STEP`, `runtimeClassName` needs `WOODPECKER_BACKEND_K8S_RUNTIME_CLASS_ALLOW_FROM_STEP`, annotations and labels need `..._POD_ANNOTATIONS_ALLOW_FROM_STEP` and `..._POD_LABELS_ALLOW_FROM_STEP`. In multi-tenant setups these allow privilege escalation, so enable them only for trusted authors.

## Checked

2026-11-03. Read the Woodpecker Kubernetes backend page and confirmed resources, securityContext, seccompProfile, apparmorProfile, fsGroupChangePolicy (Kubernetes v1.30), capability dropping only, runtimeClassName, hostUsers, workspaceVolume and the *_ALLOW_FROM_STEP agent flags. Nothing removed. 

Method: documentation only; no commands were run.
