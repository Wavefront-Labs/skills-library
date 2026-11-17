---
id: computing-software.cloud-infrastructure-engineering.google-cloud.gke-internal-load-balancer-services-and-egress-nat
name: gke-internal-load-balancer-services-and-egress-nat
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, gke, internal-lb-service, service-type-loadbalancer, gke-cloud-nat, egress-nat-gateway, ip-masq-agent, private-cluster]
level: practitioner
status: docs-checked
description: "Expose GKE services privately with internal passthrough load balancers (subnet, static IP, global access, subsetting) and give private clusters controlled egress through Cloud NAT."
sources: ["https://docs.cloud.google.com/kubernetes-engine/docs/how-to/internal-load-balancing", "https://docs.cloud.google.com/kubernetes-engine/docs/concepts/service-load-balancer-parameters", "https://docs.cloud.google.com/kubernetes-engine/docs/how-to/ip-masquerade-agent", "https://docs.cloud.google.com/sdk/gcloud/reference/compute/routers/nats/create"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GKE internal LoadBalancer services and egress NAT

## 1. Internal passthrough Network Load Balancer
```yaml
apiVersion: v1
kind: Service
metadata:
  name: orders
  annotations:
    networking.gke.io/load-balancer-type: "Internal"
    networking.gke.io/internal-load-balancer-allow-global-access: "true"   # clients in other regions
    networking.gke.io/internal-load-balancer-subnet: "ilb-frontends"       # VIP from a dedicated subnet
spec:
  type: LoadBalancer
  loadBalancerIP: 10.20.0.15      # a reserved internal address in the chosen subnet; to share one IP across Services, reserve it with --purpose=SHARED_LOADBALANCER_VIP
  externalTrafficPolicy: Local    # only nodes with ready Pods receive traffic
  selector: {app: orders}
  ports: [{name: grpc, port: 443, targetPort: 8443, protocol: TCP}]
```
Enable **GKE subsetting** on large clusters (`gcloud container clusters update <C> --enable-l4-ilb-subsetting`). Once enabled it cannot be disabled.
For L7 (HTTP routing, TLS) use a Gateway or Ingress instead of this passthrough load balancer.

## 2. Egress for private nodes
Private nodes have no external IPs; give them Cloud NAT that includes the pod secondary range (`--nat-custom-subnet-ip-ranges=<SUBNET>:<RANGE_NAME>` includes only that secondary range):
```bash
gcloud compute routers create gke-nat-rtr --network=<VPC> --region=<R>
gcloud compute addresses create gke-egress-1 gke-egress-2 --region=<R>
gcloud compute routers nats create gke-nat --router=gke-nat-rtr --region=<R> \
  --nat-custom-subnet-ip-ranges=gke-subnet,gke-subnet:pods \
  --nat-external-ip-pool=gke-egress-1,gke-egress-2 \
  --enable-dynamic-port-allocation --min-ports-per-vm=256 --max-ports-per-vm=8192
```
Partners allow-listing your egress use the reserved static NAT addresses.

## 3. IP masquerade
If the `ip-masq-agent` ConfigMap is not defined, traffic to the default destinations is not masqueraded and keeps the Pod IP. Define the ConfigMap to control which destinations are not masqueraded; `nonMasqueradeCIDRs` should at least include the node and Pod ranges of the cluster (and the ranges where you want to use Cloud NAT):
```yaml
apiVersion: v1
kind: ConfigMap
metadata: {name: ip-masq-agent, namespace: kube-system}
data:
  config: |
    nonMasqueradeCIDRs: [10.0.0.0/8]
    resyncInterval: 60s
```

## Gotchas
- Allow the load balancer health-check ranges (see the load balancer firewall documentation) to reach the nodes.
- `externalTrafficPolicy: Local` sends traffic only to nodes with ready Pods, so load can be uneven across nodes.
- NAT port exhaustion shows as intermittent egress timeouts; raise `--min-ports-per-vm` or use dynamic port allocation (disabled by default; `--max-ports-per-vm` can only be set when it is enabled).

## Verify
- [ ] `kubectl get svc orders` shows the reserved internal IP; a VM in another region connects (global access).
- [ ] An outbound request from a Pod to an external service is seen from one of the reserved NAT addresses.

## Checked

2026-10-24, GKE internal load balancer, Service load-balancer parameters, IP masquerade agent pages and the Cloud NAT `routers nats create` reference on docs.cloud.google.com. Confirmed: the three `networking.gke.io/...` annotations, `--enable-l4-ilb-subsetting` and its irreversibility, `loadBalancerIP` with `SHARED_LOADBALANCER_VIP`, ConfigMap `ip-masq-agent` in `kube-system` with key `config`, `nonMasqueradeCIDRs`, NAT flags and defaults. Corrected: masquerade defaults (no ConfigMap means no masquerading of default destinations). Removed unconfirmed claims: the 250-backend limit, Gateway class name, health-check ranges, NAT drop metric name, external IP echo service.

Method: documentation only; no commands were run.
