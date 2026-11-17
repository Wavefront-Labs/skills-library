---
id: computing-software.cloud-infrastructure-engineering.kubernetes.pod-startup-failures-containercreating-and-errimagepull
name: pod-startup-failures-containercreating-and-errimagepull
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, troubleshooting, containercreating, stuck-containercreating, errimagepull, imagepullbackoff, registry-rate-limit, createcontainerconfigerror, cka]
level: practitioner
status: docs-checked
description: "Unstick pods before Running: ContainerCreating (volumes, CNI, secrets, sandbox), ErrImagePull/ImagePullBackOff (name, tag, auth, rate limits, arch) and CreateContainerConfigError."
sources: ["https://kubernetes.io/docs/tasks/debug/debug-application/debug-pods/", "https://kubernetes.io/docs/concepts/containers/images/#imagepullbackoff", "https://docs.docker.com/docker-hub/usage/pulls/", "https://github.com/containerd/containerd/blob/main/docs/hosts.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pod startup failures: ContainerCreating and ErrImagePull

Always start with the events at the bottom of:
```bash
kubectl describe pod <p> | sed -n '/Events/,$p'
```

## Stuck ContainerCreating
| Event | Cause | Fix |
|---|---|---|
| `FailedMount` naming a missing ConfigMap or Secret | missing object or key | create it / fix name; `optional: true` if appropriate |
| `FailedAttachVolume` for a ReadWriteOnce volume | volume still attached to another node | wait for old pod/VolumeAttachment, see multi-attach skill |
| `FailedMount` after a long wait | CSI node plugin issue, NFS unreachable | CSI node pod logs on that node |
| `FailedCreatePodSandBox` with a network setup error | CNI broken/IPAM exhausted on node | CNI pod logs on node, IP pool usage |
| `FailedCreatePodSandBox` with an image pull error | sandbox image unreachable (air gap) | mirror the sandbox image your runtime uses |
| no events, minutes | kubelet overloaded / PLEG / runtime hung | node triage |

## ErrImagePull / ImagePullBackOff
```bash
kubectl get pod <p> -o jsonpath='{.status.containerStatuses[*].state.waiting.message}'
```
| Message fragment | Cause |
|---|---|
| manifest not found | wrong tag or repo; typo; tag deleted |
| access denied, 401, 403 | private registry, missing/incorrect imagePullSecret or SA, expired token |
| `You have reached your pull rate limit` | Docker Hub limits (unauthenticated pulls are limited per IPv4 address or IPv6 /64, so NAT shares it) → mirror/proxy cache, authenticated pulls |
| no matching manifest for the node platform | image lacks the node's architecture (for example ARM nodes) |
| DNS lookup failure or i/o timeout | node DNS/egress/proxy to registry |
| `x509: certificate signed by unknown authority` | private registry CA not trusted by containerd (`certs.d/<host>/hosts.toml` `ca =`) |
Reproduce on the node by pulling the same image with the runtime's CLI — same error without Kubernetes in the way.
BackOff retries grow to 5 minutes; after fixing, `kubectl delete pod` to retry immediately.

## CreateContainerConfigError
Env var references a missing ConfigMap/Secret **key** (`couldn't find key X in Secret <ns>/<name>`), or
`runAsNonRoot: true` with an image that would run as root (the kubelet verifies this before starting the container).

## Verify
- [ ] Pod Running; for pulls, the image digest is the expected one (`.status.containerStatuses[].imageID`).

## Checked

Date: 2026-10-27. Documentation release: Kubernetes v1.37.1 (latest release; website main is the v1.38 development tree).

- Kubelet event reasons `FailedMount`, `FailedAttachVolume`, `FailedCreatePodSandBox`, and error names `ErrImagePull`,
  `ImagePullBackOff`, `CreateContainerConfigError`: kubelet `events/event.go`, `images/types.go`, `kuberuntime_container.go`
  v1.37.1.
- `couldn't find key %v in Secret %v/%v` message: kubelet `kubelet_pods.go` v1.37.1; kubelet verifies `runAsNonRoot` before
  start (`verifyRunAsNonRoot`).
- ImagePullBackOff delay grows to 300 seconds (5 minutes): container images page.
- Docker Hub text `You have reached your pull rate limit` and the unauthenticated limit scope (per IPv4 address or IPv6 /64,
  per 6 hours): Docker Hub pull-usage page.
- containerd `ca` setting in `hosts.toml` under `certs.d`: containerd `docs/hosts.md`.
- Removed: quoted registry and runtime error strings, the `plugin type="calico"` text, the `registry.k8s.io/pause` image
  name and the `crictl pull` command, which the checked sources do not document.

Method: documentation only; no commands were run.
