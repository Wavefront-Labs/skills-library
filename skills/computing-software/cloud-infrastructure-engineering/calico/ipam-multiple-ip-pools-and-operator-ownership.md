---
id: computing-software.cloud-infrastructure-engineering.calico.ipam-multiple-ip-pools-and-operator-ownership
name: ipam-multiple-ip-pools-and-operator-ownership
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [ipam, ip-pools, installation, nodeselector, operator, no-default-pools, calicoctl]
level: practitioner
status: docs-checked
description: "Create several Calico IP pools in the Installation resource, or take pool management from the operator with ipPools [] or NO_DEFAULT_POOLS."
sources:
  - https://docs.tigera.io/calico/latest/networking/ipam/ippools
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A default install creates one IPv4 pool, used for pod addresses and any tunnel addresses. Add more pools when pod address space is disjoint or when you want topology-based assignment.

**With the operator**, list the pools in the Installation resource:

```yaml
apiVersion: operator.tigera.io/v1
kind: Installation
metadata:
  name: default
spec:
  calicoNetwork:
    ipPools:
    - name: pool-zone-1
      cidr: 192.168.0.0/24
      encapsulation: VXLAN
      nodeSelector: "zone == 'zone-1'"
    - name: pool-zone-2
      cidr: 192.168.1.0/24
      encapsulation: VXLAN
      nodeSelector: "zone == 'zone-2'"
```

Check with `kubectl get ippools`.

**Take pools away from the operator.** Set `ipPools: []` in the Installation. The operator then waits for you to create pools with calicoctl or kubectl before installing Calico components.

**Manifest installs.** To stop the default pool being created, add this to the `calico-node` DaemonSet environment before installing `calico.yaml`:

```yaml
env:
- name: NO_DEFAULT_POOLS
   value: "true"
```

Then create pools yourself, for example an `IPPool` named `pool-zone-1` with `cidr: 192.168.0.0/24`, `vxlanMode: Always`, `natOutgoing: true` and `nodeSelector: zone == "zone-1"` using `calicoctl create -f`.

Note the two syntaxes: the operator Installation uses `encapsulation`, while the `projectcalico.org/v3` IPPool resource uses `vxlanMode`.

## Checked

Read in full on 2026-11-08: the Create multiple IP pools page. Both Installation examples, the empty-list behaviour, NO_DEFAULT_POOLS and the calicoctl IPPool example match it. A remark on `ipipMode` that the page does not make was removed.

Method: documentation only; no commands were run.
