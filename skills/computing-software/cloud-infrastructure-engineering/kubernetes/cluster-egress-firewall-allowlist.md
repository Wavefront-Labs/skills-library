---
id: computing-software.cloud-infrastructure-engineering.kubernetes.cluster-egress-firewall-allowlist
name: cluster-egress-firewall-allowlist
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, egress-control, egress-allowlist, firewall, nat-gateway, aks]
level: practitioner
status: docs-checked
description: "Build the cloud firewall allowlist a cluster needs for egress (registries, cloud APIs, control plane, OS updates), and test it before locking down."
sources: ["https://learn.microsoft.com/en-us/azure/aks/outbound-rules-control-egress", "https://learn.microsoft.com/en-us/azure/aks/limit-egress-traffic", "https://docs.cloud.google.com/kubernetes-engine/docs/how-to/private-clusters", "https://docs.aws.amazon.com/eks/latest/userguide/private-clusters.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cluster egress allowlists

Locking down egress breaks clusters in subtle ways (nodes cannot pull images, join, or reach
cloud APIs). Build the list first, apply it in log-only mode, then enforce.

## Categories to allow
| Need | Examples |
|---|---|
| Control plane | managed API endpoint (`*.hcp.<region>.azmk8s.io`, EKS endpoint), or keep it private |
| Images | `registry.k8s.io`, your registry, `*.dkr.ecr.<region>.amazonaws.com` plus S3, `mcr.microsoft.com`, `*.data.mcr.microsoft.com` |
| Identity and cloud APIs | STS, `login.microsoftonline.com`, `management.azure.com`, metadata-based auth |
| Node OS | package mirrors, NTP, time and certificate revocation endpoints |
| Add-ons | cert-manager ACME servers, external-dns provider API, monitoring SaaS |
AKS: Azure Firewall offers an `AzureKubernetesService` FQDN tag that restricts outbound traffic
from the cluster; Microsoft's guide also lists network rules (for example UDP 123 for NTP) and,
for the API server, a TCP 443 rule to its IP in some configurations, so follow the current rules
page rather than the tag alone.
EKS: AWS lists VPC endpoints for private clusters, including `ecr.api`, `ecr.dkr` and `s3` for
image pulls. GKE: Private Google Access is enabled automatically on a private cluster unless you
use Shared VPC, and Cloud NAT provides outbound internet access for private nodes.

## Give egress a stable identity
Route nodes through a NAT gateway or firewall with static IPs so partners can allowlist them.
Check whether your CNI translates pod source addresses before they reach the NAT or firewall.

## Test
```bash
kubectl run egress-test --rm -it --image=curlimages/curl --restart=Never -- \
  sh -c 'for u in https://registry.k8s.io https://login.microsoftonline.com https://api.github.com; do curl -s -o /dev/null -w "%{http_code} $u\n" -m 5 $u; done'
```
Also test from a node (`kubectl debug node/<n> -it --image=curlimages/curl`), because kubelet and
containerd egress do not pass through pod network policies.

## Verify
Firewall deny logs are empty for a full day in log-only mode before enforcing; new node
scale-up succeeds after enforcement.

## Checked

2026-10-27. Release: Microsoft AKS docs (azure-aks-docs main), AWS EKS and GKE private cluster pages, October 2026
- Confirmed in the AKS outbound rules page the FQDNs `*.hcp.<location>.azmk8s.io`, `mcr.microsoft.com`, `*.data.mcr.microsoft.com`, `management.azure.com`, `login.microsoftonline.com`, `packages.microsoft.com` and the NTP rule (UDP 123); confirmed the `AzureKubernetesService` FQDN tag and the extra API-server network rule in the AKS limit-egress guide.
- Confirmed in the EKS private cluster page the VPC endpoints `ecr.api`, `ecr.dkr` and `s3` for image pulls, and in the GKE private cluster page that Private Google Access is enabled automatically unless Shared VPC is used and that Cloud NAT provides outbound access.
- Removed the `gcr.io` and `*.pkg.dev` entries, the pod SNAT claim and the pinned curl image tag, which were not confirmed.

Method: documentation only; no commands were run.
