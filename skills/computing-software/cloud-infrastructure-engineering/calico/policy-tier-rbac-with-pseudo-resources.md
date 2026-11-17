---
id: computing-software.cloud-infrastructure-engineering.calico.policy-tier-rbac-with-pseudo-resources
name: policy-tier-rbac-with-pseudo-resources
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [rbac, tiers, network-policy, clusterrole, tier-networkpolicies, authorization, kubectl]
level: advanced
status: docs-checked
description: "Control who can read or change tiered policy using Kubernetes Roles with pseudo resources tier.networkpolicies and tier.globalnetworkpolicies and resourceNames like tiername.*."
sources:
  - https://docs.tigera.io/calico/latest/network-policy/policy-tiers/rbac-tiered-policies
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Calico uses standard Kubernetes RBAC (Role, ClusterRole) for tiers and policy. Because each policy belongs to a tier, access to a policy requires access to its tier too.

Pseudo resources used in rules: `tier.globalnetworkpolicies` and `tier.networkpolicies`. `resourceNames` selects scope:

- blank: any policy of that kind across all tiers
- `<tiername>.*`: any policy of that kind in the tier
- `<tiername.policyname>`: that specific policy (the prefix also identifies the tier)

```yaml
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: tier-default-reader
rules:
  - apiGroups: ['projectcalico.org']
    resources: ['tiers']
    resourceNames: ['default']
    verbs: ['get']
  - apiGroups: ['projectcalico.org']
    resources: ['tier.networkpolicies']
    resourceNames: ['default.*']
    verbs: ['get', 'list']
```

**Admin user:** `kubectl create clusterrolebinding permissive-binding --clusterrole=cluster-admin --user=<USER>`.

**Native v3 CRDs caveat.** With native `projectcalico.org/v3` CRDs, tier RBAC is enforced for create, update and delete through the admission webhook; GET, LIST and WATCH on tiered policies are not enforced.

**Testing and querying.** `kubectl auth can-i` cannot check tiered-policy RBAC. Use the `.p` suffix (`networkpolicies.p`) to name the Calico resource rather than the Kubernetes one. Select a tier with the label `projectcalico.org/tier` (for example `-l projectcalico.org/tier==net-sec`) or `--field-selector spec.tier=net-sec`; with no selector the server uses the `default` tier. A denied read fails with a message such as user cannot get tier.

## Checked

2026-11-08. The Configure RBAC for tiered policies page was read in full (tutorial examples skimmed against the concept section). Pseudo resource names, ClusterRole YAML, the native CRD caveat and query selectors were confirmed on the Configure RBAC for tiered policies page.

Method: documentation only; no commands were run.
