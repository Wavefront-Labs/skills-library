---
id: computing-software.cloud-infrastructure-engineering.azure.aks-egress-lockdown-with-azure-firewall
name: aks-egress-lockdown-with-azure-firewall
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, aks, aks-egress-lockdown, aks-fqdn-tag, user-defined-routing, azure-firewall, outbound-type]
level: advanced
status: docs-checked
description: "Force all AKS egress through Azure Firewall: userDefinedRouting outbound type, AzureKubernetesService FQDN tag, required network rules, API access and ingress routing pitfalls."
sources: ["https://learn.microsoft.com/azure/aks/limit-egress-traffic", "https://learn.microsoft.com/azure/aks/outbound-rules-control-egress", "https://learn.microsoft.com/azure/aks/egress-outboundtype", "https://learn.microsoft.com/azure/aks/egress-udr"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AKS egress lockdown with Azure Firewall

**Goal:** nodes and pods reach only approved destinations; every outbound flow is logged at the firewall.

## Network design
1. Firewall in the hub (or same VNet); AKS node subnet route table: `0.0.0.0/0 -> firewall private IP`.
2. Create the cluster with `--outbound-type userDefinedRouting` (no public LB outbound, no SNAT IPs on AKS):
```bash
az aks create -g rg -n aks01 --vnet-subnet-id <node-subnet-id> --outbound-type userDefinedRouting \
  --network-plugin azure --network-plugin-mode overlay --enable-managed-identity ...
```
Outbound type `userDefinedRouting` requires a `0.0.0.0/0` route with the firewall (or other NVA) as next hop in the node subnet's route table; each subnet supports at most one route table. Set the route table up before you create the cluster, because AKS validates the egress path. Outbound type `none` is the variant that does not require a default route.

## Firewall rules (minimum)
- Application rule: FQDN tag **AzureKubernetesService** (it contains the FQDNs in the AKS outbound rules article and is updated automatically; examples are `*.hcp.<location>.azmk8s.io`, `mcr.microsoft.com`, `*.data.mcr.microsoft.com`, `login.microsoftonline.com`, `packages.microsoft.com`), source = node subnet, HTTP 80 and HTTPS 443.
- Workloads outside `kube-system` and `gatekeeper-system` that talk to the API server need an extra network rule for TCP 443 to the API server IP in addition to the FQDN tag rule.
- Clusters using konnectivity do not need outbound TCP 9000 or UDP 1194, and nodes provisioned after March 2021 do not need outbound NTP on UDP 123.
- Add-ons and features have extra rules, listed per add-on in the outbound rules article: for example Azure Monitor uses the `AzureMonitor` service tag on TCP 443, Azure Policy needs `data.policy.core.windows.net` and `store.policy.core.windows.net`, and Defender, Key Vault, workload identity and cost analysis each have their own entries. Add your ACR (and its data endpoints or private endpoints).
- Then workload FQDNs (package repos, SaaS APIs) explicitly.

## API server access
With an API server public endpoint and authorized IP ranges, add the **firewall public frontend IP** to the authorized ranges (node traffic egresses there); developers need a jump box inside the firewall VNet or their own IPs in the range.

## Ingress pitfall (asymmetric routing)
With a 0/0 UDR to the firewall, publish inbound services through the firewall: a DNAT rule translates the firewall public IP to the load balancer frontend IP, and an internal load balancer (possibly in its own subnet) can serve internal traffic instead of or alongside the public one.

## Gotchas
- A missing FQDN or port typically shows as nodes failing to join, image pull errors or add-on pods crashlooping - read the firewall's application and network rule deny logs.

## Verify
- [ ] Cluster creates and upgrades cleanly; `curl` from a pod to an unapproved FQDN is denied and logged; approved ones work.

## Checked
Date: 2026-10-24. Checked against MicrosoftDocs/azure-aks-docs (limit-egress-traffic, outbound-rules-control-egress, egress-outboundtype, egress-udr; main branch).
- Confirmed: `userDefinedRouting` needs a 0.0.0.0/0 route to the NVA, one route table per subnet, `none` needs no default route; FQDN tag `AzureKubernetesService` (auto-updated, application rule HTTP/HTTPS); extra API-server rule for non-system workloads; konnectivity and NTP port exemptions; firewall public IP in authorized ranges; DNAT to the load balancer frontend; Azure Monitor service tag and Azure Policy FQDNs.
- Removed as unconfirmed: `az aks check-network outbound`, the Azure Monitor `*.ods`/`*.oms` FQDNs, the Network Contributor requirement, the asymmetric-routing explanation, the firewall log table name, and the SNAT capacity remark.
Method: documentation only; no commands were run.
