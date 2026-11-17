---
id: computing-software.cybersecurity-defensive.cloud-security.gvisor-kata-sandboxing
name: gvisor-kata-sandboxing
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [gvisor, kata-containers, sandboxed-runtimes, runtimeclass, container-isolation, multi-tenant-kubernetes, cloud-workload-protection]
level: advanced
status: draft
description: "Isolate untrusted workloads with sandboxed runtimes: gVisor (runsc) and Kata Containers, RuntimeClass scheduling, GKE Sandbox, performance trade-offs and compatibility."
sources: ["https://gvisor.dev/docs/", "https://katacontainers.io/docs/", "https://kubernetes.io/docs/concepts/containers/runtime-class/", "https://cloud.google.com/kubernetes-engine/docs/concepts/sandbox-pods"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sandboxed runtimes with gVisor or Kata

Standard containers share the host kernel: one kernel exploit escapes to the node. Sandboxed runtimes
add a boundary for untrusted code (customer workloads, CI jobs, code execution features, AI agents).

## Options
| Runtime | Isolation | Trade-offs |
|---|---|---|
| gVisor (`runsc`) | User-space application kernel (Sentry) intercepts syscalls; host kernel exposure greatly reduced | Syscall-heavy and I/O workloads slower; some syscalls/features unsupported |
| Kata Containers | Each pod in a lightweight VM (QEMU/Cloud Hypervisor/Firecracker) with its own kernel | Needs nested virtualisation or bare metal; more memory per pod |

## Kubernetes RuntimeClass
```yaml
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata: {name: gvisor}
handler: runsc
scheduling: {nodeSelector: {sandbox: gvisor}}
---
spec:
  runtimeClassName: gvisor     # in the untrusted pod spec
```
Install runsc as a containerd shim on dedicated nodes (`containerd` config `runtimes.runsc` with `runtime_type = "io.containerd.runsc.v1"`).

## Managed
- **GKE Sandbox** (gVisor): node pool with `--sandbox type=gvisor`; pods select `runtimeClassName: gvisor`.
- AWS Fargate uses Firecracker micro-VMs per pod (isolation by design).
- AKS: Pod Sandboxing (Kata-based) node pools.

## Policy
Admission policy forcing `runtimeClassName: gvisor` in untrusted namespaces (Kyverno/Gatekeeper), and
taints so trusted workloads do not land on sandbox nodes (and vice versa).

## Gotchas
- Not a substitute for least privilege: privileged sandboxed pods still get broad access inside the sandbox; keep Pod Security Standards restricted.
- Monitoring/EDR agents may not see inside gVisor sandboxes; check vendor support.

## Verify
- [ ] Inside a sandboxed pod `dmesg` shows gVisor (or `uname` shows the Kata guest kernel).
- [ ] Untrusted namespace pods cannot be created without the runtime class.
