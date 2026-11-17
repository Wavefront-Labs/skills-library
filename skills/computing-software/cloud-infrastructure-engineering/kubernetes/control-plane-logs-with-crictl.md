---
id: computing-software.cloud-infrastructure-engineering.kubernetes.control-plane-logs-with-crictl
name: control-plane-logs-with-crictl
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, control-plane-troubleshooting, crictl-logs, crictl, kube-apiserver, static-pod]
level: practitioner
status: docs-checked
description: "Read kube-apiserver, etcd, scheduler and controller-manager logs with crictl and /var/log/pods when kubectl is unavailable because the API server is down."
sources: ["https://kubernetes.io/docs/tasks/debug/debug-cluster/crictl/", "https://kubernetes.io/docs/tasks/debug/debug-cluster/", "https://kubernetes.io/docs/concepts/cluster-administration/logging/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Control-plane logs when the API is down

`kubectl logs` needs the API server. When it is down, go to the node.

## crictl
```bash
sudo crictl ps -a --name kube-apiserver          # -a: include exited containers
sudo crictl logs --tail 50 <container-id>
sudo crictl logs --tail 50 $(sudo crictl ps -a --name etcd -q | head -1)
sudo crictl inspect <container-id> | jq '.status | {state, exitCode, reason, message}'
sudo crictl pods --name kube-apiserver            # sandbox state
```
crictl reads its endpoints from `--runtime-endpoint`/`--image-endpoint` or `/etc/crictl.yaml` (use `--config` for another file); without one it tries a list of known endpoints. For containerd the documented file is:
```yaml
runtime-endpoint: unix:///var/run/containerd/containerd.sock
image-endpoint: unix:///var/run/containerd/containerd.sock
```

## Log files
```bash
sudo ls /var/log/pods/ | grep kube-system_kube-apiserver
sudo tail -50 /var/log/pods/kube-system_kube-apiserver-*/kube-apiserver/*.log
```
By default the kubelet keeps one terminated container with its logs after a restart, so look at the
older log file in the container's directory when the container restarts before you can attach.

## Container never created
No container in `crictl ps -a`: the kubelet rejected the manifest.
```bash
sudo journalctl -u kubelet --since -10m | grep -iE 'manifest|static|apiserver' | tail
```
Typical: YAML syntax error, unknown field, a hostPath that does not exist.

## Typical apiserver log lines
| Line | Cause |
|---|---|
| connection refused dialing 127.0.0.1:2379 | etcd down |
| `open /etc/kubernetes/pki/...: no such file or directory` | bad flag path or missing volume mount |
| unknown flag | typo in manifest |
| x509 certificate expired | renew certs (see `expired-control-plane-certificates`) |

## Checked

Checked 2026-10-27 against Kubernetes documentation (kubernetes/website main tree, v1.38 development; latest release v1.37.1) and kubeadm/kubectl source: crictl task page (endpoint flags and /etc/crictl.yaml, crictl pods --name, ps -a, logs --tail), cri-tools source (ps --name, logs --tail), logging page (kubelet keeps one terminated container with its logs; logs under /var/log/pods). Removed the unconfirmed /var/log/containers symlink claim and quoted error strings.

Method: documentation only; no commands were run.
