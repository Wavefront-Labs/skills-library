---
id: computing-software.systems-network-administration.bash.bash-arithmetic-expansion
name: bash-arithmetic-expansion
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, linux, arithmetic-expansion, bash-arithmetic, let, declare-i, integer-math, bc, floating-point, base-conversion, bit-operations, random, shell-scripting, lpic-1, sysadmin]
level: practitioner
status: verified
description: "Do integer math in bash with $(( )), (( )), let and declare -i: operators, assignment forms, bases (0x, 2#), overflow, octal traps with leading zeros, and reaching for bc/awk for floats."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html#Shell-Arithmetic
  - https://www.gnu.org/software/bash/manual/bash.html#Arithmetic-Expansion
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Arithmetic — integers in the shell, and knowing when to leave the shell

**Goal:** compute counts, sizes, percentages and offsets in bash without `expr`, and avoid
the octal/overflow/float traps.

## 1. Forms
```bash
total=$(( a + b * 2 ))        # expansion: value substituted
(( total > 100 )) && echo big # command: exit 0 if non-zero result
(( i++ )); (( n += 5 ))       # side effects
let 'x = 3 * 4' y=x+1         # older; quote to protect * and spaces
declare -i n; n='2 * 21'      # integer attribute: RHS evaluated arithmetically
```
Inside `(( ))` and `$(( ))` variables need no `$` (`$a` works but is unnecessary, and an empty `$n` leaves a bare operator behind, see Failure modes). Spaces are free.

## 2. Operators (C semantics, 64-bit signed)
`+ - * / % **` (power), `++ --`, `<< >> & | ^ ~`, `! && ||`, comparisons `< <= == != >= >`,
ternary `c ? a : b`, comma, assignment `= += -= *= /= %= <<= >>= &= |= ^=`.
- Integer division truncates toward zero: `(( 7 / 2 ))` = 3, `(( -7 / 2 ))` = -3.
- Percent: `(( pct = used * 100 / total ))` — multiply **before** dividing.
- Rounding: `(( r = (a + b/2) / b ))`.

## 3. Bases and constants
```bash
echo $(( 0x1f ))     # 31 hex
echo $(( 010 ))      # 8  — LEADING ZERO = OCTAL
echo $(( 2#1011 ))   # 11 binary; base#digits up to 64
echo $(( 10#$day ))  # force decimal: date +%d gives "08" → "value too great for base" otherwise
printf '%x %o %d\n' 255 255 0xff     # convert out
```
The octal trap hits anything from `date`, zero-padded IDs or `read` input. Always
`10#${var}` when the string may be zero-padded.

## 4. Limits and overflow
```bash
echo $(( 9223372036854775807 + 1 ))   # wraps to -9223372036854775808, no error
```
Bytes of large disks fit (2^63 ≈ 9.2 EB) but products like `blocks * bs * 1024` can
overflow silently. Validate magnitude or use `bc`.

## 5. Floats and big numbers — leave bash
```bash
bc -l <<< 'scale=2; 7/3'                 # 2.33
awk 'BEGIN { printf "%.1f\n", 1024*1.5 }'
printf '%.2f\n' "$(bc -l <<< "$used*100/$total")"
python3 -c 'print(2**100)'
```
`$(( ))` rejects `3.5` ("syntax error: invalid arithmetic operator"). `bc` needs
`scale` for decimals; `-l` loads the math library and sets scale=20.

## 6. Useful idioms
```bash
(( RANDOM % 100 ))              # 0–99 (not cryptographic); $SRANDOM for 32-bit random (5.1+)
(( size = $(stat -c %s f) / 1024 / 1024 ))
for (( i=0; i<${#arr[@]}; i++ )); do ...; done
(( flags & 0x4 )) && echo "bit 2 set"
secs=$SECONDS; ...; echo "took $(( SECONDS - secs ))s"
```

## Failure modes
- "value too great for base": zero-padded input → `10#`.
- "syntax error: operand expected (error token is ...)": an empty variable expanded with `$` in `$(( $n * 2 ))` leaves `* 2`
  (bash 5.2: `$(( n * 2 ))` with empty `n` is just 0, and `$(( ))` is 0). Use the bare name, or default it (`${n:-0}`).
  Under `set -u`, a bare unset name fails with "unbound variable" instead.
- `(( x = 0 ))` under `set -e` exits the script: a result of 0 is a non-zero exit status.
  Use `x=0` or `(( x = 0 )) || true`.
- `$[ ]` old syntax: still works in bash 5.2 (printed 3 for `$[ 1+2 ]`) but is deprecated; avoid.
- Comparing versions arithmetically (`1.10 > 1.9`): not numbers — use `sort -V`.

## Verify
- [ ] `echo $(( 10#08 + 1 ))` prints 9 and `echo $(( 08 + 1 ))` errors — you understand the base rule.
- [ ] Percentages for a 1-of-3 case print 33, not 0.
