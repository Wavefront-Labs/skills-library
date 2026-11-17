---
id: computing-software.cybersecurity-defensive.suricata.thresholding-keyword
name: thresholding-keyword
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [threshold, rate-limiting, track-by-src, alert-limiting]
level: practitioner
status: docs-checked
description: "Control alert volume with the threshold keyword: types threshold, limit, both and backoff, track options, count and seconds."
sources: ["https://docs.suricata.io/en/latest/rules/thresholding.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# threshold keyword

`threshold: type <type>, track <option>, count <N>` plus `seconds <T>` (or `multiplier <M>` for backoff).

## Types
- `threshold`: alert on the Cth match, or C matches within N seconds.
- `limit`: at most N alerts per period.
- `both`: alert once the count is reached, then rate-limit. The docs syntax lists `multiplier` but the example uses `seconds`; verify before relying on it.
- `backoff`: alert after `count`, then at growing intervals. Count 1 with multiplier 10 alerts on matches 1, 10, 100, 1000. Requires `track by_flow`.

## Track
`by_src`, `by_dst`, `by_both`, `by_rule`, `by_flow`.

## Behaviour
For limit, backoff and both, drop and reject apply to every matching packet. State keywords (flowbits, xbits, hostbits, flowint) are not thresholded. `tag` is skipped when a match is suppressed.

## Checked

2026-11-08: read in full against the OISF/suricata doc/userguide rst source (rules/thresholding) read in full; the claims, names, values and examples left in this skill match the page text. Nothing else was removed.

Method: documentation only; no commands were run.
