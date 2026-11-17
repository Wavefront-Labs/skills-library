---
id: creative-arts.film-live-action.cinema-cameras.camera-build-and-on-set-data-management
name: camera-build-and-on-set-data-management
category: creative-arts
field: film-live-action
product: cinema-cameras
tags: [cinema-cameras, film-live-action, camera-assistant, 1st-ac, 2nd-ac, camera-build, camera-prep, rigging, matte-box, follow-focus, wireless-focus, lens-mount, pl-mount, ef-mount, lpl, v-mount, gold-mount, timecode, media-management, data-wrangling, dit, offload, checksum, xxhash, md5, mhl, ascmhl, silverstack, shotput-pro, hedge, 3-2-1-backup, camera-reports, arri, red, sony-venice, blackmagic, gimbal, dji-ronin, prep-checklist, rental-prep, camera-checkout, cable-management, mhl-manifest, checksum-verification, verification-report, offload-software, silverstack-use, shotput-use, card-recycling, card-formatting, card-labels, camera-report-writing, camera-log, report-fields]
level: practitioner
status: draft
description: "Prep and build a cinema camera reliably, then protect the footage: build order, power and balance, timecode, camera reports, and checksum-verified offloads with a 3-copy rule."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Camera build and on-set data management

**Goal:** a camera that works every take for 12 hours, and footage that cannot be lost.
On a set, a missing or corrupted card is the one mistake that can't be reshot cheaply.
Applies across ARRI, RED, Sony Venice/FX, Blackmagic and similar bodies; exact menus
differ by camera — check its manual.

## 1. Prep at the rental house (camera test day)
- Check every lens: mount, focus marks against a measured distance chart (back-focus /
  flange check), iris and focus rings smooth, no haze or scratches.
- Shoot a short test: each lens at wide-open, a framing chart, a skin/colour chart, and
  a black (cap on) clip to check sensor noise/hot pixels. Review on a calibrated monitor.
- Test every battery, cable, monitor and wireless link; format and test every card.
- Check firmware matches across bodies and the DIT's software supports it.

## 2. Build order (one habit, every time)
1. **Base:** baseplate and rods (15 mm LWS or 19 mm studio) on the tripod head or
   quick-release plate.
2. **Body** onto baseplate; **lens** into mount (support long lenses with a lens support).
3. **Top handle, viewfinder/monitor**, then **power** (V-mount/Gold-mount/B-mount plate)
   at the back as counterweight.
4. **Matte box** and filters, then **follow focus** or wireless focus motors (calibrate
   the lens map after mounting).
5. **Timecode box/jam, video transmitter, cable management** last — tidy with velcro.
6. **Balance** front to back on the head or gimbal; re-balance after any lens change.
Check: everything tight, nothing hanging, no cable crossing the lens or the operator's eye.

**Gimbals:** strip the build to the minimum (light lens, small monitor), balance each
axis with the motors off, then run auto-tune. Re-balance for any change in lens or accessory.

## 3. Timecode and slates
Jam sync the camera to the sound recorder's master clock (or a timecode box) at call
and after lunch/battery swaps; use time-of-day timecode, free run. Slate every take,
including MOS (no sound) noted on the slate. Smart slates display the same timecode.

## 4. Camera reports
Per roll/card: card ID, scene/shot/take, lens, stop, filters, fps, shutter, EI, white
balance, notes (circle takes, problems). The 2nd AC usually keeps them (paper or app) and
the DIT and editorial rely on them.

## 5. Data: offload safely
- **Never format a card until copies are verified.** Use a clear physical system: tape
  colour or labels for "full/not offloaded", "offloaded/ok to format".
- Offload with checksum-verifying software (e.g. Silverstack, ShotPut Pro, Hedge or
  similar), not drag-and-drop. They compare a hash (xxHash, MD5) of source and copy and
  write a report; **ASC MHL** is the industry manifest format for this.
- **3 copies on 2 different media types/locations** is a common baseline (e.g. two drives
  on set + one sent to editorial/stored offsite). The production may specify more.
- Name folders by date/shoot day and card/roll name exactly as the camera labels it.
- Check a sample of clips play (and look right) after offload; verify card count matches
  camera reports.
- Only then return the card to the 1st/2nd AC for formatting **in the camera**.

## Gotchas
- Formatting a card from the wrong pile — the classic data-loss story. Separate,
  labelled piles; one person formats.
- Running out of disk on set: estimate data rate × hours (codec and resolution make this
  vary by an order of magnitude) and bring drive space for the whole shoot plus margin.
- Drifting timecode after power loss; re-jam.
- Cold or heat: batteries drain fast in cold; cameras overheat in sun — shade and fans.

## Verify
- [ ] All lenses checked for back-focus and marks; test footage reviewed.
- [ ] Build order followed; rig balanced; cables managed.
- [ ] Timecode jammed and re-jammed after power changes; every take slated.
- [ ] Camera reports complete and matching the cards.
- [ ] Every card has 3 checksum-verified copies before formatting.
