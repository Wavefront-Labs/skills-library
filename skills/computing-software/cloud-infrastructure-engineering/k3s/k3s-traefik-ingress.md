---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-traefik-ingress
name: k3s-traefik-ingress
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, traefik, ingress, loadbalancer-service]
level: practitioner
status: docs-checked
description: "How the packaged Traefik ingress works in K3s, how to customise it, and how to limit which nodes expose ports 80 and 443."
sources:
  - https://docs.k3s.io/networking/networking-services
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Traefik is deployed by default and runs a LoadBalancer Service on ports 80 and 443, advertising the Service external IPs in Ingress status.

By default ServiceLB uses all nodes to host that Service, so ports 80 and 443 cannot be used by other HostPort or NodePort pods and Ingress status lists every node IP. To restrict this, limit ServiceLB node selection (label nodes svccontroller.k3s.cattle.io/enablelb=true) or put nodes in a LoadBalancer pool and set matching labels in the Traefik HelmChartConfig.

Customise through a HelmChartConfig in /var/lib/rancher/k3s/server/manifests, never by editing /var/lib/rancher/k3s/server/manifests/traefik.yaml, which K3s overwrites at startup. See the values.yaml of the Traefik chart shipped with your K3s version, and the release notes for the exact Traefik version.

Remove Traefik by starting all servers with `--disable=traefik` (see the FAQ for using another ingress).

Service type: to use ClusterIP, for example behind an external load balancer or tunnel:

```
apiVersion: helm.cattle.io/v1
kind: HelmChartConfig
metadata:
  name: traefik
  namespace: kube-system
spec:
  valuesContent: |-
    service:
      spec:
        type: ClusterIP
```

Chart v40 warning: from the June 2026 releases (v1.33.13+k3s1, v1.34.9+k3s1, v1.35.6+k3s1, v1.36.2+k3s1) the Service type moved from service.type to service.spec.type. The old key is silently ignored and the Service falls back to LoadBalancer, so move it before upgrading.

## Checked

2026-11-03: read docs.k3s.io networking/networking-services. Confirmed: default Traefik LoadBalancer on 80/443, ServiceLB node selection label, HelmChartConfig customisation, --disable=traefik, and the June 2026 chart v40 service.spec.type change with its release list.

Method: documentation only; no commands were run.
