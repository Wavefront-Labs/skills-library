---
id: computing-software.cryptography-implementation.applied-cryptography.rdrand-and-rdseed-hardware-rng
name: rdrand-and-rdseed-hardware-rng
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, rdrand, rdseed, hardware-rng, x86, entropy, trng]
level: advanced
status: docs-checked
description: "Use RDRAND and RDSEED correctly: check the carry flag and retry, use RDSEED for seeding, and mix into the OS pool rather than trusting the CPU alone."
sources: ["https://www.intel.com/content/www/us/en/developer/articles/guide/intel-digital-random-number-generator-drng-software-implementation-guide.html", "https://www.kernel.org/doc/html/latest/admin-guide/kernel-parameters.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RDRAND and RDSEED

## Semantics
- RDRAND returns output of an on-chip CTR_DRBG (SP 800-90A) fed by the hardware entropy source.
- RDSEED returns seed values from the hardware entropy source; Intel provides it for seeding software PRNGs.
- Both set CF=1 on success. CF=0 means no value was available: test CF, never a zero result. Intel recommends 10
  RDRAND retries in a tight loop.

Wrap the instruction in a bounded retry loop (Intel's guide shows `rdrand64_retry`) and fail closed if every retry
fails.

## Trust model
- Do not use RDRAND as the only source; call `getrandom()` and let the OS combine sources. The Linux kernel
  parameter `random.trust_cpu=off` disables trusting the CPU's random number generator to initialize the kernel's RNG.

## Verify
- [ ] Code checks CF and has a bounded retry with a fail-closed path.
- [ ] A continuous test rejects stuck or repeated values when RDRAND is used directly.

## Checked

- 2026-11-01. Confirmed (Intel DRNG software implementation guide): RDRAND uses a CTR_DRBG per SP 800-90A; RDSEED draws seeds from the entropy source and is provided for seeding software PRNGs; CF must be checked and CF=0 means unavailable; 10 retries recommended. Confirmed (kernel parameters doc): `random.trust_cpu=off`.
- Removed as unconfirmed: AMD bug reports, CrossTalk CVE, hypervisor trapping, RDSEED load behaviour, intrinsic code and cpuinfo command.

Method: documentation only; no commands were run.
