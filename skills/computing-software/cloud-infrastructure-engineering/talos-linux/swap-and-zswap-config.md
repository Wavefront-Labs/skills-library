---
id: computing-software.cloud-infrastructure-engineering.talos-linux.swap-and-zswap-config
name: swap-and-zswap-config
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [swapvolumeconfig, zswapconfig, swap, kubelet, limitedswap, sysctl, swappiness, cgroups]
level: advanced
status: docs-checked
description: "Enable swap and zswap on Talos: encrypted SwapVolumeConfig, ZswapConfig pool size, kubelet LimitedSwap, swappiness and page-cluster sysctls, and talosctl cgroups."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/configure-your-talos-cluster/storage-and-disk-management/swap.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Swap and zswap are disabled by default in Talos. Swap extends memory by moving inactive pages to disk (and can free RAM for caches) but excessive use hurts performance; zswap is a compressed in-memory cache for swap pages and requires swap to be enabled. Swap holds memory pages, so encrypt it, and prefer a separate disk from the system disk.

```yaml
apiVersion: v1alpha1
kind: SwapVolumeConfig
name: swap1
provisioning:
    diskSelector:
        match: 'disk.transport == "nvme"'
    minSize: 4GiB
    maxSize: 4GiB
encryption:
    provider: luks2
    keys:
        - slot: 0
          tpm: {}
        - slot: 1
          static:
            passphrase: topsecret
```

Talos provisions the partition, labels it `s-swap1`, encrypts and enables it. Check with `talosctl -n 172.20.0.5 get swap`. Removing the document disables the device but leaves the partition; free it with `talosctl wipe disk nvme0n2p2 --drop-partition`.

Zswap:

```yaml
apiVersion: v1alpha1
kind: ZswapConfig
maxPoolPercent: 20
```

Check with `talosctl -n 172.20.0.5 get zswapstatus`; deleting the document disables it.

Kubernetes does not let containers use swap by default. At minimum enable it in the kubelet:

```yaml
apiVersion: v1alpha1
kind: KubeletConfig
config:
  memorySwap:
    swapBehavior: LimitedSwap
```

View per-cgroup usage with `talosctl cgroups --preset=swap`; `SwapMax` of `0 B` means swap is off for that cgroup. Tuning via `SysctlConfig`: `vm.swappiness: "130"` (default 60, more aggressive on fast NVMe) and `vm.page-cluster: "0"` (default 3 reads 8 pages; 0 disables swap read-ahead on non-rotational media).

## Checked

2026-11-04. SwapVolumeConfig and ZswapConfig YAML, status commands, kubelet LimitedSwap patch, cgroups preset and sysctl descriptions confirmed on the Swap page.

Method: documentation only; no commands were run.
