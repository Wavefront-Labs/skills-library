---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-persistent-enforcement
name: tetragon-persistent-enforcement
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [enforcement-persistent, tetragon, keep-sensors-on-exit, grpc-policies]
level: advanced
status: docs-checked
description: "Keep Tetragon enforcement policies active across agent exit and restart, and persist and restore gRPC-installed policies."
sources:
  - "https://tetragon.io/docs/concepts/enforcement/persistent-enforcement/"
  - "https://tetragon.io/docs/concepts/enforcement/persistent-grpc-policies/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tetragon persistent enforcement

Goal: an enforcement policy keeps running when the tetragon process is gone.

Start with `--keep-sensors-on-exit`. Policies are pinned under `/sys/fs/bpf/tetragon`. A new tetragon process moves any existing `/sys/fs/bpf/tetragon` to `/sys/fs/bpf/tetragon_old`, sets up the configured policy, then removes `tetragon_old`. Limitation: no events are received during the downtime; only enforcement stays in place.

Example policy: Sigkill any process touching `/tmp/tetragon`.

```yaml
apiVersion: cilium.io/v1alpha1
kind: TracingPolicy
metadata:
 name: "enforcement"
spec:
 kprobes:
 - call: "fd_install"
   syscall: false
   args:
   - index: 0
     type: int
   - index: 1
     type: "file"
   selectors:
   - matchArgs:
     - index: 1
       operator: "Equal"
       values:
       - "/tmp/tetragon"
     matchActions:
     - action: Sigkill
```

Run `tetragon --bpf-lib bpf/objs/ --keep-sensors-on-exit --tracing-policy enforcement.yaml`, then `cat /tmp/tetragon` prints `Killed`. After stopping tetragon with Ctrl+C it still prints `Killed`.

## Persistent gRPC policies

Policies installed through gRPC (including `tetra tracingpolicy add`) can be stored and restored. Kubernetes and static policies are managed by their own sources. Use the same options every start:

```shell
sudo ./tetragon --btf /sys/kernel/btf/vmlinux --bpf-lib ./bpf/objs/ \
  --keep-sensors-on-exit --release-pinned-bpf=false \
  --persist-grpc-policies --persist-grpc-policies-dir /var/run/tetragon/grpc-policies
```

`--release-pinned-bpf` defaults to `true`; set it to `false` for continuous enforcement across a restart. The store directory default is `/var/run/tetragon/grpc-policies`.

Restart sequence: rename the tree to `tetragon_old` (old programs stay attached), create a new tree and load initial sensors, validate all store records, recreate each policy (disabled ones are registered without loading BPF), then remove `tetragon_old`. Policies are rebuilt from the store, not from the old tree.

`add`, `delete`, `enable`, `disable` and `set-mode` update the store. One JSON record per policy, named `<name>:<namespace>:<domain>.json`, with `yaml` and `enabled`. A failed runtime change restores the previous record.

## Checked

Date: 2026-11-07

Both enforcement pages (persistent enforcement and persistent gRPC policies) read in full; every claim matched, no change.

Method: documentation only; no commands were run.
