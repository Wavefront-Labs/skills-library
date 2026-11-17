---
id: computing-software.cryptography-implementation.secure-implementation.data-independent-timing-cpu-modes
name: data-independent-timing-cpu-modes
category: computing-software
field: cryptography-implementation
product: secure-implementation
tags: [secure-implementation, cryptography-implementation, data-independent-timing, intel-doit, constant-time, side-channel]
level: sme
status: docs-checked
description: "Use Intel's data operand independent timing mode (DOITM) for constant-time crypto: enumeration, MSR, OS role, performance trade-off and what it does not cover."
sources: ["https://www.intel.com/content/www/us/en/developer/articles/technical/software-security-guidance/best-practices/data-operand-independent-timing-isa-guidance.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data-independent timing CPU modes

CPUs may use value-dependent optimisations such as data-dependent prefetching. Intel's DOIT guidance describes a
mode that makes a listed subset of instructions run with timing independent of their data values. Other vendors
(ARM DIT, AMD) have their own mechanisms; read the vendor documentation, not this skill, for those.

## Intel DOITM
- Enumerated by `IA32_ARCH_CAPABILITIES[12]`; controlled by bit 0 (DOITM) of the `IA32_UARCH_MISC_CTL` MSR
  (index 1B01H), logical-processor scoped, reset value 0. Core processors from Ice Lake and Atom from Gracemont
  onward enumerate it; some processors need a microcode update first.
- Processors that do not enumerate it (Core before Ice Lake, Atom before Gracemont) can be assumed to behave as if
  DOITM were enabled for the listed instructions. On certain processors MXCSR may also need configuring.
- Intel describes enabling it per thread or per process via system software; Intel suggests operating systems
  could support the MSR similarly to speculative store bypass disable. Check your OS and kernel.
- Inside SGX enclave mode, processors that enumerate DOITM always run with it enabled.

## Cost and scope
- It can disable hardware optimisations such as data-dependent prefetching. Intel does not recommend enabling it
  globally and expects the performance impact may be significantly higher on future processors.
- Only the documented instruction list is covered; memory addresses, code bytes and immediates can still leak,
  and power, frequency and thermal side channels are not addressed. It gives no benefit to code that is not
  already written to be constant time.
- Speculative execution may still handle secrets in a data-dependent way; see Intel's timing side-channel
  guidance.

## Verify
- [ ] Target CPUs enumerate DOITM or predate it; the OS enables it only for the crypto software that needs it;
  constant-time checks still pass.

## Checked
2026-11-01. Confirmed against Intel's Data Operand Independent Timing ISA Guidance: enumeration bit, MSR and bit,
scope, pre-Ice Lake assumption, SGX behaviour, performance and coverage caveats. Removed: ARM DIT, Apple, GoFetch,
BoringSSL, Go and AMD claims (their sources could not be read in this batch).
Method: documentation only; no commands were run.
