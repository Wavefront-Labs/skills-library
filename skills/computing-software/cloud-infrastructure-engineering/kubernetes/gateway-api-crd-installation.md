---
id: computing-software.cloud-infrastructure-engineering.kubernetes.gateway-api-crd-installation
name: gateway-api-crd-installation
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, gateway-api, gateway-api-crds, experimental-channel, crd-upgrade]
level: practitioner
status: docs-checked
description: "Install and upgrade Gateway API CRDs (standard vs experimental channel, server-side apply), match versions to your implementation, and avoid CRD ownership clashes."
sources: ["https://gateway-api.sigs.k8s.io/guides/getting-started/introduction/", "https://gateway-api.sigs.k8s.io/guides/crd-management/", "https://gateway-api.sigs.k8s.io/docs/concepts/versioning/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Installing Gateway API CRDs

Gateway API is not built into Kubernetes; CRDs are installed per cluster.

## Channels
| Channel | Contains |
|---|---|
| Standard | resources and fields that reached GA (or Beta): GatewayClass, Gateway, HTTPRoute, GRPCRoute, ReferenceGrant, BackendTLSPolicy (v1.4.0), TLSRoute (v1.5.0), TCPRoute and UDPRoute (v1.6.0) |
| Experimental | everything in standard plus resources with alpha API versions and fields not yet graduated; no backwards-compatibility guarantee |

```bash
VERSION=v1.6.1                      # the version the Gateway API getting-started page uses; pick the release your implementation supports
kubectl apply --server-side -f https://github.com/kubernetes-sigs/gateway-api/releases/download/$VERSION/standard-install.yaml
# or
kubectl apply --server-side -f https://github.com/kubernetes-sigs/gateway-api/releases/download/$VERSION/experimental-install.yaml
```
Server-side apply avoids the `metadata.annotations: Too long` error large CRDs hit with
client-side apply.

## Version matching
- Each implementation (Envoy Gateway, Istio, Cilium, NGINX Gateway Fabric and others with conformance
  reports) supports specific Gateway API versions; check its compatibility table before upgrading CRDs.
  Each Gateway API release supports the five most recent Kubernetes minor versions.
- Many controllers install the CRDs for you. The CRD management guide says a cluster admin or the
  cluster provider should own them; a bundling implementation must never overwrite CRDs with newer
  or unrecognised versions, overwrite CRDs of a different channel, or remove them. Choose ONE owner.

## Upgrading
- Moving from experimental to standard can remove fields in use; check with
  `kubectl get httproutes -A -o yaml | grep -i <field>` before switching. Avoid moving backwards, read the
  release notes, and upgrade one minor version at a time where possible.
- CRDs carry `gateway.networking.k8s.io/bundle-version` and `channel` annotations; read them:
```bash
kubectl get crd gateways.gateway.networking.k8s.io -o jsonpath='{.metadata.annotations}'
```
- ValidatingAdmissionPolicies ship with the CRDs: the Upgrade VAP prevents applying experimental CRDs
  over standard ones (remove it if you really must), and the Guardrails VAP blocks experimental fields
  unless an annotation is present.

## Verify
```bash
kubectl api-resources --api-group=gateway.networking.k8s.io
kubectl get gatewayclass         # ACCEPTED True for your implementation
```

## Checked

Documentation release: Gateway API docs (kubernetes-sigs/gateway-api site/content and apis/v1, latest release v1.6.3, repo commit 2026-10-23; v1.7.0 is at release-candidate stage).
Confirmed: channel contents and the graduation releases for BackendTLSPolicy (v1.4.0), TLSRoute (v1.5.0), TCPRoute and UDPRoute (v1.6.0); `kubectl apply --server-side` install commands for `standard-install.yaml` and `experimental-install.yaml`; `bundle-version` and `channel` annotations; the two VAPs; CRD ownership rules; five Kubernetes minors supported.
Corrected: TCPRoute, UDPRoute and TLSRoute are Standard channel in current releases, not experimental-only; the VAP description. Removed the GKE claim and the Helm-chart claim, which no Gateway API page covers.

Method: documentation only; no commands were run.
