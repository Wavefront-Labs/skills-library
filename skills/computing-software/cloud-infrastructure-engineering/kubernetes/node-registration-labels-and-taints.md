---
id: computing-software.cloud-infrastructure-engineering.kubernetes.node-registration-labels-and-taints
name: node-registration-labels-and-taints
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kubelet, node-labels, register-with-taints, node-registration-flags, noderestriction, kubeadm, node-role, node-restriction-labels]
level: practitioner
status: docs-checked
description: "Have nodes register with the right labels and taints (kubelet --node-labels, registerWithTaints, kubeadm nodeRegistration) and respect the NodeRestriction label limits."
sources: ["https://kubernetes.io/docs/reference/config-api/kubeadm-config.v1beta4/", "https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/#noderestriction", "https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Node registration: labels and taints at join time

Labelling/tainting after join leaves a window where pods land on the wrong node. Register
nodes with their identity instead.

## kubeadm
```yaml
apiVersion: kubeadm.k8s.io/v1beta4
kind: JoinConfiguration
nodeRegistration:
  name: gpu-node-01
  kubeletExtraArgs:
  - {name: node-labels, value: "pool=gpu,topology.example.com/rack=r12"}
  taints:
  - {key: nvidia.com/gpu, value: "present", effect: NoSchedule}
```
If `taints` is unset, control-plane nodes get the control-plane taint by default; set `taints: []`
explicitly to leave the node untainted (single-node clusters). The field is used only for Node
registration. `kubeletExtraArgs` is a list of name/value pairs in `kubeadm.k8s.io/v1beta4`.

## Raw kubelet
`--node-labels=pool=gpu,tier=batch` (key=value pairs separated by commas) and
`--register-with-taints=dedicated=batch:NoSchedule` (`<key>=<value>:<effect>`; a no-op if
`register-node` is false). Both apply when the node registers; to change them on an existing Node
use `kubectl label` / `kubectl taint`.

## NodeRestriction limits
kubeadm enables the NodeRestriction admission plugin. A kubelet may modify labels under the
`kubernetes.io` / `k8s.io` prefixes only from an allow-list: `kubernetes.io/hostname`,
`kubernetes.io/arch`, `kubernetes.io/os`, `beta.kubernetes.io/instance-type`,
`node.kubernetes.io/instance-type`, the deprecated `failure-domain.beta.kubernetes.io/region|zone`,
`topology.kubernetes.io/region`, `topology.kubernetes.io/zone`, and `kubelet.kubernetes.io/` and
`node.kubernetes.io/` prefixed labels. Labels with the `node-role.kubernetes.io/` or
`node-restriction.kubernetes.io/` prefix are forbidden for kubelets. The kubelet also validates
`--node-labels` itself and refuses to start with an unknown `kubernetes.io` or `k8s.io` label
("unknown 'kubernetes.io' or 'k8s.io' labels specified with --node-labels"), so
`--node-labels=node-role.kubernetes.io/worker=` does not work: set node-role labels from an admin or
controller after join. Use the `node-restriction.kubernetes.io/` prefix for isolation labels that a
compromised node cannot set.

## Cloud equivalents
Managed node pools and autoscalers have their own label and taint settings (read your provider's
or Karpenter's documentation); set them there rather than by hand.

## Verify
```bash
kubectl get nodes -L pool,topology.kubernetes.io/zone
kubectl get node gpu-node-01 -o jsonpath='{.spec.taints}'
```
- [ ] New nodes appear with labels/taints from first `Ready`, no manual step.

## Checked
2026-10-23, against the Kubernetes website kubeadm configuration reference (v1beta4 NodeRegistrationOptions: taints default and `taints: []`, kubeletExtraArgs name/value list), kubeadm implementation details (NodeRestriction enabled), the admission-controllers page (NodeRestriction allowed and forbidden labels), and the kubelet options source (`--node-labels` validation, `--register-with-taints` format). Cloud-provider flags and the journalctl pattern were removed as unconfirmed.
Method: documentation only; no commands were run.
