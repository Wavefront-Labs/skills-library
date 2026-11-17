---
id: manufacturing-production.packaging-operations.form-fill-seal.threading-splicing-and-setting-seal-jaws-on-a-vffs
name: threading-splicing-and-setting-seal-jaws-on-a-vffs
category: manufacturing-production
field: packaging-operations
product: form-fill-seal
tags: [form-fill-seal, packaging-operations, vffs, vertical-form-fill-seal, hffs, horizontal-form-fill-seal, flow-wrapper, bagger, pouch, film-threading, film-splicing, splice, reel-change, forming-tube, forming-collar, seal-jaws, jaw-temperature, dwell-time, seal-pressure, fin-seal, lap-seal, registration, print-mark, eye-mark, film-tracking, laminate, bopp, multihead-weigher]
level: practitioner
status: draft
description: "Run a vertical form-fill-seal bagger: thread film over the collar, splice reels, register the print mark, set jaw temperature/dwell/pressure, keep film tracking, and fix common bag defects."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Threading, splicing and setting seal jaws on a VFFS

**Goal:** turn a reel of film into well-sealed, correctly printed bags at rate on a
vertical form-fill-seal (VFFS) machine. Horizontal FFS (flow wrappers) share the same
seal and registration principles with a different film path.

**How it works:** film unwinds from the reel, over dancer and guide rollers, round the
**forming collar** onto the **forming tube**; a vertical (back) sealer makes a fin or lap
seal; pull belts draw film down a bag length; product drops through the tube (often from
a multihead weigher); horizontal **jaws** seal the top of one bag and bottom of the
next and the knife separates them.

## 1. Threading
- Isolate the machine (LOTO) and let jaws cool — they run around 100–200 °C.
- Follow the **threading diagram** on the machine (usually on a plate or the HMI). Film
  print side and direction matter: wrong way round = print inside the bag or upside
  down.
- Keep film flat and centred over each roller; a crease at the collar becomes a
  channel leak in the back seal.
- Easiest after a reel run-out is to splice the new reel onto the tail of the old one
  still threaded (section 2) rather than re-thread from scratch.

## 2. Splicing a new reel
- Cut both ends square, overlap them, and tape across with **splice tape** on the side
  that doesn't contact the sealing elements (check what your machine wants).
- Match print registration across the splice if you can.
- Bags containing the splice must be **rejected** — many machines detect it with a
  sensor; otherwise mark and pull by hand.
- Check the new reel's label: same film spec, lot recorded for traceability.

## 3. Registration (print in the right place)
- A **registration (eye-mark) sensor** reads a printed mark each bag length and
  corrects pull length so the print sits in the same position.
- Teach the sensor on the mark vs background (most need a fresh teach on a new film
  design or colour). If print drifts, check sensor alignment with the mark lane,
  dirty lens, and the bag length setpoint being close to the print repeat.

## 4. Seal jaws: temperature, dwell, pressure
- Start from the **film supplier's seal window** (minimum seal-initiation temp to
  maximum before distortion/burn). Laminates such as BOPP/CPP or PET/PE have different
  windows.
- Set temperature, then **dwell** (jaw closed time) and **pressure**. At higher speeds
  dwell drops, so temperature may need to rise within the window.
- Check temperature with a calibrated contact probe on the jaw face occasionally — the
  thermocouple display reads inside the jaw, not at the surface.
- Jaw faces: clean, matching serrations, parallel; a worn or misaligned jaw gives a weak
  seal on one side.
- **Product in the seal** is the commonest leak: time the jaw close after product has
  dropped (adjust the weigher discharge timing), use a stripper/settling device,
  reduce dust.

## 5. Film tracking
Film wandering on the tube makes the back seal miss or overlap. Causes: reel not
centred on the shaft, dancer tension wrong, collar dirty/damaged, film with uneven
thickness (supplier issue). Use the film edge-guide/tracking adjust in small steps
and wait several bags for it to settle.

## 6. Fault finder
| Defect | Likely cause |
|---|---|
| Leaking top/bottom seal | Product in seal, temp/dwell too low, worn jaws |
| Burnt or puckered seal | Temp too high or dwell too long |
| Leaking back seal | Film tracking, crease at collar, back-seal temp |
| Print off-position | Registration sensor, wrong bag length |
| Short/heavy bags | Weigher, timing, product bridging in the tube |

## Verify
- [ ] Threaded per the diagram; print correct side and orientation.
- [ ] Splice bags rejected; reel lot recorded.
- [ ] Registration taught; print within tolerance over 20+ bags.
- [ ] Seal settings within the film's window; squeeze or bubble test passed.
- [ ] Back seal centred and continuous.

*Uncertain: temperature ranges are typical, not universal — always use the film data
sheet.*
