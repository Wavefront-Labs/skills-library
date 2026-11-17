---
id: computing-software.cloud-infrastructure-engineering.talos-linux.talos-root-ca-rotation
name: talos-root-ca-rotation
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [ca-rotation, pki, rotate-ca, accepted-cas, talosconfig, kubeconfig, kubeapiservercaconfig, security]
level: advanced
status: docs-checked
description: "Rotate the Talos API or Kubernetes API root CA with talosctl rotate-ca (dry-run first), the five-phase accepted/issuing flow, and the manual acceptedCAs steps."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/security/ca-rotation.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Root CAs live ten years, so rotation is needed only if the private key is compromised, you must revoke a leaked `talosconfig` or `kubeconfig`, or at the ten-year mark.

The flow is the same for both APIs: generate a new CA; add it as 'accepted'; swap the issuing CA to the new one with the old as accepted; refresh all certificates; remove the old CA from 'accepted'. Afterwards everything issued by the old CA is invalid.

**Talos API** (no connection interruptions, no reboot). Always dry-run first:

```shell
talosctl -n <CONTROLPLANE> rotate-ca --dry-run=true --talos=true --kubernetes=false
talosctl -n <CONTROLPLANE> rotate-ca --dry-run=false --talos=true --kubernetes=false
```

Capture the output: it contains the new CA. Record the Talos API users so each gets a new `talosconfig`; the new one is written to `talosconfig` in the current directory (merge with `talosctl config merge ./talosconfig`). Update `secrets.yaml` if you generate configs from it. Pods using Talos API access from Kubernetes may need manual restarts.

**Kubernetes API** (restarts control plane components; pods may need restarts and in-cluster traffic may be disrupted):

```shell
talosctl -n <CONTROLPLANE> rotate-ca --dry-run=false --talos=false --kubernetes=true
```

Fetch the new kubeconfig with `talosctl kubeconfig`. Only the Kubernetes API CA rotates; other Kubernetes secrets may need manual rotation.

**Manual Talos steps:** patch `.machine.acceptedCAs` on all nodes with the new CA; verify a new client cert is accepted; set `.machine.ca` to the new CA keeping the old one in `.machine.acceptedCAs` (workers have no key in `.machine.ca`); verify; remove the old one. For Kubernetes use `KubeAPIServerCAConfig` (`acceptedCAs`, `issuingCA`); the aggregator CA is `KubeAggregatorCAConfig`.

## Checked

Whole page read; triggers, flow, commands and manual field names confirmed.

Method: docs-checked 2026-11-09 against Talos v1.15 docs security/ca-rotation.mdx (read in full).
