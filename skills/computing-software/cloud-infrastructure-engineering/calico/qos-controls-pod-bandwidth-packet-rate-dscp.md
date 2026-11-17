---
id: computing-software.cloud-infrastructure-engineering.calico.qos-controls-pod-bandwidth-packet-rate-dscp
name: qos-controls-pod-bandwidth-packet-rate-dscp
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [qos, bandwidth, annotations, packet-rate, max-connections, dscp, diffserv, hostendpoint, pods]
level: advanced
status: docs-checked
description: "Limit pod bandwidth, packet rate and connections with qos.projectcalico.org annotations, and set DSCP on pod or host endpoint egress; eBPF bandwidth needs kernel 6.6+."
sources:
  - https://docs.tigera.io/calico/latest/networking/configuring/qos-controls
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Applies to Kubernetes pods through annotations (OpenStack QoS is a separate mechanism). Values accept suffixes such as `k`, `M`, `G`, plus binary forms like `Ki`. In the eBPF data plane, bandwidth QoS needs Linux kernel 6.6 or later.

Pod template example:

```yaml
metadata:
  annotations:
    qos.projectcalico.org/egressBandwidth: "100M"
    qos.projectcalico.org/egressBurst: "200M"
```

| Control | Annotations (prefix `qos.projectcalico.org/`) | Limits |
|---|---|---|
| Bandwidth, bits per second | `ingressBandwidth`, `egressBandwidth` | 1k to 1P |
| Burst, bits | `ingressBurst`, `egressBurst` | default 4Gi, max 34359738360 |
| Peak rate | `ingressPeakrate`, `egressPeakrate` | default unlimited, must exceed bandwidth |
| Minburst, bytes | `ingressMinburst`, `egressMinburst` | default MTU, 1k to 100M |
| Packet rate | `ingressPacketRate`, `egressPacketRate` | 1 to 10k per second |
| Packet burst | `ingressPacketBurst`, `egressPacketBurst` | default 5 |
| Connections | `ingressMaxConnections`, `egressMaxConnections` | 1 to 4294967295 |

Kubernetes bandwidth plugin annotations (`kubernetes.io/ingress-bandwidth`, `kubernetes.io/egress-bandwidth`) are accepted but ignored when the matching Calico one is present. Calico limits take effect immediately; the plugin needs pods recreated.

**DiffServ.** `qos.projectcalico.org/dscp` sets DSCP on egress traffic leaving the cluster or going to another host, and unlike the others it can go on a host endpoint:

```yaml
apiVersion: projectcalico.org/v3
kind: HostEndpoint
metadata:
  name: my-hep
  annotations:
    qos.projectcalico.org/dscp: "AF11"
```

## Checked

2026-11-04. Annotation names, limits, defaults and the DSCP example were confirmed on the Configure QoS Controls page. The HostEndpoint spec is abridged to the annotation.

Method: documentation only; no commands were run.
