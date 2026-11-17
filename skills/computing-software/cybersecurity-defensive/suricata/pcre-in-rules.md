---
id: computing-software.cybersecurity-defensive.suricata.pcre-in-rules
name: pcre-in-rules
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [pcre, regex, pcre-modifiers, pcre2]
level: practitioner
status: docs-checked
description: "Use pcre in rules: format, i, s, m, A, E, G and R modifiers, buffer selectors like U and P, captures, and PCRE2 behaviour changes."
sources: ["https://docs.suricata.io/en/latest/rules/payload-keywords.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# pcre

Format: `pcre:"/<regex>/opts";`. Regex is costly, so pair it with a `content` that must match first.

- `i` case insensitive; `s` makes pcre check newline characters; `m` can make one line of the payload count as two; `A` anchor at buffer start; `E` ignore trailing newline; `G` invert greediness.
- Buffer selectors: `U` normalized URI, `I` raw URI, `P` request body, `Q` response body, `H` headers, `D` raw headers, `M` method, `C` cookie, `S` status code, `Y` status message, `V` User-Agent, `W` Host.
- `R` makes the match relative to the previous match.
- Captured groups can be logged with `pkt:`, `alert:` or `flow:` prefixes; `flow:` needs a flow to store into.
- PCRE1 to PCRE2 changed behaviour: `[\d-a]` now needs the dash escaped as `[\d\-a]`.

## Checked

2026-11-08: read in full against the OISF/suricata doc/userguide rst source (rules/payload-keywords) read in full; the claims, names, values and examples left in this skill match the page text. Reworded the s and m modifier descriptions to the page wording.

Method: documentation only; no commands were run.
