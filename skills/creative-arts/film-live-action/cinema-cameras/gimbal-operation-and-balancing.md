---
id: creative-arts.film-live-action.cinema-cameras.gimbal-operation-and-balancing
name: gimbal-operation-and-balancing
category: creative-arts
field: film-live-action
product: cinema-cameras
tags: [cinema-cameras, film-live-action, camera-operator, gimbal-operation, gimbal-balancing, gimbal, ronin, dji-ronin, rs4, ronin-2, movi, movi-pro, freefly, balancing, tilt-axis, roll-axis, pan-axis, auto-tune, motor-stiffness, follow-mode, lock-mode, fpv-mode, inverted, underslung, briefcase-mode, ninja-walk, easyrig, ready-rig, wireless-focus, lens-control, camera-weight, payload, battery, force-mobile, vehicle-mount, car-mount, operator-technique, axis-balancing, balance-procedure, gimbal-balance-steps, gimbal-tuning, motor-tuning, auto-tune-gimbal, gimbal-modes, follow-modes, control-profiles, gimbal-support, gimbal-vest, ready-rig-use, gimbal-focus, gimbal-remote, gimbal-monitoring, gimbal-walking, gimbal-moves, gimbal-footwork]
level: practitioner
status: draft
description: "Balance and operate a cinema gimbal: three-axis balancing order, auto-tune and motor stiffness, modes, operator footwork and support rigs, wireless focus and monitoring, vehicle and remote use."
sources:
  - "https://www.dji.com/support (DJI Ronin / RS series user manuals - balancing, auto tune, modes)"
  - "https://freeflysystems.com/support (Freefly MoVI Pro operator manual)"
  - "American Cinematographer Manual, 10th ed. - Camera stabilisation systems"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gimbal operation and balancing

**Goal:** a gimbal shot that looks like a dolly or Steadicam move, not a floating
security camera - which is 30% the rig and 70% the balance, the footwork and the lens.

## 1. Build for the rig first
- Check **payload**: camera + lens + follow-focus motor + wireless video + batteries
  under the gimbal's rated maximum with margin (e.g. RS 4 Pro ~4.5 kg; Ronin 2 ~13.6 kg;
  MoVI Pro ~6.8 kg). Overweight rigs vibrate and drain motors.
- Strip the camera: remove the top handle, EVF and anything that catches wind; use a short
  SDI/HDMI cable and a small monitor on the gimbal handle or wireless to the AC.
- Lenses: light primes (not zooms) 18-50 mm S35 equivalent; long lenses amplify every
  micro-wobble. Set the lens to the shooting focal length *before* balancing (zooms shift weight).
- Rods, matte box, filters and the follow-focus motor all mounted *before* balancing.

## 2. Balance in order (power off)
1. **Tilt (vertical)**: point the lens up 90°; slide the camera plate fore/aft until it stays.
   Then level it and adjust the vertical arm so it stays level - the camera should hold
   any tilt angle.
2. **Roll**: adjust the roll arm until the camera stays level sideways without drifting.
3. **Pan**: tilt the whole gimbal 15-20° on its handle; adjust the pan arm until it doesn't
   swing. A balanced gimbal holds any position with motors off.
Mark the plate positions with tape/notes per camera build; rebalance after any accessory
change (even a battery swap on some cameras).

## 3. Power on and tune
- Run **auto-tune / balance test** in the app or on-screen (DJI "Auto Tune", MoVI "Auto
  Tune"); aim for a balance score in the good range. Set **motor stiffness** as low as holds
  the camera without vibration - too high buzzes, too low drifts under acceleration.
- Calibrate the IMU on a flat, still surface if the horizon drifts.
- Set **follow speeds / deadband**: slow, wide deadband for cinematic (pan follows the
  operator's turn with a lag); tight for action.
- **Modes**: *Pan follow* (default; tilt locked), *Pan-tilt follow*, *Lock* (camera holds
  direction - for orbits and reveals), *FPV* (all axes follow - car rigs, handheld chaos).
  Pick per shot. Enable **SmoothTrack** style damping for the slow version of each.

## 4. Operator technique
- **Ninja walk**: bent knees, heel-to-toe roll, arms soft, elbows in, move from the hips;
  the rig only removes rotation - vertical bob is yours to kill. Practice with a glass of water.
- Two hands on the rig; the second hand steadies without fighting. For longer takes use an
  **Easyrig / Ready Rig / Steadimate-style support** or a two-person "dual operator"
  setup (one carries, one operates pan/tilt by remote - the real cinema way on Ronin 2/MoVI).
- **Underslung / briefcase / inverted** modes for low shots and doorways; practise
  transitions before the take.
- Start and stop moves gently; cut points want a settled frame.
- Keep the horizon honest: a slightly rolled horizon on a wide lens is the gimbal tell.
  Use the app's horizon correction or re-calibrate.

## 5. Focus and monitoring
Focus is pulled by a 1st AC on a **wireless follow focus** (Tilta Nucleus, DJI Focus,
Teradek RT, ARRI WCU-4) - the operator can't. Marks are approximate; the AC uses
monitor + distance habit or a rangefinder (Light Ranger 2, Cine Tape) on the rig. Send
wireless video (Teradek, DJI transmitter) to AC and DP; the operator monitors a small
screen on the handle, framing only.

## 6. Vehicles and remote
Gimbal on a car (hostess tray, hood mount, Russian-arm style crane) in FPV/lock mode with
a remote operator on a wheel/joystick controller (DJI Master Wheels / Force Pro, MoVI
Mimic). Dampen with a vibration isolator (Flowcine/Black Arm) and never trust the
mount - safety cable everything.

## Gotchas
- Balancing with the lens cap on, then removing it; or zoom not at shooting focal length.
- Motor stiffness maxed to hide an unbalanced rig; vibration in the footage.
- Long takes with no support rig; the operator fatigues and the last take wobbles.
- Wind on a big matte box; the gimbal fights and buzzes.
- Battery dying mid-shot: gimbal drops the camera onto the lens - swap at 20%.

## Verify
- [ ] Rig under payload with accessories mounted; balanced on all three axes with motors off.
- [ ] Auto-tune passed; stiffness lowest stable; IMU calibrated; horizon level on a wide.
- [ ] Mode chosen per shot; follow speed set for the look.
- [ ] AC on wireless focus with video; support rig for takes over 30 s.
