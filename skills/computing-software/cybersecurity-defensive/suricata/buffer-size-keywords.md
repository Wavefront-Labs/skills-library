---
id: computing-software.cybersecurity-defensive.suricata.buffer-size-keywords
name: buffer-size-keywords
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [isdataat, bsize, dsize, buffer-length]
level: practitioner
status: docs-checked
description: "Test data presence and sizes: isdataat (with its off-by-one rules), bsize for buffers, dsize for packet payloads."
sources: ["https://docs.suricata.io/en/latest/rules/payload-keywords.html", "https://docs.suricata.io/en/latest/rules/differences-from-snort.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# isdataat, bsize, dsize

## isdataat
Checks data exists at a position; `!` negates. Absolute and relative checks differ by one byte: for a 32-byte payload `isdataat:31;` matches but `32` does not, while `isdataat:32,relative;` matches and `33,relative` does not. To prove nothing follows the last match use `isdataat:!1,relative;` (Snort uses `!0`).

## bsize
Length of a buffer (unsigned 64-bit). Default operator `=`; `<`, `>` and `<>` ranges (exclusive): `bsize:6<>15;` means more than 6 and less than 15. Preceding contents are checked and an error is raised if a match is impossible.

## dsize
Packet payload size (unsigned 16-bit): `dsize:[<>!]number;` or `dsize:min<>max;`. Useful for abnormal sizes. Not usable with app-layer keywords such as `http.uri`.

## Checked

2026-11-08: read in full against the OISF/suricata doc/userguide rst source (rules/payload-keywords and rules/differences-from-snort) read in full; the claims, names, values and examples left in this skill match the page text. Nothing else was removed.

Method: documentation only; no commands were run.
