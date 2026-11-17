---
id: computing-software.firmware-embedded-development.zephyr.user-mode-threads
name: user-mode-threads
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [user-mode-thread, k-user, k-thread-user-mode-enter, config-userspace, k-thread-stack-define, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Run untrusted or fault-isolated code in Zephyr user mode: create K_USER threads or drop privileges, grant kernel objects, give memory access, and call drivers via syscalls."
sources:
  - https://docs.zephyrproject.org/latest/kernel/usermode/overview.html
  - https://docs.zephyrproject.org/latest/kernel/usermode/kernelobjects.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# User mode threads

```
CONFIG_USERSPACE=y      # needs architecture support for memory protection (MPU or MMU)
```
A user thread runs unprivileged: it can only touch its own stack, memory partitions granted to
its domain, and kernel objects it has been granted. Kernel and driver calls go through system
calls that validate arguments.

## Create a user thread
```c
#define STACK 1024
K_THREAD_STACK_DEFINE(app_stack, STACK);     /* MPU-aligned stack, required for user threads */
static struct k_thread app_thread;

K_SEM_DEFINE(app_sem, 0, 1);
K_MSGQ_DEFINE(app_q, sizeof(struct msg), 8, 4);

void start_app(void)
{
    k_tid_t t = k_thread_create(&app_thread, app_stack, STACK, app_entry, NULL, NULL, NULL,
                                5, K_USER, K_FOREVER);          /* not started yet */
    k_thread_access_grant(t, &app_sem, &app_q, sensor_dev);     /* objects it may use */
    k_mem_domain_add_thread(&app_domain, t);                    /* memory it may touch */
    k_thread_start(t);
}
```
Or from a supervisor thread: `k_thread_user_mode_enter(entry, p1, p2, p3)`; it does not return.
Threads defined with `K_THREAD_DEFINE` run in kernel mode only and cannot make this transition.
`K_INHERIT_PERMS` gives a child all of the creator's object permissions except on the creator's own thread
object; user threads cannot be `K_ESSENTIAL`. Newly created threads inherit the creator's memory domain.

## Stack rules
- Use `K_THREAD_STACK_DEFINE` (or the array variant), never a plain array: the macros apply the
  alignment and size rounding the MPU needs (power of two where
  `CONFIG_MPU_REQUIRES_POWER_OF_TWO_ALIGNMENT` applies).
- `K_KERNEL_STACK_DEFINE` stacks are for supervisor threads only; `K_THREAD_STACK_DEFINE` stacks can
  host either. Exceeding the stack space generates a hardware fault.

## What user code may call
- Kernel and driver APIs declared with `__syscall` (for example `k_sem_*`, `k_msgq_*`, `k_sleep`).
  The syscall handlers validate the object type and permission, whether it is initialised, and
  read/write access to every buffer passed in.
- Driver APIs on devices it has been granted (`k_object_access_grant(dev, t)` or
  `k_thread_access_grant`); device instances are kernel objects.
All other RAM must be reached through system calls or a memory domain granted by a supervisor thread.

## Global variables
User threads can't read ordinary globals. Place shared data in an app memory partition:
```c
K_APPMEM_PARTITION_DEFINE(app_part);
K_APP_DMEM(app_part) int counter = 0;    /* initialised */
K_APP_BMEM(app_part) uint8_t buf[256];   /* zeroed */
```
Add `app_part` to a memory domain the thread belongs to. libc globals need `z_libc_partition`, and
the libc `malloc()` pool is `z_malloc_partition`, in the domain.

## Cost
Syscalls add a validation layer, and power-of-two stack rounding can waste RAM on MPUs that need it.
Measure before moving hot loops to user mode.

## Verify
- [ ] User thread created with `K_USER`, granted only the objects/devices it needs.
- [ ] Deliberate bad access from the thread produces a fault, not silent corruption.

## Checked

Checked 2026-10-26 against the Zephyr documentation and sources on the main branch (repository head 2026-10-25; latest release v4.4.2).
- User thread privileges, memory-domain inheritance, `K_INHERIT_PERMS` semantics, syscall validation duties, stack
  guarantee wording, `K_ESSENTIAL` not allowed for user threads (doc: kernel/usermode/overview and /syscalls;
  `kernel.h` comments on stack macros and `K_THREAD_DEFINE`).
- Wrong or removed: the architecture list for `CONFIG_USERSPACE`, the "Not allowed: irq_lock ..." line, the syscall cost
  figure, "static inline helpers" bullet and "one-way" wording (no source).

Method: documentation only; no commands were run.
