---
id: computing-software.networking-hardware-and-wireless.asterisk.pjsip-advanced-codec-negotiation
name: pjsip-advanced-codec-negotiation
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, pjsip, codec, sdp, codec-prefs, negotiation, transcode, topology]
level: advanced
status: docs-checked
description: "Tune PJSIP codec negotiation with the four codec_prefs_* endpoint parameters and their prefer, operation, keep and transcode settings across offer and answer stages."
sources:
  - https://docs.asterisk.org/Configuration/Channel-Drivers/SIP/Configuring-res_pjsip/PJSIP-Advanced-Codec-Negotiation/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pjsip advanced codec negotiation
Asterisk is a back-to-back user agent, so each leg negotiates separately. A "pending" topology (from the SDP or the core) is resolved against the endpoint's "configured" topology (its `allow` list) at four points, each with its own endpoint parameter:
`codec_prefs_incoming_offer`, `codec_prefs_outgoing_offer`, `codec_prefs_incoming_answer`, `codec_prefs_outgoing_answer`.

Values are comma-separated `name: value` pairs:
- `prefer`: `pending` or `configured`, whose order is preferred.
- `operation`: `union` (preferred order, then extras from the other), `intersect` (only codecs in both), `only_preferred`, `only_nonpreferred`.
- `keep`: `all` or `first`.
- `transcode`: `allow` the call even with no codecs, or `prevent` it.

Defaults shown on the page (with `allow = !all,g722,ulaw`):
- incoming_offer: `prefer: pending, operation: union, keep: all, transcode: allow`
- outgoing_offer: `prefer: pending, operation: intersect, keep: all, transcode: allow`

Because the defaults prefer pending, the caller's SDP offer order sets the stage. The page states the feature is incomplete for direct media, 100rel/early media, re-invites, fax, multi-stream and deferred SDP.

## Checked

2026-11-09. Confirmed against the Asterisk PJSIP Advanced Codec Negotiation page: four control points and parameter names, prefer, operation, keep and transcode values, the two defaults shown, and the list of unfinished areas. Nothing changed.
Method: documentation only; no commands were run.
