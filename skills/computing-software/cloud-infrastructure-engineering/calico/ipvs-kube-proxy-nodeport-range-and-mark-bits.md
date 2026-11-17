---
id: computing-software.cloud-infrastructure-engineering.calico.ipvs-kube-proxy-nodeport-range-and-mark-bits
name: ipvs-kube-proxy-nodeport-range-and-mark-bits
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [ipvs, kube-proxy, nodeport, felixconfiguration, iptablesmarkmask, kubenodeportrange, autodetect]
level: advanced
status: docs-checked
description: "Calico auto-detects IPVS kube-proxy; match KubeNodePortRange if the NodePort range changed and consider IptablesMarkMask above 1022 pods."
sources:
  - https://docs.tigera.io/calico/latest/networking/configuring/use-ipvs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
kube-proxy IPVS mode is a load balancer with scheduling options (round robin, shortest expected delay, least connections), and its connection-processing cost stays constant as services grow. In iptables mode that cost grows with cluster size. The page suggests considering IPVS above roughly 1,000 services and notes that real-world comparisons are not straightforward.

**Nothing to enable in Calico.** Calico detects IPVS when calico-node starts, during or after installation. If you change kube-proxy's mode on a running cluster, calico-node must be restarted for detection to happen (the page states detection is at start-up).

Requirements: kube-proxy configured for IPVS, and services of type NodePort.

**Two settings may need changing**, both in FelixConfiguration:

- `KubeNodePortRange`: Calico uses NodePorts for routing too, with the Kubernetes default range 30000:32767. If you changed the Kubernetes range, change this to match.
- `IptablesMarkMask`: in IPVS mode Calico stores an ID for each local endpoint in extra iptables mark bits. With more than 1,022 pods per host you may need to enlarge the mark bit size.

The fetched text does not give example values or a command for either parameter; consult the FelixConfiguration reference page it links to.

## Checked

Read in full on 2026-11-08: the Use IPVS kube-proxy page. IPVS auto-detection at calico-node start-up, the NodePort range default, the 1,022-pod mark-bit note and the prerequisites match it.

Method: documentation only; no commands were run.
