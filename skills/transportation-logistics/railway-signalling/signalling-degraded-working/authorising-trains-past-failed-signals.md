---
id: transportation-logistics.railway-signalling.signalling-degraded-working.authorising-trains-past-failed-signals
name: authorising-trains-past-failed-signals
category: transportation-logistics
field: railway-signalling
product: signalling-degraded-working
tags: [signalling-degraded-working, degraded-working, signal-failure, track-circuit-failure, axle-counter-failure, points-failure, authority-to-pass-signal-at-danger, pass-signal-at-danger, spad-authority, permissive-working, caution-working, temporary-block-working, tbw, pilotman, hand-points, clipping-points, scotching-points, points-secured, safety-critical-communications, read-back, phonetic-alphabet, incident-log, occurrence-book, signaller, dispatcher]
level: advanced
status: draft
description: "Keep trains moving safely through a signalling failure: confirm the line ahead is clear, authorise drivers past signals at danger with exact wording, secure points, and set up temporary block working."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Authorising trains past failed signals

**Goal:** when the signalling can no longer prove the line is clear, you prove it by
other means — and give each driver an unambiguous, recorded authority.

*Draft: exact forms of words, permitted speeds and the conditions for each method
are set by the rulebook (UK, North American, European networks all differ). This
is the reasoning common to them; do not use it as the rule text.*

## 1. Establish what has failed
- Signal can't clear: is it a **lamp/aspect failure** (line likely clear) or a
  **train-detection failure** (track circuit/axle counter showing occupied — there may
  be a train or obstruction)? The method differs.
- Points: detected? If not, they must be examined and **secured** (clipped and padlocked
  or scotched) in the required position by competent staff before a train runs over
  them in the facing direction.
- Log the failure time, call technicians, inform control.

## 2. Prove the line is clear
Before authorising a train past a signal at danger, establish as far as possible that:
- the previous train has passed clear (complete, with tail lamp where you can check),
- no other authority (possession, line blockage, another train) overlaps the section,
- points on the route are set, detected or secured.
If you can't prove the section clear (e.g. track circuit failure with no way to check),
the driver proceeds at caution — prepared to stop short of any obstruction.

## 3. Giving the authority — safety-critical communication
1. Identify yourself, your box/workstation, and confirm the driver's **train
   identity and exact signal number** — the most common error is authorising the wrong
   train or at the wrong signal.
2. Explain why ("signal 123 has failed, track circuit showing occupied").
3. Give the authority in your rule's set wording, including any speed/caution
   instructions and how far it extends (to the next signal only).
4. **Driver reads back**; you confirm only if exact. Use the phonetic alphabet for
   letters/headcodes.
5. Record each authority (time, train, signal, driver) in the log.

## 4. Temporary block working (extended failures)
When many signals or a whole area fail, switch from train-by-train authority to a
block system: staff (handsignallers / block posts) at key points, one train in each
block at a time, train-out-of-section confirmations exchanged between posts. Set it
up with control, brief everyone, and keep a running train register.

## 5. Ending degraded working
When technicians hand the equipment back: test-run a route, confirm normal indications,
and tell everyone (drivers, control, block posts) the moment you revert. Keep the old
arrangement until everyone has acknowledged.

## Gotchas
- Authorising a train past a signal when the "failed" track circuit is actually
  occupied by a failed train or a broken rail.
- Assuming points are correctly set because the panel says so — not if detection is lost.
- Shortcutting the read-back under delay pressure. Errors are made at the 20th train,
  not the first.

## Verify
- [ ] Failure type identified (aspect vs detection vs points) before choosing a method.
- [ ] Each authority to the correct train at the correct signal, read back and logged.
- [ ] Facing points examined and secured before use.
- [ ] Reversion to normal working communicated and acknowledged.
