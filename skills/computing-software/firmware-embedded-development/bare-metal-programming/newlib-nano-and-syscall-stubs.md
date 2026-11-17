---
id: computing-software.firmware-embedded-development.bare-metal-programming.newlib-nano-and-syscall-stubs
name: newlib-nano-and-syscall-stubs
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [newlib-nano, newlib, syscalls, sbrk, nosys-specs, retarget-printf, write-syscall, malloc-lock, arm-none-eabi-gcc, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Use newlib-nano on bare metal: specs files, implementing write/read/sbrk stubs, printf float support via -u, heap limits, and malloc locking for threads."
sources:
  - https://sourceware.org/newlib/libc.html
  - https://sourceware.org/git/?p=newlib-cygwin.git;a=blob_plain;f=newlib/README
  - https://gcc.gnu.org/onlinedocs/gcc-14.2.0/gcc/Overall-Options.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# newlib-nano and syscall stubs

**Goal:** a small C library that links cleanly, routes `printf` to a UART/RTT, and has a heap
that cannot silently overrun the stack.

## Specs files
`-specs=file` makes GCC read an extra spec file after its standard one to override the driver's
defaults; several can be given and are processed left to right. Embedded toolchains can supply
ready-made spec files for a smaller C library, placeholder stubs or semihosting. Their contents
are toolchain-specific and not documented on the pages checked here, so read the files your
toolchain ships (or the link map) to see which C library variant and stubs each one selects.
Whichever you use, the rest of this skill applies: supply your own syscalls rather
than relying on placeholder stubs, and check the map file to see where each syscall symbol came from.

## What newlib needs from you
The newlib manual's "System Calls" chapter: on a bare-board system without an OS you at least
need do-nothing stubs (or minimal implementations) so the program links against `libc.a`. The
manual's list is `_exit`, `close`, `environ`, `execve`, `fork`, `fstat`, `getpid`, `isatty`,
`kill`, `link`, `lseek`, `open`, `read`, `sbrk`, `stat`, `times`, `unlink`, `wait` and `write`.
Its examples spell them without a leading underscore (except `_exit`); match the exact symbol your
link error reports (for example `undefined reference to _write`). Stubs that set `errno` must
`#include <errno.h>`, then `#undef errno` and declare `extern int errno;`, because newlib defines
`errno` as a macro over its reentrancy structure.

## Minimal syscalls.c
```c
#include <sys/stat.h>
#include <errno.h>
#undef errno
extern int errno;
extern char _end[], _heap_limit[];          /* _end from the GNU linker; _heap_limit from your script */
static char *heap_ptr = _end;

int _write(int fd, const char *buf, int len) { (void)fd; uart_write(buf, len); return len; }
int _read(int fd, char *buf, int len)        { (void)fd; return uart_read(buf, len); }
void *_sbrk(ptrdiff_t incr) {
    if (heap_ptr + incr > _heap_limit) { errno = ENOMEM; return (void *)-1; }
    char *prev = heap_ptr; heap_ptr += incr; return prev;
}
int _close(int fd) { return -1; }
int _fstat(int fd, struct stat *st) { st->st_mode = S_IFCHR; return 0; }  /* manual: treat every file as a character device */
int _isatty(int fd) { return 1; }
int _lseek(int fd, int ptr, int dir) { return 0; }
```
- The manual's `write` example sends each byte to an output routine (for example a serial port)
  and returns `len`; it notes libc uses `write` for all output including stdout.
- The manual's `sbrk` example starts at the linker-defined `_end` and compares against the stack
  pointer; it aborts on a collision. Bounding it with an explicit heap-limit symbol (leaving a
  stack reserve), as above, is this skill's variation. `sbrk` is what `malloc` calls to get space
  (`_sbrk_r` is called with a negative value to release space), so a working one matters.
- The manual's `fstat` and `stat` stubs return `S_IFCHR` ("all files are character special
  devices"), `isatty` returns 1, `lseek` returns 0, `close` returns -1.

## printf and float
- The newlib README documents `--enable-newlib-nano-formatted-io` (a size-reduced formatted I/O
  build). In that build floating-point support is split into weak functions that are not linked
  by default; to print or scan floats you must force them in with the linker `-u` option:
  `-u _printf_float` and/or `-u _scanf_float`. Float specifiers are still recognised without them,
  which the README says may give undefined behaviour. The nano build also supports only C89 formatted
  I/O, and computes with `double` internally.
- Whether your toolchain's nano library was built this way is a toolchain question; confirm by
  printing `%f` on hardware.
- Float conversion needs heap: the README says gdtoa (default) sometimes requires 16 KB of heap, while the
  legacy ldtoa mallocs about 1 KB, so budget heap before enabling float output on small parts.
- `--enable-newlib-nano-malloc` selects a malloc for small systems with very limited memory.

## Thread safety
The manual says that if several threads can call `malloc`/`realloc`/`free`, or they can be called
reentrantly, you must provide your own `__malloc_lock(struct _reent *)` and
`__malloc_unlock(struct _reent *)`; without them the memory pool may become corrupted.
`malloc` may call `__malloc_lock` recursively (lock, lock, unlock, unlock), so the implementation
must not block on a lock the same thread already holds (use a recursive lock). The `_r` covers
(`_write_r`, `_sbrk_r`, ...) take a pointer to the reentrancy structure that holds `errno`.
Which RTOS option wires these locks for you is RTOS-specific; read your RTOS port's documentation.

## Verify
- [ ] Link map shows the syscalls you wrote, not placeholder stubs, for `_write` and `_sbrk`.
- [ ] `printf("%f", 1.5)` prints when float support is intended.
- [ ] Forcing a large `malloc` returns NULL instead of corrupting the stack.

## Checked
Checked 2026-11-08 against the newlib libc manual (System Calls chapter, `malloc`, `__malloc_lock`),
the newlib README (nano formatted I/O, `_printf_float`/`_scanf_float`, nano malloc, gdtoa and
ldtoa heap figures), and GCC 14.2 Overall Options (`-specs=file`). Removed because no readable
page states them: the names and effects of the toolchain's spec files (`nano.specs`, `nosys.specs`, `rdimon.specs`, `libc_nano`, `libnosys`), the GCC 11 linker warning text, the
"stdout becomes line-buffered via `S_IFCHR`" claim, the 10-15 KB float cost, the first-`printf`
buffer size, and the FreeRTOS `configUSE_NEWLIB_REENTRANT` / `heap_useNewlib` pointers.
Method: documentation only; no commands were run.
