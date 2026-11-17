---
id: computing-software.firmware-embedded-development.zephyr.thread-local-storage
name: thread-local-storage
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [thread-local-storage, config-thread-local-storage, thread-keyword, per-thread-errno, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Use C11 _Thread_local / __thread variables in Zephyr with CONFIG_THREAD_LOCAL_STORAGE: architecture support, stack cost, errno, userspace, and alternatives like custom data."
sources:
  - https://docs.zephyrproject.org/latest/kernel/services/other/thread_local_storage.html
  - https://docs.zephyrproject.org/latest/kernel/services/threads/index.html
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/kernel/Kconfig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Thread-local storage

```
CONFIG_THREAD_LOCAL_STORAGE=y
```
The option depends on architecture support (the hidden `CONFIG_ARCH_HAS_THREAD_LOCAL_STORAGE`) and on
toolchain support (`CONFIG_TOOLCHAIN_SUPPORTS_THREAD_LOCAL_STORAGE`); it is unavailable otherwise.

```c
static Z_THREAD_LOCAL uint32_t call_depth;    /* Zephyr's macro for thread-local variables */

void work(void) {
    call_depth++;                              /* each thread sees its own copy */
}
```

## How it works
- TLS variables are stored in the thread stack, so every thread has its own copy and the stack
  must be large enough to hold them; every thread pays for the TLS area, even if it never touches
  the variables.
- Toolchain support is required.

## errno
`CONFIG_ERRNO_IN_TLS` can be enabled together with `CONFIG_ERRNO` to make `errno` a thread-local
variable, which lets user threads read `errno` without a system call.

## Userspace
TLS lives on the thread's own stack, which a user thread can already access.

## Alternative: thread custom data
`CONFIG_THREAD_CUSTOM_DATA=y` lets each thread store one word of custom data (the Kconfig help says
32 bits) via `k_thread_custom_data_set()` / `k_thread_custom_data_get()`, which act on the calling
thread.

## Gotchas
- Large TLS arrays multiply by thread count; keep TLS small and put big buffers elsewhere.
- Stack sizes must be increased by the TLS size.

## Verify
- [ ] TLS size is small and accounted for in every thread's stack size.
- [ ] Two threads modifying the same TLS variable see independent values.

## Checked

Checked 2026-10-26 against the Zephyr documentation and sources on the main branch (repository head 2026-10-25; latest release v4.4.2).
- TLS stored in the thread stack, toolchain requirement, `Z_THREAD_LOCAL`, `CONFIG_ERRNO_IN_TLS` with `CONFIG_ERRNO`
  (doc: kernel/services/other/thread_local_storage); `CONFIG_THREAD_LOCAL_STORAGE`, `CONFIG_THREAD_CUSTOM_DATA` and
  the arch/toolchain dependency (`kernel/Kconfig`); `k_thread_custom_data_set/get` (`kernel.h`).
- Removed: the architecture list, `.tdata`/`.tbss` and thread-pointer register details, the ISR behaviour paragraph, the
  `__thread` / `_Thread_local` spellings and the whole-system-TLS remark (no source); the `ERRNO_IN_TLS` default.

Method: documentation only; no commands were run.
