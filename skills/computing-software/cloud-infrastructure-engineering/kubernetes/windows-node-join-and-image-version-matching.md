---
id: computing-software.cloud-infrastructure-engineering.kubernetes.windows-node-join-and-image-version-matching
name: windows-node-join-and-image-version-matching
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, windows-nodes, windows-node-join, windows-containerd, windows-image-compat, os-version-match, runtimeclass, process-isolation]
level: advanced
status: docs-checked
description: "Join Windows Server worker nodes to a kubeadm cluster and keep container image OS builds matched to host builds with node labels, taints and RuntimeClass."
sources: ["https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/adding-windows-nodes/", "https://kubernetes.io/docs/concepts/windows/user-guide/#ensuring-os-specific-workloads-land-on-the-appropriate-container-host", "https://learn.microsoft.com/en-us/virtualization/windowscontainers/deploy-containers/version-compatibility"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows node join and image OS version matching

## Joining a node to a kubeadm cluster
Prerequisites: a Windows Server 2022 (or higher) machine with administrative access, and a cluster created by `kubeadm init` (control plane stays Linux). Use PowerShell as Administrator and the scripts from `kubernetes-sigs/sig-windows-tools`.
```powershell
curl.exe -LO https://raw.githubusercontent.com/kubernetes-sigs/sig-windows-tools/master/hostprocess/Install-Containerd.ps1
.\Install-Containerd.ps1 -ContainerDVersion <containerd-version-without-v-prefix>
curl.exe -LO https://raw.githubusercontent.com/kubernetes-sigs/sig-windows-tools/master/hostprocess/PrepareNode.ps1
.\PrepareNode.ps1 -KubernetesVersion v<current-patch-version>
kubeadm join --token <token> <control-plane-host>:<control-plane-port> --discovery-token-ca-cert-hash sha256:<hash>
```
- `Install-Containerd.ps1` takes the version without a `v` prefix (for example `1.7.22`), plus optional parameters such as `netAdapterName`, `skipHypervisorSupportCheck` and `CNIBinPath`/`CNIConfigPath` (if you change the CNI paths, configure the Windows CNI plugin with matching values).
- Tokens expire after 24 hours by default; `kubeadm token create` on a control plane node makes a new one.
- CNI setup on mixed clusters needs more than one `kubectl apply`; the docs link Calico's Windows instructions.

## Keep Linux and Windows workloads apart
Every node has `kubernetes.io/os` and `kubernetes.io/arch`. The best practice is a `nodeSelector` of `kubernetes.io/os: windows`. For clusters full of existing Linux manifests, register Windows nodes with a taint (for example `--register-with-taints='os=windows:NoSchedule'`) and give Windows Pods a matching toleration plus the nodeSelector. `.spec.os.name` should also be set but the scheduler ignores it.

## Image and host OS version matching
The Windows Server version of the container base image must match the node. Kubernetes labels nodes `node.kubernetes.io/windows-build` (major.minor.build): Windows Server 2022 is `10.0.20348`, Windows Server 2025 is `10.0.26100`. Mismatch produces an error like `The operating system of the container does not match the operating system of the host`. Kubernetes supports process isolation only (not Hyper-V isolation) and Windows Server 2022 and 2025 nodes. Microsoft's compatibility page covers when images and hosts must match.
```yaml
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata: {name: windows-2022}
handler: <your-runtime-handler>
scheduling:
  nodeSelector:
    kubernetes.io/os: windows
    kubernetes.io/arch: amd64
    node.kubernetes.io/windows-build: "10.0.20348"
  tolerations:
  - {key: os, operator: Equal, value: windows, effect: NoSchedule}
```
Pods then set `runtimeClassName: windows-2022`. The handler name depends on how the runtime is configured; use the one your containerd installation defines.

## Verify
```bash
kubectl get nodes -L kubernetes.io/os,node.kubernetes.io/windows-build
kubectl get pods -o wide
```
- [ ] Windows nodes are Ready and a test Windows Pod is Running on a node whose windows-build label matches the image.

## Checked

Checked 2026-10-26 against Kubernetes website docs (main branch, latest commit 2026-10-25, covering Kubernetes 1.36) and Microsoft version-compatibility page (source repo, 2026-10-20). Confirmed: supported Windows Server versions (2022 and 2025), join scripts and parameters, windows-build label values, process isolation only, mismatch error wording.

Method: documentation only; no commands were run.
