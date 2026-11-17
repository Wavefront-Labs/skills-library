---
id: computing-software.cloud-infrastructure-engineering.kubernetes.node-networkunavailable-condition
name: node-networkunavailable-condition
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, troubleshooting-nodes, networkunavailable, node-conditions, cni, cloud-routes]
level: practitioner
status: docs-checked
description: "Diagnose the NetworkUnavailable node condition and network-unavailable taint, set by cloud route controllers or the CNI, that keeps pods off a node."
sources: ["https://kubernetes.io/docs/reference/node/node-status/#condition", "https://kubernetes.io/docs/reference/labels-annotations-taints/#node-kubernetes-io-network-unavailable", "https://kubernetes.io/docs/concepts/architecture/cloud-controller/", "https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/#taints-and-tolerations"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NetworkUnavailable

```bash
kubectl get node <n> -o jsonpath='{range .status.conditions[?(@.type=="NetworkUnavailable")]}{.status} {.reason} {.message}{"\n"}{end}'
kubectl describe node <n> | grep -i taint
```
The kubelet sets taint `node.kubernetes.io/network-unavailable:NoSchedule` at registration when
the cloud provider needs extra network configuration; the cloud provider removes it once the route is
configured. Ordinary pods do not schedule onto a node with this taint (DaemonSet pods that use
`hostNetwork` tolerate it).

## Who sets it
- Cloud route controller (cloud-controller-manager, `--configure-cloud-routes`, default true): sets
  True with reason `NoRouteCreated` while the node has no route, then False with reason
  `RouteCreated` once the route for the node's pod CIDR exists.
- CNIs that manage routing without cloud routes set the condition to False themselves when ready;
  check your CNI's documentation for the reason string it uses.

## Causes
| Situation | Fix |
|---|---|
| cloud route quota reached | use a VPC-native or overlay CNI; raise the quota with the cloud provider |
| cloud controller lacks permission to create routes | check cloud-controller-manager logs for route creation errors |
| CNI pod not running on the node | `kubectl -n kube-system get pods -o wide --field-selector spec.nodeName=<n>` |
| CNI changed, old condition left `True` | the new CNI must set it, or turn off cloud routes |

## Verify
Condition `False`, taint gone, and a test pod schedules and reaches pods on other nodes.

## Checked

Date: 2026-10-27. Documentation release: Kubernetes v1.37.1 (latest release; website main is the v1.38 development tree).

- `NetworkUnavailable` condition meaning: node-status reference.
- `node.kubernetes.io/network-unavailable` NoSchedule taint, set by the kubelet and removed by the cloud provider; added
  toleration for hostNetwork DaemonSet pods only: labels/taints page and DaemonSet page.
- Reasons `RouteCreated` / `NoRouteCreated` and the `--configure-cloud-routes` flag (default true): cloud-provider route
  controller and options source, v1.37.1.
- Removed: Calico and Cilium reason strings, Weave, and the GCE/AWS route quota figures, which no checked source covers.

Method: documentation only; no commands were run.
