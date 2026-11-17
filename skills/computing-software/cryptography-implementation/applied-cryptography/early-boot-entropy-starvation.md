---
id: computing-software.cryptography-implementation.applied-cryptography.early-boot-entropy-starvation
name: early-boot-entropy-starvation
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, early-boot-entropy, getrandom, random-seed, systemd-random-seed, entropy-starvation, embedded, first-boot]
level: advanced
status: docs-checked
description: "Handle early-boot RNG blocking and weak first-boot keys on Linux: getrandom blocking and EAGAIN, systemd random seed file, cloned images."
sources: ["https://man7.org/linux/man-pages/man2/getrandom.2.html", "https://www.freedesktop.org/software/systemd/man/latest/systemd-random-seed.service.html", "https://factorable.net/weakkeys12.extended.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Early-boot entropy starvation

**Symptoms:** services hang at boot waiting for randomness, or devices generate weak or repeated keys on first boot.
The 2012 weak-keys study (factorable.net) reported that 0.50% of TLS hosts and 0.03% of SSH hosts it scanned had
keys exposed by weak randomness, and traced much of it to a boot-time entropy hole on embedded or headless devices.

## getrandom behaviour (man-pages)
- By default getrandom() draws from the urandom source. If that source has not yet been initialised, the call
  blocks.
- With `GRND_NONBLOCK` it instead returns -1 with `errno` set to `EAGAIN`, so use that flag to detect "not ready".
- Once initialised, reads of up to 256 bytes always return in full and are not interrupted by signals. Larger reads
  may be partial or fail with `EINTR`. Always check the return value.
- Reading small buffers (256 bytes or less) from the urandom source is the preferred mode.
- getrandom() needs no pathname or file descriptor, so it works after chroot or when a library closed the fd.

## Seed file (systemd-random-seed.service)
- Loads `/var/lib/systemd/random-seed` into the kernel pool at boot and saves it at shutdown. On load, the file is
  immediately replaced with a new seed from the kernel so no two boots use the same seed.
- No entropy is credited by default. `$SYSTEMD_RANDOM_SEED_CREDIT` can change this; the docs advise enabling it only
  after removing the seed from images that are replicated.
- It runs late in early boot, after the initrd and once /var is mounted, so many services need entropy earlier. The
  docs recommend a boot loader that passes an initial seed, for example systemd-boot with `bootctl random-seed`.
- Start-up does not complete until the pool is initialised, which makes the service a synchronisation point for
  services that read /dev/urandom without other precautions. On entropy-starved systems this may take a while.
- An image replicated to many systems with the seed file included gives each the same pool contents. Remove the seed
  from such images.

## First-boot key generation
- Generate host and device identity keys only after the random pool is initialised; order such services after
  `systemd-random-seed.service`.
- Never bake host keys or seed files into golden images.
- The weak-keys paper notes that embedded devices with a real-time clock can still produce keys that look distinct
  but depend only on configuration and boot time, so the keys can be enumerated by a targeted attacker.

## Verify
- [ ] Key-generating services start only after the pool is initialised (test with `GRND_NONBLOCK` or the service order).
- [ ] Keys from freshly booted clones are all distinct.

## Checked

Read the getrandom(2) man page (blocking, GRND_NONBLOCK and EAGAIN, 256-byte rule, EINTR, notes on pathnames), the systemd-random-seed.service page (seed file path, replace-on-load, no credit by default, late start, image cloning, bootctl random-seed) and the weak-keys paper abstract plus the passage on boot-time entropy hole and real-time clocks. Removed because not in these sources: kernel 5.4 and 5.18 behaviour changes, virtio-rng and trust_cpu settings, haveged, vmgenid, container remarks, dmesg message and old-kernel /dev/urandom claims.

Method: docs-checked 2026-11-09 against getrandom(2) man page, systemd-random-seed.service page and weakkeys12 extended paper.
