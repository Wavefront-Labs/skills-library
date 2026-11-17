---
id: computing-software.cloud-infrastructure-engineering.kubernetes.networkpolicy-advanced-fqdn-l7-tiers
name: networkpolicy-advanced-fqdn-l7-tiers
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, networkpolicy, cilium, calico, fqdn, l7-policy, tiered-policy, globalnetworkpolicy, ciliumnetworkpolicy, http-policy, egress-control, zero-trust]
level: advanced
status: docs-checked
description: "Go past core NetworkPolicy with CNI-specific CRDs: FQDN-based egress allow-lists, L7 HTTP/gRPC method rules, and tiered/ordered policy precedence across teams."
sources: ["https://github.com/cilium/cilium/blob/main/Documentation/security/policy/layer3.rst", "https://github.com/cilium/cilium/blob/main/Documentation/security/policy/layer7.rst", "https://github.com/cilium/cilium/blob/main/examples/policies/l3/fqdn/fqdn.yaml", "https://docs.tigera.io/calico/latest/network-policy/policy-tiers/tiered-policy", "https://docs.tigera.io/calico/latest/reference/resources/tier", "https://docs.tigera.io/calico/latest/reference/resources/globalnetworkpolicy", "https://kubernetes.io/docs/concepts/services-networking/network-policies/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NetworkPolicy beyond core k8s — FQDN, L7, and tiered precedence

**Goal:** write policy for the things core `networking.k8s.io/v1` cannot express at all:
egress to a named external domain, HTTP method/path rules, and multi-team policy ordering.

**Relation to existing coverage:** the base allow-list model, default-deny, and the AND/OR
`from` gotcha are in
`computing-software.cloud-infrastructure-engineering.kubernetes.k8s-networking-and-ingress`.
This skill is the CNI-CRD layer on top of that model.

## 1. Why core NetworkPolicy can't do this
Core NetworkPolicy matches on `podSelector`/`namespaceSelector`/`ipBlock` only — no DNS names,
no L7 fields. An external API whose IPs change cannot be pinned with `ipBlock`; that needs a
CNI CRD.

## 2. Cilium `CiliumNetworkPolicy` — FQDN egress
```yaml
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata: {name: allow-stripe-api, namespace: billing}
spec:
  endpointSelector: {matchLabels: {app: billing-worker}}
  egress:
  - toEndpoints:
    - matchLabels: {"k8s:io.kubernetes.pod.namespace": kube-system, "k8s:k8s-app": kube-dns}
    toPorts:
    - ports: [{port: "53", protocol: ANY}]
      rules:
        dns: [{matchPattern: "*"}]          # sends DNS through Cilium's DNS proxy
  - toFQDNs: [{matchName: "api.stripe.com"}]
    toPorts: [{ports: [{port: "443", protocol: TCP}]}]
```
- Cilium learns name-to-IP mappings by intercepting DNS responses in its per-node DNS proxy
  (respecting TTLs) and allows the returned IPs. This needs `--enable-l7-proxy` (default true)
  **and** an L7 DNS rule (`rules.dns`) on the DNS egress rule. A plain port-53 allow without
  `rules.dns` lets lookups through but Cilium never learns the IPs: the most common "my FQDN
  policy doesn't work" bug.
- `toFQDNs` rules cannot be combined with other L3 selectors (`toEndpoints`, `toCIDR`) in the
  same egress rule, but can carry `toPorts`.
- `matchPattern: "*.stripe.com"` matches one subdomain level (`sub.stripe.com`, not
  `stripe.com` or `a.b.stripe.com`); `**.stripe.com` matches all nested subdomains.
- DNS proxy availability depends on the Cilium agent pod on that node.
- Debug with `cilium-dbg fqdn cache list` (in the agent pod) to see what's cached, and Hubble
  flow logs to see denied egress.

## 3. L7 HTTP policy (Cilium)
```yaml
  ingress:
  - fromEndpoints: [{matchLabels: {app: frontend}}]
    toPorts:
    - ports: [{port: "8080", protocol: TCP}]
      rules:
        http:
        - {method: "GET", path: "/api/v1/products.*"}
        - {method: "POST", path: "/api/v1/orders$"}
```
- `method` and `path` are extended POSIX regexes; paths must begin with `/`.
- L7 rules send matching traffic through a node-local Envoy proxy. A request that violates the
  policy gets a protocol-specific denial, for HTTP a 403 access denied.
- This is policy enforcement, not a service mesh: no retries, no mTLS, no traffic shifting.
  For that, see
  `computing-software.cloud-infrastructure-engineering.kubernetes.service-mesh-sidecar-networking-mtls`.

## 4. Calico `GlobalNetworkPolicy` and tiers
```yaml
apiVersion: projectcalico.org/v3
kind: Tier
metadata: {name: platform-security}
spec: {order: 100}
---
apiVersion: projectcalico.org/v3
kind: GlobalNetworkPolicy
metadata: {name: platform-security.deny-metadata-api}
spec:
  tier: platform-security
  selector: all()
  types: [Egress]
  egress:
  - {action: Deny, destination: {nets: ["169.254.169.254/32"]}}
  - {action: Pass}                       # hand everything else to later tiers
```
- **Tiers are evaluated in `order`, smallest first.** A platform tier with a low order can
  hard-deny something (for example the cloud metadata IP) that no namespace NetworkPolicy can
  override, because Kubernetes NetworkPolicies live in the `default` tier (order 1,000,000,
  evaluated last). Calico also creates `kube-admin` (order 1,000) and `kube-baseline` (order
  10,000,000) tiers for Kubernetes ClusterNetworkPolicy.
- Within a tier, policies run in `order` (lowest first). `Allow` and `Deny` end evaluation;
  `Pass` jumps to the next tier that has a policy for the endpoint. If a tier applies to an
  endpoint but no rule matches, the packet is **dropped** unless the tier's `defaultAction` is
  `Pass`. That is why the guardrail policy above ends in `Pass`, not `Allow`: an `Allow` would
  skip every later tier, including the app teams' policies.
- `GlobalNetworkPolicy` is cluster-scoped and defaults to the `default` tier when `tier` is
  unset; the tier must exist first. Calico's namespaced `NetworkPolicy` uses the same rule
  language.

## 5. Zero-trust egress pattern
Combine both: default-deny all egress (core NetworkPolicy or `CiliumNetworkPolicy`), explicit
FQDN allow-list per workload for third-party APIs, explicit CIDR allow for known internal
systems, and a platform-tier hard-deny on metadata/link-local ranges that no app team policy
can punch a hole through.

## Verify
- [ ] FQDN policy: the DNS egress rule carries `rules.dns`, and `cilium-dbg fqdn cache list`
  shows a resolved entry for the name.
- [ ] L7 rule: a request to a disallowed method/path on an allowed port returns the proxy's
  403, not an app-level 404.
- [ ] Tiered policy: a namespace-level Allow cannot override the platform tier's Deny, and
  ordinary traffic still reaches the namespace policies (the platform policy ends in `Pass`).
- [ ] Policy change propagation time (edit to enforced) is measured under load, not assumed.

## Checked
Checked 2026-10-27 against cilium/cilium main documentation (layer 3 DNS-based policy: DNS
proxy, `--enable-l7-proxy` plus `rules.dns` requirement, TTLs, `matchName`/`matchPattern`
wildcard semantics, no other L3 selectors with `toFQDNs`; layer 7: POSIX regex method and
path, Envoy, HTTP 403; the fqdn example policy; `cilium-agent` flag default; `cilium-dbg fqdn
cache list` reference) and tigera/docs Calico Open Source (Tier resource: smallest order first,
`defaultAction` Deny/Pass; tiered policy: default tier 1,000,000 holding Kubernetes policies,
kube-admin and kube-baseline tiers, Pass semantics, implicit drop; GlobalNetworkPolicy fields).
Fixed the FQDN example (DNS rule lacked `rules.dns`, so Cilium could not learn IPs) and the
tier example (a trailing `Allow` would bypass all later tiers; now `Pass`). Removed unconfirmed
Hubble and calicoctl invocations and the sub-second propagation figure.

Method: documentation only; no commands were run.
