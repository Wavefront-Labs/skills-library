---
id: computing-software.firmware-embedded-development.zephyr.memory-domains-and-partitions
name: memory-domains-and-partitions
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [zephyr-userspace, memory-domain, k-appmem-partition-define, k-app-dmem, user-mode-threads, mpu-regions, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Isolate Zephyr user-mode threads with memory domains and app partitions: defining partitions, placing data, starting a K_USER thread, and MPU region limits."
sources:
  - https://docs.zephyrproject.org/latest/kernel/usermode/memory_domain.html
  - https://docs.zephyrproject.org/latest/kernel/usermode/overview.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Memory domains and partitions

With `CONFIG_USERSPACE=y`, threads created with `K_USER` run unprivileged and can access only
their own stack plus the partitions of their **memory domain**. A bug or exploit in a
parser thread then can't scribble over the rest of the system.

## Define partitions and place data
```c
#include <zephyr/app_memory/app_memdomain.h>

K_APPMEM_PARTITION_DEFINE(parser_part);
K_APP_DMEM(parser_part) int parse_count = 0;          /* initialised data */
K_APP_BMEM(parser_part) uint8_t parse_buf[512];        /* zero-initialised (bss) */
```
The build collects these into aligned linker sections (`gen_app_partitions.py`). Plain globals
stay kernel-only.

## Build the domain and start the thread
```c
static struct k_mem_domain parser_dom;
K_THREAD_STACK_DEFINE(parser_stack, 2048);
static struct k_thread parser_thread;

void start_parser(void)
{
    struct k_mem_partition *parts[] = { &parser_part, &z_libc_partition };
    k_mem_domain_init(&parser_dom, ARRAY_SIZE(parts), parts);

    k_tid_t tid = k_thread_create(&parser_thread, parser_stack,
                                  K_THREAD_STACK_SIZEOF(parser_stack),
                                  parser_entry, NULL, NULL, NULL,
                                  5, K_USER, K_FOREVER);      /* created but not started */
    k_mem_domain_add_thread(&parser_dom, tid);
    k_object_access_grant(&rx_msgq, tid);                     /* kernel objects it may use */
    k_thread_start(tid);
}
```
Creating the thread with a `K_FOREVER` delay lets you add it to the domain and grant objects
before `k_thread_start`. `k_mem_domain_add_thread` removes the thread from any domain it was
already in; a child thread joins its parent's domain.
- `z_libc_partition` holds globals required by the C library and runtime (needed with the Minimal C
  library or Newlib, and when `CONFIG_STACK_CANARIES` is enabled); `z_malloc_partition` is the
  system-wide pool behind libc `malloc()` (the docs recommend per-domain `sys_heap` objects instead).
  Using mbedTLS from user mode needs `k_mbedtls_partition`. Library partitions are listed in
  `include/zephyr/app_memory/partitions.h`.
- A privileged thread can drop to user mode in place with `k_thread_user_mode_enter()`.

## MPU limits (the practical constraint)
- A partition must be something the memory-management hardware can program. The MPU has a fixed
  number of regions, so the number of partitions per domain is limited (`CONFIG_MAX_DOMAIN_PARTITIONS`).
  `k_mem_domain_init` returns `-EINVAL` when `num_parts` exceeds the maximum and
  `k_mem_domain_add_partition` returns `-ENOSPC` when no free slot is left; check the return codes.
- Partitions in one domain may not overlap, and the same partition may belong to several domains
  (shared memory).
- Many MPUs need power-of-two sizes aligned to their own size (Arm v6-M/v7-M with user mode set
  `CONFIG_MPU_REQUIRES_POWER_OF_TWO_ALIGNMENT`); a 520-byte partition then occupies 1 KiB. MMU
  systems need page alignment and a multiple of the page size. Group data into few partitions.

## Access faults
A user thread touching memory outside its stack and domain partitions causes a memory-protection
fault, which is handled as a fatal error; `k_sys_fatal_error_handler()` is the hook that decides
what happens next. That is the feature working; log it and restart the component.

## Verify
- [ ] A deliberate out-of-domain write from the user thread faults and is contained.
- [ ] Partition count fits the MPU's free regions on every target board.
- [ ] `build/zephyr/zephyr.map` shows partition sections with expected sizes (check padding waste).

## Checked

Checked 2026-10-26 against the Zephyr documentation and sources on the main branch (repository head 2026-10-25; latest release v4.4.2).
- Partition constraints, `K_APPMEM_PARTITION_DEFINE`, `K_APP_DMEM` / `K_APP_BMEM`, pre-defined partitions,
  `k_mem_domain_init/add_partition/add_thread/remove_partition`, `CONFIG_MAX_DOMAIN_PARTITIONS`, child inheritance
  (doc: kernel/usermode/memory_domain); power-of-two rule (doc: kernel/usermode/mpu_stack_objects).
- `-EINVAL` / `-ENOSPC` returns (`kernel/userspace/mem_domain.c`).
- Removed: the 8-region Cortex-M example, the ARMv8-M 32-byte granularity statement and the "or an assert" outcome
  (no source); libc names reworded to the documented conditions.

Method: documentation only; no commands were run.
