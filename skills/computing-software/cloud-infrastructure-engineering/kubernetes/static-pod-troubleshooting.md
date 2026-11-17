---
id: computing-software.cloud-infrastructure-engineering.kubernetes.static-pod-troubleshooting
name: static-pod-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, static-pods, static-pod-troubleshooting, kubelet-journal, crictl, control-plane, cka]
level: practitioner
status: docs-checked
description: "Diagnose a static pod that will not start or vanished: kubelet journal, manifest YAML errors, staticPodPath, crictl logs of the dead container, and mirror pod mismatches."
sources: ["https://kubernetes.io/docs/tasks/configure-pod-container/static-pod/", "https://kubernetes.io/docs/concepts/workloads/pods/static-pods/", "https://kubernetes.io/docs/tasks/debug/debug-cluster/crictl/", "https://kubernetes.io/docs/reference/using-api/health-checks/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Static pod troubleshooting

Static pods are run by the kubelet from files; the API only shows a read-only **mirror pod**.
If the kubelet cannot parse the file, nothing appears in `kubectl` at all.

## Sequence
```bash
# 1. Is the kubelet looking where you think?
grep staticPodPath /var/lib/kubelet/config.yaml        # usually /etc/kubernetes/manifests
ls -la /etc/kubernetes/manifests/

# 2. Did the kubelet reject the manifest?
journalctl -u kubelet --since "10 min ago" | grep -iE "static|manifest|error"

# 3. Did the container start and die? (API may be down, so use the runtime)
crictl ps -a --name kube-apiserver
crictl logs <container-id>          # works on exited containers listed by ps -a
crictl inspect <container-id>       # exit code and reason are in the status section

# 4. Mirror pod status (if API is up)
kubectl -n kube-system get pod kube-apiserver-<node> -o wide
kubectl -n kube-system describe pod kube-apiserver-<node>
```

## Usual causes
| Symptom | Cause |
|---|---|
| No container ever created, journal shows YAML error | indentation/tab, `---` multi-doc, wrong apiVersion |
| Container exits immediately, log: "unknown flag" | typo or flag removed in this version |
| Log: "open /etc/kubernetes/pki/x.crt: no such file" | hostPath volume/mount missing or path typo |
| Liveness probe kills it repeatedly | probe port/host changed (e.g. `--secure-port`) but probe not |
| Edit made, nothing changes | edited a backup copy elsewhere, or file saved with an editor swap file in manifests dir |
| Two apiservers fighting | a `.bak`/`.yaml.old` left **inside** the manifests dir: the kubelet reads every file that does not start with a dot |

Keep backups **outside** `/etc/kubernetes/manifests` (the docs suggest a directory such as
`/etc/kubernetes/backup/`). When two files define a pod with the same name the result is
undefined; the outdated spec can silently take effect.

## Forcing a restart
Static pods cannot be deleted via the API (the mirror is recreated). Move the file out, wait
for `crictl ps` to show it gone, move it back. `kubectl delete pod` only recreates the mirror.

## Gotchas
- Static pods cannot reference ConfigMaps/Secrets/ServiceAccounts; use hostPath.
- The mirror pod name has the node name suffix; the kubelet needs permission to create the
  mirror pod in the API server.

## Verify
- [ ] `crictl ps --name <component>` shows Running with a stable restart count.
- [ ] `kubectl get --raw '/readyz?verbose'` all `ok` after apiserver changes.

## Checked

Checked 2026-10-26 against Kubernetes documentation v1.37 (kubernetes/website commit 2026-10-25) and kubernetes/kubernetes master (kubelet source, 2026-10-24). Confirmed: `staticPodPath`, that every non-dot file in the directory is read (no extension filtering) and duplicate-name behaviour is undefined, the documented backup location outside the directory, `crictl ps`/`logs` usage, mirror pod behaviour, the 20s scan interval. Removed as unconfirmed: the quoted kubelet log message, the `jq` pipeline, and the NodeRestriction mirror-pod wording.

Method: documentation only; no commands were run.
