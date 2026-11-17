---
id: computing-software.cloud-infrastructure-engineering.calico.ipam-change-pool-block-size
name: ipam-change-pool-block-size
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [ipam, blocksize, ip-pools, migration, calicoctl, temporary-pool, disruption]
level: advanced
status: docs-checked
description: "Change an IP pool block size after install by swapping through a temporary pool, since blockSize cannot be edited in place; valid ranges are /20-/32 IPv4 and /116-/128 IPv6."
sources:
  - https://docs.tigera.io/calico/latest/networking/ipam/change-block-size
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Calico IPAM allocates in blocks of 64 addresses by default (/26 IPv4, /122 IPv6). Allowed values: IPv4 20 to 32, IPv6 116 to 128. Lower the number to expand blocks, raise it to shrink them. You may have only one default IP pool per protocol in the installation manifest (two IPv4 pools there is invalid).

`blockSize` cannot be edited after install, so the best practice is to set it before installation. Otherwise replace the pool, ordering the steps to limit disruption (pods may lose connectivity when redeployed and external connectivity while in the temporary pool):

1. Create a temporary pool that does not overlap the existing one:
   ```yaml
   apiVersion: projectcalico.org/v3
   kind: IPPool
   metadata:
     name: temporary-pool
   spec:
     cidr: 10.0.0.0/16
     ipipMode: Always
     natOutgoing: true
   ```
   apply with `calicoctl apply -f temporary-pool.yaml`.
2. Disable the existing pool (blocks only new allocations): `calicoctl patch ippool default-ipv4-ippool -p '{"spec": {"disabled": true}}'`.
3. Delete pods from the existing pool, and check new pods get addresses from the temporary pool. `kubectl delete pod -A --all` restarts everything but is disruptive.
4. Delete the existing pool with `calicoctl delete ippool default-ipv4-ippool`.
5. Create the pool again with the desired size, for example `blockSize: 28`.
6. Disable the temporary pool, delete its pods, then delete it.

Confirm state at each step with `calicoctl get ippool -o wide`. Calico IPAM must be in use; verify first.

## Checked

2026-11-04. Block size ranges, the one-default-per-protocol rule, YAML and the step order were confirmed on the Change IP pool block size page.

Method: documentation only; no commands were run.
