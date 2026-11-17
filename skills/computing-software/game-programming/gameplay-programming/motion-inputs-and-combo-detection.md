---
id: computing-software.game-programming.gameplay-programming.motion-inputs-and-combo-detection
name: motion-inputs-and-combo-detection
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, input-system, motion-inputs, input-buffering, fighting-game-input, game-programming]
level: practitioner
status: draft
description: "Detect fighting-game motion inputs (quarter circles, dragon punch, charge, double taps) and combos with an input history buffer, leniency windows and priority rules."
sources: ["https://www.dustloop.com/w/Notation", "https://andrea-jens.medium.com/i-wanna-make-a-fighting-game-a-practical-guide-for-beginners-part-6-311c51ab21c4"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Motion inputs and combo detection

**Goal:** 236P, 623P, [4]6P charges and dash double-taps recognised reliably at 60 Hz, with lenient
but unambiguous rules.

## Input history buffer
Record per **frame** (fixed tick): stick direction in numpad notation (1-9, 5 = neutral, relative to
facing) and button press/release edges. Keep ~60 frames in a ring buffer.
```csharp
struct FrameInput { public byte dir; public Buttons pressed, held; }
RingBuffer<FrameInput> history = new(60);
```
Facing-relative: mirror left/right (4<->6, 1<->3, 7<->9) when facing left — at input time per frame
(commonly the facing when the motion started; decide and be consistent).

## Matching a motion
Search backwards from the button press frame for the motion's directions in reverse order, within a
total window:
```csharp
bool Match(int[] seq, int windowFrames, int pressFrame) {
    int si = seq.Length - 1;
    for (int f = pressFrame; f >= pressFrame - windowFrames && si >= 0; f--)
        if (history[f].dir == seq[si] || Lenient(seq[si], history[f].dir)) si--;
    return si < 0;
}
// 236: {2,3,6} within ~12-15 frames; 623: {6,2,3} within ~15; 41236: within ~20
```
Leniency: accept 1 or 3 for 2 in some motions, allow skipping diagonals (2,6 for 236 on pads), allow
the button within a few frames after the final direction.

## Charge
Track how many consecutive frames a direction (4, 1, 7 for back-charge) was held; on release + forward
+ button within N frames, fire if charge >= threshold (~30-45 frames). Keep charge briefly after release
(a few frames) for leniency.

## Priority and conflicts
- Check complex motions before simple: 623 before 236, 236236 before 236, then normals.
- Shortcuts: 6236 may read as 623 — common accepted behaviour (Street Fighter), decide explicitly.
- Negative edge (button release triggers specials) optional.

## Combos and cancel windows
Combos are mostly game-state: attack frame data defines cancel windows; buffered inputs during
recovery are checked when the window opens (input buffer ~3-8 frames).

## Gotchas
- Variable frame rate input sampling breaks timing; sample on the fixed simulation tick.
- Pad d-pads vs sticks: stick deadzones produce diagonal noise; quantise with angle sectors and
  hysteresis.
- Rollback netcode requires input processing to be deterministic and part of the simulation state.

## Verify
- [ ] Automated tests feed recorded input sequences and assert recognised moves.
- [ ] Training mode input display shows history and recognised motion.
