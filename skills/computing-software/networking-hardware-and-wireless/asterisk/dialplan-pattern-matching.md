---
id: computing-software.networking-hardware-and-wireless.asterisk.dialplan-pattern-matching
name: dialplan-pattern-matching
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, dialplan, pattern-matching, wildcards, x, z, n, character-sets, overlap-dialing]
level: practitioner
status: docs-checked
description: "Write dialplan patterns starting with underscore: X, Z, N, character sets, the period and exclamation wildcards, and how Asterisk sorts multiple matching patterns."
sources:
  - https://docs.asterisk.org/Configuration/Dialplan/Pattern-Matching/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dialplan pattern matching
Asterisk tries an exact extension first, then patterns. A pattern begins with `_`.

- `X` is 0-9, `Z` is 1-9, `N` is 2-9.
- `[1237-9]` is a character set; `[1-468]` means 1 to 4, 6 or 8 (a single digit, not a number). X, N, Z have no special meaning inside a set; only `-`, `\` and the set brackets matter.
- `.` matches one or more remaining characters; `!` matches zero or more and supports overlap dialing, answering as soon as the match is unambiguous. Both end the pattern; put them in a set (`[.]`, `[!]`) to match literally.
- Example: `exten => _64XX,1,SayDigits(${EXTEN})`.

Caution: `.` and `!` match any characters, not only digits. Filter caller input; the page points to README-SERIOUSLY.bestpractices.txt in the source tree.

Sort order (best match first): dashes are ignored; non-pattern extensions sort by ASCII before patterns; patterns sort by the most constrained character set per digit (N before X because it has fewer matches), and so on through the remaining rules on the page.

## Checked
2026-11-04: read the cited Asterisk documentation pages (Pattern-Matching) and confirmed the commands, options, defaults and names stated above. Nothing removed; every claim was confirmed.

Method: documentation only; no commands were run.
