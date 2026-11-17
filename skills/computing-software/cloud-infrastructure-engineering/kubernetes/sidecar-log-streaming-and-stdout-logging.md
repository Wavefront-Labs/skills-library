---
id: computing-software.cloud-infrastructure-engineering.kubernetes.sidecar-log-streaming-and-stdout-logging
name: sidecar-log-streaming-and-stdout-logging
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, logging-sidecar, stdout-logging, logging, native-sidecar, log-rotation, ckad]
level: practitioner
status: docs-checked
description: "Get logs from apps that write to files into the node log pipeline: symlink to stdout, streaming sidecars per file, agent sidecars, and the rotation and disk traps of each."
sources: ["https://kubernetes.io/docs/concepts/cluster-administration/logging/", "https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/", "https://kubernetes.io/docs/reference/config-api/kubelet-config.v1beta1/", "https://github.com/nginx/docker-nginx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sidecar log streaming and logging to stdout

Cluster logging (Fluent Bit, Vector, OTel DaemonSets) reads
`/var/log/pods/<ns>_<pod>_<uid>/<container>/*.log`, i.e. whatever containers write to
**stdout/stderr**. Kubelet rotates those (`containerLogMaxSize` default 10Mi,
`containerLogMaxFiles` 5). Files written inside the container are invisible and unrotated.

## Option 1: make the app log to stdout (best)
- A config setting that sends logs to stdout/stderr (the Kubernetes docs recommend
  `/dev/stdout` as the destination for an app that writes a single file).
- Symlink in the image, as the official nginx image does for `/var/log/nginx/access.log` and
  `error.log`:
```dockerfile
RUN ln -sf /dev/stdout /var/log/app/access.log && ln -sf /dev/stderr /var/log/app/error.log
```
  Breaks if the app rotates/renames its files or checks they are regular files.

## Option 2: streaming sidecar per file
```yaml
initContainers:                      # native sidecar (on by default since 1.29): starts before, stops after the app
- name: access-log
  image: busybox:1.36
  restartPolicy: Always
  args: [/bin/sh, -c, 'tail -n+1 -F /var/log/app/access.log']
  volumeMounts: [{name: logs, mountPath: /var/log/app}]
- name: audit-log
  image: busybox:1.36
  restartPolicy: Always
  args: [/bin/sh, -c, 'tail -n+1 -F /var/log/app/audit.log']
  volumeMounts: [{name: logs, mountPath: /var/log/app}]
containers:
- name: app
  volumeMounts: [{name: logs, mountPath: /var/log/app}]
volumes:
- name: logs
  emptyDir: {sizeLimit: 500Mi}
```
One sidecar per stream keeps formats separate (`kubectl logs pod -c audit-log`), as in the
Kubernetes logging docs' streaming sidecar example. `tail -F` follows renames. Costs: the docs
warn this can double the storage needed on the node, and **the app must still
rotate its files** or the emptyDir fills and the pod is evicted (`sizeLimit` makes that
explicit instead of filling the node).

## Option 3: agent sidecar
A Fluent Bit sidecar reading the files and shipping directly to the backend. Use only when
logs must bypass the node pipeline (different tenant destination, compliance). The docs warn
of significant resource consumption, and `kubectl logs` cannot show these logs because the
kubelet does not handle them.

## Native vs regular sidecars
Before native sidecars, sidecars were plain containers: Jobs never completed because the
sidecar kept running, and shutdown ordering could lose final log lines. Native sidecars
(`initContainers` with `restartPolicy: Always`) do not block Job completion, and on Pod
termination the kubelet stops them only after the main containers have stopped.

## Verify
```bash
kubectl logs deploy/app -c access-log --tail=5
kubectl exec deploy/app -c app -- du -sh /var/log/app     # bounded over time
# in the backend: query by container name, confirm no gaps across a rotation
```

## Checked
2026-10-27 against the Kubernetes logging architecture, sidecar containers and kubelet
configuration pages (kubernetes/website main, v1.38 development tree; v1.37 is the latest
release) and the nginx/docker-nginx Dockerfile. Confirmed: `/var/log/pods`, the
`containerLogMaxSize` 10Mi and `containerLogMaxFiles` 5 defaults, the SidecarContainers feature on
by default since v1.29, Job completion and termination ordering with native sidecars, the
streaming sidecar pattern and its storage cost, the logging-agent sidecar caveats, and nginx's
stdout/stderr symlinks. Removed app-specific flag examples that were not checked.
Method: documentation only; no commands were run.
