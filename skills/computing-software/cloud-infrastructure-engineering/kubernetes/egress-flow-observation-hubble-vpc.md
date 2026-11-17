---
id: computing-software.cloud-infrastructure-engineering.kubernetes.egress-flow-observation-hubble-vpc
name: egress-flow-observation-hubble-vpc
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, egress-control, egress-flow-logs, hubble, vpc-flow-logs, observability]
level: practitioner
status: docs-checked
description: "See which pods talk to which external destinations using Hubble flows, DNS logs and cloud VPC flow logs, and attribute SNATed traffic back to pods."
sources: ["https://docs.cilium.io/en/stable/observability/hubble/", "https://docs.cilium.io/en/stable/observability/visibility/", "https://docs.cilium.io/en/stable/observability/hubble/configuration/export/", "https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html", "https://cloud.google.com/vpc/docs/about-flow-logs-records", "https://coredns.io/plugins/log/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Observing egress flows

## Cilium Hubble
```bash
hubble observe --namespace shop --to-label reserved:world --last 200
hubble observe --namespace shop --type l7 --protocol dns          # what names pods resolve
hubble observe --verdict DROPPED --to-label reserved:world -f    # policy drops to the internet
```
Hubble flows identify the source and destination endpoints (pod, namespace, labels), so it
answers "which workload called this IP". L3/L4 events are visible by default; DNS and HTTP
(L7) visibility needs an L7 `CiliumNetworkPolicy` rule for that traffic, and such a policy
also restricts the traffic it selects (see Cilium's visibility page). With a DNS rule,
flows show the queried name next to the IP.
For history beyond Hubble's in-memory buffer, use the Hubble exporter
(`hubble.export.static.enabled=true` and `hubble.export.static.filePath=...` in Helm; the
file path can be `stdout`) and ship the log to your log store or SIEM.

## Cloud flow logs
VPC flow logs record the traffic of a network interface, so after SNAT the source is the
node or NAT gateway address, not the pod.
- AWS: add the custom fields `pkt-srcaddr` and `pkt-dstaddr` to the flow log format. AWS
  documents them as the packet-level (original) addresses, to be read with `srcaddr` and
  `dstaddr`, including the case where an EKS pod IP differs from the interface IP.
  With the AWS VPC CNI, `AWS_VPC_K8S_CNI_EXTERNALSNAT` (default `false`) controls whether
  the node SNATs pod traffic (the default) or an external NAT gateway does.
- GKE: enable flow logs on the subnet; GKE records carry pod and Service metadata when the
  source or destination of the traffic is a Pod or Service endpoint.
- Map IPs to pods at the time of the flow: pod IPs are reused, so keep a log of pod IP
  assignments or use the CNI's flow export.

## Without Cilium
- CoreDNS `log` plugin (query logging) shows which clients resolve which names.
- Calico policy rules support a `Log` action (processing continues to the next rule), so
  open-source Calico can log matching traffic from a `GlobalNetworkPolicy`.

## Verify
For a known test pod, `curl https://example.com` appears in Hubble with the pod name and in the
VPC flow log with the NAT IP at the same timestamp.

## Checked
2026-10-27. Documentation releases: Cilium v1.20.4, AWS VPC flow log record reference and amazon-vpc-cni-k8s README (current), Google Cloud flow log record reference, CoreDNS plugin docs, Calico 3.33.
Confirmed: hubble observe flags (`--to-label`, `--type l7`, `--protocol dns`, `--verdict`, follow) from the CLI source; L7 visibility requires L7 policy; Hubble exporter Helm keys; `pkt-srcaddr`/`pkt-dstaddr` semantics; `AWS_VPC_K8S_CNI_EXTERNALSNAT` default; GKE pod metadata in flow logs; Calico `Log` action.
Method: documentation only; no commands were run.
