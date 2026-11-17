---
id: computing-software.cloud-infrastructure-engineering.observability.kubernetes-pod-logs-with-filelog
name: kubernetes-pod-logs-with-filelog
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [k8s-pod-logs-filelog, container-log-parsing, otel-kubernetes, filelog-receiver-config, otel-collector]
level: practitioner
status: docs-checked
description: "Collect Kubernetes pod logs with the OTel filelog receiver: /var/log/pods mounts, container operator for CRI/docker, excluding own logs, k8sattributes association."
sources: ["https://opentelemetry.io/docs/platforms/kubernetes/collector/components/#filelog-receiver", "https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/pkg/stanza/docs/operators/container.md", "https://kubernetes.io/docs/concepts/cluster-administration/logging/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pod logs with filelog

By default the kubelet directs the container runtime to write container logs into directories under `/var/log/pods`
(the path can be changed with the kubelet `podLogsDir` setting). Run the collector as a DaemonSet that reads those files.

## Receiver
```yaml
receivers:
  filelog:
    include: [/var/log/pods/*/*/*.log]
    exclude: [/var/log/pods/*/otel-collector/*.log]   # do not read the collector's own logs
    start_at: end
    include_file_path: true
    operators:
      - type: container
        id: container-parser
```
- The `container` operator parses docker, cri-o and containerd formats; with `format` unset it detects the format.
- It merges partial log lines (up to `max_log_size`, default 1MiB).
- With `add_metadata_from_filepath` (default true) it needs `include_file_path: true`; it then sets resource
  attributes such as `k8s.pod.uid` and `k8s.container.name` from the file path.
- Mount the host path `/var/log/pods` into the collector pod. The Helm chart's `logsCollection` preset gets you
  started.

## Enrichment
The `k8sattributes` processor can associate by the `k8s.pod.uid` resource attribute; the Kubernetes components page
shows a `pod_association` entry with `from: resource_attribute` and `name: k8s.pod.uid`.

## Gotchas
- The kubelet rotates container logs by `containerLogMaxSize` (default 10Mi) and `containerLogMaxFiles` (default 5);
  a pod that logs faster than the collector reads can lose lines to rotation, so raise the limits if you see gaps.
- Do not run a second log shipper on the same files unless you intend duplicates.

## Checked
2026-11-01. Confirmed on the OpenTelemetry Kubernetes components page (filelog include/exclude/start_at/
include_file_path, hostPath mount, logsCollection preset, pod_association by k8s.pod.uid), the container operator
page (formats, fields, defaults, file-path metadata) and the Kubernetes logging page (`/var/log/pods`, `podLogsDir`,
`containerLogMaxSize`, `containerLogMaxFiles`). Removed: file_storage offsets, retry_on_failure, file permission
claim, JSON/recombine parsing advice, Loki query example, docker-runtime mounts, filename pattern and CRI line layout.
Method: documentation only; no commands were run.
