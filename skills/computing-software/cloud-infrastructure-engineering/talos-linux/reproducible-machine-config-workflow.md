---
id: computing-software.cloud-infrastructure-engineering.talos-linux.reproducible-machine-config-workflow
name: reproducible-machine-config-workflow
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [machine-config, reproducibility, secrets-yaml, gen-config, patches, drift, talos-version-contract]
level: advanced
status: docs-checked
description: "Avoid machine config drift: keep secrets.yaml and small patches in Git, regenerate configs with a pinned talos-version contract and kubernetes-version, apply, discard output."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/configure-your-talos-cluster/system-configuration/reproducible-machine-configuration.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Upgrades can make the declared config in Git drift from what runs on nodes. The docs recommend not storing full generated configs; store inputs and regenerate on demand.

Required inputs:

- `secrets.yaml`, generated once at cluster creation.
- Patch files describing your differences from defaults (networking, node labels, extra arguments).
- Cluster name and Kubernetes control plane endpoint.
- `--kubernetes-version`: the version the cluster runs right now.
- `--talos-version`: the contract, the Talos version you originally generated with. Keep it fixed. Leaving it unset or raising it can introduce new fields or defaults and silently change behaviour; bump it only when you deliberately upgrade Talos.

Regenerate:

```bash
talosctl gen config <cluster-name> <cluster-endpoint> \
    --with-secrets secrets.yaml \
    --kubernetes-version <kubernetes-version> \
    --talos-version <talos-version-contract> \
    --config-patch @patches/common.yaml \
    --config-patch @patches/controlplane.yaml \
    --config-patch @patches/my-node1.yaml \
    --output-types controlplane \
    --output controlplane-my-node1.yaml
```

Then apply the result to the node and discard it; do not commit it. Version bumps live in the regenerated base while intent stays in small durable patches. Layer patches from common to per-node as shown (`common`, `controlplane`, node-specific).

## Checked

2026-11-04. Reproducible Machine Configuration page confirms the inputs list, version-contract warning and the gen config command.

Method: documentation only; no commands were run.
