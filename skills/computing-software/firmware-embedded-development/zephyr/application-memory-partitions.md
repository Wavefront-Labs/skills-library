---
id: computing-software.firmware-embedded-development.zephyr.application-memory-partitions
name: application-memory-partitions
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [app-memory-partition, k-appmem-partition-define, k-app-dmem, k-app-bmem, app-smem, zephyr-libc-partition, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Place Zephyr userspace data in application memory partitions with K_APPMEM_PARTITION_DEFINE, K_APP_DMEM/BMEM and per-library placement in CMake, then add them to domains."
sources:
  - https://docs.zephyrproject.org/latest/kernel/usermode/memory_domain.html
  - https://docs.zephyrproject.org/latest/kernel/usermode/overview.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Application memory partitions

With `CONFIG_USERSPACE=y`, the build collects variables tagged for a partition into one
contiguous block and defines a partition (base address and size) that covers it. Automatic
partitions are read-write regions only.

## Define and tag
```c
#include <zephyr/app_memory/app_memdomain.h>

K_APPMEM_PARTITION_DEFINE(sensor_part);

K_APP_DMEM(sensor_part) struct cfg sensor_cfg = { .rate = 50 };   /* .data: initialised */
K_APP_BMEM(sensor_part) int16_t samples[512];                     /* .bss: zeroed */
```
The build logic is `scripts/build/gen_app_partitions.py`; it coalesces the tagged globals into
one block and zeroes the BSS variables at boot.

## Whole libraries into a partition
In CMake, assign every global of a library to a partition without editing its source:
```cmake
zephyr_library_named(sensor_algo)
zephyr_library_sources(algo.c)
zephyr_library_app_memory(sensor_part)
```

## Domains
```c
static struct k_mem_domain sensor_dom;

void setup_domain(k_tid_t t)
{
    struct k_mem_partition *parts[] = {
        &sensor_part,
#if Z_LIBC_PARTITION_EXISTS
        &z_libc_partition,         /* libc globals: errno, stdio state */
#endif
#if Z_MALLOC_PARTITION_EXISTS
        &z_malloc_partition,       /* malloc arena, if user threads use malloc */
#endif
    };
    k_mem_domain_init(&sensor_dom, ARRAY_SIZE(parts), parts);
    k_mem_domain_add_thread(&sensor_dom, t);
}
```
A thread belongs to one domain (by default `k_mem_domain_default`; adding it to another domain
removes it from the old one, and a child thread inherits its parent's domain). Several threads can
share a domain; the same partition can be listed in several domains for shared buffers.

## Partition limits
- The number of partitions per domain is bounded by `CONFIG_MAX_DOMAIN_PARTITIONS` and by the
  memory-protection hardware; keep it small.
- Many MPU-based systems require partitions sized to a power of two and aligned to their own
  size; on MMU systems a partition must be page-aligned and a multiple of the page size.
- Partitions in one domain must not overlap. Attributes are architecture-specific (listed in
  `include/zephyr/arch/<arch>/arch.h`), for example `K_MEM_PARTITION_P_RW_U_RW` (almost always
  the right choice) and `K_MEM_PARTITION_P_RW_U_RO`.

## Debugging
- A user-mode fault on a global means that global is not in a partition of the thread's domain.
- `build/zephyr/zephyr.map` shows where the partition sections landed and their sizes.

## Verify
- [ ] Every global a user thread touches is in a partition of its domain.
- [ ] Partition sizes reviewed in the map (alignment padding acceptable).

## Checked

Checked 2026-10-25 against the Zephyr documentation source (main, latest release v4.4.2), doc/kernel/usermode/memory_domain.rst and include/zephyr/app_memory.
Confirmed: `K_APPMEM_PARTITION_DEFINE`, `K_APP_DMEM`/`K_APP_BMEM` usage; `scripts/build/gen_app_partitions.py`; `zephyr_library_app_memory`; `k_mem_domain_default` and thread/domain membership rules; `z_libc_partition`/`z_malloc_partition` and the `Z_LIBC_PARTITION_EXISTS`/`Z_MALLOC_PARTITION_EXISTS` macros (include/zephyr/sys/libc-hooks.h); power-of-two (MPU) and page (MMU) alignment; `CONFIG_MAX_DOMAIN_PARTITIONS`.

Method: documentation only; no commands were run.
