---
id: computing-software.cloud-infrastructure-engineering.external-dns.service-source-targets
name: service-source-targets
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, service-source, loadbalancer-targets, headless-service, srv-nodeport, listen-endpoint-events]
level: advanced
status: docs-checked
description: "How the ExternalDNS service source picks domain names and targets for LoadBalancer, ClusterIP, headless, NodePort and ExternalName Services, including SRV records."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/sources/service.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service source: names and targets

**Domain names**, in order: `hostname` / `internal-hostname` annotations (unless `--ignore-hostname-annotation`); then `--compatibility` modes if nothing produced; then `--fqdn-template` if nothing produced or `--combine-fqdn-annotation` is set. Filter with `--service-type-filter` (repeatable) and `--label-filter`.

**Targets.** A `target` annotation wins. Otherwise by `spec.type`:
- **LoadBalancer:** internal-hostname uses `spec.clusterIP` (none if `None`); else `spec.externalIPs`; else each `status.loadBalancer.ingress` ip or hostname. `--resolve-service-load-balancer-hostname` resolves hostnames to IPs; a DNS failure yields zero targets.
- **ClusterIP headless:** Endpoints addresses matching the selector (also `notReadyAddresses` if `publishNotReadyAddresses` or `--always-publish-not-ready-addresses`). Pod `target` annotation, then `endpoints-type` NodeExternalIP or HostIP (or `--publish-host-ip`), else the address IP. A Pod with `spec.hostname` also gets `<hostname>.<name>`.
- **ClusterIP, not headless:** `clusterIP` only with internal-hostname or `--publish-internal-services`; otherwise no targets.
- **NodePort:** with `externalTrafficPolicy: Local`, only Nodes with a running matching pod, in tiers (ready, then terminating, then not-ready). `access` public or private chooses address types.
- **ExternalName:** `spec.externalIPs`, else the `externalName` value.

**SRV for NodePort:** one SRV per `nodePort` port (priority 0, weight 50). Requires `SRV` in `--managed-record-types`:
```console
external-dns ... --managed-record-types=A --managed-record-types=CNAME --managed-record-types=SRV
```

**Endpoint changes** are not watched by default; add `--listen-endpoint-events`, at the cost of more reconciles and provider calls.

## Checked

2026-11-04. Confirmed against the ExternalDNS Service source page: filtering, domain names, headless pod names, targets per service type, NodePort tiers and SRV records, and endpoint reconciliation. Nothing removed.
Method: documentation only; no commands were run.
