---
id: computing-software.cryptography-implementation.secure-implementation.memfd-secret-and-hardware-memory-encryption
name: memfd-secret-and-hardware-memory-encryption
category: computing-software
field: cryptography-implementation
product: secure-implementation
tags: [secure-implementation, cryptography-implementation, memfd-secret, memory-encryption, amd-sev, intel-tdx, secure-memory, cold-boot]
level: sme
status: docs-checked
description: "Use memfd_secret for secret memory removed from the kernel page tables, locked and excluded from hibernation, and reason about hardware memory encryption threat models."
sources: ["https://man7.org/linux/man-pages/man2/memfd_secret.2.html", "https://www.amd.com/en/developer/sev.html", "https://www.intel.com/content/www/us/en/developer/tools/trust-domain-extensions/overview.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# memfd_secret and hardware memory encryption

## memfd_secret (Linux 5.14+)
Creates memory removed from the kernel page tables: only processes holding the file descriptor map it, the kernel
itself cannot access it (so pointers to it cannot be passed to system calls), and it is locked like mlock (never swapped).
```c
int fd = syscall(SYS_memfd_secret, 0);
ftruncate(fd, 4096);
void *key = mmap(NULL, 4096, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
```
- Before Linux 6.5 it is disabled unless the administrator sets the `secretmem.enable=y` kernel parameter; mapped size
  cannot exceed `RLIMIT_MEMLOCK`. glibc has no wrapper, so use `syscall(2)`.
- Raises the bar against ROP and kernel-flaw exfiltration, but the man page gives no 100% guarantee against the
  kernel. Hibernation is inhibited while any memfd_secret descriptor exists.

## Hardware memory encryption
Confidential-VM technologies target a threat model that includes the host or hypervisor. Read the vendor documentation
for what each technology protects (not checked here), and verify attestation before releasing keys to a confidential VM.

## Limits
Memory encryption does not stop attacks from inside the guest/process, side channels, or bugs in the code itself.

## Checked

2026-10-31. Confirmed in the memfd_secret(2) man page: Linux 5.14, off by default before 6.5 (secretmem.enable=y), removed from kernel page tables, locked like mlock, hibernation inhibited, RLIMIT_MEMLOCK, no glibc wrapper. Removed: AMD/Intel/Arm technology table and cloud key-release names (AMD page unreadable, Intel page had no matching content).

Method: documentation only; no commands were run.

## Verify
- [ ] Key service runs on confidential VMs with attestation-gated key release, or uses memfd_secret where supported.
