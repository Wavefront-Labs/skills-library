---
id: computing-software.cloud-infrastructure-engineering.calico.ipam-migrate-between-ip-pools
name: ipam-migrate-between-ip-pools
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [ipam, ip-pools, migration, cluster-cidr, kube-proxy, disable-pool, allowed-uses]
level: practitioner
status: docs-checked
description: "Move running pods from one IP pool to another without outage: add the new pool, disable the old, recycle pods, verify, then delete; keep pools inside the Kubernetes cluster CIDR."
sources:
  - https://docs.tigera.io/calico/latest/networking/ipam/migrate-pools
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Use this when you need more addresses or must change CIDR. Calico supports several disjoint pool CIDRs, but Kubernetes expects all pod addresses within one cluster CIDR, and not every orchestrator supports changing the pod network CIDR, so check yours. Calico IPAM must be in use.

Order matters. Existing pods stay connected only if you do not delete the old pool before the new one is verified.

1. **Add the new pool.** Strongly recommended: keep it inside the Kubernetes cluster CIDR. Addresses outside it may get unwanted NAT; if kube-proxy has a cluster CIDR configured, it must contain the new pool.
2. **Disable the old pool.** This blocks only new allocations; existing pods keep networking.
3. **Delete pods from the old pool**, including any created from it before it was disabled.
4. **Verify new pods get addresses from the new pool.**
5. **Delete the old pool.**

With an operator install, the tutorial edits `kubectl edit installation default`. Add the new pool:

```yaml
- name: new-ipv4-pool
  cidr: 10.0.0.0/16
  encapsulation: IPIP
```

Then disable the old pool by editing its entry in the same resource (here named `192.168.0.0-16`) so it selects no nodes, which prevents allocation from it:

```yaml
- nodeSelector: all()
+ nodeSelector: "!all()"
```

For a manifest install with calicoctl, set `disabled: true` on the old IPPool and apply it; remove the old pool at the end with `calicoctl delete pool <name>`. For an operator install, deleting the old pool means removing its entry from the default Installation. The example starts from a kubeadm cluster whose pool (192.168.0.0/16) did not match the cluster CIDR and moves to 10.0.0.0/16.

Verify with `kubectl get ippools`, and check that a new test pod gets an address from the new range (`kubectl -n <ns> get pods -o wide`).

## Checked

2026-11-08. The Migrate from one IP pool to another page was read in full. The step order, cluster CIDR and kube-proxy caution, the new-pool YAML and the disable edit (nodeSelector "!all()" for operator installs, disabled: true for manifest installs) were confirmed. Replaced the earlier partial description of the disable edit.

Method: documentation only; no commands were run.
