---
id: transportation-logistics.railway-signalling.mechanical-signal-boxes.absolute-block-and-lever-frame-working
name: absolute-block-and-lever-frame-working
category: transportation-logistics
field: railway-signalling
product: mechanical-signal-boxes
tags: [mechanical-signal-boxes, signal-box, signal-cabin, interlocking-tower, lever-frame, mechanical-interlocking, signaller, signalman, absolute-block, block-instruments, block-bell, bell-codes, is-line-clear, train-entering-section, train-out-of-section, tyer-instruments, token-working, electric-token, tablet, single-line, train-register, tail-lamp, line-clear, heritage-railway]
level: practitioner
status: draft
description: "Work a mechanical lever-frame signal box under absolute block: bell codes, block instrument states, pulling levers in order, checking the tail lamp, and token exchange on single lines."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Absolute block and lever-frame working

**Goal:** pass trains safely between boxes so that only one train is ever in a block
section, using the bell, the block instrument and the frame in the correct order.

*Draft: modelled on British absolute-block practice (still used on parts of the
network and on heritage railways). Bell codes and regulations vary by railway and
era — always work from your box's instructions and the regulations you are passed on.*

## 1. The frame
- Levers are coloured by function (UK convention): **red** stop signals, **yellow**
  distant signals, **black** points, **blue** facing point locks, **white** spare.
  Check your box's lever diagram.
- **Mechanical interlocking** prevents conflicting levers: if a lever won't move,
  something else is reversed first. Never force a lever — that's the interlocking
  telling you something.
- Pulling order for a route: points → facing point lock → home/starting signals →
  distant (the distant last, since it can only clear when all stop signals ahead
  are off).
- Pull with a smooth full stroke; check the repeater/indicator shows the arm moved.

## 2. Block instrument states
Typically three: **Line Blocked** (normal), **Line Clear**, **Train On Line**. Only the
box *in advance* (receiving) can give Line Clear to the box in rear.

## 3. Passing a train (box A → box B)
1. A calls attention (1 beat); B acknowledges.
2. A offers the train with the correct bell code ("Is Line Clear?" for that class).
3. B checks the line is clear to its clearing point (the overlap beyond its home
   signal), repeats the code back, and sets its instrument to **Line Clear**.
4. A clears its section signal(s).
5. As the train passes A, A sends **Train Entering Section** (2 beats); B acknowledges
   and sets its instrument to **Train On Line**. A replaces signals behind the train.
6. B offers the train forward to C as appropriate.
7. When the train passes B complete **with tail lamp**, B sends **Train Out Of
   Section** (2-1 beats), sets its instrument to **Line Blocked**, and A acknowledges.

## 4. The tail lamp is the whole point
Before sending Train Out Of Section, **see the tail lamp** (or end-of-train marker).
No tail lamp = the train may have divided; part of it could still be in the section.
Don't give Line Clear for the next train; send the appropriate "train passed without
tail lamp" code and follow regulations.

## 5. Token working on single lines
- A single-line token (staff, tablet, key token) is the train's authority. Instruments
  between boxes release only one token at a time.
- Exchange: hand the token to the driver, who confirms it's for the right section
  (name engraved), and collect the incoming token. Never let a train leave without
  the correct token.

## 6. Train register
Record every bell signal and time in the train register as it happens, not later from
memory. It is the legal record and your memory aid.

## Gotchas
- Giving Line Clear before the previous train is out of section complete.
- Working the frame from habit with an unusual move (shunt, wrong-line) — re-read
  the lever leads before pulling.
- Ambiguous bell codes: if you're not sure what was sent, ask for it again.

## Verify
- [ ] Every train offered, accepted, entered and cleared with matching bell codes.
- [ ] Tail lamp seen before every Train Out Of Section.
- [ ] Register entries contemporaneous and complete.
- [ ] Correct token handed over for every single-line departure.
