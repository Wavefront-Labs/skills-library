---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-getting-started-files
name: tetragon-getting-started-files
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [demo-file-events, tetragon, file-monitoring, tracingpolicy]
level: intro
status: docs-checked
description: "Apply the Tetragon quickstart file_monitoring policy and watch read and write events on sensitive files in Kubernetes or Docker."
sources:
  - "https://tetragon.io/docs/getting-started/file-events/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Monitor file events with Tetragon

Goal: extend execution monitoring with a tracing policy that reports sensitive file access. Policies filter in kernel, so only interesting events reach userspace and overhead stays low.

## Apply the policy

Kubernetes (the policy uses a CRD installed by Tetragon):

```shell
kubectl apply -f https://raw.githubusercontent.com/cilium/tetragon/main/examples/quickstart/file_monitoring.yaml
```

Docker loads the same YAML from disk at launch:

```shell
wget https://raw.githubusercontent.com/cilium/tetragon/main/examples/quickstart/file_monitoring.yaml
docker stop tetragon
docker run -d --name tetragon --rm --pull always \
  --pid=host --cgroupns=host --privileged \
  -v ${PWD}/file_monitoring.yaml:/etc/tetragon/tetragon.tp.d/file_monitoring.yaml \
  -v /sys/kernel/btf/vmlinux:/var/lib/tetragon/btf \
  quay.io/cilium/tetragon:<latest-version>
```

## What the policy hooks

`TracingPolicy` `file-monitoring-filtered` with three kprobes, all `syscall: false`, `return: true`:

- `security_file_permission` (args `file`, `int`): `Prefix` match on `/boot`, `/root/.ssh`, `/etc/shadow`, `/etc/profile`, `/etc/sudoers` and shell configs with arg 1 `Equal` `4` (MAY_READ); `Postfix` match on `.bashrc`, `.profile`, `.history` etc. with `4`; `Prefix` match on `/etc`, `/bin`, `/usr/bin`, `/var/log`, `/root/.ssh` etc. with `2` (MAY_WRITE).
- `security_mmap_file` (args `file`, `uint32`, `uint32`): same paths, with `Equal` or `Mask` on the prot flags (arg 1) and `Mask` on the map flags (arg 2).
- `security_path_truncate` (arg `path`): truncation under `/etc`, `/boot`, `/usr/bin`, `/var/log` etc.

## Observe

```shell
kubectl exec -ti -n kube-system ds/tetragon -c tetragon -- tetra getevents -o compact --pods xwing
kubectl exec -ti xwing -- bash -c 'cat /etc/shadow'
```

Docker: `docker exec -ti tetragon tetra getevents -o compact`. Output:

```
🚀 process default/xwing /bin/cat /etc/shadow
📚 read    default/xwing /bin/cat /etc/shadow
💥 exit    default/xwing /bin/cat /etc/shadow 0
```

Writing, e.g. `echo foo >> /etc/bar`, produces `📝 write` events.

## Checked

Date: 2026-11-07

File events page read in full, plus the file_monitoring.yaml quickstart policy. Corrected the security_mmap_file operators (Equal or Mask on arg 1, Mask on arg 2).

Method: documentation only; no commands were run.
