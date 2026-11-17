---
id: computing-software.firmware-embedded-development.zephyr.kernel-object-permissions
name: kernel-object-permissions
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [zephyr-userspace, kernel-object-permissions, k-object-access-grant, k-thread-access-grant, dynamic-objects, syscall-verification, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Grant Zephyr user-mode threads access to semaphores, queues and devices: static and runtime grants, inheritance, dynamic objects, and reading syscall permission failures."
sources:
  - https://docs.zephyrproject.org/latest/kernel/usermode/kernelobjects.html
  - https://docs.zephyrproject.org/latest/kernel/usermode/syscalls.html
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/kernel/userspace/userspace.c
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kernel object permissions

User threads reach kernel objects only through system calls, and each syscall checks that the
calling thread has **permission** on the object and that the object is valid and initialised.

## What counts as a kernel object
Semaphores, mutexes, message queues, pipes, stacks, threads, thread stacks, timers, events,
and device driver instances. For a user thread to use one through a system call it must be a
top-level global (static scope is fine), located in kernel memory (not in a user-accessible
partition), used exclusively for that object (not a union member). The post-build script
`gen_kobject_list.py` scans the ELF and builds the table that validates object pointers. Objects
that do not meet these conditions are left out of the table; supervisor-only objects have no such
restrictions.

## Granting
```c
K_SEM_DEFINE(data_ready, 0, 1);
K_MSGQ_DEFINE(rx_msgq, sizeof(msg_t), 8, 4);

/* run time, on a thread created with K_FOREVER and started afterwards */
k_object_access_grant(&rx_msgq, tid);
k_thread_access_grant(tid, &data_ready, &rx_msgq, uart_dev);   /* expands to one grant per object */
```
`K_THREAD_ACCESS_GRANT(name, ...)` grants objects at boot to a thread declared with `K_THREAD_DEFINE`.
Note that the header states threads defined with `K_THREAD_DEFINE` run in kernel mode only and
cannot be turned into user threads, so user threads are created with `k_thread_create` (a
`K_THREAD_STACK_DEFINE` stack and the `K_USER` option).
A user caller of `k_object_access_grant` needs permission on both the object and the target thread.

- `K_INHERIT_PERMS` option on thread creation: the child gets the permissions of the parent on all
  kernel objects, except the parent thread object itself. Convenient but defeats least privilege;
  prefer explicit grants.
- `k_object_access_revoke(obj, tid)` is supervisor-only; a user thread drops its own permission
  with `k_object_release(obj)`. `k_object_access_all_grant(obj)` makes an object public to every
  thread, current and future: use with caution.
- Supervisor threads can access any kernel object; their permissions are still tracked, because
  they matter for `k_thread_user_mode_enter` and `K_INHERIT_PERMS`.
- Setting permissions on an untracked object is a no-op from supervisor mode and a fatal error for
  the calling thread from user mode.

## Dynamic objects
```
CONFIG_DYNAMIC_OBJECTS=y
```
```c
struct k_sem *s = k_object_alloc(K_OBJ_SEM);   /* also callable from user mode */
k_sem_init(s, 0, 1);
```
Allocated from the calling thread's resource pool; the creating thread gets permission; freed when
no thread holds permission (via `k_object_release` or thread termination) or explicitly by a
supervisor thread with `k_object_free`. See the dynamic-kernel-objects skill for sizing.

## Diagnosing failures
A failed check logs one of these messages (from `kernel/userspace/userspace.c`) and raises a kernel oops:
```
thread <ptr> (<index>) does not have permission on <type> <ptr>      (missing grant)
<ptr> is not a valid <type>                                          (wrong type or untracked)
address is not a known kernel object                                 (not in the object table)
<ptr> used before initialization                                     (never initialised)
<ptr> <type> in use                                                  (object busy)
```
Match the object address against the build's symbol map, then add the grant. "Not a known
kernel object" means the object was left out of the table (stack-allocated, in a user partition,
or not a top-level global).

## Verify
- [ ] Each user thread has an explicit grant list documented next to its definition.
- [ ] Removing one grant in a test build produces the expected access-denied oops.
- [ ] Devices used from user mode are granted (common miss with sensor and GPIO APIs).

## Checked

Checked 2026-10-26 against the Zephyr documentation and sources on the main branch (repository head 2026-10-25; latest release v4.4.2).
- Object table conditions, supervisor access, `K_INHERIT_PERMS`, `k_object_access_grant` / `revoke` / `release` /
  `all_grant`, dynamic allocation and untracked-object behaviour (doc: kernel/usermode/kernelobjects;
  `include/zephyr/sys/kobject.h`).
- The error strings (`kernel/userspace/userspace.c`: `dump_permission_error`, `k_object_dump_error`).
- Wrong in the draft: the `K_THREAD_DEFINE(... K_USER ...)` example (the `kernel.h` header says `K_THREAD_DEFINE` threads
  run in kernel mode only); invented log text `k_sem_take: object ... access denied`; "allocated from the system heap"
  (docs say the calling thread's resource pool).

Method: documentation only; no commands were run.
