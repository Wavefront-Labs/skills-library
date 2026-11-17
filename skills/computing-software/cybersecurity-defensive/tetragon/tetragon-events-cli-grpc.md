---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-events-cli-grpc
name: tetragon-events-cli-grpc
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [events-cli-grpc]
level: practitioner
status: docs-checked
description: "Watch Tetragon events with the tetra CLI (compact output, process and pod filters) and enable or move the gRPC endpoint through Helm."
sources:
  - "https://tetragon.io/docs/concepts/events/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Consuming events with tetra and gRPC

Goal: view and filter Tetragon events without reading raw JSON.

## tetra CLI

`tetra` can filter and pretty print events, by process, pod and other fields. Install it first (see the tetra install page). Pipe the export-stdout log into it:

```shell
kubectl logs -n kube-system -l app.kubernetes.io/name=tetragon -c export-stdout -f | tetra getevents -o compact
```

`tetra` is also available inside the `tetragon` container:

```shell
kubectl exec -it -n kube-system ds/tetragon -c tetragon -- tetra getevents -o compact
```

Filter by binary and pod:

```shell
kubectl logs -n kube-system -l app.kubernetes.io/name=tetragon -c export-stdout -f | tetra getevents -o compact --processes curl --pod xwing
```

Output:

```
🚀 process default/xwing /usr/bin/curl https://ebpf.io/applications/#tetragon
💥 exit    default/xwing /usr/bin/curl https://ebpf.io/applications/#tetragon 60
```

## gRPC

Tetragon can also expose a gRPC endpoint for listeners. A default Helm install exposes it on `unix:///var/run/tetragon/tetragon.sock`. Change the address with `--server-address`, or in Helm with `tetragon.grpc.address`; disable it with `tetragon.grpc.enabled`.

```shell
helm install tetragon cilium/tetragon -n kube-system --set tetragon.grpc.enabled=true --set tetragon.grpc.address=unix:///var/run/tetragon/tetragon.sock
```

An example gRPC client is `tetra` when it is not piped JSON output directly:

```shell
kubectl exec -ti -n kube-system ds/tetragon -c tetragon -- tetra getevents -o compact
```

## Checked

Date: 2026-11-07

Cited page read in full; every claim matched to page text.

Method: documentation only; no commands were run.
