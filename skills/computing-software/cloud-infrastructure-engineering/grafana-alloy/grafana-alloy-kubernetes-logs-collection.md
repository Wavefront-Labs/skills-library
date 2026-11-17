---
id: computing-software.cloud-infrastructure-engineering.grafana-alloy.grafana-alloy-kubernetes-logs-collection
name: grafana-alloy-kubernetes-logs-collection
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-alloy
tags: [lokisourcekubernetes, lokisourcekubernetes-events, localfile-match, discoveryrelabel, stagestatic-labels, raw-string-regex]
level: practitioner
status: docs-checked
description: "Collect Kubernetes system logs, pod logs via the Kubernetes API and cluster events with Alloy, forwarding through loki.process to loki.write."
sources: ["https://github.com/grafana/alloy/blob/main/docs/sources/collect/logs-in-kubernetes.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Collecting Kubernetes logs

Define a `loki.write` destination first (multiple `endpoint` blocks and `basic_auth` are supported), then pick log types.

## System logs
`local.file_match` discovers files by glob, `loki.source.file` reads them:
```alloy
local.file_match "node_logs" {
  path_targets = [{ __path__ = "/var/log/syslog", job = "node/syslog", node_name = sys.env("HOSTNAME") }]
}
loki.source.file "node_logs" {
  targets    = local.file_match.node_logs.targets
  forward_to = [loki.write.default.receiver]
}
```

## Pod logs via the Kubernetes API
Needs no node file privileges. In a DaemonSet restrict discovery to the local node to save CPU and memory:
```alloy
discovery.kubernetes "pod" {
  role = "pod"
  selectors {
    role  = "pod"
    field = "spec.nodeName=" + coalesce(sys.env("HOSTNAME"), constants.hostname)
  }
}
discovery.relabel "pod_logs" {
  targets = discovery.kubernetes.pod.targets
  rule {
    source_labels = ["__meta_kubernetes_namespace"]
    action        = "replace"
    target_label  = "namespace"
  }
  rule {
    source_labels = ["__meta_kubernetes_pod_name"]
    action        = "replace"
    target_label  = "pod"
  }
}
loki.source.kubernetes "pod_logs" {
  targets    = discovery.relabel.pod_logs.output
  forward_to = [loki.process.pod_logs.receiver]
}
loki.process "pod_logs" {
  stage.static_labels {
    values = { cluster = "CLUSTER_NAME" }
  }
  forward_to = [loki.write.default.receiver]
}
```
The page also builds `job`, `app`, `container` and `container_runtime` labels the same way. Reading `/var/log/pods` files instead needs system privileges.

## Events
`loki.source.kubernetes_events` with `job_name = "integrations/kubernetes/eventhandler"` and `log_format = "logfmt"`, then `loki.process` with `stage.static_labels` and `stage.labels`.

## Gotcha
Use backtick raw strings for `regex` (for example `` `^(\S+):\/\/.+$` ``); in a double-quoted string `\S` fails with `unknown escape sequence`.

## Checked

2026-11-08. Read in full the raw Alloy docs page behind the cited URL (docs/sources/collect/logs-in-kubernetes.md): loki.write delivery, system logs, pod logs via the Kubernetes API with the same-node selector and relabel rules, cluster events settings, and the raw-string regex tip. Nothing removed.

Method: documentation only; no commands were run.
