---
id: computing-software.networking-hardware-and-wireless.f5-big-ip.irules-tables-and-session
name: irules-tables-and-session
category: computing-software
field: networking-hardware-and-wireless
product: f5-big-ip
tags: [networking-hardware-and-wireless, f5-big-ip, irules-table, session-table, rate-limiting]
level: practitioner
status: draft
description: "Maintain BIG-IP iRules table state for per-client rate limiting and session tracking with timeouts and cleanup."
sources:
  - https://clouddocs.f5.com/api/irules/table.html
  - https://clouddocs.f5.com/api/irules/class.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# iRules table command and session state

```
when RULE_INIT { set static::max 20 ; set static::win 10 }
when HTTP_REQUEST {
  set k "rl:[IP::client_addr]"
  set n [table incr -notouch -subtable rate $k]
  if { $n == 1 } { table timeout -subtable rate $k $static::win }
  if { $n > $static::max } {
    HTTP::respond 429 content "slow down" Retry-After $static::win
    return
  }
}
```
```
table set -subtable sess $id $user 3600 7200
table lookup -subtable sess $id
table delete -subtable sess $id
table keys -subtable sess -count
```
- `table` entries are replicated to the HA peer (when enabled) and live in TMM memory. `timeout` is idle expiry, `lifetime` the absolute maximum. No explicit expiry means the entry lives until reboot.
- Always use a named `-subtable` to avoid collisions, and keep key cardinality bounded: unbounded keys (e.g. full URLs) can exhaust memory.
- `table incr` is atomic across TMM threads, so counters are correct; `table add` only sets when the key is missing.
- Gotcha: the table is per traffic domain and per unit-state; failover moves entries only if the connection mirroring/sync is set, so a rate limiter resets after failover.
- Consider a built-in alternative: LTM rate classes (`ltm rate-shaping`), or AFM/Advanced WAF DoS profiles, for production-grade rate limits.

Verify: `tmsh show ltm rule` and `tmsh show sys tmm-info`/memory; hit the VS 25 times with `for i in $(seq 25); do curl -so/dev/null -w '%{http_code}\n' http://vip/; done` and see 429 after the 20th.
