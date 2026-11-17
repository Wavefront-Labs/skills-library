---
id: media-communication.broadcasting.live-production.running-orders-gallery-calling-and-on-air-recovery
name: running-orders-gallery-calling-and-on-air-recovery
category: media-communication
field: broadcasting
product: live-production
tags: [live-production, live-tv, broadcast-production, producer, director, gallery, control-room, pcr, running-order, rundown, enps, inews, octopus, gallery-calling, standby, cue, timing, backtiming, hard-out, under-over, floor-manager, pa, production-assistant, on-air-recovery, contingency, breaking-news, broadcasting]
level: advanced
status: draft
description: "Produce and direct live output: build a timed running order, call the gallery with standby/go discipline, backtime to hard outs, and recover on air from failed items without panic."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Running orders, gallery calling and on-air recovery

**Goal:** a live programme that comes off air within seconds of its slot, where every
failure is covered so smoothly the viewer never notices.

## 1. The running order (rundown)
Built in the newsroom system (ENPS, iNEWS, Octopus or similar) or a spreadsheet. Each
item line has:
- Item number and slug, **type** (live intro, package, VT, live two-way, studio
  interview, graphics, ad break), **source** (camera, VT server, line/feed ID).
- **Duration** (planned) and **cumulative/backtime** column — the time each item must
  start to land the hard out.
- Presenter, script status, graphics/strap requirements, and notes.
- **Floats and drops:** mark which items can be dropped or shortened (with their duration)
  and an emergency **filler** item.

Gotcha: the planned total should come in a little *under* the slot; live items almost
always over-run.

## 2. The gallery team
Typically: director (calls shots), producer/editor (editorial decisions, talks to
presenter), PA/timing (counts in and out, backtimes), vision mixer, sound, graphics,
VT/playout, lighting and floor manager. Roles merge on smaller productions.
**One voice calls shots; one voice talks to the presenter.** Mixed messages in a
presenter's ear are the most common self-inflicted error.

## 3. Calling discipline
- **Standby, then go.** "Standby VT 3… roll VT 3." "Standby camera 2… cut 2."
  Standby gives the operator time; go is the instant.
- Pre-roll: give VT its run-up if your playout needs one (often zero with modern
  servers, but know your system).
- Count presenters in and out of VTs: "30… 10… 5, 4, 3…" then hand signals from the
  floor manager for the last seconds (practice varies).
- Talk only when necessary. Silence in a gallery is a sign it's going well.
- Exact phrasing differs between broadcasters and countries; learn your house's calls.

## 4. Timing to the second
- The PA/timer tracks **under/over** continuously against the backtime column.
- Decide drops **early** — at the halfway point, not in the last item. Shorten the
  flexible items (studio chat, round-ups), not the packaged ones.
- The final item before the hard out is often a flexible one so it can absorb error.
- Use a backtimed closing sequence (headline recap, credits) of known duration.

## 5. On-air recovery
Pre-agree the **contingency** for each risky item before air:
| Failure | Standard recovery |
|---|---|
| VT/package fails to roll | Cut back to presenter; "We'll bring you that report later"; go to next item |
| Live line drops | Presenter thanks correspondent, summarises; go to next item; re-establish if possible |
| Guest late/missing | Move them down the order; pull a float forward |
| Wrong graphic/strap on air | Take it off immediately; correct verbally if it named someone wrongly |
| Prompter dies | Presenter to paper script |
| Total gallery failure | Emergency slide/holding loop and continuity as per station procedure |

Rules: **keep the presenter informed in short, calm instructions**, never blame on talkback,
and always know your next item before you need it.

## 6. After air
Debrief within the hour: what failed, root cause, change for next time. Log technical
faults with engineering. Note compliance issues (a defamatory remark, unconfirmed claim)
and whether an on-air correction is needed.

## Verify
- [ ] Running order shows durations, backtimes, sources, floats and filler.
- [ ] Contingency agreed for every live and VT item.
- [ ] One caller for shots, one voice for the presenter.
- [ ] Programme came off within a few seconds of the hard out.
- [ ] Debrief done and faults logged.
