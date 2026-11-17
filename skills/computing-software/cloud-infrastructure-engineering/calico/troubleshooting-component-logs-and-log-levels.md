---
id: computing-software.cloud-infrastructure-engineering.calico.troubleshooting-component-logs-and-log-levels
name: troubleshooting-component-logs-and-log-levels
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [logs, log-level, felix, bird, bgpconfiguration, felixconfiguration, cni, calico-node, troubleshooting]
level: practitioner
status: docs-checked
description: "Where Calico logs live (calico-node, CNI plugin files) and how to set BGP and Felix log levels globally or per node with logSeverityScreen."
sources:
  - https://docs.tigera.io/calico/latest/operations/troubleshoot/component-logs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**calico-node logs** include per-node startup, the BGP agent and the Felix policy agent:

```
kubectl logs -n calico-system calico-node-xxxx
```

Components log to disk in `/var/log/calico`, to stdout, or both. Disk logs rotate: by default 10 files of 1MB are kept; the current file is `current`, and rotated files carry an `@` plus a timestamp.

**CNI plugin logs** are not available via kubectl. They go to the host disk and stderr, by default under `/var/log/calico/cni/`; the container runtime may also show them.

**BGP agent level** is `logSeverityScreen` in BGPConfiguration:

| Value | Effect |
|---|---|
| Debug | "debug all" for BIRD, most verbose |
| Info | protocol state changes (default) |
| Warning, Error, Fatal | BIRD logging off; only that level of configuration logs |

**Felix level** is `logSeverityScreen` in FelixConfiguration: Debug (most verbose), Info (default), Warning, Error, Fatal.

To change either:

```bash
kubectl get felixconfig -o yaml > felixconfig.yaml
# edit logSeverityScreen
kubectl replace -f felixconfig.yaml
```

Use `kubectl get bgpconfig -o yaml > bgp.yaml` for BGP. The resource named `default` is global; a node-specific one is named `node.<node-name>`, for example `node.node-1`.

## Checked

2026-11-04. Log locations, rotation defaults, level values and the edit workflow were confirmed on the Component logs page.

Method: documentation only; no commands were run.
