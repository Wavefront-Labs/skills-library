---
id: computing-software.firmware-embedded-development.zephyr.userspace-fault-troubleshooting
name: userspace-fault-troubleshooting
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [userspace-fault, mpu-fault, k-err-kernel-oops, syscall-verification-failure, permission-denied-object, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Diagnose Zephyr userspace failures: MPU faults on globals, syscall oopses for ungranted kernel objects or bad buffers, stack overflows in user threads, and reading the fault dump."
sources:
  - https://docs.zephyrproject.org/latest/kernel/usermode/overview.html
  - https://docs.zephyrproject.org/latest/kernel/usermode/syscalls.html
  - https://docs.zephyrproject.org/latest/kernel/services/other/fatal.html
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/kernel/userspace/userspace.c
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Userspace fault troubleshooting

Enable first:
```
CONFIG_ASSERT=y
CONFIG_LOG=y
CONFIG_EXCEPTION_STACK_TRACE=y
CONFIG_THREAD_NAME=y
```

## 1. MPU / memory fault from a user thread
```
***** MPU FAULT *****
  Data Access Violation
  MMFAR Address: 0x20001234
Current thread: 0x20000a40 (app)
```
(Cortex-M wording from `arch/arm/core/cortex_m/fault.c`; other architectures print their own dumps.)
Look up the address in `zephyr.map`:
- In another module's `.bss`/`.data`: the variable isn't in a partition of the thread's domain.
  Tag it with `K_APP_BMEM/DMEM(part)` or `zephyr_library_app_memory()`.
- In libc data (`errno`, `_impure_ptr`, malloc arena): add `z_libc_partition` /
  `z_malloc_partition` to the domain.
- In a peripheral range: user code touching registers directly; move into a driver/syscall.
- Near the thread's stack bottom: stack overflow (see 3).
- In a library's data: see the pre-defined partitions `z_libc_partition`, `z_malloc_partition`, `k_mbedtls_partition`.

## 2. Kernel oops from a syscall
The syscall verification layer (`z_vrfy_*`, using `K_OOPS(...)`) rejected an argument and the kernel
raises a fatal error with reason `K_ERR_KERNEL_OOPS`. The log lines come from `kernel/userspace/userspace.c`:
| Message | Fix |
|---|---|
| `thread <ptr> (<n>) does not have permission on <type> <ptr>` | `k_thread_access_grant(tid, &obj)` before start, or `K_INHERIT_PERMS` |
| `<ptr> is not a valid <type>` / `address is not a known kernel object` | object not in the kernel object table: top-level global in kernel memory, defined with `K_*_DEFINE`, or allocated with `k_object_alloc` |
| `<ptr> used before initialization` | object never initialised (supervisor must call the init function or `k_object_init` for private static initialisers) |
| `<ptr> <type> in use` | object busy |
| buffer pointer rejected | the caller lacks read or write permission on the buffer: place it in the thread's partition or stack |
| device denied | grant the `struct device` (`DEVICE_DT_GET(...)`) to the thread |

What happens next is decided by `k_sys_fatal_error_handler()`; a user thread cannot call `k_panic()`
(it becomes an oops).

## 3. Stack overflow in user mode
In user mode, overflows are always caught because the thread has no write permission outside its stack.
The fatal error reads `Stack overflow` (reason `K_ERR_STACK_CHK_FAIL`) or shows as an MPU fault just below
the stack. Increase the stack size, check with the thread analyzer, and remember TLS.
On MPU systems each user thread also has a privileged stack that system calls switch to; supervisor-mode
overflow (including while handling a system call) is caught only with `CONFIG_HW_STACK_PROTECTION`.

## 4. Builds that fault immediately
- User thread stack defined with a plain array or `K_KERNEL_STACK_DEFINE`.
- Too many partitions for the domain: `k_mem_domain_add_partition` returns `-ENOSPC` and
  `k_mem_domain_init` returns `-EINVAL` (check return codes).

## Verify
- [ ] Each fault type reproduced once deliberately so the team recognises the dumps.
- [ ] All grant/domain calls check return values.

## Checked

Checked 2026-10-26 against the Zephyr documentation and sources on the main branch (repository head 2026-10-25; latest release v4.4.2).
- Fault strings: `***** MPU FAULT *****`, `Data Access Violation`, `MMFAR Address` (`arch/arm/core/cortex_m/fault.c`);
  `Stack overflow` reason and `Current thread:` (`kernel/fatal.c`); permission / validity / initialisation / in-use
  messages (`kernel/userspace/userspace.c`); `K_OOPS` use in `z_vrfy_*` handlers (doc: kernel/usermode/syscalls);
  `K_ERR_KERNEL_OOPS`, user-mode `k_panic` becomes an oops, user-mode overflow always caught (doc: kernel/services/other/fatal).
- `-ENOSPC` / `-EINVAL` from the memory-domain API (`kernel/userspace/mem_domain.c`); pre-defined partitions (doc: memory_domain).
- Wrong or removed: invented `access denied` / `Kernel OOPS!` / `Stack Check Fail!` text, the `CONFIG_KERNEL_LOG_LEVEL_DBG`
  requirement (the messages use error-level logs), the `CONFIG_PRIVILEGED_STACK_SIZE` option and the claim that an
  oops always kills only the thread.

Method: documentation only; no commands were run.
