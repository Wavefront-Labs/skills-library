---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-events-export-filtering
name: tetragon-events-export-filtering
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [events-export-filter]
level: advanced
status: docs-checked
description: "Restrict Tetragon JSON event export with allowlist and denylist filters, combining expressions with OR across lines and AND within a line."
sources:
  - "https://tetragon.io/docs/concepts/events/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Event export filtering

Goal: export only the events you want to the JSON output.

## How filters combine

Export filters are a line-separated list of JSON objects. Each object holds one or more filter expressions. Lines are combined with logical OR; sibling expressions within one object are combined with logical AND. For example:

```json
{"event_set": ["PROCESS_EXEC", "PROCESS_EXIT"], "namespace": ["foo"]}
{"event_set": ["PROCESS_KPROBE"]}
```

matches when the event is `PROCESS_EXEC` or `PROCESS_EXIT` AND the pod namespace is "foo"; OR when the event is `PROCESS_KPROBE`.

## Allowlist and denylist

- Neither configured: all events are exported.
- Only an allowlist: default-deny, so only listed events are exported.
- The denylist takes precedence over the allowlist when both match an event.

Configure them with Helm options, command line flags or environment variables. They apply only to events exported as JSON files (for example a `file` sink), not to the gRPC API: `tetra` still sees unfiltered events.

## Process event filters

- `event_set`: event types `PROCESS_EXEC`, `PROCESS_EXIT`, `PROCESS_KPROBE`, `PROCESS_UPROBE`, `PROCESS_TRACEPOINT`, `PROCESS_LOADER`.
- `binary_regex`, `parent_binary_regex`, `ancestor_binary_regex`: lists of regular expressions on binary names (for example `"^/path/to/kubelet$"`).
- `arguments_regex`, `parent_arguments_regex`, `pod_regex`, `namespace_regex`: lists of regular expressions. `container_id` filters the `process.docker` field with RE2 syntax.
- `namespace`: pod namespaces; `""` matches processes in no pod namespace.
- `pid`; `pid_set` (also includes descendants of the listed PIDs).
- `health_check`: binaries matching Kubernetes liveness/readiness probe commands.
- `labels`: Kubernetes label selector syntax; never matches events without the pod field (host processes).
- `policy_names`, `capabilities`.
- `in_init_tree`: whether a containerized process descends from the container init process, which can reveal processes injected by `docker exec` or `kubectl exec`.
- `cel_expression`: CEL expressions, with k8s IP and CIDR library extensions.

## Checked

Date: 2026-11-07

Events page read in full. Corrected the kubelet regex example and limited the RE2 claim to container_id, which is the only filter the page says uses RE2.

Method: documentation only; no commands were run.
