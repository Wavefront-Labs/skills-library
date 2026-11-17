---
id: manufacturing-production.cnc-machining-production.in-process-probing.probing-cycles-offset-update-and-broken-tool-detection
name: probing-cycles-offset-update-and-broken-tool-detection
category: manufacturing-production
field: cnc-machining-production
product: in-process-probing
tags: [in-process-probing, probing, spindle-probe, touch-probe, renishaw, blum, marposs, heidenhain-ts, tool-setter, laser-tool-setter, ots, nc4, probe-calibration, stylus-calibration, ring-gauge, work-offset-setting, datum-finding, in-process-gauging, adaptive-machining, automatic-offset-update, wear-offset-feedback, broken-tool-detection, tool-breakage-detection, tool-length-measurement, inspection-plus, protected-positioning, closed-loop-machining, process-control, spc, cnc-machining-production]
level: practitioner
status: draft
description: "Automate setup and in-cycle measurement: calibrate probes and tool setters, set work offsets by probing, feed measured sizes back into wear offsets with limits, and catch broken tools."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Probing cycles, automatic offset update and broken tool detection

**Goal:** let the machine set its own work offsets, measure tools, check critical
features mid-cycle and correct itself within safe limits — so setups are faster and
unattended runs stop instead of making scrap.

*Draft: method is generic; cycle names and variable numbers differ between probe
makers (Renishaw Inspection Plus, Blum, Marposs, Heidenhain TS) and controls. Use
your probe software manual for syntax.*

## 1. Calibrate before you trust it
- **Spindle probe:** calibrate stylus **length** (against a known surface/tool setter),
  **ball radius/effective radius** (in a certified **ring gauge**) and **XY stylus offset**
  (centre in the ring with spindle oriented). Effective radius is smaller than the
  physical ball because of pre-travel; that's what calibration captures.
- Recalibrate after stylus change, a collision, a big temperature change, and on a
  schedule. Probe at the **same feed** used in calibration.
- **Tool setter** (contact or laser): calibrate its position with a reference tool of
  known length/diameter.

## 2. Setting work offsets by probing
- Typical cycles: single surface (Z or X/Y), web/pocket centre, bore/boss centre,
  corner (two surfaces), plus angle for rotated parts.
- Write directly into the target work offset (G54, G55…). Probe **protected
  positioning** moves (moves that stop if the stylus touches unexpectedly) to approach.
- For a rough casting, probe locating surfaces then let the program shift (and rotate)
  the coordinate system to the actual part — "best fit" before machining.

## 3. Tool measurement
- **Length** on every new tool before first use (and after replacement), automatically
  written to the length offset.
- **Diameter** of end mills on a laser setter, at spindle speed, to capture runout.
- Don't measure dirty tools — coolant drops on a laser give wrong readings; use the
  air blast and repeat-and-compare logic.

## 4. In-process gauging and offset feedback
1. After roughing/semi-finishing (or after finishing a test feature), probe the critical
   size.
2. Compare to nominal; compute the error.
3. **Update the wear offset** of the tool that made it by a fraction of the error
   (e.g. 50–100%; damping avoids chasing noise), only if the error is within an
   **update window**.
4. If the error is **outside an upper limit**, stop with an alarm — something is wrong
   (broken tool, wrong tool, loose part) and blind correction would hide it.
5. Re-finish if the feature is still oversize (only on features where re-cutting is safe).
Log results to a file/variable for SPC trends; drift tells you about thermal growth
and tool wear long before scrap.

Keep a **dead band** (no correction for errors smaller than probing repeatability,
e.g. a few µm) — otherwise offsets random-walk.

## 5. Broken tool detection
- **Tool setter break check:** after drilling/tapping with small tools, check length with
  a quick touch or laser beam break; alarm if shorter than expected minus tolerance.
- Cheaper alternatives: spindle **load monitoring**, or probing the feature (hole present
  and deep enough).
- Put the check **after** the tool's work but **before** the next tool depends on it
  (tap after drill).

## 6. Measurement uncertainty
- The machine measuring its own work shares the machine's errors (thermal, geometry).
  In-process probing controls the process; it doesn't replace final inspection on a CMM
  for critical characteristics — correlate the two.

## Gotchas
- Probe battery low/signal loss mid-cycle — handle the alarm and the "probe not
  triggered" error path in the macro.
- Chips/coolant on the measured surface — blow off first.
- Probing at the wrong temperature (cold machine, warm part) gives consistent but
  wrong numbers.
- Offset updates applied to the wrong tool number after a tool-list change.

## Verify
- [ ] Probe and tool setter calibrated (date, ring gauge used, feed).
- [ ] Work offsets set by cycle match a manual check on the first setup.
- [ ] Offset feedback has dead band, damping and an upper alarm limit.
- [ ] Broken tool checks after every small drill/tap.
- [ ] Probe results correlated against CMM for critical features.

Related: `manufacturing-production.cnc-machining-production.fanuc-cnc-control.offsets-macro-b-and-alarm-recovery`.
