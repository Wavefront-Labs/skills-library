---
id: computing-software.cloud-infrastructure-engineering.kubernetes.static-pod-limitations
name: static-pod-limitations
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, static-pods, static-pod-limitations, mirror-pods, kubelet]
level: practitioner
status: docs-checked
description: "Know what static pods cannot do (ServiceAccounts, ConfigMap or Secret refs, ephemeral containers, API edits) and design control-plane style pods around it."
sources: ["https://kubernetes.io/docs/tasks/configure-pod-container/static-pod/", "https://kubernetes.io/docs/concepts/workloads/pods/static-pods/", "https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/#noderestriction"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Static pod limitations

Static pods are created by the kubelet from local manifests; the API server only shows a
read-only mirror pod. Consequences:

| Limitation | Effect | Work-around |
|---|---|---|
| Cannot refer to a ServiceAccount | no API-issued identity | use host-mounted kubeconfig or certs (as kube-apiserver does) |
| Cannot refer to ConfigMaps or Secrets | no API-object volumes or env | `hostPath` files written by your config tooling |
| No ephemeral containers | not supported | debug from the node, for example `kubectl debug node/<n> -it --image=<debug-image>` or `crictl` |
| Controlled only by the kubelet | the mirror pod cannot be controlled from the API | edit the manifest on disk |
| `kubectl delete pod` | removes the mirror; kubelet recreates it | remove the file from `staticPodPath` |
| No controller | cannot be rolled out, rolled back or scaled by standard mechanisms | one pod per node; the kubelet restarts it if it fails; use a DaemonSet for node-level workloads on a running cluster |

## Behaviour notes
- Mirror pod name is `<name>-<nodeName>`; the `kubernetes.io/config.mirror` annotation marks it.
- The NodeRestriction admission plugin only lets a kubelet modify Pod objects bound to its own
  node, and the kubelet needs permission to create the mirror pod (otherwise the API server
  rejects it).
- File changes are picked up by periodic rescans of `staticPodPath` (default 20s); if a pod does
  not appear, check `journalctl -u kubelet`.

## Verify
```bash
kubectl get pod <name>-<node> -n kube-system -o jsonpath='{.metadata.annotations.kubernetes\.io/config\.source}'
```
Output `file` (or `http`) confirms it is static.

## Checked

Checked 2026-10-26 against Kubernetes documentation v1.37 (kubernetes/website commit 2026-10-25) and kubernetes/kubernetes master (kubelet source, 2026-10-24). Confirmed: static pod specs cannot refer to ServiceAccounts, ConfigMaps or Secrets; no ephemeral containers; the mirror pod cannot be controlled from the API and deleting it does not remove the static pod; static pods cannot be rolled out, rolled back or scaled and a DaemonSet is the recommended alternative; mirror pod naming and annotation; `config.source` values `file` and `http`; NodeRestriction limits a kubelet to Pod objects bound to its node; the kubelet needs permission to create the mirror pod. Removed as unconfirmed: the claims about admission rejection of SA fields, `clusterTrustBundle` volumes, and edit rejection on the mirror.

Method: documentation only; no commands were run.
