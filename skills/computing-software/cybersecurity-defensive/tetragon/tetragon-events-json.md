---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-events-json
name: tetragon-events-json
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [events-json]
level: practitioner
status: docs-checked
description: "Read Tetragon JSON events: where to collect them and the key fields of a process_exec event such as exec_id, pod, binary, node_name and time."
sources:
  - "https://tetragon.io/docs/concepts/events/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JSON event format

Goal: read raw Tetragon JSON events and know which fields identify the process, the workload and the time.

## Where to get them

On Kubernetes read the stdout container log:

```shell
kubectl logs -n kube-system -l app.kubernetes.io/name=tetragon -c export-stdout -f
```

A default deployment also writes the JSON log to `/var/log/tetragon/tetragon.log`, where normal log collection tooling (for example fluentd, logstash) can export it. The file is rotated and compressed by default; the Helm options customize the location.

## What a base install produces

A base installation produces `process_exec` and `process_exit` events encoded as JSON. They carry Kubernetes API and identity metadata plus OS-level process visibility about the executed binary, its parent and the execution time.

## Key fields (process_exec example)

```json
{
  "process_exec": {
    "process": {
      "exec_id": "Z2tl...",
      "pid": 52699,
      "uid": 0,
      "cwd": "/",
      "binary": "/usr/bin/curl",
      "arguments": "https://ebpf.io/applications/#tetragon",
      "flags": "execve rootcwd",
      "start_time": "2023-10-06T22:03:57.700327580Z",
      "auid": 4294967295,
      "pod": { "namespace": "default", "name": "xwing", "workload": "xwing" },
      "docker": "551e161c47d8ff0eb665438a7bcd5b4",
      "parent_exec_id": "Z2tl...",
      "tid": 52699
    },
    "parent": { "binary": "/bin/bash" }
  },
  "node_name": "gke-john-632-default-pool-7041cac0-9s95",
  "time": "2023-10-06T22:03:57.700326678Z"
}
```

(Shortened; the full event also holds the container, image and pod labels for both process and parent.)

- Every event contains a `process_exec` block identifying the process that generated it. For execution events it is the primary block; Tracing Policy events attach the hook's data to it.
- `process_exec.exec_id` is a cluster-wide unique id for the process.
- `process_exec.process.pod` holds the Kubernetes metadata.
- `node_name` and `time` give location and time and are present in all event types.

## Checked

Date: 2026-11-07

Cited page read in full; every claim matched to page text.

Method: documentation only; no commands were run.
