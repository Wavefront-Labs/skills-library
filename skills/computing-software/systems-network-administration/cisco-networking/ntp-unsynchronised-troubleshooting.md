---
id: computing-software.systems-network-administration.cisco-networking.ntp-unsynchronised-troubleshooting
name: ntp-unsynchronised-troubleshooting
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, ios-xe, ntp-associations, ntp-troubleshooting, clock-unsynchronized, stratum, reach, ntp, sanity-tests, rfc5905]
level: practitioner
status: docs-checked
description: "Diagnose an NTP client that will not sync, using the reach register, dispersion, stratum 16, the eight validity tests and the RFC 5905 step and panic thresholds."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/network-time-protocol-ntp/116161-trouble-ntp-00.html
  - https://www.rfc-editor.org/rfc/rfc5905
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NTP unsynchronised troubleshooting

## Read the association table (Cisco TechNote 116161)
- Markers before the address: `*` synchronised to this peer, `#` almost synchronised, `+` selected for possible
  synchronisation, `-` candidate, `~` statically configured.
- `st`: stratum, NTP hops from an authoritative source, up to 16. The client prefers the lowest stratum it can reach.
  RFC 5905 treats stratum 16 (MAXSTRAT) as unsynchronised: a peer at or above it, or with the leap indicator set to
  "unsynchronized", is not usable.
- `when` must be lower than `poll`. Poll starts at 64 s and can rise to 1024 s; Cisco states it cannot be adjusted on
  a router.
- `reach` is an 8-bit register printed in octal, one bit per recent poll: 377 = last eight received, 0 = none,
  1 = only the latest, 357 = one lost five polls ago. A packet counts only if the NTP process accepted it as valid, not
  merely if the device received it. RFC 5905: any non-zero bit means the server is considered reachable.
- `disp`: dispersion, maximum 16000 in the display. High dispersion plus reach 0 means the client does not accept
  that server even if the offset looks small (Cisco example: offset -4.26, disp 16000, reach 0).
- `offset` positive: server clock ahead. Negative: client clock ahead.
- `show ntp associations detail` flags: `sane`/`insane` (packet passed or failed sanity tests), `valid`/`invalid`,
  `our_primary` (synced to it), `selected`. An `insane, invalid` association is not accepted.

## The eight validity tests (Cisco, from RFC 1305)
| Test | Mask | Meaning |
|---|---|---|
| 1 | 0x01 | Duplicate packet |
| 2 | 0x02 | Bogus packet |
| 3 | 0x04 | Protocol unsynchronised |
| 4 | 0x08 | Peer delay/dispersion failed boundary check |
| 5 | 0x10 | Peer authentication failed |
| 6 | 0x20 | Peer clock unsynchronised (common for an unsynced server) |
| 7 | 0x40 | Peer stratum out of bound |
| 8 | 0x80 | Root delay/dispersion failed boundary check |

Tests 1-4 passing makes the packet data valid. Tests 5-8 passing makes the header valid, and only then can the peer be
selected. `debug ntp validity` reports a failure with the reason, for example "failed validity tests 52" followed by
"Authentication failed" and "Peer/Server Stratum out of bound" in Cisco's sample; compare against the table.

## Symptom to cause
- **reach 0, stale `when`**: no valid replies are arriving. Cisco says to check the path for saturated links, drops,
  WAN loss and encryption. Packets delayed by queuing make later timestamps vary and the client cannot compensate.
  Low or intermittent reach means the client drifts out of sync.
- **Server shows as unsynchronised or stratum out of bound** (tests 6 and 7): fix the server's own upstream first.
- **Authentication failed** (test 5): key or trusted-key mismatch between the two ends; see
  `computing-software.systems-network-administration.cisco-networking.ntp-client-server-and-authentication`.
- **Huge dispersion with reach 0**: past loss made the filter hold maximum-dispersion samples; wait for fresh good
  polls or fix the path.

## Large offsets (RFC 5905 clock discipline)
- Offset above the step threshold STEPT (125 ms) but under PANICT (1000 s): the clock is stepped, all associations
  are reset, and the client restarts from the initial state, so expect a pause before `*` returns.
- Offset above PANICT (1000 s): the update SHOULD cause the program to exit with a log message; the operator must set
  the clock by hand before restart.
- Below STEPT: normal slewing adjustment.
- Sources: RFC 5905 sections on the clock update procedure and the constants table.

## Configuration traps
- Cisco warns that `ntp master` is easy to misuse and can override valid sources (see
  `computing-software.systems-network-administration.cisco-networking.ntp-hierarchy-design`).
- Check access lists and VRF placement only against your platform guide; those details were not confirmed here.

## Verify
- [ ] Association shows reach 377 with `*` on one peer and `+` on others.
- [ ] No validity test is failing in the debug output.
- [ ] Offset is well under STEPT and dispersion is small.

## Checked
Date: 2026-11-08
Method: documentation only; no commands were run. Read Cisco TechNote 116161 (association columns, reach examples,
dispersion, association detail terms, the eight sanity tests, debug validity sample, link-check advice) and RFC 5905
(MAXSTRAT, reachability, STEPT and PANICT behaviour). Removed as unconfirmed: all IOS config lines (ntp source, vrf,
access-group, authenticate, update-calendar), the claim that IOS refuses large steps, the 5-10 minute convergence figure,
refid kiss-code meanings, and the stack/HA note.
