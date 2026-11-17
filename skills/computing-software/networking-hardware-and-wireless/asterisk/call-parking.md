---
id: computing-software.networking-hardware-and-wireless.asterisk.call-parking
name: call-parking
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, call-parking, res-parking, parkingtime, comebacktoorigin, parkcall, features]
level: practitioner
status: docs-checked
description: "Configure call parking with res_parking.conf (parkext, parkpos, context, parkingtime, comebacktoorigin), park-and-retrieve flows, and what happens when parked calls time out."
sources:
  - https://docs.asterisk.org/Configuration/Features/Call-Parking/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# call parking
Parking lets a party put the other participants on hold, hang up, and have the call retrieved elsewhere. From Asterisk 12 parking is the loadable module `res_parking`, configured in `res_parking.conf`. It uses the configuration framework: an invalid configuration makes the module fail to load or reload.

Settings shown on the page:
- `parkext` (default extension to park calls), `parkpos` (range of parking extensions, e.g. 701-709), `context` (where those extensions live).
- `parkingtime` (seconds before timeout), `findslot` (slot selection, e.g. `next`).
- `comebacktoorigin` and `comebackdialtime`: with `yes`, a timed-out call goes back to the party that parked it and rings for `comebackdialtime` seconds; if unanswered, the `t` extension in the `park-dial` context runs. With `no`, the call goes to a configured timeout context (`parkedcallstimeout` in the example).

One-touch parking uses `parkcall` in `[featuremap]` of `features.conf` plus the Dial options `k` (called party) or `K` (caller). Retrieval is by dialing the parking extension the caller was told.

Page examples need edits to `res_parking.conf`, `features.conf` and `extensions.conf`.

## Checked
2026-11-04: read the cited Asterisk documentation pages (Call-Parking) and confirmed the commands, options, defaults and names stated above. Dial/Queue option wording narrowed to Dial.

Method: documentation only; no commands were run.
