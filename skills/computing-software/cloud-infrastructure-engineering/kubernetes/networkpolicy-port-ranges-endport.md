---
id: computing-software.cloud-infrastructure-engineering.kubernetes.networkpolicy-port-ranges-endport
name: networkpolicy-port-ranges-endport
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, networkpolicy, endport, port-ranges, network-policy, cni]
level: practitioner
status: gated
description: "Allow a contiguous port range in a NetworkPolicy with endPort, the CNI support it needs, its limits (numeric ports only), and how to prove the range is enforced."
sources: ["https://kubernetes.io/docs/concepts/services-networking/network-policies/#targeting-a-range-of-ports", "https://kubernetes.io/blog/2021/08/12/kubernetes-1-22-networkpolicy-endport/", "https://docs.cilium.io/en/stable/security/policy/language/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NetworkPolicy port ranges with endPort

## When
A workload uses a port range (passive FTP data ports, RTP/media 10000-20000, game servers,
Ray/Spark worker ports) and listing hundreds of `ports:` entries is unworkable.

## The field
`endPort` is Stable since Kubernetes v1.25 (NetworkPolicy docs). It turns `port` into the start of an inclusive range.
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: {name: allow-media, namespace: voip}
spec:
  podSelector: {matchLabels: {app: media-relay}}
  policyTypes: [Ingress]
  ingress:
  - from:
    - namespaceSelector: {matchLabels: {kubernetes.io/metadata.name: sip}}
    ports:
    - protocol: UDP
      port: 10000
      endPort: 20000
```

## Rules the API server enforces
- `endPort` requires `port` (`may not be specified when port is not specified`), and `endPort >= port`
  (`must be greater than or equal to port`); both are checked in `pkg/apis/networking/validation/validation.go`.
- `port` must be **numeric** when `endPort` is set; named ports (`port: http`) are rejected (`may not be specified when
  port is non-numeric`).
- Protocol applies to the whole range; TCP and UDP ranges need two entries.

## CNI support is the real constraint
The API server stores `endPort` whether or not the CNI understands it. A CNI that ignores
the field enforces **only `port`** (the first port), which silently blocks the rest of the range.
- Which CNIs and versions support it was not confirmed here (gated: unconfirmed, source is paywalled or blocked); check your CNI's release notes. The Kubernetes docs
  say a plugin without support applies the policy to the single `port` only.
- Cilium's own `CiliumNetworkPolicy` also has `endPort` under `toPorts.ports` (gated: unconfirmed, source is paywalled or blocked).

## Verify
The policy above passes `kubeconform -strict` (run); the probe commands need a cluster and were not run (gated: unconfirmed, source is paywalled or blocked).
```bash
kubectl get netpol allow-media -n voip -o jsonpath='{.spec.ingress[0].ports}'   # field persisted
# probe first, middle and last port from an allowed and a denied namespace
kubectl run -n sip probe --rm -it --image=nicolaka/netshoot -- \
  sh -c 'for p in 10000 15000 20000 20001; do nc -zuv -w2 media-relay.voip $p; done'
```
UDP "open" results from `nc` are unreliable; for UDP verify with the app itself or watch
CNI flow logs (`hubble observe --to-pod voip/media-relay --port 15000`, Calico flow logs).

## Gotchas
- A range never spans protocols or named ports, so a container using named ports needs
  numeric ports in the policy.
- Very wide ranges (1-65535) are usually a sign the rule should drop `ports:` entirely.
- Egress policies need the same treatment; for egress to a range on external IPs combine
  `ipBlock` with `endPort`.
