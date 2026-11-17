---
id: computing-software.cryptography-implementation.crypto-libraries.reseeding-after-fork-and-vm-snapshot
name: reseeding-after-fork-and-vm-snapshot
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [cryptography-implementation, crypto-libraries, random-generation, vm-snapshot-reseed, fork-safety, vmgenid, getrandom, csprng, cloned-vm, openssl]
level: advanced
status: verified
description: "Keep RNG output unique after fork, VM snapshot restore and cloning: userspace PRNG state, VMGenID, getrandom, and regenerating per-instance keys."
sources: ["https://www.man7.org/linux/man-pages/man2/getrandom.2.html", "https://man7.org/linux/man-pages/man2/madvise.2.html", "https://kernelnewbies.org/Linux_5.18", "https://kernelnewbies.org/Linux_6.11", "https://www.qemu.org/docs/master/specs/vmgenid.html", "https://github.com/openssl/openssl/blob/master/CHANGES.md", "https://docs.openssl.org/3.0/man7/RAND/", "https://cloudinit.readthedocs.io/en/latest/reference/modules.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reseeding after fork and VM snapshot

Any RNG whose state is copied produces the same output in both copies. That
repeats nonces, ECDSA `k` values (leaking the private key), session ids and
"unique" keys.

## Where state gets copied

- **fork()**: a userspace PRNG buffer (app-level ChaCha/AES-CTR buffers,
  older OpenSSL, some language runtimes) is duplicated into the child.
- **VM snapshot restore**: every restored instance resumes with the same RNG
  state, including the kernel's, until something reseeds it.
- **Golden images and clones**: identical SSH host keys, machine ids, TLS
  keys baked into the image.

## Defences

1. **Call the kernel per use.** `getrandom(2)` / `os.urandom` /
   `crypto/rand` read the kernel CSPRNG. The Linux 5.18 release notes list `vmgenid: notify RNG of VM fork and supply generation
   ID` (a guest that sees a changed VM Generation ID tells the kernel RNG; QEMU documents a `vmgenid` device), and Linux 6.11 adds a
   vDSO implementation of `getrandom()` (kernelnewbies release notes). Check your distribution kernel and hypervisor for both.
2. **Library fork detection.** OpenSSL 1.1.1 shipped fork protection that was not active by default until 1.1.1d (CVE-2019-1549 in
   the OpenSSL changelog: a partial mitigation mixes in a high-precision timer, and `OPENSSL_INIT_ATFORK` avoids the problem
   entirely); check the manual for your OpenSSL release. Verify your library version and avoid caching random bytes yourself.
3. **If you must keep a userspace buffer**, register `pthread_atfork` (or
   `MADV_WIPEONFORK` on the buffer, available since Linux 4.14 per `madvise(2)`) to discard it in the child, and do not
   rely on PIDs (PIDs recycle). CPython does this for its `random` module with `os.register_at_fork(after_in_child=_inst.seed)`.
4. **Never snapshot running hosts holding live keys** for cloning; snapshot
   powered-off templates.
5. **Regenerate per-instance identity on first boot**: SSH host keys
   (cloud-init's ssh module removes the default host keys with `ssh_deletekeys` and regenerates them), `/etc/machine-id` (systemd treats an
   empty or absent file as first boot), TLS keys, any key in the image. A microVM restore needs VM Generation ID support or an explicit
   reseed hook.

## Verify

- [ ] Test: fork a process after initialising the RNG; parent and child produce different bytes (fork needs Linux or macOS; this was not run
      on the Windows review host).
- [ ] Restore one snapshot twice; generated nonces/keys differ.
- [ ] Image build contains no private keys (scan the image).
