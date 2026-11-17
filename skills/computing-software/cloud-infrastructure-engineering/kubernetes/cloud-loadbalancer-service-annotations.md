---
id: computing-software.cloud-infrastructure-engineering.kubernetes.cloud-loadbalancer-service-annotations
name: cloud-loadbalancer-service-annotations
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, services, loadbalancer, loadbalancersourceranges, internal-load-balancer, nlb, loadbalancerclass, aws-load-balancer-controller]
level: practitioner
status: gated
description: "Shape LoadBalancer Services per cloud: internal vs internet-facing, AWS NLB via the LB Controller, source ranges, static IPs, loadBalancerClass and provider annotations."
sources: ["https://kubernetes-sigs.github.io/aws-load-balancer-controller/latest/guide/service/annotations/", "https://learn.microsoft.com/en-us/azure/aks/internal-lb", "https://github.com/kubernetes-sigs/cloud-provider-azure/blob/master/pkg/consts/consts.go", "https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer", "https://cloud.google.com/kubernetes-engine/docs/concepts/service-load-balancer-parameters"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud LoadBalancer Service annotations

## Portable fields first
```yaml
spec:
  type: LoadBalancer
  loadBalancerClass: service.k8s.aws/nlb      # which controller handles it; cannot be changed once set
  loadBalancerSourceRanges: [203.0.113.0/24]  # firewall at the LB / security group
  externalTrafficPolicy: Local                # keep client IP, no extra hop
  allocateLoadBalancerNodePorts: false        # only for LBs that route straight to pods
```
`spec.loadBalancerIP` is deprecated since Kubernetes v1.24; prefer provider annotations for
static addresses.

## AWS (AWS Load Balancer Controller → NLB)
```yaml
metadata:
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: external
    service.beta.kubernetes.io/aws-load-balancer-nlb-target-type: ip
    service.beta.kubernetes.io/aws-load-balancer-scheme: internal          # default; or internet-facing
    service.beta.kubernetes.io/aws-load-balancer-subnets: subnet-a,subnet-b
    service.beta.kubernetes.io/aws-load-balancer-eip-allocations: eipalloc-1,eipalloc-2   # static IPs (internet-facing)
    service.beta.kubernetes.io/aws-load-balancer-ssl-cert: arn:aws:acm:...
    service.beta.kubernetes.io/aws-load-balancer-ssl-ports: "443"
    service.beta.kubernetes.io/aws-load-balancer-attributes: load_balancing.cross_zone.enabled=true
```
The older `aws-load-balancer-cross-zone-load-balancing-enabled` annotation is deprecated in
favour of `aws-load-balancer-attributes`. From controller v2.5.0 a mutating webhook sets
`spec.loadBalancerClass` so the controller handles new LoadBalancer Services by default;
otherwise the legacy cloud provider handles Services whose type annotation is not `nlb-ip` or
`external`. Set the type annotation at creation and do not edit it later.

## GCP
```yaml
metadata:
  annotations:
    networking.gke.io/load-balancer-type: "Internal"
    networking.gke.io/internal-load-balancer-allow-global-access: "true"
```
These GKE annotations are (gated: unconfirmed, source is paywalled or blocked). GKE
documentation is not in a readable source repository for this review, so confirm the names and
how to reserve a static internal IP in the GKE LoadBalancer Service parameters page.

## Azure
```yaml
metadata:
  annotations:
    service.beta.kubernetes.io/azure-load-balancer-internal: "true"
    service.beta.kubernetes.io/azure-load-balancer-internal-subnet: "apps-subnet"   # same VNet as the cluster
    service.beta.kubernetes.io/azure-pip-name: "web-pip"                       # static public IP
    service.beta.kubernetes.io/azure-load-balancer-health-probe-request-path: /healthz
```

## Gotchas
- Treat LoadBalancer Services as hard to mutate: `loadBalancerClass` cannot change, and the
  AWS type annotation should not be edited after creation. Test annotation changes in staging.
- Each LoadBalancer Service is one cloud load balancer and its cost. Consolidate HTTP behind
  Ingress/Gateway.
- Stuck `EXTERNAL-IP <pending>`: check controller logs and Service events (subnet tags,
  quotas, IAM).

## Verify
- [ ] `kubectl get svc web -o wide` shows the expected address type; reachable only from allowed ranges.

## Checked
Checked 2026-10-27 against kubernetes/website Service docs (main tree, v1.38 development;
latest release v1.37: `loadBalancerClass` immutable once set, `allocateLoadBalancerNodePorts`,
`loadBalancerIP` deprecated in v1.24), the AWS Load Balancer Controller Service annotations page
(type, target type, scheme default `internal`, subnets, EIP allocations, SSL cert and ports,
deprecated cross-zone annotation replaced by `aws-load-balancer-attributes`, webhook from v2.5.0,
legacy cloud provider behaviour), the AKS internal load balancer page and the
cloud-provider-azure annotation constants (`azure-load-balancer-internal`,
`azure-load-balancer-internal-subnet`, `azure-pip-name`,
`azure-load-balancer-health-probe-request-path`). Removed an unconfirmed claim about source
ranges with `externalTrafficPolicy: Cluster` and the GKE `loadBalancerIP` usage. GKE claims are
gated because GKE docs were not readable.

Method: documentation only; no commands were run.
