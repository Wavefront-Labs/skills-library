---
id: computing-software.cloud-infrastructure-engineering.kubernetes.windows-node-troubleshooting
name: windows-node-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, windows-nodes, windows-node-troubleshooting, hostprocess, node-log-query, containerd]
level: practitioner
status: docs-checked
description: "Troubleshoot Windows worker nodes: get a shell with HostProcess pods, read kubelet and containerd logs, and fix OS version mismatches, pause image and HNS issues."
sources: ["https://kubernetes.io/docs/tasks/debug/debug-cluster/windows/", "https://kubernetes.io/docs/tasks/configure-pod-container/create-hostprocess-pod/", "https://kubernetes.io/docs/concepts/cluster-administration/system-logs/#log-query"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows node troubleshooting

## Get onto the node
Use a HostProcess pod (stable since 1.26). Requirements from the docs: containerd 1.6 or higher (1.7 recommended), `hostProcess: true`, `hostNetwork: true`, `runAsUserName` set to `NT AUTHORITY\SYSTEM`, `NT AUTHORITY\Local service`, `NT AUTHORITY\NetworkService` or a local usergroup name (local usergroups need containerd 1.7+), and `runAsNonRoot` not true.
```yaml
apiVersion: v1
kind: Pod
metadata: {name: win-shell, namespace: kube-system}
spec:
  nodeSelector: {kubernetes.io/os: windows, kubernetes.io/hostname: <node>}
  hostNetwork: true
  securityContext:
    windowsOptions: {hostProcess: true, runAsUserName: "NT AUTHORITY\\SYSTEM"}
  containers:
  - name: shell
    image: <windows-image-matching-the-node-build>
    command: ["powershell.exe", "-Command", "Start-Sleep 2147483"]
```
`kubectl exec -it win-shell -n kube-system -- powershell`. The container has full access to the host, so delete it when done. In containerd 1.7+ volumes are reachable at their `mountPath`; in 1.6 use paths relative to `$CONTAINER_SANDBOX_MOUNT_POINT`.

## Logs
The node log query feature works on Windows and Linux nodes. It needs the kubelet option `enableSystemLogHandler` (default false); `NodeLogQuery` is stable and locked on from 1.36 (beta and off by default in 1.30 to 1.35, which also needed `enableSystemLogQuery`). On Windows it assumes service logs are in the application log provider. Granting `nodes/proxy` access is powerful (it can reach kubelet APIs that run commands in containers).
```bash
kubectl get --raw "/api/v1/nodes/<node>/proxy/logs/?query=kubelet"
```

## Frequent failures (Kubernetes Windows debugging tips)
| Symptom | Cause and fix |
|---|---|
| Pods stuck in ContainerCreating or restarting | Pause image incompatible with the Windows version; with containerd set it in the `sandbox_image` setting of config.toml (see the Windows intro page for the recommended image) |
| `ErrImagePull` / `ImagePullBackOff` | Pod scheduled to an incompatible Windows node; use the nodeSelector or RuntimeClass for the right `node.kubernetes.io/windows-build` |
| Error `The operating system of the container does not match the operating system of the host` | Image base OS version differs from the node build; use a matching image tag (Microsoft version compatibility page) |
| No pod connectivity on VMs | Enable MAC spoofing on the VM network adapters |
| Pods cannot ping external hosts | Windows Pods have no outbound ICMP rules; use `curl` |
| Node cannot reach NodePort or Service IPs of local Pods | Known Windows networking limitation |
| Install fails behind a proxy | Set `HTTP_PROXY` and `HTTPS_PROXY` as machine environment variables |
| Linux Pods land on Windows nodes | Taint Windows nodes (`os=windows:NoSchedule`) and select the OS |

## Verify
`kubectl get node <node> -o wide` shows Ready and the expected OS image; a test Windows Pod starts and serves traffic.

## Checked

Checked 2026-10-26 against Kubernetes website docs (main branch, latest commit 2026-10-25, covering Kubernetes 1.36). Confirmed: HostProcess pod requirements, node log query gate and kubelet options, debugging-tips table.

Method: documentation only; no commands were run.
