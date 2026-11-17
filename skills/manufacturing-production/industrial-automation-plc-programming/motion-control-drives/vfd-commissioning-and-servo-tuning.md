---
id: manufacturing-production.industrial-automation-plc-programming.motion-control-drives.vfd-commissioning-and-servo-tuning
name: vfd-commissioning-and-servo-tuning
category: manufacturing-production
field: industrial-automation-plc-programming
product: motion-control-drives
tags: [motion-control-drives, vfd, variable-frequency-drive, inverter, ac-drive, servo, servo-drive, servo-tuning, motor-nameplate, autotune, motor-identification, v-hz, sensorless-vector, closed-loop-vector, acceleration-ramp, braking-resistor, dc-bus-overvoltage, overcurrent-trip, inertia-ratio, load-inertia, velocity-loop, position-loop, gain, notch-filter, resonance, following-error, electronic-gearing, electronic-camming, plcopen-motion, mc-power, mc-moveabsolute, homing, industrial-automation-plc-programming]
level: practitioner
status: draft
description: "Commission VFDs and tune servos: nameplate entry and autotune, ramps and braking, common trips, inertia ratio, velocity/position loop tuning with notch filters, and PLCopen motion basics."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# VFD commissioning and servo tuning

**Goal:** a drive that starts first time, doesn't nuisance-trip, and (for servos) holds
position without hunting or noise — regardless of the drive brand.

*Draft: generic method; parameter numbers and names are vendor-specific (look them up
in your drive's manual). Electrical work on drives needs isolation and DC-bus discharge
time — capacitors stay charged for minutes after power-off.*

## 1. VFD commissioning sequence
1. **Check the installation:** supply voltage, motor connection (star/delta for the
   voltage), shielded motor cable with 360° glanding, brake resistor wired if specified.
2. **Enter the motor nameplate:** rated voltage, current, frequency, speed, power, cos φ.
   Wrong current = wrong overload protection.
3. **Choose control mode:** V/Hz for fans, pumps and multiple motors on one drive;
   **sensorless vector** for good torque at low speed; **closed-loop vector** (encoder)
   for full torque at zero speed (hoists, winders).
4. **Run motor identification/autotune.** Rotating autotune (motor uncoupled) is better
   than static if you can uncouple it.
5. Set **min/max frequency**, **accel/decel ramps**, stop mode (ramp vs coast) and
   control source (fieldbus, terminals, keypad) — and the comms-loss reaction.
6. Jog, check direction, then run to max speed under load and watch current.

## 2. Common trips and fixes
- **Overvoltage on decel (DC bus OV):** load is regenerating faster than the drive can
  absorb. Lengthen the decel ramp, enable the drive's OV controller, or add a braking
  resistor/regenerative unit.
- **Overcurrent on accel:** ramp too short or high-inertia load; lengthen ramp, check
  torque boost (V/Hz) or autotune.
- **Motor overload (I²t):** real mechanical overload or wrong nameplate current.
- **Earth fault:** motor insulation or wet cable; megger the motor *with drive
  disconnected*.

## 3. Servo tuning method
1. **Inertia ratio first.** Run the drive's inertia estimation (auto-tune move). Ratios
   below ~10:1 (load:motor) tune easily; far higher ratios are hard — consider a
   gearbox or bigger motor. (Rule of thumb, varies by drive.)
2. **Current loop** is set by the drive from motor data — leave it.
3. **Velocity loop:** raise proportional gain until you hear/see oscillation, back off
   ~30–50%; then add integral gain to remove steady-state error. Check with a step
   velocity command on the drive's scope.
4. **Resonance:** a high-pitched whine at a fixed frequency → use the drive's FFT/frequency
   response tool, add a **notch filter** at that frequency, then gains can go higher.
5. **Position loop gain:** increase until following error is acceptable without overshoot
   at the end of moves. Add **velocity/acceleration feed-forward** to cut following
   error during moves (most of the gain comes from feed-forward, not loop gain).
6. Test with the **real move profile** at full speed and payload; tune for the worst case.

## 4. Motion in the PLC (PLCopen-style)
- Sequence: `MC_Power` (enable) → **homing** (`MC_Home`) → moves (`MC_MoveAbsolute`,
  `MC_MoveRelative`, `MC_MoveVelocity`) → `MC_Stop`/`MC_Halt`.
- Each FB has `Busy`, `Done`, `CommandAborted`, `Error` — handle all four; don't start a
  new move until the last is `Done` or deliberately aborted.
- **Electronic gearing/camming** (`MC_GearIn`, `MC_CamIn`): slave follows a master axis
  (often a virtual axis). Check engage/disengage happen at defined positions.
- **Following error limit** is a fault, not a nuisance — investigate, don't just widen it.

## Gotchas
- Absolute encoder battery dead → loss of home; schedule battery changes.
- Safe Torque Off (STO) removes torque but not power — hazard isolation still needed.
- Long motor cables → reflected-wave overvoltage; use dV/dt or sine filters per vendor limits.
- Tuning with the machine empty, then running full, is how oscillation appears in production.

## Verify
- [ ] Nameplate data entered, autotune done, direction correct.
- [ ] Full-speed start/stop under max load with no OV/OC trips.
- [ ] Servo step response on scope: no sustained oscillation, acceptable overshoot.
- [ ] Following error within limit on the real profile at full payload.
- [ ] Drive parameters backed up (file + PLC-held where supported) after tuning.
