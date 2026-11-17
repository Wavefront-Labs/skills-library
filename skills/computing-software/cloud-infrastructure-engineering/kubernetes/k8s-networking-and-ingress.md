---
id: computing-software.cloud-infrastructure-engineering.kubernetes.k8s-networking-and-ingress
name: k8s-networking-and-ingress
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, networking, cni, cilium, calico, kube-proxy, iptables, ipvs, nftables, ebpf, service, clusterip, nodeport, loadbalancer, headless-service, externaltrafficpolicy, coredns, ndots, ingress, ingress-controller, ingress-nginx, gateway-api, httproute, cert-manager, tls, networkpolicy, default-deny, egress, ingressclass]
level: practitioner
status: docs-checked
description: "Route traffic into and within a cluster: Service types, kube-proxy modes, CoreDNS and ndots, Ingress vs Gateway API, cert-manager TLS, and default-deny NetworkPolicies."
sources: ["https://kubernetes.io/docs/concepts/services-networking/service/", "https://kubernetes.io/docs/reference/networking/virtual-ips/", "https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/", "https://kubernetes.io/docs/concepts/services-networking/ingress/", "https://gateway-api.sigs.k8s.io/", "https://kubernetes.io/docs/concepts/services-networking/network-policies/", "https://cert-manager.io/docs/usage/gateway/", "https://github.com/kubernetes/ingress-nginx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kubernetes networking and ingress: from the internet to the pod, and pod to pod

**Goal:** know exactly which hop a request takes, expose HTTP services through one managed
entry point with TLS, and lock east-west traffic down without breaking DNS.

## 1. The model in four facts
- Every pod gets a routable cluster IP; the **CNI** (Cilium, Calico, cloud VPC CNIs) provides it.
- A **Service** is a stable virtual IP + DNS name; kube-proxy or an eBPF dataplane (Cilium)
  load-balances to pod IPs listed in **EndpointSlices** (the older Endpoints API has been
  deprecated since v1.33). kube-proxy modes on Linux: `iptables` (the default today, with
  the docs saying a future release will change it to `nftables`), `nftables` (GA since
  v1.33, needs kernel 5.13+) and `ipvs` (deprecated since v1.35, to be disabled by default
  from v1.40 and removed in v1.43). Set the mode explicitly so an upgrade cannot change it.
- **DNS**: `<svc>.<ns>.svc.cluster.local` via CoreDNS.
- **NetworkPolicy** is enforced only if the CNI supports it (plain Flannel does not unless
  you add its optional policy controller).

## 2. Service types
| Type | Use |
|---|---|
| ClusterIP | default, in-cluster only |
| Headless (`clusterIP: None`) | no virtual IP and no kube-proxy handling; DNS returns pod IPs; StatefulSets, client-side LB, gRPC |
| NodePort | port from 30000-32767 by default (`--service-node-port-range`) on every node; mostly a building block |
| LoadBalancer | provisions an external (usually cloud L4) load balancer per Service; often reserved for the ingress controller or gateway |
| ExternalName | DNS CNAME to an external host; no proxying; the hostname clients use differs from the referenced one, which causes trouble for HTTP and HTTPS |

- `externalTrafficPolicy: Local` preserves the client source IP: kube-proxy only sends to
  node-local endpoints, and if a node has none the packets are dropped, so load
  balancer health checks should only pass on nodes that have a ready pod.
- gRPC/HTTP2 keeps long-lived connections, so connection-level (L4) balancing through a
  ClusterIP pins each client to the pod it first connected to. Use a headless Service with
  client-side balancing, or an L7 proxy/mesh.

## 3. DNS gotchas
- Pods get `options ndots:5` by default, so a name with fewer than five dots such as
  `api.example.com` is tried against the search domains before being tried as-is. Use a
  trailing dot (`api.example.com.`) or set
  `dnsConfig: {options: [{name: ndots, value: "2"}]}` for chatty clients.
- NodeLocal DNSCache runs a DNS cache on each node and skips iptables DNAT and connection
  tracking, which the Kubernetes docs say reduces conntrack races and stops UDP DNS entries
  filling the conntrack table.

## 4. Ingress vs Gateway API
**Ingress** (`networking.k8s.io/v1`, stable since v1.19) is frozen per the Kubernetes docs:
host/path routing + TLS, everything else via controller-specific annotations that do not
port. **Gateway API** splits roles: platform owns `GatewayClass`/`Gateway`, app teams own
`HTTPRoute`; `HTTPRoute`, `Gateway` and `GatewayClass` have been GA (`v1`) since Gateway API
v1.0, and header matching and weighted `backendRefs` are part of `HTTPRoute`.
```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata: {name: api, namespace: shop}
spec:
  parentRefs: [{name: public, namespace: gateway-infra}]
  hostnames: [api.example.com]
  rules:
  - matches: [{path: {type: PathPrefix, value: /v2}}]
    backendRefs: [{name: api-v2, port: 80, weight: 90}, {name: api-v3, port: 80, weight: 10}]
```
`weight` is a proportion of the rule's total weight, not a percentage.
- For new platforms prefer Gateway API. The community ingress-nginx project is retired: its
  README says best-effort maintenance ended in March 2026, with no further releases, bug
  fixes or security updates afterwards, and tells new users to pick a Gateway API
  implementation instead. Plan migrations for existing clusters.
- With Ingress always set `spec.ingressClassName`. If it is omitted, the Ingress is assigned
  the IngressClass annotated `ingressclass.kubernetes.io/is-default-class: "true"`, so keep
  at most one default (with several, the admission controller rejects new Ingresses that
  have no class). Some controllers work without any IngressClass, but Kubernetes
  recommends defining a default.

## 5. TLS with cert-manager
- `ClusterIssuer` for ACME (Let's Encrypt) with HTTP-01 or DNS-01. Let's Encrypt issues
  wildcard certificates only with DNS-01 (HTTP-01 and TLS-ALPN-01 cannot).
- Annotate the Ingress `cert-manager.io/cluster-issuer`, or annotate the `Gateway` the same
  way and reference the Secret from the listener's `certificateRefs`. For Gateway API,
  cert-manager 1.15+ no longer needs a feature flag but you must still enable Gateway API
  support in its configuration and install the Gateway API CRDs first.
- Debug chain: `kubectl get certificate,certificaterequest,order,challenge -A`.

## 6. NetworkPolicy
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: {name: default-deny, namespace: shop}
spec: {podSelector: {}, policyTypes: [Ingress, Egress]}
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: {name: allow-dns, namespace: shop}
spec:
  podSelector: {}
  policyTypes: [Egress]
  egress:
  - to: [{namespaceSelector: {matchLabels: {kubernetes.io/metadata.name: kube-system}}, podSelector: {matchLabels: {k8s-app: kube-dns}}}]
    ports: [{protocol: UDP, port: 53}, {protocol: TCP, port: 53}]
```
- Policies are additive allow-lists: they do not conflict, and any policy selecting a pod
  makes that direction default-deny for it.
- `from: [{namespaceSelector: ..., podSelector: ...}]` (one element) is AND; two list
  elements are OR, a classic accidental over-permit.
- Ingress and egress mechanisms often rewrite source or destination IPs, and the docs say it
  is not defined whether that happens before or after NetworkPolicy processing; the
  "source IP" a policy sees may be a load balancer or the node. Test the real path and allow
  the ingress controller's namespace rather than "the internet".
- The core API has no TLS-related rules, no targeting of Services by name and no node-identity
  targeting (per the Kubernetes docs list of gaps); L7 and FQDN rules come from CNI CRDs
  such as Cilium's.

## Debug routine
```bash
kubectl get svc,endpointslices -n shop
kubectl run -it --rm net --image=nicolaka/netshoot -- bash   # curl, dig, tcpdump
dig +search api.shop.svc.cluster.local; curl -v http://api.shop/healthz
kubectl get gateway,httproute -A; kubectl describe httproute api -n shop   # check Accepted/ResolvedRefs conditions
```

## Verify
- [ ] Every Service resolves and its EndpointSlice lists only ready pods.
- [ ] HTTPRoute/Ingress status shows Accepted and a valid certificate is served (`curl -vI`).
- [ ] With default-deny applied, an unlisted pod cannot connect, and DNS still works.
- [ ] Client IP appears correctly in app logs if the app needs it.
- [ ] A canary weight change shifts measured traffic as configured.

## Checked
2026-10-27. Documentation releases: Kubernetes website main (v1.38 dev tree; latest release v1.37.1) with feature-gate pages; Gateway API v1.6.3; ingress-nginx README (controller v1.15.1 tree); cert-manager website docs (main); Let's Encrypt challenge types page.
Confirmed: kube-proxy mode list, default and statuses (nftables GA 1.33, ipvs deprecated 1.35/removal 1.43), Endpoints deprecation (1.33), NodePort default range, `ndots:5`, NodeLocal DNSCache rationale, Ingress "frozen", Gateway API v1 GA at v1.0 and `weight` semantics, ingress-nginx retirement, cert-manager Gateway annotations and enablement, wildcard-only-DNS-01, NetworkPolicy additive and NAT-ordering text.
Method: documentation only; no commands were run.
