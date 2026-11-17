---
id: computing-software.cloud-infrastructure-engineering.calico.bgp-advertise-service-cluster-and-external-ips
name: bgp-advertise-service-cluster-and-external-ips
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [bgp, services, cluster-ip, external-ip, ecmp, externaltrafficpolicy, bgpconfiguration, advertisement]
level: practitioner
status: docs-checked
description: "Advertise Kubernetes service cluster IPs and external IPs over BGP using serviceClusterIPs and serviceExternalIPs in BGPConfiguration; Local versus Cluster mode and ECMP needs."
sources:
  - https://docs.tigera.io/calico/latest/networking/configuring/advertise-service-ips
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Calico can advertise service IPs to external BGP peers, avoiding a dedicated load balancer. Requirements: at least one external router, route reflector or ToR peered with Calico nodes; for ECMP the upstream routers need BGP multipath; for `externalTrafficPolicy: Local` the Service must be `LoadBalancer` or `NodePort`.

| Service mode | What is advertised | Traffic |
|---|---|---|
| Cluster (default) | Every node advertises a route to the service CIDR | ECMP across nodes, then SNAT to the pod |
| Local | Only nodes with a backing pod advertise a /32 or /128 | Load balanced across nodes with endpoints, avoiding the second hop |

The page recommends Local: source IPs are preserved (so source-IP policy still works) and return traffic needs no SNAT undo. Cluster advertisement works best with an ECMP-capable ToR; otherwise all traffic for a route goes to one node.

**Cluster IPs.** Find the range from the API server's `--service-cluster-ip-range` (more than one if dual stack), check `calicoctl get bgpconfig default`, then patch or create:

```bash
calicoctl patch bgpconfig default --patch \
   '{"spec": {"serviceClusterIPs": [{"cidr": "10.0.0.0/24"}]}}'
```

Creating the default resource uses the same field, for example CIDRs `10.96.0.0/16` and `fd00:1234::/112`.

**External IPs** use the `serviceExternalIPs` field the same way; a service external IP is only advertised if it lies inside a listed block.

The older IPv4-only `CALICO_ADVERTISE_CLUSTER_IPS` variable is deprecated and still takes precedence over the BGPConfiguration if set.

Known issue: on OpenShift 4.5 and 4.6 (and Kubernetes 1.18 and 1.19) source IP is not preserved for NodePort or ExternalIP with Local policy without the `ExternalPolicyForExternalIP` feature gate; it is on by default from OpenShift 4.7 and Kubernetes 1.20.

## Checked

2026-11-04. The mode table, recommendations, commands, deprecation note and limitations were confirmed on the Advertise Kubernetes service IP addresses page.

Method: documentation only; no commands were run.
