---
id: computing-software.cloud-infrastructure-engineering.google-cloud.gke-networking-ingress-and-gateway
name: gke-networking-ingress-and-gateway
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, gke, gke-networking, vpc-native, alias-ip, gke-ingress, gke-gateway, gateway-api, container-native-load-balancing, neg, network-endpoint-groups, backendconfig, frontendconfig, internal-ingress, gke-dataplane-v2, cilium, network-policy, cloud-armor-gke, managed-certificates, multi-cluster-gateway]
level: practitioner
status: docs-checked
description: "Expose GKE workloads: VPC-native pod IPs, container-native load balancing with NEGs, Ingress with BackendConfig/FrontendConfig, Gateway API, Dataplane V2."
sources: ["https://cloud.google.com/kubernetes-engine/docs/concepts/alias-ips", "https://cloud.google.com/kubernetes-engine/docs/how-to/container-native-load-balancing", "https://cloud.google.com/kubernetes-engine/docs/concepts/ingress", "https://cloud.google.com/kubernetes-engine/docs/how-to/ingress-configuration", "https://cloud.google.com/kubernetes-engine/docs/concepts/gateway-api", "https://cloud.google.com/kubernetes-engine/docs/concepts/dataplane-v2"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# GKE networking, Ingress and Gateway

**Goal:** traffic hits pods directly from Google's load balancers (no kube-proxy double hop),
TLS and WAF are declared in Kubernetes objects, and east-west traffic is governed by network policy.

## 1. VPC-native: what it buys you
Pods get alias IPs from the subnet's secondary range, so they are routable in the VPC, reachable
over VPN/Interconnect, usable as **Network Endpoint Group** members, and firewall rules can target pod CIDRs.
Plan ranges per `gke-autopilot-vs-standard-cluster-design`; adding a pod range later: `clusters update --additional-pod-ipv4-ranges` (Standard, newer versions).

## 2. Container-native load balancing (always)
Annotate the Service: `cloud.google.com/neg: '{"ingress": true}'` (see the container-native load balancing page for when it is the default). The LB backend becomes a zonal NEG of pod IP:port; health checks go to the pod, rolling updates drain correctly through Pod readiness gates (the load balancer's view of Pod health).
Standalone NEGs are the option when you want to manage the whole load balancer yourself.

## 3. GKE Ingress (classic, still common)
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web
  annotations:
    kubernetes.io/ingress.class: "gce"            # "gce-internal" for an internal ALB (needs proxy-only subnet)
    kubernetes.io/ingress.global-static-ip-name: web-ip
    networking.gke.io/v1beta1.FrontendConfig: web-fe
spec:
  rules: [{host: www.example.com, http: {paths: [{path: /, pathType: Prefix, backend: {service: {name: web, port: {number: 80}}}}]}}]
```
- **BackendConfig** (per Service, `cloud.google.com/backend-config` annotation): health check path/port, timeouts, connection draining, session affinity, **Cloud Armor** policy (`securityPolicy.name`), **IAP** (`iap.enabled`), CDN (`cdn.enabled`), custom request/response headers, logging sample rate.
- **FrontendConfig**: HTTP→HTTPS redirect (`redirectToHttps.enabled`), SSL policy.
- GKE derives the health check from the Pod's readiness probe when one exists at Ingress creation (replicas scaled to 0 get the default check, path `/`). A missing readiness probe is the usual cause of UNHEALTHY backends.

## 4. Gateway API (the forward path)
Enable: `clusters update --gateway-api=standard`. GatewayClasses: `gke-l7-global-external-managed`, `gke-l7-regional-external-managed`, `gke-l7-rilb` (internal), `gke-l7-gxlb` (classic global), plus `-mc` variants for **multi-cluster** (fleet + `ServiceExport`), including `gke-l7-cross-regional-internal-managed-mc`.
```yaml
kind: Gateway
spec: {gatewayClassName: gke-l7-global-external-managed, listeners: [{name: https, protocol: HTTPS, port: 443, tls: {mode: Terminate}}]}
---
kind: HTTPRoute
spec: {parentRefs: [{name: external}], hostnames: [www.example.com], rules: [{backendRefs: [{name: web, port: 80, weight: 90}, {name: web-canary, port: 80, weight: 10}]}]}
```
Policies attach as CRs: `GCPBackendPolicy` (Cloud Armor, IAP, timeouts, session affinity), `HealthCheckPolicy`, `GCPGatewayPolicy` (SSL policy), `GCPTrafficDistributionPolicy`. Weighted `backendRefs` give canaries without a mesh. Gateway supports traffic splitting, header matching and cross-namespace routes that Ingress cannot.

## 5. Dataplane V2 and NetworkPolicy
`--enable-dataplane-v2` (enabled by default for new Autopilot clusters) is built on Cilium (eBPF) instead of the legacy Calico dataplane and does not use kube-proxy for Services. `NetworkPolicy` is enforced without add-ons and **network policy logging** is built in (configure the logging CRD).

## Gotchas
- Internal Ingress/Gateway needs a **proxy-only subnet** in the region; without one, creation fails.
- In Shared VPC the Ingress controller may not be able to create the health-check firewall rules in the host project; create them yourself there (see the container-native load balancing page for the source ranges).
- Each Ingress makes its own load balancer (forwarding rule, proxy, URL map) and consumes quota; consolidate hosts/paths into one Ingress or use Gateway.
- `type: LoadBalancer` Services are not supported as Ingress backends (use ClusterIP with NEGs); GKE subsetting (`--enable-l4-ilb-subsetting`) is a cluster option for internal passthrough load balancers.

## Verify
- [ ] `kubectl get svc web -o yaml` shows the `cloud.google.com/neg-status` annotation with a NEG per zone; `gcloud compute backend-services get-health` reports pods HEALTHY.
- [ ] `curl -I http://www.example.com` → 301 to https.
- [ ] The weight-10 canary backend receives roughly a tenth of requests in backend logs.
- [ ] A default-deny `NetworkPolicy` in a namespace blocks cross-namespace curl, and the denial appears in network policy logs.

## Checked

2026-10-27. Confirmed in the GKE Ingress, container-native load balancing, ingress configuration, Gateway API, alias IP and Dataplane V2 pages: GatewayClass names and the `-mc` split, Gateway policy CRs, BackendConfig fields (iap, cdn, securityPolicy, connectionDraining, timeoutSec, customRequestHeaders, logging sampleRate), FrontendConfig `redirectToHttps` and `sslPolicy`, ingress annotations (`ingress.class`, `global-static-ip-name`, `v1beta1.FrontendConfig`, `backend-config`), readiness-probe-derived health checks, standalone NEGs, proxy-only subnet need, pod IPs routable over peering and reachable on-premises through Cloud VPN or Interconnect, Dataplane V2 built on Cilium without kube-proxy, default for new Autopilot clusters, built-in policy logging, LoadBalancer Services not valid Ingress backends. `gcloud container clusters` flags (`--gateway-api`, `--additional-pod-ipv4-ranges`, `--enable-l4-ilb-subsetting`, `--enable-dataplane-v2`) confirmed on the create and update reference pages. Removed: the 60-minute certificate figure, 250-node figure, ManagedCertificate and managed-certificates annotation, `exposed_ports`, `pre-shared-certs`, `load-balancer-type` annotation, `NetworkLogging`/`FQDNNetworkPolicy` names, claim that Standard clusters cannot switch to Dataplane V2, `--purpose` value, IAM role for firewall rules, orphaned-resource gotcha.

Method: documentation only; no commands were run.
