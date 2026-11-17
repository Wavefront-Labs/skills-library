---
id: computing-software.firmware-embedded-development.device-driver-development.kmalloc-and-gfp-flags
name: kmalloc-and-gfp-flags
category: computing-software
field: firmware-embedded-development
product: device-driver-development
tags: [kmalloc, linux-kernel-module, gfp-flags, devm-kzalloc, dma-coherent, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Allocate memory in Linux drivers correctly: kmalloc/kzalloc vs vmalloc vs devm_ variants, GFP_KERNEL vs GFP_ATOMIC by context, DMA-able buffers, and leak/overflow detection."
sources:
  - https://docs.kernel.org/core-api/memory-allocation.html
  - https://docs.kernel.org/core-api/dma-api-howto.html
  - https://docs.kernel.org/dev-tools/kmemleak.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kmalloc and GFP flags

## Allocators
| API | Use |
|---|---|
| `kzalloc(size, gfp)` / `kmalloc` | small to medium, physically contiguous; limited by `KMALLOC_MAX_SIZE`, and large orders may fail on fragmented systems |
| `kcalloc(n, size, gfp)` / `kmalloc_array` | arrays with overflow-checked size multiplication |
| `kvmalloc` | large buffers that need not be physically contiguous (falls back to vmalloc) |
| `devm_kzalloc(dev, size, GFP_KERNEL)` | per-device state freed automatically on driver detach or probe failure |
| `dma_alloc_coherent(dev, size, &dma_handle, gfp)` | buffers shared with a DMA engine (coherent mapping) |
| `kmem_cache_create` + `kmem_cache_alloc` | many same-size objects (descriptors) |

## GFP flags by context
- `GFP_KERNEL`: may sleep and reclaim. Default in probe, file operations, workqueues, threaded IRQs.
- `GFP_ATOMIC`: never sleeps, may dip into reserves, more likely to fail. Required in hard IRQ,
  softirq/tasklet, timers, and while holding a spinlock.
- `GFP_NOWAIT`: no sleep, no reserves (fail fast).
- `GFP_DMA`/`GFP_DMA32`: zone restrictions for devices with limited addressing; prefer setting
  the device DMA mask (`dma_set_mask_and_coherent`) and using the DMA API.
- `__GFP_NOWARN`: suppress the allocation-failure splat when you handle failure gracefully.
Always check for NULL; `GFP_ATOMIC` failures are normal under memory pressure.

## DMA buffers
`kmalloc` memory is physically contiguous and can be mapped with `dma_map_single()`. Stack
memory and `vmalloc` memory are **not** DMA-safe (DMA-API-HOWTO):
SPI/I2C controller drivers that DMA will corrupt or crash with on-stack buffers passed to
`spi_sync`. Use `kmalloc`ed buffers (or `____cacheline_aligned` members of a kmalloc'ed struct).

## devm and lifetime
`devm_` memory lives until the device is unbound, not until the last file handle closes. If
userspace can still hold the char device open after unbind, objects referenced by the open file
must be refcounted (`kref`) and freed on last release, not devm-managed.

## Debugging
`CONFIG_KASAN` (out-of-bounds and use-after-free), `CONFIG_DEBUG_KMEMLEAK`
(`echo scan > /sys/kernel/debug/kmemleak`), `CONFIG_SLUB_DEBUG` with the `slub_debug=` boot option,
`/proc/slabinfo` and `slabtop` for growth.

## Verify
- [ ] Each allocation's GFP flag matches its context (review against call sites; DEBUG_ATOMIC_SLEEP catches GFP_KERNEL in atomic context).
- [ ] KASAN and kmemleak clean after probe/remove cycles (`echo <dev> > unbind/bind` loops).

## Checked

2026-10-26, Linux kernel documentation tree and headers (mainline, v7.3 tag, checked 2026-10-26).
Confirmed in Documentation/core-api/memory-allocation.rst: GFP_KERNEL default, GFP_NOWAIT for no direct reclaim, GFP_ATOMIC for contexts that cannot sleep, GFP_DMA/GFP_DMA32 are legacy and dma_alloc* is preferred, kcalloc/kmalloc_array, KMALLOC_MAX_SIZE limit, kvmalloc falling back to vmalloc. Confirmed in Documentation/core-api/dma-api-howto.rst: no DMA from vmalloc or stack memory, dma_mapping_error check. Confirmed in Documentation/dev-tools/kmemleak.rst: CONFIG_DEBUG_KMEMLEAK and echo scan to the debugfs file. Removed as unconfirmed: the "often 4 MB" size, the ARCH_DMA_MINALIGN statement and the specific slub_debug=FZPU flag string.

Method: documentation only; no commands were run.
