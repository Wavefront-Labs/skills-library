---
id: computing-software.cloud-infrastructure-engineering.kubernetes.windows-nodes-and-containers
name: windows-nodes-and-containers
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, windows, windows-nodes, windows-containers, mixed-cluster, node-selector, taints, containerd, hostprocess, gmsa, runtimeclass, calico-windows, kube-proxy-windows, windows-server-2022, hyperv-isolation, windows-node-selector, runasusername]
level: advanced
status: docs-checked
description: "Run Windows worker nodes in a mixed cluster: OS taints and nodeSelectors, OS-version matching, HostProcess pods, gMSA, and Pod features that differ on Windows."
sources: ["https://kubernetes.io/docs/concepts/windows/intro/", "https://kubernetes.io/docs/concepts/windows/user-guide/", "https://kubernetes.io/docs/tasks/configure-pod-container/create-hostprocess-pod/", "https://kubernetes.io/docs/tasks/configure-pod-container/configure-gmsa/", "https://github.com/kubernetes-sigs/sig-windows-tools", "https://learn.microsoft.com/en-us/virtualization/windowscontainers/deploy-containers/version-compatibility"]
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# Windows nodes and containers

**Goal:** add Windows Server worker nodes to a Linux control plane cluster, keep Linux and Windows workloads apart, and know which Pod features exist on Windows.

## 1. What is supported (Kubernetes Windows intro)
- The control plane runs on Linux only; Windows nodes are workers. Supported Windows Server releases: 2022 and 2025 (the version-skew policy also applies).
- Windows containers here means process isolation; Kubernetes does not support Hyper-V isolation. The container base image OS version must match the host (node label `node.kubernetes.io/windows-build`: `10.0.20348` for Server 2022, `10.0.26100` for Server 2025).
- Runtimes: containerd 1.4.0+ (stable since 1.20) and Mirantis Container Runtime. Self-managed nodes join with `kubeadm join` after the `sig-windows-tools` scripts install containerd and the node components. Managed offerings (EKS, AKS, GKE) have their own Windows node pool settings; use their current docs.
- Not supported: HugePages, privileged containers (use HostProcess), host networking for normal Pods (the 1.26 to 1.32 alpha `WindowsHostNetwork` gate no longer exists), Pods mixing Windows and Linux containers.

## 2. Keep workloads on the right OS
Set `.spec.os.name: windows` (or `linux`) and use a nodeSelector `kubernetes.io/os: windows`; the scheduler ignores `.spec.os.name`. For many existing Linux manifests, taint Windows nodes (`--register-with-taints='os=windows:NoSchedule'`) and add the matching toleration to Windows Pods. A RuntimeClass can bundle the nodeSelector (OS, arch, windows-build) and toleration so Pods only set `runtimeClassName`.
```yaml
spec:
  os: {name: windows}
  nodeSelector:
    kubernetes.io/os: windows
    node.kubernetes.io/windows-build: "10.0.20348"
  tolerations:
  - {key: os, operator: Equal, value: windows, effect: NoSchedule}
```

## 3. Pod spec differences
Supported: Pod status, readiness/liveness/startup probes, postStart and preStop hooks, ConfigMaps and Secrets (env or volume), `emptyDir` (not `medium: Memory`), named pipe host mounts, resource limits, `kubectl exec`, HPA, resource quotas, scheduler preemption.

With `.spec.os.name: windows` the API server rejects Pods that set: `hostPID`, `hostIPC`, `shareProcessNamespace`, `securityContext.seLinuxOptions`, `seccompProfile`, `fsGroup`, `fsGroupChangePolicy`, `sysctls`, `runAsUser`, `runAsGroup`, `supplementalGroups`, and per container `capabilities`, `readOnlyRootFilesystem`, `privileged`, `allowPrivilegeEscalation`, `procMount`, `runAsUser`, `runAsGroup`. Use `windowsOptions.runAsUserName` instead of `runAsUser`; `runAsNonRoot` blocks running as `ContainerAdministrator`.
- `requests.cpu` and `requests.memory` are subtracted from node allocatable but cannot guarantee resources on an overprovisioned node; the kubelet does no memory or CPU restriction on Windows and does not take OOM eviction actions. `--kube-reserved` and `--system-reserved` only subtract from NodeAllocatable. The `PIDPressure` condition is not implemented.
- Termination: the entrypoint process gets `CTRL_SHUTDOWN_EVENT`, Windows waits 5 seconds by default (a registry setting inside the container), then shuts processes down; `terminationGracePeriodSeconds` needs containerd.
- `volumeDevices` and `mountPropagation` are not supported; `dnsPolicy: ClusterFirstWithHostNet` is not supported.
- Paths in commands may need `\`. Windows container images range from 300 MB to over 10 GB; the container `C:` drive reports 20 GB virtual size by default.

## 4. HostProcess pods (node agents)
Stable since 1.26. They run as host processes for CNI installers, monitoring agents and CSI node plugins.
```yaml
spec:
  securityContext:
    windowsOptions:
      hostProcess: true
      runAsUserName: "NT AUTHORITY\\Local service"
  hostNetwork: true
  nodeSelector: {kubernetes.io/os: windows}
```
Requirements: containerd 1.6+ (1.7 recommended), `hostNetwork: true`, an allowed `runAsUserName` (`NT AUTHORITY\SYSTEM`, `NT AUTHORITY\Local service`, `NT AUTHORITY\NetworkService`, or a local usergroup on containerd 1.7+), `runAsNonRoot` not true. containerd itself must run as LocalSystem or LocalService. `$CONTAINER_SANDBOX_MOUNT_POINT` gives the host path of the container volume.

## 5. Identity: gMSA
Windows workloads that need Active Directory use a Group Managed Service Account instead of a secret: configure the gMSA credential spec per the Kubernetes gMSA task and reference it with `securityContext.windowsOptions.gmsaCredentialSpecName`. There is a known limitation with gMSA and containerd for access to Windows network shares (requires a kernel patch); read the gMSA limitations section.

## 6. Networking and storage limits
- See `windows-container-networking-hns` for CNI modes and Service settings. Notable limits: no host networking, no local NodePort access from the node itself, at most 64 backends per Service, no outbound ICMP to remote networks.
- Storage: no subPath, no NFS, no raw block, no volume expansion on mounted volumes, no uid/gid permissions. SMB (via CSI) and Azure Files are the shared options (see `windows-node-storage-smb-csi`).

## 7. Operations
- Kubelet and the Node Problem Detector have preliminary Windows support; the Windows Operational Readiness test suite validates mixed clusters.
- LogMonitor (Microsoft) is the documented way to pipe ETW, event log and file logs to STDOUT for `kubectl logs`.
- Kubernetes also documents Cluster API as a way to automate Windows node deployment.

## Verify
- [ ] `kubectl get nodes -L kubernetes.io/os,node.kubernetes.io/windows-build` shows the Windows pool.
- [ ] No Linux DaemonSet Pods are scheduled on Windows nodes (`kubectl get pods -A -o wide --field-selector spec.nodeName=<win-node>`).
- [ ] A test Pod with `os.name: windows` reaches Running.

## Checked

Checked 2026-10-26 against Kubernetes website docs (main branch, latest commit 2026-10-25, covering Kubernetes 1.36). Confirmed: supported Windows versions, no Hyper-V isolation, forbidden Pod fields with os.name windows, kubelet differences, termination behaviour, HostProcess requirements, gMSA limitation.

Method: documentation only; no commands were run.
