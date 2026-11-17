---
id: computing-software.cloud-infrastructure-engineering.kubernetes.karpenter-nodeclaim-debugging
name: karpenter-nodeclaim-debugging
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, karpenter, nodeclaim, node-autoscaling, aws, troubleshooting]
level: practitioner
status: docs-checked
description: "Debug Karpenter NodeClaims stuck before Launched, Registered or Initialized, using their conditions, events and the controller logs."
sources: ["https://karpenter.sh/docs/concepts/nodeclaims/", "https://karpenter.sh/docs/troubleshooting/", "https://karpenter.sh/docs/concepts/nodepools/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Karpenter NodeClaim debugging

Each node Karpenter creates is first a `NodeClaim`. Its conditions show how far it got.

```bash
kubectl get nodeclaims -o wide
kubectl describe nodeclaim <name>
kubectl logs <karpenter-pod> -c controller -n <karpenter-namespace> --tail=200     # namespace: kube-system or karpenter, per your install
```

| Stuck at | Meaning | Check |
|---|---|---|
| `Launched=False` | the cloud instance was not created | controller logs and the NodeClaim and EC2NodeClass status conditions |
| `Registered=False` | the instance exists but its node has not joined the cluster and lost the `karpenter.sh/unregistered` taint | the node's bootstrap and kubelet logs |
| `Initialized=False` | the node has not become ready, startup taints remain, or requested resources (for example GPUs) are not registered | `kubectl describe node`, CNI and device plugin pods |
| NodeClaim removed after 15 minutes | registration did not complete within 15 minutes, so Karpenter removed the NodeClaim and deleted the instance | same as Registered |

## Pods not triggering any NodeClaim
```bash
kubectl describe pod <pending> | grep -A5 Events
kubectl logs <karpenter-pod> -c controller -n <karpenter-namespace>
```
Usual reasons: NodePool requirements exclude what the pod asks for (arch, zone, capacity type),
NodePool `limits` reached (Karpenter stops creating instances once a limit is exceeded), or the pod
tolerates nothing the NodePool taints.

## Disruption side
`kubectl get nodeclaims -o jsonpath='{range .items[*]}{.metadata.name} {.status.conditions[?(@.type=="Drifted")].status}{"\n"}{end}'`
shows which claims Karpenter plans to replace.

## Verify
A healthy NodeClaim shows `Launched`, `Registered`, `Initialized` and `Ready` all True and has
`status.nodeName` set.

## Checked
2026-10-26. Checked against the Karpenter docs source for v1.15 (repository aws/karpenter-provider-aws, latest release v1.15.1). Confirmed: a NodeClaim moves through launch, registration and initialization, with conditions Launched, Registered, Initialized and Ready; during registration Karpenter removes the `karpenter.sh/unregistered` taint once the node joins and, if registration does not complete within 15 minutes, removes the NodeClaim and deletes the instance; initialization waits for the node to be ready, startup taints removed and requested resources registered; NodePool `limits` stop new instance creation once exceeded; the controller container is `controller` and the install namespace varies (the getting-started guide uses kube-system, the troubleshooting page uses karpenter). Removed as unconfirmed: the per-cause error strings, IAM action names, `registrationTTL`, the log search phrase and the label selector.
Method: documentation only; no commands were run.
