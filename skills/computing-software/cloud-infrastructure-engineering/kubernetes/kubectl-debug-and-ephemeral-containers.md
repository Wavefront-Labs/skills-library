---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubectl-debug-and-ephemeral-containers
name: kubectl-debug-and-ephemeral-containers
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kubectl-debug, ephemeral-containers, distroless, process-namespace-sharing, node-debug, troubleshooting, ctr, crictl, shareprocessnamespace, copy-to, debug-copy]
level: advanced
status: docs-checked
description: "Using kubectl debug and ephemeral containers to get a shell into a running, distroless, or dying pod and the host node without redeploying anything."
sources: ["https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/", "https://kubernetes.io/docs/concepts/workloads/pods/ephemeral-containers/", "https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/kubectl/pkg/cmd/debug/debug.go"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# kubectl debug and ephemeral containers: a shell without redeploying

**Goal:** get eyes inside a running, crashing, or distroless pod, or onto the host node,
using `kubectl debug`'s three distinct modes, and know which one applies to which situation.

## 1. Why this exists
Production images are increasingly distroless or scratch-based (no shell, no `cat`, no
`curl`), so `kubectl exec` has nothing to run. **Ephemeral containers** (stable since
Kubernetes 1.25) let you add a *new* container with its own image to an *already running* Pod
through a special `ephemeralcontainers` API handler, without restarting existing containers.
They lack guarantees for resources or execution and are never restarted automatically.

## 2. The three modes
```bash
# Mode 1: attach an ephemeral debug container, targeting the container's process namespace
kubectl debug -it <POD> --image=busybox:1.28 --target=<CONTAINER>

# Mode 2: copy the pod, adding a debug container or replacing a container's image/command
kubectl debug <POD> -it --copy-to=<POD>-dbg --container=<CONTAINER> -- sh
kubectl debug <POD> -it --copy-to=<POD>-dbg --image=busybox:1.28 --share-processes
# the original pod is untouched; add --same-node to schedule the copy on the same node

# Mode 3: debug the node itself
kubectl debug node/<NODE> -it --image=ubuntu
# creates a pod on that node; the node root filesystem is mounted at /host
```

## 3. Choosing the right mode
- **Target still running, just needs inspection**: Mode 1. `--target` asks the runtime to put the
  debug container in the target container's process namespace, so `ps` should list the app.
- **Target crashes before you can attach, or the entrypoint itself is the problem**: Mode 2,
  overriding the command (`-- sh`) or swapping images with `--set-image=name=image`.
  `--target` cannot be combined with `--copy-to`; use `--share-processes` instead.
- **Suspect node-level issue** (disk, CNI, kernel or cgroup state, or you need `crictl` or `ctr`):
  Mode 3. The pod shares the host IPC, network and PID namespaces but is not privileged, so
  reading some process information and `chroot /host` may fail. For a privileged session use
  `--profile=sysadmin` (or create the pod yourself).

## 4. Profiles and customisation
`--profile` takes `general`, `baseline`, `restricted`, `netadmin`, `sysadmin` (the website page
also lists `legacy`). `baseline` and `restricted` are compatible with those Pod Security
Standards. `--custom=<file>` merges a partial container spec (JSON or YAML) over a profile;
it cannot change `name`, `command`, `image`, `lifecycle` or `volumeDevices`. In the kubectl
source the flag default is `general`; `legacy` prints a deprecation warning and is planned for
removal in v1.39. The website page still says `legacy` is the default, so pass `--profile`
explicitly. If the target pod runs as non-root, kubectl warns that some profile capabilities
may not work; use `--custom` with `securityContext.runAsUser: 0`.

## 5. Gotchas
- `--target` depends on runtime support. If unsupported, the ephemeral container may not start or may
  start with an isolated process namespace where `ps` shows no other containers. Verify with `ps`.
- Ephemeral containers cannot be changed or removed after they are added, and they are not
  supported on static pods. They cannot have ports or probes, and `resources` is disallowed.
  You cannot add one with `kubectl edit`.
- The node-debug pod is not deleted for you. Clean up with
  `kubectl delete pod node-debugger-<node>-<suffix>`.
- A `kubectl debug` on a running pod patches the `ephemeralcontainers` subresource and, with
  `-it`, attaches like `kubectl attach` (the `--attach` flag defaults to true with `-i`). Grant
  RBAC for `pods/ephemeralcontainers` and `pods/attach` to a break-glass role, and treat node
  debugging and the `sysadmin` profile as highly privileged access.
- Mirror a known-good debug image into restricted or air-gapped registries beforehand.
- Use a `kubectl` client recent enough to know `--profile`, `--custom` and `--share-processes`;
  old pinned clients give "unknown flag" errors.

## Verify
- [ ] `kubectl debug -it <pod> --image=busybox:1.28 --target=<container>` reaches a shell and `ps` shows the target app's process.
- [ ] A `--copy-to` debug pod with overridden command starts even when the original container crash-loops.
- [ ] `kubectl debug node/<node> -it --image=ubuntu` reaches `/host`.
- [ ] RBAC for `pods/ephemeralcontainers`, `pods/attach`, and node debug is limited to an on-call role.

## Checked
Date: 2026-10-27. Documentation: Kubernetes website "Debug Running Pods" and "Ephemeral
Containers" (current docs; latest release v1.37.1) plus the kubectl `debug.go` source on main.
Confirmed: ephemeral containers stable v1.25 and their disallowed fields; `--target` runtime
note; node debug pod namespaces, `/host` mount and non-privileged default; profile list,
`--custom` restrictions (stable v1.32); flags `--copy-to`, `--same-node`, `--share-processes`,
`--set-image`; `--target` incompatible with `--copy-to`. Removed unconfirmed claims (exec error
text, PVC sharing on copies, lifecycle hooks, default limits, network namespace remark).
Method: documentation only; no commands were run.
