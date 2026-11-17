---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.container-runtime-security
name: container-runtime-security
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, infrastructure-protection, runtime-security, falco, kubernetes-security, pod-security-standards, ebpf]
level: practitioner
status: draft
description: "Secure containers and Kubernetes at runtime: Pod Security Standards, seccomp and read-only roots, eBPF runtime detection (Falco, GuardDuty, Defender), response playbooks."
sources: ["https://kubernetes.io/docs/concepts/security/pod-security-standards/", "https://falco.org/docs/", "https://docs.aws.amazon.com/guardduty/latest/ug/runtime-monitoring.html", "https://learn.microsoft.com/azure/defender-for-cloud/defender-for-containers-introduction"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Container and Kubernetes runtime security

## Steps
1. **Prevent at admission**: enforce Pod Security Standards `restricted` via Pod Security
   Admission labels (`pod-security.kubernetes.io/enforce: restricted`) on workload namespaces;
   add Kyverno/Gatekeeper for registry allow-lists and signed images.
2. **Harden pods**: non-root, `readOnlyRootFilesystem: true`, drop all capabilities,
   `seccompProfile: RuntimeDefault`, no hostPath/hostNetwork, no automounted service account
   tokens unless needed.
3. **Runtime detection**: eBPF sensors watching syscalls and process/network events: Falco
   (rules for shell in container, writes below /etc, unexpected outbound), or managed (GuardDuty
   Runtime Monitoring for EKS/ECS/EC2, Defender for Containers, GKE Threat Detection in SCC).
4. **Network**: default-deny NetworkPolicies per namespace; egress restricted.
5. **Response playbook**: isolate pod (label to a quarantine NetworkPolicy), capture forensic
   data (container filesystem diff, memory if possible), cordon node, rotate exposed
   credentials, redeploy from a clean image.
6. **Tune**: baseline noisy rules per workload; route high-severity to SIEM/on-call.

## Gotchas
- Privileged DaemonSets (agents, CNI) are exempt by necessity; inventory and watch them.
- Killing the pod destroys evidence; isolate first.

## Verify
- [ ] Restricted PSS enforced on workload namespaces.
- [ ] Simulated attack (shell in container) raises an alert end-to-end.
