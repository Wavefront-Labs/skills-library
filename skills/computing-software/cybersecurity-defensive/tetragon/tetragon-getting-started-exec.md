---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-getting-started-exec
name: tetragon-getting-started-exec
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [demo-exec, tetragon, process-exec, tetra-getevents]
level: intro
status: docs-checked
description: "Observe Tetragon process execution events with tetra getevents on Kubernetes or Docker, in compact or full JSON form."
sources:
  - "https://tetragon.io/docs/getting-started/execution/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Monitor process execution with Tetragon

Goal: see every execution in a cluster, VM or bare metal host, attributed to a binary and its metadata (container, Pod, Node, cluster). Events come out as JSON logs and over a gRPC stream. The steps assume the Cilium demo app (with an `xwing` Pod) is deployed.

## Read the events

Single node Kubernetes cluster, target the DaemonSet:

```shell
kubectl exec -ti -n kube-system ds/tetragon -c tetragon -- tetra getevents -o compact --pods xwing
```

Multiple nodes: the Tetragon Pod must be on the same node as `xwing`.

```shell
POD=$(kubectl -n kube-system get pods -l 'app.kubernetes.io/name=tetragon' -o name --field-selector spec.nodeName=$(kubectl get pod xwing -o jsonpath='{.spec.nodeName}'))
kubectl exec -ti -n kube-system $POD -c tetragon -- tetra getevents -o compact --pods xwing
```

Docker:

```shell
docker exec tetragon tetra getevents -o compact
```

## Trigger an event

```shell
kubectl exec -ti xwing -- bash -c 'curl https://ebpf.io/applications/#tetragon'
```

(Docker: `docker exec -ti starwars-xwing-1 curl https://ebpf.io/applications/#tetragon`.) Compact output:

```
🚀 process default/xwing /bin/bash -c "curl https://ebpf.io/applications/#tetragon"
🚀 process default/xwing /usr/bin/curl https://ebpf.io/applications/#tetragon
💥 exit    default/xwing /usr/bin/curl https://ebpf.io/applications/#tetragon 60
```

A compact event holds the event type, pod name, binary and args; the exit event adds the return code (60 for this curl).

## Full JSON

Drop `-o compact` to get the full `process_exec` event. It includes `exec_id`, `pid`, `uid`, `cwd`, `binary`, `arguments`, `flags`, `start_time`, `auid`, and on Kubernetes the `pod` (namespace, name, container id, image, labels, workload), plus a `parent` block, `node_name` and `time`.

Next steps in the guide: file monitoring, then network monitoring.

## Checked

Date: 2026-11-07

Execution getting-started page read in full, plus the quickstart YAML it uses.

Method: documentation only; no commands were run.
