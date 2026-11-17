---
id: computing-software.cybersecurity-defensive.suricata.byte-test-jump-extract
name: byte-test-jump-extract
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [byte-test, byte-jump, byte-extract, binary-protocols]
level: advanced
status: docs-checked
description: "Parse binary fields in rules with byte_test, byte_jump and byte_extract: operators, endianness, relative offsets, variables and bitmask."
sources: ["https://docs.suricata.io/en/latest/rules/payload-keywords.html", "https://docs.suricata.io/en/latest/rules/differences-from-snort.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# byte_test, byte_jump, byte_extract

## byte_test
`byte_test:<num of bytes> | <variable_name>, [!]<operator>, <test value>, <offset> [,relative] ...`. Operators `<`, `>`, `=`, `<=`, `>=`, `&`, `^`. Options: `big`/`little`, string type `hex`/`dec`/`oct`, `dce`, `bitmask`. Example: `byte_test:2,=,0x01,0;`.

## byte_jump
Reads bytes at an offset and moves the detection pointer there. Options: `relative`, `multiplier`, endianness, string type, `align`, `from_beginning`, `from_end`, `post_offset`, `dce`, `bitmask` (applied before the multiplier). Example: `byte_jump:0,0, from_end, post_offset -8;`.

## byte_extract
Stores bytes into a named variable usable by `content`, `byte_test`, `byte_math`, `byte_jump` and `isdataat`. Options: `relative`, `multiplier`, endianness, string type, `dce`, `align` (2 or 4).

Differences from Snort: an extracted variable must be used in the same buffer or it evaluates to zero, and repeated keywords in one rule, such as `byte_math: endian big, endian little`, are rejected.

## Checked

2026-11-08: read in full against the OISF/suricata doc/userguide rst source (rules/payload-keywords and rules/differences-from-snort) read in full; the claims, names, values and examples left in this skill match the page text. Narrowed the repeated-keyword rejection claim to what the Snort-differences page says (byte_math).

Method: documentation only; no commands were run.
