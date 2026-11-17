---
id: computing-software.networking-hardware-and-wireless.asterisk.cdr-lifecycle-and-party-selection
name: cdr-lifecycle-and-party-selection
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, cdr, call-detail-records, party-a, party-b, linkedid, bridge, dial, dispatch]
level: advanced
status: docs-checked
description: "Understand how Asterisk CDRs are created, forked, finalized and dispatched, why one call yields several records, and how Party A and Party B are chosen."
sources:
  - https://docs.asterisk.org/Configuration/Reporting/Call-Detail-Records-CDR/CDR-Specification/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CDR lifecycle and party selection
The specification applies to Asterisk 12 and later. A CDR always describes one path of communication between **Party A** (the owner; the record is its view) and **Party B** (the target). Depending on dialing and bridging, one call produces multiple CDRs, so post-processing is needed for overall call statistics. CEL is the alternative when CDRs cannot meet billing needs.

States: Single (default), Dial, Bridge, Finalized, Dispatched.

A CDR is created when a channel is created, when a channel leaves a bridge without hanging up, when forked, when a channel enters a multi-party bridge, and when a channel dials more than one channel (one CDR per dial attempt). It inherits `uniqueid` and `linkedid` from Party A and gets a new `sequence`.

Finalized when a dial ends with a status other than ANSWER, when either party leaves the bridge, when either hangs up, or when a fork says so. Finalized CDRs cannot be modified. When Party A hangs up, all its CDRs are dispatched to the backends.

Pairing rule: keep using a channel's existing CDR as long as possible, and make CDRs for all pairings in a bridge (a three-way call gives three records).

Choosing Party A:
1. A dialed (not originated) channel is always Party B.
2. Otherwise the channel with the `party_a` flag (set via the CDR function).
3. Otherwise the oldest channel.

`linkedid`: the oldest wins when channels bridge; dialed channels inherit the caller's.

## Checked
2026-11-04: read the cited Asterisk documentation pages (CDR-Specification) and confirmed the commands, options, defaults and names stated above. Nothing removed; every claim was confirmed.

Method: documentation only; no commands were run.
