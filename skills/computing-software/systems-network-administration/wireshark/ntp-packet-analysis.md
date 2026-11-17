---
id: computing-software.systems-network-administration.wireshark.ntp-packet-analysis
name: ntp-packet-analysis
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, ntp-analysis, ntp, time-sync, protocol-analysis]
level: practitioner
status: verified
description: "Analyse NTP in Wireshark: modes, stratum, leap and kiss codes, root delay/dispersion, and computing offset and delay from the four timestamps."
sources:
  - https://www.rfc-editor.org/rfc/rfc5905
  - https://www.wireshark.org/docs/dfref/n/ntp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NTP analysis

## Filters
```
ntp
ntp.flags.mode == 3          # client; 4 server; 1/2 symmetric; 5 broadcast; 6 control; 7 reserved for private use (RFC 5905)
ntp.stratum == 16            # unsynchronised server
ntp.flags.li == 3            # leap indicator: alarm, clock not synchronised
ntp.refid == "RATE"          # kiss-o'-death (stratum 0) rate limiting
```

## Fields that matter
| Field | Meaning |
|-------|---------|
| Stratum | 1 = attached to reference clock; 16 = unsynchronised |
| Reference ID | upstream server IP (stratum 2+) or a short source code, or a kiss-o'-death code (RATE, DENY, RSTR; RFC 5905) |
| Root delay / dispersion | accumulated error to the reference; big values = poor source |
| Origin (T1), Receive (T2), Transmit (T3) timestamps | used with client receive time T4 |

## Offset and delay
For a client request/response pair:
- delay = (T4 - T1) - (T3 - T2)
- offset = ((T2 - T1) + (T3 - T4)) / 2
T4 is the capture time of the response at the client (if capturing on the client). Check: with T1 = 0, T2 = 0.510,
T3 = 0.511 and T4 = 0.021 these formulas gave delay 0.02 s and offset 0.5 s, the values the test was built with;
the formulas are RFC 5905's theta and delta. `ntp.delta_time` ("Time between request and response") stayed empty for a
mode 3/4 pair in 4.4.1, so compute T4 - T1 from frame times instead. Fields `ntp.org`, `ntp.rec` and `ntp.xmt`
decode T1..T3; the filters above (mode, stratum 16, `ntp.flags.li == 3`, `ntp.refid == "RATE"`) all matched the
intended frames.

## Common findings
- No responses: UDP 123 blocked, or server restricts (`restrict` / KoD DENY).
- Responses with stratum 16 or LI=3: server itself unsynced; clients will reject it.
- `monlist` responses much larger than the requests from the internet: amplification abuse (CVE-2013-5211; the CISA
  alert recommends upgrading ntpd or adding `noquery` to the `restrict default` lines).
- Origin timestamp mismatch: the client discards the packet as bogus (RFC 5905 sanity check: origin must equal the
  client's transmit timestamp), sometimes due to NAT sending replies to the wrong client.

## Verify
- [ ] Computed offset roughly matches the offset your NTP client reports for the same server.
