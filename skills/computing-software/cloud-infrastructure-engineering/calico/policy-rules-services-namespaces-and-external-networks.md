---
id: computing-software.cloud-infrastructure-engineering.calico.policy-rules-services-namespaces-and-external-networks
name: policy-rules-services-namespaces-and-external-networks
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [network-policy, services, namespaceselector, networkset, globalnetworkset, nets, kubernetes-api, dns]
level: practitioner
status: docs-checked
description: "Write rules that match Kubernetes Services by name, namespaces by label, and external CIDRs or GlobalNetworkSets, with the sample policies for API access, DNS, and a deny list."
sources:
  - https://docs.tigera.io/calico/latest/network-policy/policy-rules/service-policy
  - https://docs.tigera.io/calico/latest/network-policy/policy-rules/namespace-policy
  - https://docs.tigera.io/calico/latest/network-policy/policy-rules/external-ips-policy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Services by name.** `destination.services` or `source.services` take `name` and `namespace`; addresses and ports are detected from the Service. Egress to the Kubernetes API for pods in `my-app`:

```yaml
apiVersion: projectcalico.org/v3
kind: NetworkPolicy
metadata:
  name: allow-api-access
  namespace: my-app
spec:
  selector: all()
  egress:
    - action: Allow
      destination:
        services:
          name: kubernetes
          namespace: default
```

The same rule with `name: kube-dns` and `namespace: kube-system` in a `GlobalNetworkPolicy` gives every pod DNS access, but note it also creates default-deny behaviour for all pods, so allow other needed traffic. Ingress works via `source.services` (for example from `frontend-service` in namespace `frontend`).

**Namespaces by label.** Add `namespaceSelector` to a rule, for example `source: {selector: color == 'blue', namespaceSelector: shape == 'circle'}`. Because selectors can match namespace labels, Kubernetes RBAC over who may label namespaces becomes a policy control. A GlobalNetworkPolicy can use a top-level `namespaceSelector: 'environment == "development"'` with matching source and destination `namespaceSelector` rules to keep development namespaces talking only to each other.

**External networks.** Put CIDRs straight into a rule (IPv4 and IPv6 supported):

```yaml
egress:
  - action: Allow
    destination:
      nets:
        - 192.0.2.0/24
```

For reuse, a `NetworkSet` is a labelled set of CIDRs selectable from Kubernetes or Calico policy; a `GlobalNetworkSet` can be selected only by global policies. The page's deny list uses a GlobalNetworkSet labelled `ip-deny-list: 'true'` with `nets` `192.0.2.55/32` and `203.0.113.0/24`, referenced from a policy source selector `ip-deny-list == 'true' && !has(projectcalico.org/namespace)`. The page pairs a low-order (0) Deny policy with a high-order (1000) default-allow policy, both with `doNotTrack: true` and `applyOnForward: true` for faster packet-level denial.

## Checked

2026-11-08. The three policy rules pages (service, namespace, external IPs or networks) were read in full. Service, namespace, nets and deny list examples were confirmed.

Method: documentation only; no commands were run.
