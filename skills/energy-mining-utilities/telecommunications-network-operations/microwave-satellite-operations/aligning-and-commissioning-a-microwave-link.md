---
id: energy-mining-utilities.telecommunications-network-operations.microwave-satellite-operations.aligning-and-commissioning-a-microwave-link
name: aligning-and-commissioning-a-microwave-link
category: energy-mining-utilities
field: telecommunications-network-operations
product: microwave-satellite-operations
tags: [microwave-satellite-operations, telecommunications-network-operations, microwave-link, point-to-point, ptp, backhaul, dish-alignment, antenna-alignment, rsl, received-signal-level, side-lobe, main-lobe, polarisation, xpic, xpd, fade-margin, link-budget, odu, idu, ericsson-minilink, nokia-wavence, aviat, ceragon, ber-test, rfc-2544, commissioning, interference, frequency-licence]
level: practitioner
status: draft
description: "Align a point-to-point microwave dish pair onto the main lobe, hit the planned RSL, set polarisation, then prove the link with error tests and record the commissioning values."
sources: ["Radio vendor installation guides (Ericsson MINI-LINK, Nokia Wavence, Aviat, Ceragon — general practice)", "ITU-R P.530 (fade margin concepts)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Aligning and commissioning a microwave link

**Goal:** bring up a licensed point-to-point microwave link so that both ends are on the
**main lobe** of each other's antenna, received signal level (RSL) is within ~2–3 dB
of the planned value, polarisation is right and the link passes an error test —
and leave a record the NOC can compare against later. Path design and fade margin
are covered in
engineering-technology.telecommunications-engineering.rf-link-budget.point-to-point-link-budget.

## 1. Before going up
- **Link plan:** site coordinates, azimuth (true), elevation, antenna size, frequency
  channel and polarisation from the licence, transmit power, **expected RSL** at each end.
- Confirm magnetic declination to convert true to magnetic bearing for the compass,
  or use a GPS/alignment tool. Check for nearby steel that deflects a compass.
- Radios configured with the licensed channel and power; both ends agreed on
  ATPC (automatic transmit power control) **off** during alignment so power is fixed.
- Two crews, one at each end, with phones/radios. Tower-work rules apply
  (energy-mining-utilities.telecommunications-network-operations.tower-work.climbing-a-telecom-tower-with-full-fall-protection).

## 2. Rough alignment
- Mount the antenna plumb on the pole. Set azimuth by compass/landmark/sighting and
  elevation by inclinometer.
- Power both ends. Most ODUs give an **RSL voltage** at a BNC/test port (mapping in the
  manual, e.g. volts proportional to dBm) or a reading in the web/craft tool.

## 3. Fine alignment — find the main lobe
1. **One end at a time.** End B holds still while A pans.
2. Pan azimuth slowly across a wide arc, noting RSL peaks. You'll see a big peak
   (main lobe) and smaller peaks either side (side lobes), typically 15–25 dB down.
3. A peak **far below** the expected RSL is probably a side lobe. Keep panning until
   you find one within a few dB of expected.
4. Peak azimuth, lock it, then peak elevation, then azimuth again.
5. Swap: A holds, B peaks. Repeat until neither end can improve by more than ~0.5 dB.
6. Torque the fine-adjust bolts while watching RSL — tightening can shift the dish.

## 4. Polarisation and XPIC
- Confirm both ends match the licensed polarisation (V or H); a 90° error costs
  20–30 dB.
- For dual-polarisation links with **XPIC**, align carefully and measure cross-polar
  discrimination (XPD); a commonly expected value is >25–30 dB, but use the
  vendor figure.

## 5. Commission
- Re-enable ATPC and adaptive modulation as designed.
- Record at both ends: RSL, transmit power, modulation, MSE/SNR, XPD.
- **Error test:** a BER test or Ethernet RFC 2544 / Y.1564 test for an agreed period
  (often 15 minutes for basic, 24 hours for acceptance). Zero errors expected under
  clear conditions.
- Check for interference: with the far-end transmitter muted, the receiver should
  see only noise floor. A strong signal means someone else is on your channel.
- Photograph mounts, labels and weatherproofing; send results to the NOC.

## Gotchas
- RSL 15–20 dB low but stable = side lobe. Don't accept it as "the path is longer than
  planned".
- Rain fades are normal; a link that's error-free in clear sky and fails in moderate
  rain probably lacks fade margin or has a misalignment.
- Wind-induced twist on tall poles shows as fluctuating RSL — check mount rigidity.
- Uncertain: RSL voltage scale, XPD targets and test durations vary by vendor and
  operator; use the job spec.

## Verify
- [ ] Both ends on main lobe; RSL within ~2–3 dB of plan at each end.
- [ ] Polarisation matches licence; XPD acceptable for XPIC links.
- [ ] Bolts torqued with RSL unchanged.
- [ ] Error test passed and commissioning values recorded both ends.
- [ ] Interference check done with far end muted.
