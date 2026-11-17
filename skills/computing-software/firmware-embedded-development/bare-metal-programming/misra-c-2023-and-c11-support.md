---
id: computing-software.firmware-embedded-development.bare-metal-programming.misra-c-2023-and-c11-support
name: misra-c-2023-and-c11-support
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [misra-c-2023, misra-c, c11-features, amendment-4, misra-c-2025, firmware-embedded-development]
level: advanced
status: draft
description: "Migrate a MISRA C:2012 project to MISRA C:2023 (C11/C18 support, threads and atomics guidance, Amendment 4 consolidation) and update tool configs and compliance docs."
sources:
  - https://misra.org.uk/product/misra-c2023/
  - https://misra.org.uk/app/uploads/2021/06/MISRA-C-2012-AMD2.pdf
  - https://www.misra.org.uk/app/uploads/2021/06/MISRA-Compliance-2020.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# MISRA C 2023 and C11 support

## Edition history (what you might be claiming)
| Edition | Language | Notes |
|---|---|---|
| MISRA C:2012 (third edition) | C90, C99 | base |
| Amendment 1 (2016) | | security-related rules (21.13-21.20, Dir 4.14) |
| Amendment 2 (2020) | C11/C18 | allows C11/C18 compilation, `_Noreturn`, `_Static_assert` usable |
| Amendment 3 (2022) | | new rules on C11 features |
| Amendment 4 (2023) | | multithreading and atomics (Rules 22.11-22.20, 9.7, 21.25, 21.26) |
| MISRA C:2023 | C90/C99/C11/C18 | consolidates 2012 + AMD1-4 + TC1-2 into one document |
| MISRA C:2025 | | further revision; check whether your tools support it before claiming |

## Notable C11-related guidance
- `_Atomic` objects: Rule 9.7 requires atomic objects to be initialised before access;
  Rule 21.25 requires all memory synchronisation to be `memory_order_seq_cst` (deviate with
  rationale if you use acquire/release for ISR flags).
- `<threads.h>`: Rules 22.11-22.20 cover thread joins, mutex init/destroy, `tss` use. Rarely
  relevant on bare metal; relevant on RTOS wrappers that use C11 threads.
- `_Generic` (Rules 23.x): constrained heavily; most firmware just avoids it.
- `_Noreturn` and `_Alignas`/`_Alignof` permitted with conditions.
- C11 Annex K (`memcpy_s` etc.): optional and rarely implemented by embedded libcs; don't rely on it.

## Migration steps
1. Decide the language standard (`-std=c11` or `c17`) and record it in the compliance plan.
2. Update tools: cppcheck 2.13+ MISRA addon, PC-lint Plus 2.0+, Polyspace R2024a+, Helix QAC,
   LDRA versions that list MISRA C:2023 support. Rule texts are not freely distributable; the
   cppcheck addon needs your own `--rule-texts` file from the purchased PDF.
3. Re-run analysis; new findings mostly come from atomics, the C11-feature rules added by
   Amendments 3 and 4, and re-categorised rules.
4. Rebase the Guideline Re-categorisation Plan and deviation records on 2023 rule numbers
   (most numbers are unchanged from 2012; amendments added new ones).
5. Update the compliance statement in release documentation: "MISRA C:2023, per MISRA Compliance:2020".

## Verify
- [ ] Analyser configured for MISRA C:2023 and the chosen C standard.
- [ ] Deviation records reference 2023 rule IDs.
- [ ] Atomic usage either complies with 21.25 or has a documented deviation.
