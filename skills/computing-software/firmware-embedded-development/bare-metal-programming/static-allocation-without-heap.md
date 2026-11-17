---
id: computing-software.firmware-embedded-development.bare-metal-programming.static-allocation-without-heap
name: static-allocation-without-heap
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [no-dynamic-memory, static-allocation, misra-dir-4-12, misra-rule-21-3, memory-pool, malloc-free, fragmentation, safety-critical, firmware-embedded-development]
level: practitioner
status: draft
description: "Build firmware with no heap per MISRA Dir 4.12/Rule 21.3: static objects, fixed-block pools, init-time-only allocation, banning malloc at link time, and RTOS static APIs."
sources:
  - https://www.misra.org.uk/misra-c/
  - https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation
  - https://barrgroup.com/embedded-systems/books/embedded-c-coding-standard
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# No dynamic memory (Directive 4.12)

**Goal:** firmware whose memory use is fully known at link time: no fragmentation, no
out-of-memory at month six, no nondeterministic allocation time.

## The rules
- MISRA C:2012 **Directive 4.12**: dynamic memory allocation shall not be used.
- **Rule 21.3**: `malloc`, `calloc`, `realloc`, `free` from `<stdlib.h>` shall not be used.
- Many safety standards (IEC 61508, DO-178C practice) expect the same or allocation only
  during initialisation.

## Techniques
- **Static objects** sized for the worst case, owned by the module that uses them:
  `static uint8_t rx_buf[RX_LEN];` - the map file now shows the real RAM budget.
- **Fixed-block pools** when objects come and go (messages, packets): N blocks of one size,
  O(1) alloc/free from a free list, no fragmentation, exhaustion is a detectable design
  error.
```c
#define POOL_N 16
static msg_t pool[POOL_N]; static msg_t *free_list;
void pool_init(void) { for (int i = 0; i < POOL_N - 1; i++) pool[i].next = &pool[i + 1]; pool[POOL_N-1].next = NULL; free_list = pool; }
msg_t *msg_alloc(void) { uint32_t s = cs_enter(); msg_t *m = free_list; if (m) free_list = m->next; cs_exit(s); return m; }
void msg_free(msg_t *m) { uint32_t s = cs_enter(); m->next = free_list; free_list = m; cs_exit(s); }
```
- **Init-time-only allocation**: a bump allocator usable until `system_started = true`,
  then it asserts. Acceptable under many deviation policies.
- **RTOS static APIs**: FreeRTOS `configSUPPORT_DYNAMIC_ALLOCATION 0` with
  `xTaskCreateStatic`, `xQueueCreateStatic`; Zephyr `K_THREAD_DEFINE`, `K_MSGQ_DEFINE`.

## Enforce it, do not trust it
- Link without a heap: set heap size 0 in the linker script and make `_sbrk` fail or not
  exist; any accidental `malloc` (including from `printf`, `strdup`, C++ `new`,
  `std::vector`) shows up as a link error or immediate failure.
- `-Wl,--wrap=malloc` with a `__wrap_malloc` that calls `assert(0)`, or `nm` in CI to
  reject `malloc` in the final symbol table.
- newlib's stdio allocates buffers lazily - use a custom printf or pre-set buffers with
  `setvbuf`.

## Trade-offs
Worst-case sizing costs RAM; pools of a few sizes (e.g. 32/128/512 bytes) give flexibility.
Stack is still dynamic: measure it (stack painting, `-fstack-usage`) as part of the same
discipline. VLAs and `alloca` are dynamic too (MISRA Rule 18.8 bans VLAs).

## Verify
- [ ] `arm-none-eabi-nm app.elf | grep -E ' (malloc|free|_sbrk)$'` is empty (or only the trap).
- [ ] Pool high-water marks logged under stress stay below capacity.
