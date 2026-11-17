---
id: natural-sciences.physics.optics-photonics.two-mirror-beam-walking-alignment
name: two-mirror-beam-walking-alignment
category: natural-sciences
field: physics
product: optics-photonics
tags: [optics-photonics, optics, laser-alignment, beam-walking, beam-steering, kinematic-mirror-mount, irises, optical-table, breadboard, beam-height, fibre-coupling, fiber-coupling, single-mode-fiber, mode-matching, interferometer-alignment, ir-viewer, ir-card, beam-profiler, laser-safety, laser-goggles, od-rating, near-field, far-field, collimation, shear-plate]
level: practitioner
status: gated
description: "Align a laser beam onto a target axis with two steering mirrors (beam walking): irises, near/far points, convergence, fibre coupling, and laser safety."
sources: ["Thorlabs and Newport application notes on beam steering and fiber coupling", "ANSI Z136.1 Safe Use of Lasers / IEC 60825-1"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Two-mirror beam walking

**Goal:** put a laser beam on a defined axis (position *and* angle) — through two
irises, into a fibre, or down an interferometer arm — quickly and repeatably.

## 0. Safety first (non-negotiable)
- Wear eyewear rated for the wavelength **and** power (check the OD on the goggle
  label at your λ). Visible-laser alignment goggles that let some light through
  exist for Class 3B work; follow your lab's laser safety officer.
- Align at the lowest power that you can see (attenuate, or turn the diode current down).
- Keep beams horizontal at a fixed height, below eye level; block every stray
  reflection with beam blocks/dumps. Remove watches and rings. Never bend down to
  table height with the beam on.
- For IR, use a viewer card or IR viewer — never look for the beam directly.

## 1. Set up the reference axis
- Pick a beam height (e.g. 75–125 mm) and keep it everywhere; post holders make it repeatable.
- Place two irises on the target axis, as far apart as possible (longer baseline =
  better angle definition). Centre them with a ruler/grid on the table holes.
- Two steering mirrors upstream, M1 then M2, each in a kinematic mount, roughly at
  45°, with the beam centred on both and mounts near mid-travel.

## 2. The walk
1. Using **M1**, put the beam through the centre of the **near** iris (I1).
2. Using **M2**, put the beam through the centre of the **far** iris (I2).
3. Repeat. Each iteration should get closer. If it converges slowly, **overshoot**:
   when you adjust M2 to fix I2, deliberately go past centre by roughly the same
   amount again (the exact factor depends on distances), then fix I1 with M1.
4. Do horizontal and vertical separately if it helps.
If it diverges, you have the mirror-iris pairing backwards: the **upstream** mirror
(M1) must correct the **near** iris and the downstream mirror (M2) the **far** iris.
The reverse pairing makes each correction undo more than it fixes (checked with a linear ray model, M1-M2 0.3 m, M2-I1 0.2 m, I1-I2 1 m: the stated pairing halves the error each round, the reverse grows about 2x each round).

## 3. Fibre coupling (single-mode) variant
- Rough-align the beam onto the fibre axis with irises or by back-propagating a
  visible laser from the fibre's far end (very effective).
- Match the focused spot to the fibre mode field diameter: choose lens focal length
  f ≈ π·w_in·MFD/(2λ) (algebra from w0 = λf/(π·w_in), MFD = 2·w0) (w_in = input beam 1/e² radius). A mismatch caps coupling.
- Walk with the two mirrors while watching a power meter; then adjust lens focus
  (z), re-walk, repeat. 60–80% is good for a Gaussian beam into SMF; >85% needs
  careful mode matching. Below ~30% usually means the focus is wrong or the beam is far off axis (gated: unconfirmed, source is paywalled or blocked). For reference, a pure waist-size mismatch of 1.2x or 1.5x limits coupling to 96.7 % or 85.2 % (4r²/(1+r²)², computed).

## 4. Check collimation and the result
- Collimation: beam diameter equal at near and far (a few metres), or use a shear plate.
- Lock mount screws (lock nuts) gently and re-check; locking often moves the beam.
- Mark beam positions on cards or irises for future re-alignment.

## Gotchas
- Mirrors far off 45° cause polarisation changes and astigmatism; keep angles small.
- Long, thin posts and spring-loaded mounts drift; use short pedestal posts, clamp
  forks, and let thermal transients settle (laser warm-up 15–30 min (gated: unconfirmed, source is paywalled or blocked).
- Back-reflections into a laser (especially diode or fibre-coupled) destabilise it;
  slightly tilt optics or add an isolator.
- *Uncertainty note:* the coupling percentages above are typical for a well-matched
  Gaussian beam; real figures depend on beam quality (M²) and fibre type.

## Verify
- [ ] Beam centred on both irises without readjusting either mirror between checks.
- [ ] Beam height constant along the path (check with a ruler at each optic).
- [ ] Fibre coupling (if used) stable over several minutes and after locking screws.
- [ ] All stray reflections blocked; eyewear rated for the λ and power in use.
