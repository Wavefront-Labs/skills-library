---
id: computing-software.cybersecurity-defensive.crowdsec.crowdsec-syslog-kubernetes-windows-datasources
name: crowdsec-syslog-kubernetes-windows-datasources
category: computing-software
field: cybersecurity-defensive
product: crowdsec
tags: [syslog-datasource, kubernetes-datasource, windows-event-log, wineventlog, xpath]
level: practitioner
status: docs-checked
description: "Use the syslog server, Kubernetes pod and Windows Event Log datasources and know the limits of each."
sources: ["https://docs.crowdsec.net/docs/log_processor/data_sources/syslog", "https://docs.crowdsec.net/docs/log_processor/data_sources/kubernetes", "https://docs.crowdsec.net/docs/log_processor/data_sources/windows_evt_log"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
## Syslog service

CrowdSec can run a syslog server and ingest logs forwarded to it. **UDP only**; messages must follow RFC3164 or RFC5424 and are at most 2048 bytes by default.

```yaml
source: syslog
listen_addr: 127.0.0.1
listen_port: 4242
labels:
  type: syslog
```

`listen_addr` defaults to 127.0.0.1, `listen_port` to 514, `max_message_len` to 2048. There is no command-line mode. The docs warn it is for small setups and can lose messages above a few hundred events per second; for volume, let a dedicated syslog server such as rsyslog write files that CrowdSec reads.

## Kubernetes

Streams container logs of pods selected by label via the Kubernetes API; streaming only. When a matching pod starts or restarts it follows its containers.

```yaml
source: kubernetes
namespace: ingress-nginx
selector: "app.kubernetes.io/name=ingress-nginx"
kube_config: /path/to/kubeconfig
kube_context: production
labels:
  type: nginx
```

`selector` uses standard label selector syntax. `namespace` defaults to `default`; use one entry per namespace. The datasource tries in-cluster service-account credentials first and reads `kube_config` (default `~/.kube/config`) only when those are unavailable.

## Windows Event Log

```yaml
source: wineventlog
event_channel: Security
event_ids:
  - 4625
event_level: information
labels:
  type: eventlog
```

`event_level` is one of VERBOSE, INFORMATION, WARNING, ERROR or CRITICAL, and `event_ids` and `event_level` apply only with `event_channel`. Alternatively set `xpath_query` to a custom XPath query; one of the two is required.

## Checked

2026-11-03. Confirmed against the Syslog Server, Kubernetes and Windows Event Log datasource pages (UDP only, RFC3164/RFC5424, defaults 127.0.0.1, 514 and 2048, the small-setup warning, kubernetes selector/namespace/kube_config/kube_context and in-cluster-first auth, wineventlog event_channel/event_ids/event_level/xpath_query rules). Fixed: two dead source URLs replaced with the live pages. Removed: nothing.

Method: documentation only; no commands were run.
