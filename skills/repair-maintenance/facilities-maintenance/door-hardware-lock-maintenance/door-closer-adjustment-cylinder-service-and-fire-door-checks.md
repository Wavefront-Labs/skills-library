---
id: repair-maintenance.facilities-maintenance.door-hardware-lock-maintenance.door-closer-adjustment-cylinder-service-and-fire-door-checks
name: door-closer-adjustment-cylinder-service-and-fire-door-checks
category: repair-maintenance
field: facilities-maintenance
product: door-hardware-lock-maintenance
tags: [door-hardware-lock-maintenance, door-closer, overhead-closer, closing-speed, latching-speed, backcheck, fire-door, fire-door-inspection, intumescent-seal, smoke-seal, panic-bar, panic-hardware, exit-device, push-bar, lock-cylinder, euro-cylinder, rekeying, master-key, hinge, door-alignment, access-control, maglock, dorma, allegion]
level: practitioner
status: docs-checked
description: "Adjust door closers (sweep, latch, backcheck), service lock cylinders and panic hardware, fix hinge sag and alignment, and run routine fire door checks without voiding certification."
sources: ["https://www.access-board.gov/ada/chapter/ch04/", "https://www.ada.gov/law-and-regs/design-standards/2010-stds/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Door closers, cylinders, panic hardware and fire door checks

**Goal:** doors that close and latch every time, open with reasonable force, lock and
unlock smoothly, and — for fire and escape doors — still do their life-safety job
after you have worked on them.

## 1. Start with the door, not the closer
Most "closer faults" are door faults. Before adjusting:
1. Open the door 90° and let go from several points: does it bind, rub or bounce?
2. Check hinges: loose or missing screws on the top hinge cause sag; worn knuckles
   show as a vertical drop at the lock edge. Replace screws with longer ones into the
   frame; replace worn hinges like for like (on fire doors, same rating and number).
3. Check gaps are even and within the limits in the door's own certification data
   (limits differ by standard — e.g. UK BS 8214, US NFPA 80).
4. Check the latch meets the strike: file the strike opening or reposition the keep
   rather than slamming the door with a stronger closer.

## 2. Adjusting an overhead closer
Typical valves (usually on the closer body, marked S, L and BC — check the maker's
sheet):
- **Sweep/closing speed (S):** controls travel from fully open to about 10–15° open.
  Under the 2010 ADA Standards (404.2.8) the door must take at least 5 seconds to move
  from 90° to 12° from the latch; set it slower where users need more time.
- **Latch speed (L):** the last 10–15°. Speed it up just enough to overcome seals and
  latch reliably, without a slam.
- **Backcheck (BC):** cushions opening beyond ~70° to protect the frame and wall.
- **Spring power:** set by size/adjuster nut; fire doors need enough power to close
  and latch from any angle, but opening force should stay reasonable for accessibility.
  (Under the 2010 ADA Standards 404.2.9, interior hinged doors are limited to 5 lbf
  opening force; fire doors use the minimum the authority having jurisdiction allows.
  Other jurisdictions set their own limits.)
Turn valves 1/8–1/4 turn at a time; clockwise usually slows. Never back a valve fully
out — it leaks oil and the closer must be replaced. An oil-leaking closer is scrap.

## 3. Lock cylinders and rekeying
- Stiff key: clean with dry PTFE or graphite lubricant; never use oil, which gathers
  dust. Spray, cycle the key 10 times, wipe.
- Euro cylinders: measure from the centre of the fixing screw to each face (e.g.
  35/35, 40/50). Fit so it does not protrude beyond the handle/escutcheon,
  and fit anti-snap rated types on external doors.
- Rekeying master-keyed systems is done by the system holder or locksmith using the
  key plan; record every change against the key register. Restricted keyways cannot be
  cut by you.

## 4. Panic and push-bar hardware
- Test monthly: the bar releases with a single push, the door opens fully, and the
  latch re-engages when closed. Vertical rod devices: check top and bottom bolts
  retract fully and the bottom bolt is not catching on flooring.
- Never add padlocks, chains or extra bolts to an escape door; never disable dogging
  rules set by the fire plan.
- Access-controlled doors (maglocks, electric strikes) must fail-safe and release on
  fire alarm and the green break-glass. Test with the security/fire contractor, not
  by cutting power.

## 5. Routine fire door checks (e.g. quarterly)
Check: label/certification plug present; leaf, frame and glazing undamaged;
intumescent and smoke seals continuous and unpainted; the hinges the certification specifies, all screws
present; closer shuts and latches the door from fully open; gaps within limits; no wedges
or hold-opens other than alarm-linked ones; hardware is fire-rated (often CE/UKCA
marked or listed). Log each door in the CMMS by asset ID.

## Gotchas
- Drilling, planing or adding hardware to a fire door can void its certification;
  repairs beyond like-for-like go to a certified installer.
- Painting over intumescent strips stops them working.
- Over-powered closers fail accessibility and break frames; under-powered ones fail
  fire safety. Adjust, don't swap.

## Verify
- [ ] Door closes and latches from 90°, 45° and 15° without slamming.
- [ ] Closing time meets the applicable standard (ADA: at least 5 s from 90° to 12°); opening force acceptable.
- [ ] Keys turn smoothly; key register updated after any cylinder change.
- [ ] Panic devices release with one push and re-latch.
- [ ] Fire door checks logged with defects raised as work orders.

## Checked

Date checked: 2026-10-25. Jurisdiction: United States (2010 ADA Standards 404.2.8 and 404.2.9); fire door limits come from the door's own certification (NFPA 80, BS 8214).
2010 ADA Standards via Access Board and ADA.gov (search results): door closers must be adjusted so the door takes at least 5 seconds to move from 90 degrees to 12 degrees from the latch (404.2.8.1); interior hinged doors are limited to 5 lbf opening force while fire doors use the minimum the authority having jurisdiction allows (404.2.9). The earlier 3 to 7 second sweep and 30 N UK figure did not match and were removed. Gap sizes, cylinder protrusion and hinge counts for fire doors were replaced by a deferral to the door's certification data.

Method: documentation only; no commands were run.
