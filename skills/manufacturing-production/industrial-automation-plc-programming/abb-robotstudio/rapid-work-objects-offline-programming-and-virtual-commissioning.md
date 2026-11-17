---
id: manufacturing-production.industrial-automation-plc-programming.abb-robotstudio.rapid-work-objects-offline-programming-and-virtual-commissioning
name: rapid-work-objects-offline-programming-and-virtual-commissioning
category: manufacturing-production
field: industrial-automation-plc-programming
product: abb-robotstudio
tags: [abb-robotstudio, robotstudio, abb, abb-robot, rapid, irc5, omnicore, flexpendant, virtual-controller, offline-programming, olp, virtual-commissioning, station, work-object, wobj, tooldata, tcp, loaddata, robtarget, movel, movej, zonedata, fine, speeddata, calibration, three-point-calibration, signal-i-o, smart-components, emulated-plc, opc-ua, collision-detection, reachability, configuration, confdata, industrial-automation-plc-programming]
level: practitioner
status: draft
description: "Program ABB robots offline in RobotStudio: tooldata, work objects and loaddata, RAPID motion with zones, reach and configuration checks, and calibrating the virtual cell to the real one."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# RAPID, work objects, offline programming and virtual commissioning

**Goal:** write an ABB RAPID program in RobotStudio against a virtual controller,
prove reach, cycle time and logic virtually, then load it onto the real IRC5/OmniCore
robot with only a few touch-ups.

*Draft: from RobotStudio 2019–2024 / RobotWare 6 and 7 practice. Some features
(e.g. virtual commissioning with external PLC emulators) need premium licences.*

## 1. The data that makes programs portable
- **tooldata** — TCP and tool mass/CoG. Define it by the 4-point (+Z, +X) method on
  the FlexPendant, or from CAD if the tool is accurately made.
- **wobjdata (work object)** — a user frame (fixture) and optional object frame.
  Every robtarget is stored *relative to* the wobj it was taught in. Re-calibrate
  the wobj (three-point user-frame method) and all targets move with it.
- **loaddata** — payload carried by the tool (part mass/CoG); switch it in RAPID when
  gripping: `GripLoad load_part;` and `GripLoad load0;` after release.
- Always pass tool and wobj explicitly:
  `MoveL p_pick, v500, fine, tGripper\WObj:=wobjFixture1;`

## 2. Motion and zones
- `MoveJ` joint interpolation for free space; `MoveL` straight line near parts.
- **zonedata**: `fine` = stop at the point; `z10`, `z50` = blend radius in mm.
  Logic after a zoned move executes *early* (the program pointer runs ahead of the
  robot). Use `fine` before I/O that must happen at the point, or `TriggL`/`TriggIO`
  for position-timed I/O.
- **speeddata** in mm/s (`v200`, `v1000`). Set realistic speeds in simulation; cycle
  time estimates are only as good as the speeds and zones used.

## 3. Offline programming workflow
1. Build the **station**: robot model of the exact variant (reach/payload matter),
   tool CAD with tooldata, fixture/part CAD, guarding, other machines.
2. Create a **virtual controller from the same RobotWare version and options** as the
   real one (or from a backup of the real controller — best).
3. Create wobjs on fixture features; generate targets from CAD edges/surfaces or teach
   in 3D.
4. Check **reachability** and **configuration** (confdata — which of the arm's
   solutions it uses). Use auto-configuration on paths, then lock it in; a config flip
   mid-path is an error at runtime (or a wild swing if `ConfL\Off`).
5. Enable **collision detection** sets (robot+tool vs fixture/guarding) and run the
   cycle. Fix near-misses with margin, not just zero contact.
6. **Synchronise to RAPID**, review generated code, add logic and error handlers.

## 4. Virtual commissioning
- Model conveyors, grippers and sensors with **Smart Components** (signals, sensors,
  attachers) so I/O responds as in the cell.
- Connect the virtual controller's I/O to an emulated PLC (e.g. PLCSIM Advanced via
  plugins, or OPC-UA) to test the real PLC code against the virtual robot. Licence and
  plug-in availability vary — check before planning on it.

## 5. Bringing it to the real cell
- Measure/calibrate the real wobjs (three points on the real fixture). If the virtual
  and real fixture match within tolerance, most targets need no touch-up.
- Touch up a few critical points; check **TCP** is identical to the simulation.
- Run first at reduced speed with `VelSet 25, 250;` (or override) and single-step.

## Gotchas
- Targets created in `wobj0` (world) don't move when the fixture moves.
- Modules saved in RobotStudio and on the controller diverge — always back up the
  controller before loading, and compare files.
- `SingArea\Wrist` helps through wrist singularities but changes orientation along the path.
- Unhandled `ERR_*` errors stop execution; add `ERROR` handlers with `RETRY`/`TRYNEXT`
  only where a retry is genuinely safe.

## Verify
- [ ] Every move names tool and wobj; no production targets in wobj0.
- [ ] Simulation runs full cycle without collisions, config errors or reach limits.
- [ ] Virtual controller RobotWare/options match the real one.
- [ ] Real-cell wobj calibrated; first cycle at reduced speed, single-stepped.
- [ ] Backup of the real controller taken before and after loading.
