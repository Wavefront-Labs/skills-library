---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-kubernetes-scheduling
name: woodpecker-kubernetes-scheduling
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [node-selector, affinity, tolerations]
level: sme
status: docs-checked
description: "Control Woodpecker pod placement with nodeSelector, tolerations and affinity on Kubernetes."
sources: ["https://woodpecker-ci.org/docs/administration/configuration/backends/kubernetes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker Kubernetes scheduling

Per step, under `backend_options.kubernetes`:

```yaml
backend_options:
  kubernetes:
    nodeSelector:
      kubernetes.io/arch: "${ARCH}"
    tolerations:
      - key: 'key1'
        operator: 'Equal'
        value: 'value1'
        effect: 'NoSchedule'
    affinity:
      nodeAffinity:
        requiredDuringSchedulingIgnoredDuringExecution:
          nodeSelectorTerms:
            - matchExpressions:
                - key: topology.kubernetes.io/zone
                  operator: In
                  values: [eu-central-1a]
```

Node selector: your labels are appended to a list that already has `kubernetes.io/arch`, inferred from the agent platform. Override it per matrix element by defining a matrix variable (such as `ARCH: arm64`) and referencing it in `nodeSelector`. Per-step `nodeSelector` is blocked unless `WOODPECKER_BACKEND_K8S_POD_NODE_SELECTOR_ALLOW_FROM_STEP` is true. Agent-wide: `WOODPECKER_BACKEND_K8S_POD_NODE_SELECTOR`, a YAML object.

Tolerations: agent-wide `WOODPECKER_BACKEND_K8S_POD_TOLERATIONS`; per step allowed by default (`..._POD_TOLERATIONS_ALLOW_FROM_STEP` is true).

Affinity: agent-wide `WOODPECKER_BACKEND_K8S_POD_AFFINITY`, a YAML string. Per-step affinity needs `WOODPECKER_BACKEND_K8S_POD_AFFINITY_ALLOW_FROM_STEP: true`, and then replaces the agent-wide affinity entirely, without merging.

To co-locate all pods of a workflow, use `podAffinity` with `matchLabelKeys: [woodpecker-ci.org/task-uuid]` and `topologyKey: kubernetes.io/hostname`; `matchLabelKeys` needs Kubernetes v1.29+ with a feature gate, or v1.33+.

If a PVC is not highly available or NFS-based, use affinity to run steps on the correct node.

## Checked

2026-11-03. Read the Woodpecker Kubernetes backend page and confirmed nodeSelector arch handling and matrix override, tolerations default of allow-from-step true, affinity agent-wide and per-step replace behaviour, matchLabelKeys co-location example and its Kubernetes version gates. Nothing removed. 

Method: documentation only; no commands were run.
