---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubeedge-edge-nodes-and-offline-operation
name: kubeedge-edge-nodes-and-offline-operation
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kubeedge, edge-offline-operation, edge-computing, keadm, iot, edgemesh]
level: advanced
status: docs-checked
description: "Extend a cluster to unreliable edge sites with KubeEdge: keadm install of cloudcore/edgecore, offline autonomy, eviction tolerations, and cloud DaemonSets kept off edge nodes."
sources: ["https://kubeedge.io/docs/setup/install-with-keadm/", "https://kubeedge.io/docs/setup/prerequisites/runtime/", "https://kubeedge.io/docs/architecture/edge/metamanager/", "https://kubeedge.io/docs/advanced/debug/", "https://kubeedge.io/docs/faq/setup/", "https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/#taint-based-evictions"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# KubeEdge and offline edge operation

## Architecture
- **cloudcore** runs in the cloud cluster; edge nodes connect to it (WebSocket or QUIC), so
  ports `10000` and `10002` on cloudcore must be reachable from the edge.
- **edgecore** runs on each edge device as a binary (typically a systemd service). Its
  MetaManager stores pod and config metadata in a local SQLite database, which is what lets
  the edge keep its workload state while the link is down.
- EdgeMesh replaces kube-proxy for service traffic between edge pods.

## Install
```bash
# cloud side (kubectl context pointed at the cluster)
keadm init --advertise-address=<public-ip-or-lb> --kubeedge-version=<vX.Y.Z> --kube-config=<kubeconfig>
keadm gettoken
# edge side (needs a CRI runtime, for example containerd)
keadm join --cloudcore-ipport=<cloud-ip>:10000 --token=<token> \
  --kubeedge-version=<vX.Y.Z> \
  --remote-runtime-endpoint=unix:///run/containerd/containerd.sock
```
`--advertise-address` is added to the cloudcore certificate SANs; `--cloudcore-ipport` is
mandatory on join, and `--token` lets the edge get its certificate automatically. Use the
same KubeEdge version on the cloud and edge sides. `keadm init` deploys cloudcore in a
container by default. Ports 10003 (cloudStream) and 10004 (tunnel) carry `kubectl logs/exec`;
newer versions enable cloudStream by default.

## Designing for disconnection
When the link drops, the node becomes unreachable. Kubernetes gives pods default tolerations
for `node.kubernetes.io/not-ready` and `node.kubernetes.io/unreachable` with
`tolerationSeconds: 300`, after which the pods are evicted from the API, which is not what an
offline edge site wants. For edge workloads:
```yaml
tolerations:
- {key: node.kubernetes.io/unreachable, operator: Exists, effect: NoExecute}   # no tolerationSeconds = stays bound
- {key: node.kubernetes.io/not-ready,  operator: Exists, effect: NoExecute}
```
Also: images must already be on the device (pre-pull, local registry mirror), config and
secrets cached, and the app itself tolerant of losing upstream APIs.

## Keep cloud-only components off edge nodes
kube-proxy must not run on edge nodes (edgecore rejects it by default), and other cloud
DaemonSets may not work there either. KubeEdge documents this affinity for kube-proxy; use it
for other cloud-only DaemonSets too:
```yaml
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
      - matchExpressions: [{key: node-role.kubernetes.io/edge, operator: DoesNotExist}]
```
and target edge workloads with a `nodeSelector` on the edge label.

## Operations
- Upgrade cloudcore first, then edge nodes in waves, keeping versions matched.
- Monitor connection state: node Ready condition flapping per site; edgecore logs via
  `journalctl -u edgecore.service -xe` on the device.

## Verify
- [ ] Pull the network on a test edge node for longer than 5 minutes: pods keep serving
  locally, survive a device reboot, and are **not** restarted when the link comes back.

## Checked
Checked 2026-10-27 against kubeedge/website docs (install with keadm: v1.23.1 examples,
`--advertise-address`, `keadm gettoken`, `--cloudcore-ipport` mandatory, `--token`, matching
versions, ports 10000 and 10002, container-mode cloudcore; runtime prerequisites:
`--remote-runtime-endpoint` for containerd; MetaManager SQLite; debug page: cloudStream on
10003, tunnel on 10004, kube-proxy affinity on `node-role.kubernetes.io/edge`; FAQ: edgecore as
a binary, journalctl, websocket/quic config) and kubernetes/website taints and tolerations
(default 300 s not-ready/unreachable tolerations; no tolerationSeconds means bound forever).
Removed the pinned v1.21.0 version, the unconfirmed `--edgenode-name` flag, device-twin and
Sedna mentions, and the claim about deletions being applied on reconnect.

Method: documentation only; no commands were run.
