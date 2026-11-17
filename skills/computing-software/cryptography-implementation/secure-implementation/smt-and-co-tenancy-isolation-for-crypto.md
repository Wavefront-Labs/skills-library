---
id: computing-software.cryptography-implementation.secure-implementation.smt-and-co-tenancy-isolation-for-crypto
name: smt-and-co-tenancy-isolation-for-crypto
category: computing-software
field: cryptography-implementation
product: secure-implementation
tags: [secure-implementation, cryptography-implementation, smt-isolation, co-tenancy, core-scheduling, side-channel, hyperthreading, cache-attacks]
level: sme
status: draft
description: "Isolate crypto workloads from co-tenants: SMT/hyperthreading risks, core scheduling, dedicated hosts and cache partitioning to limit cross-tenant side channels."
sources: ["https://docs.kernel.org/admin-guide/hw-vuln/core-scheduling.html", "https://portsmash.github.io/", "https://docs.aws.amazon.com/whitepapers/latest/security-design-of-aws-nitro-system/the-ec2-approach-to-preventing-side-channels.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SMT and co-tenancy isolation for crypto

## Risks
- Sibling hyperthreads share execution ports, L1/L2 caches and buffers. PortSmash (2018) recovered OpenSSL P-384
  keys from a sibling thread; L1TF, MDS and Zenbleed leak data across siblings.
- Shared LLC across cores enables Prime+Probe and Flush+Reload on shared libraries (page dedup).

## Controls
1. **Dedicated hardware** for high-value keys: dedicated hosts/instances, HSMs, or bare metal.
2. **Cloud provider isolation**: major clouds do not share physical cores between tenants on the same SMT pair
   (AWS Nitro, GCP); burstable/shared-core instance types may differ; check documentation.
3. **Linux core scheduling** (5.14+): tag trusted processes so only processes with the same cookie share sibling
   threads:
   ```sh
   # prctl(PR_SCHED_CORE, PR_SCHED_CORE_CREATE, pid, PIDTYPE_TGID, 0) from a launcher
   ```
   Or disable SMT on key-holding hosts: `echo off > /sys/devices/system/cpu/smt/control` (`nosmt` boot option).
4. **Containers**: same kernel, same physical cores; container boundaries are not side-channel boundaries. Pin
   crypto services to cores not shared with untrusted workloads (cpusets) or move to VMs/dedicated nodes.
5. Disable memory deduplication (KSM, transparent page sharing) between tenants.
6. Intel CAT/AMD cache allocation can partition LLC ways for sensitive workloads.

## Verify
- [ ] Inventory states SMT/core-sharing posture for each key-holding service; kernel shows core scheduling or SMT off.
