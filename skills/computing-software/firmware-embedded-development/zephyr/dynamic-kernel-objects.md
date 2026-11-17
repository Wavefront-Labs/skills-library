---
id: computing-software.firmware-embedded-development.zephyr.dynamic-kernel-objects
name: dynamic-kernel-objects
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [dynamic-kernel-objects, k-object-alloc, k-object-release, config-dynamic-objects, k-thread-create-dynamic-stack, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Allocate Zephyr kernel objects and thread stacks at runtime with CONFIG_DYNAMIC_OBJECTS and dynamic thread stacks: k_object_alloc, permissions, release, and pool sizing."
sources:
  - https://docs.zephyrproject.org/latest/kernel/usermode/kernelobjects.html
  - https://docs.zephyrproject.org/latest/kernel/services/threads/index.html
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/sys/kobject.h
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/kernel/Kconfig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dynamic kernel objects

With userspace enabled, the kernel validates kernel object pointers from user mode against a table
generated at build time from statically defined objects (post-build script `gen_kobject_list.py`).
Objects created at runtime are tracked through dynamic objects.

```
CONFIG_USERSPACE=y
CONFIG_DYNAMIC_OBJECTS=y
CONFIG_HEAP_MEM_POOL_SIZE=4096     # backs k_malloc and the system heap; objects come from the calling thread's resource pool
```

## Allocate from supervisor or user mode
```c
struct k_sem *s = k_object_alloc(K_OBJ_SEM);     /* syscall; usable from user threads */
if (!s) return -ENOMEM;
k_sem_init(s, 0, 1);
k_object_access_grant(s, worker_tid);            /* creator gets permission automatically */

```
- `k_object_alloc_size(type, size)` exists for objects whose size varies, such as thread stacks.
- Objects allocated with `k_object_alloc` implicitly grant permission to the calling thread.
- Permissions double as references: when an object loses all references (no thread has permission)
  it is freed automatically. User threads drop theirs with `k_object_release(obj)`, and permissions
  are cleared when a thread terminates.
- Supervisor threads may call `k_object_free(obj)` to force a dynamic object to be released.

## Dynamic thread stacks
```
CONFIG_DYNAMIC_THREAD=y                # experimental; needs CONFIG_THREAD_STACK_INFO
CONFIG_DYNAMIC_THREAD_ALLOC=y          # stacks and thread objects from the system heap
CONFIG_DYNAMIC_THREAD_POOL_SIZE=4      # and/or a fixed pool pre-allocated at build time
CONFIG_DYNAMIC_THREAD_STACK_SIZE=2048  # size of each pooled stack (maximum size for pool stacks)
```
`CONFIG_DYNAMIC_THREAD_PREFER_ALLOC` / `_PREFER_POOL` choose which source is tried first.
```c
static struct k_thread th;
k_thread_stack_t *stk = k_thread_stack_alloc(CONFIG_DYNAMIC_THREAD_STACK_SIZE, K_USER);
k_thread_create(&th, stk, CONFIG_DYNAMIC_THREAD_STACK_SIZE, entry, NULL, NULL, NULL,
                5, K_USER, K_NO_WAIT);
/* after the thread exits */
k_thread_join(&th, K_FOREVER);
k_thread_stack_free(stk);
```

## Without userspace
If `CONFIG_USERSPACE=n`, kernel objects are plain structs: allocate them with `k_malloc` or
embed them in your structs and call the `k_*_init` functions. `k_object_alloc` is only needed
when userspace tracks objects.

## Design advice
- Prefer static objects (`K_*_DEFINE`): deterministic RAM, no allocation failures, smaller
  permission tables.
- Use dynamic objects for user-mode subsystems that create per-session resources (connections,
  plug-in modules) and size the heap from measured peaks.
- Permissions are reference counts, so supervisor threads should hold permissions on objects they use
  and every allocation path needs a matching release.

## Verify
- [ ] Allocation failures handled (`NULL` from `k_object_alloc`).
- [ ] Heap usage returns to baseline after creating and destroying N objects/threads.

## Checked

Checked 2026-10-26 against the Zephyr documentation and sources on the main branch (repository head 2026-10-25; latest release v4.4.2).
- Dynamic object allocation from the thread's resource pool, automatic free at zero references, `k_object_release`,
  supervisor-only `k_object_free`, implicit grant (doc: kernel/usermode/kernelobjects); `k_object_alloc_size` purpose
  (`include/zephyr/sys/kobject.h`).
- `CONFIG_DYNAMIC_THREAD*` options, defaults and the EXPERIMENTAL marker (`kernel/Kconfig`); `k_thread_stack_alloc`
  flags and stack-free pairing (`kernel.h`, doc: threads).
- Wrong in the draft: `k_object_alloc_size(K_OBJ_PIPE, ...)` (pipes no longer need it; the header says stacks do) and the
  user-mode `k_object_alloc(K_OBJ_THREAD)` thread example, which no document shows; `DYNAMIC_THREAD` is experimental.

Method: documentation only; no commands were run.
