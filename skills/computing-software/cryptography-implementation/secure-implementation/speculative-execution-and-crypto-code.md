---
id: computing-software.cryptography-implementation.secure-implementation.speculative-execution-and-crypto-code
name: speculative-execution-and-crypto-code
category: computing-software
field: cryptography-implementation
product: secure-implementation
tags: [secure-implementation, cryptography-implementation, speculative-execution, spectre, side-channel, lfence, process-isolation]
level: sme
status: draft
description: "Defend cryptographic code against speculative execution leaks (Spectre v1, v2, Retbleed): process isolation for keys, speculation barriers, and compiler mitigations."
sources: ["https://spectreattack.com/spectre.pdf", "https://www.intel.com/content/www/us/en/developer/articles/technical/software-security-guidance/technical-documentation/analysis-speculative-execution-side-channels.html", "https://llvm.org/docs/SpeculativeLoadHardening.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Speculative execution and crypto code

Constant-time code assumes the CPU executes what the program says. Speculation runs ahead on mispredicted paths and
leaves cache traces, so secrets touched speculatively can leak even from "correct" code.

## Threats relevant to crypto
- **Spectre v1 (bounds check bypass)**: attacker-controlled index read speculatively past a bounds check in the
  same process (JavaScript engines, eBPF, plugins) reads key bytes.
- **Spectre v2 / BHI / Retbleed**: cross-process or kernel branch target injection steering victim crypto code.
- **Speculative store bypass**, **MDS**, **Downfall** (gather) and **Zenbleed**: leak register or buffer
  contents across hyperthreads or processes; AVX register leaks hit crypto using vector instructions.

## Defences
1. **Isolation**: keep long-term keys in a separate process, enclave, HSM or kernel keyring, so untrusted code
   never shares an address space with them (browser site isolation model).
2. **Patches and microcode**: kernel mitigations (`/sys/devices/system/cpu/vulnerabilities/*` should show
   `Mitigation`), current microcode, and SMT considerations.
3. **Compiler mitigations**: `-mretpoline`, `-mspeculative-load-hardening` (LLVM SLH) for code processing
   attacker-chosen indices near secrets; `lfence` after critical bounds checks.
4. **Selective speculation barriers** in interpreters/JITs that run untrusted code alongside crypto.

## Practical stance
For servers, keep firmware and kernels patched and isolate key material. For multi-tenant runtimes (WASM hosts,
browsers, serverless) treat same-process secrets as reachable.

## Verify
- [ ] `grep . /sys/devices/system/cpu/vulnerabilities/*` shows mitigations on crypto hosts; keys not in
  processes running untrusted code.
