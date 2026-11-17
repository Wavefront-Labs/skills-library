---
id: computing-software.cryptography-implementation.secure-implementation.branch-free-selection-and-table-lookups
name: branch-free-selection-and-table-lookups
category: computing-software
field: cryptography-implementation
product: secure-implementation
tags: [cryptography-implementation, secure-implementation, constant-time, timing-attack, branchless-select, conditional-swap, masked-table-lookup, cache-timing, bearssl, ct-select]
level: sme
status: docs-checked
description: "Write secret-independent code: mask-based select and conditional swap, scanning whole tables instead of indexing, avoiding secret-dependent division and early exits."
sources: ["https://www.bearssl.org/constanttime.html", "https://github.com/veorq/cryptocoding", "https://datatracker.ietf.org/doc/html/rfc7748#section-5"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Branch-free selection and table lookups

Timing-safe code must not let secret values influence **branches**, **memory
addresses**, or **variable-time instructions**. The basic tools are masks.

## Masks and select

```c
#include <stdint.h>
/* mask = 0xFFFFFFFF if bit == 1 else 0; bit must be 0 or 1 */
static inline uint32_t ct_mask(uint32_t bit) { return (uint32_t)0 - bit; }
static inline uint32_t ct_select(uint32_t bit, uint32_t a, uint32_t b) {
    uint32_t m = ct_mask(bit); return (a & m) | (b & ~m);           /* bit ? a : b */
}
static inline uint32_t ct_is_zero(uint32_t x) {                     /* 1 if x == 0 */
    return 1 & ((~x & (x - 1)) >> 31);
}
static inline uint32_t ct_eq(uint32_t a, uint32_t b) { return ct_is_zero(a ^ b); }
```

The cryptocoding guide recommends a straight-line select over branches, with
dummy operations in branches as a less reliable alternative. BearSSL advises
passing a 32-bit "control word" set to 1 or 0 rather than a C `_Bool`, because
the compiler cannot then assume the value is only 0 or 1 and is less likely to
turn bitwise logic into conditional jumps.

## Conditional swap (Montgomery ladder, RFC 7748)

RFC 7748 specifies that `cswap` SHOULD be implemented in constant time.

```c
static void ct_cswap(uint32_t swap, uint32_t *a, uint32_t *b, size_t n) {
    uint32_t m = ct_mask(swap);
    for (size_t i = 0; i < n; i++) { uint32_t t = m & (a[i] ^ b[i]); a[i] ^= t; b[i] ^= t; }
}
```

## Table lookups

`table[secret_index]` leaks the index through cache timing (cache-based leaks
have recovered RSA and AES keys, including from co-hosted virtual machines). Read
every entry and keep the one you need:

```c
static uint32_t ct_lookup(const uint32_t *table, size_t n, uint32_t idx) {
    uint32_t r = 0;
    for (uint32_t i = 0; i < n; i++) r |= table[i] & ct_mask(ct_eq(i, idx));
    return r;
}
```

BearSSL uses the same idea (conditional copy of every candidate) for the
windowed point multiplication lookup in elliptic curves, and bitslicing to
replace AES S-box tables. Bitslice code tends to be about as large as the table
it replaces. Cryptocoding also names bitslicing for table-free AES.

## Other leaks to remove

- Conditional jumps on secrets: branch prediction and instruction fetch leak
  the condition. A branch on public data (for example the fixed round count of
  AES-128) is fine.
- Integer division and modulo (`/`, `%`): hardware often takes a faster path for
  small operands, and on CPUs without a divide opcode the compiler may call a
  library routine with the same behaviour.
- Multiplication: constant-time on most modern CPUs, but older designs
  (80486, ARM9) have shortcuts for small operands. The Cortex-M3 32-to-64 bit
  multiply is not constant-time; BearSSL offers a `BR_CT_MUL31` option for it.
- Secret-dependent loop bounds, a special case of secret-dependent branching
  (BearSSL's bignums carry an announced bit length so the real length stays
  hidden).
- Shifts and rotations by secret counts on CPUs without a barrel shifter
  (BearSSL cites the Pentium 4).

## Verify

- [ ] No branch, index or loop bound depends on secret data (review).
- [ ] Generated assembly checked for branches in the hot functions; BearSSL notes
      compilers may rewrite bitwise logic into jumps and advises reading the
      assembly (see compiler hazards skill).

## Checked

Method: docs-checked 2026-11-09 against bearssl.org/constanttime.html (read the execution model, compiler woes, conditional copy and bitslicing sections), bearssl.org/ctmul.html (Cortex-M3 and BR_CT_MUL31 passages), veorq/cryptocoding README (branching, table lookup sections), RFC 7748 (cswap text). Removed: dudect/ctgrind checklist item (not in cited sources), the claim that `?:` on secrets emits branches, the UMULL early-termination name (BearSSL says only that the M3 32-to-64 multiply is not constant-time and shows an undocumented early exit), and the AES T-table naming as a classic attack (kept generic cache-timing statement).
