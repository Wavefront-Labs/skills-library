---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubelet-and-node-hardening
name: kubelet-and-node-hardening
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kubelet, anonymous-auth, read-only-port, webhook-authorization, node-authorizer, noderestriction, gvisor, kata-containers, runtimeclass, container-escape, sandboxing, hostpath, privileged-container]
level: advanced
status: docs-checked
description: "kubelet authn/authz flags that leave the node API open, the deprecated read-only port, and RuntimeClass sandboxing (gVisor/Kata) for the containers you don't fully trust."
sources: ["https://kubernetes.io/docs/reference/access-authn-authz/kubelet-authn-authz/", "https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet/", "https://kubernetes.io/docs/concepts/containers/runtime-class/", "https://kubernetes.io/docs/concepts/security/pod-security-standards/", "https://github.com/google/gvisor", "https://github.com/kata-containers/kata-containers"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kubelet and node hardening: the API attackers reach after a pod escape

**Goal:** close the kubelet's own API (separate from the cluster apiserver) to
anonymous and unauthorized callers, and know when standard runc-based container
isolation is not enough and a sandboxed runtime is worth the overhead. The
`NodeRestriction` admission controller that limits what a *legitimate* kubelet
credential can modify is in
`computing-software.cloud-infrastructure-engineering.kubernetes.built-in-admission-controllers-and-apiserver-flags`;
this skill is about the kubelet's own exposed surface and runtime-level
container isolation.

## 1. The kubelet runs its own HTTPS API, separate from the apiserver
Every node's kubelet serves an HTTPS API (`port` default 10250) that gives access to data and operations of varying
power on the node and inside containers. It has its own authentication and authorization, separate from apiserver RBAC.

Per the kubelet reference and authentication page, the **defaults are open**: `--anonymous-auth` defaults to `true`
(requests not rejected by another authenticator become user `system:anonymous`, group `system:unauthenticated`) and the
default authorization mode is `AlwaysAllow`, which allows every authenticated or anonymous request. These flags are
deprecated in favour of the config file:
```yaml
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
authentication:
  anonymous: {enabled: false}        # 401 for unauthenticated requests
  webhook: {enabled: true}           # bearer tokens (incl. service account tokens) checked via TokenReview
  x509: {clientCAFile: <path>}       # client certificate authentication (the apiserver's kubelet client cert)
authorization:
  mode: Webhook                      # SubjectAccessReview against the apiserver
readOnlyPort: 0                      # default 0 = disabled
```
Flag equivalents: `--anonymous-auth=false`, `--client-ca-file`, `--authentication-token-webhook` (with `--kubeconfig`),
`--authorization-mode=Webhook`. Webhook modes need the `authentication.k8s.io/v1` and `authorization.k8s.io/v1` API groups
enabled on the apiserver. Check what a node actually runs (configz, see `kubelet-configz-live-config`) rather than trusting
the image.

## 2. The read-only port
`readOnlyPort` is the kubelet's unauthenticated, no-authorization port. It is disabled by default (`0`); set it to `0`
explicitly in node configs and do not enable it.

## 3. `authorization.mode: Webhook` closes the "kubelet trusts everyone" gap
With `AlwaysAllow`, authentication alone (or anonymous access) is enough to use the whole kubelet API. With `Webhook`
the kubelet asks the apiserver whether the caller may perform the action, using request attributes like the apiserver:
verbs from the HTTP verb, resource `nodes`, and a subresource from the path (`stats`, `metrics`, `log`, `spec`,
`checkpoint`, and `proxy` for everything else). Warnings from the docs:
- `nodes/proxy` grants access to **all other kubelet APIs**, including ones that execute commands in any container on
  the node; because some endpoints use WebSockets over HTTP GET, even **get** on `nodes/proxy` authorizes command execution.
- Make sure the identity the apiserver uses (`--kubelet-client-certificate` and `--kubelet-client-key`) is authorized for
  the subresources it needs.
- Fine-grained kubelet authorization (feature gate `KubeletFineGrainedAuthz`, stable and on by default from 1.36) lets
  `/pods`, `/runningPods`, `/configz` and `/healthz` be authorized as `nodes/pods`, `nodes/configz` and `nodes/healthz`
  before falling back to `nodes/proxy`, so monitoring identities need not hold `nodes/proxy`.

## 4. RuntimeClass and sandboxed runtimes
Standard container isolation (runc, namespaces, cgroups, seccomp) shares the host kernel. For genuinely untrusted code,
a sandboxed runtime adds another layer. Select it per pod with a RuntimeClass, which names a configured runtime handler
(containerd handlers are defined under `plugins."io.containerd.grpc.v1.cri".containerd.runtimes.<handler>` in
`/etc/containerd/config.toml`; if `runtimeClassName` is unset the default handler is used, and a pod whose RuntimeClass or
handler is missing fails to start):
```yaml
apiVersion: v1
kind: Pod
spec:
  runtimeClassName: gvisor   # or kata; the name is whatever RuntimeClass you created
```
- **gVisor**: an application kernel written in Go that runs in userspace and implements much of the Linux system call
  surface; its OCI runtime is `runsc`. The project says it is not a syscall filter such as seccomp-bpf.
- **Kata Containers**: a standard implementation of lightweight virtual machines that plug into container tooling.
- Both need the runtime installed on the nodes and a matching RuntimeClass. Test the actual workload under the sandboxed
  runtime before relying on it; compatibility and performance are workload-specific.

## 5. `hostPath`, `hostNetwork`, `hostPID`, `privileged`: no sandbox saves you here
No kubelet hardening or RuntimeClass helps if a pod is granted direct host access. The Pod Security Standards **Baseline**
profile (included in Restricted) forbids host namespaces, privileged containers and hostPath volumes. Enforce it with
Pod Security Admission (see `k8s-rbac-and-security`); this skill's controls are a second line of defence, not a substitute.

## Verify
- [ ] Every node's effective kubelet config (configz) shows anonymous authentication disabled, authorization mode Webhook and
      `readOnlyPort` 0, checked on running nodes, not just the intended base image.
- [ ] Port 10250 is not reachable from outside the cluster's control-plane or trusted network.
- [ ] No human or workload identity holds `nodes/proxy` unless it needs it.
- [ ] Workloads running untrusted code use a RuntimeClass backed by gVisor or Kata, confirmed via
      `kubectl get pod -o jsonpath='{.spec.runtimeClassName}'`.
- [ ] A test unauthenticated request to a node's kubelet API from a position that should not have access is rejected.

## Checked

2026-10-26: kubernetes.io kubelet-authn-authz page, kubelet command-line reference, RuntimeClass page and Pod Security Standards page (v1.37 docs, kubernetes/website main 2026-10-25), the kubelet config API source, the KubeletFineGrainedAuthz gate page, and the gVisor and Kata Containers READMEs. Confirmed: anonymous-auth default true, AlwaysAllow default authorization, readOnlyPort default 0, auth flags and their config-file equivalents, subresource mapping and the nodes/proxy warning, fine-grained authorization stages, RuntimeClass handler behaviour, Baseline profile controls, gVisor runsc application kernel and Kata lightweight VMs. Corrected: the old text said anonymous-auth had changed to default false in recent versions and that client-ca-file is needed for Webhook authentication; the reference shows default true and client-ca-file belongs to certificate authentication. Removed unconfirmed incident claims, performance comparisons and managed-service hardening claims.

Method: documentation only; no commands were run.
