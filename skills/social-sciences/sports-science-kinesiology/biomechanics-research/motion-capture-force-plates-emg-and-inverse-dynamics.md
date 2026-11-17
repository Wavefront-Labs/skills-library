---
id: social-sciences.sports-science-kinesiology.biomechanics-research.motion-capture-force-plates-emg-and-inverse-dynamics
name: motion-capture-force-plates-emg-and-inverse-dynamics
category: social-sciences
field: sports-science-kinesiology
product: biomechanics-research
tags: [biomechanics-research, sports-biomechanics, biomechanics, kinesiology, sports-science, motion-capture, mocap, vicon, qualisys, optitrack, markerless, theia3d, openpose, marker-set, plug-in-gait, cast, force-plate, ground-reaction-force, grf, centre-of-pressure, emg, surface-emg, seniam, mvc-normalisation, butterworth-filter, residual-analysis, inverse-dynamics, joint-moments, visual3d, opensim, c3d, ezc3d]
level: advanced
status: draft
description: "Collect and process biomechanics lab data: marker-based motion capture, force-plate sync, filtering choices, EMG normalisation and inverse dynamics in Visual3D or OpenSim."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Motion capture, force plates, EMG and inverse dynamics

**Goal:** get joint angles, moments and muscle activity that are accurate enough to
answer the research question, with processing choices that are reported and defensible.

## 1. Lab setup and calibration
- **Optoelectronic mocap** (Vicon, Qualisys, OptiTrack): calibrate the volume with the
  wand each session; check residuals (sub-mm typical in good setups) and that the global
  axes align with the force plates.
- **Force plates:** zero/tare with nothing on the plate before each trial; confirm plate
  positions in the mocap coordinate system. Sample rates: kinematics 100–250 Hz typical
  for gait/running (higher for impacts or sprinting), force 1000+ Hz.
- **Synchronise** all devices through hardware triggers/analog channels; verify with a
  known event (e.g. a tap on the plate seen by markers and force).

## 2. Marker sets and models
- Conventional gait model (Plug-in Gait) is widespread but sensitive to marker placement
  (especially knee axis/thigh wand) — consider the CAST approach with segment clusters
  (Cappozzo) or 6-DoF models for better segment tracking.
- Static calibration trial for anatomical landmarks; functional joint centre methods
  (e.g. SCoRE/SARA for hip) improve repeatability over regression equations.
- The **same trained person** places markers across sessions; inter-tester variability
  can exceed the effects you study. Soft-tissue artefact is the main residual error source.
- **Markerless** systems (Theia3D, OpenCap, OpenPose-based) are improving rapidly but
  validity varies by joint and plane — check validation studies for your movement.

## 3. Filtering
- Low-pass Butterworth (4th-order, zero-lag i.e. 2nd-order run forwards and backwards)
  is standard. Choose cut-offs by **residual analysis** (Winter) or from pilot spectra —
  roughly 6–12 Hz for gait kinematics, higher for impacts.
- **Filter kinematics and force with the same cut-off** before inverse dynamics, or
  you get artefactual impact peaks in joint moments (Bisseling & Hof; Kristianslund et al. 2012).
- Gap-filling: spline fill small gaps only (e.g. < 10 frames); pattern fill from rigid
  clusters for bigger ones; never across the event of interest.

## 4. Inverse dynamics
Segment inertial parameters (de Leva; Dempster) + kinematics + external forces → net
joint moments and powers, usually bottom-up from the force plate. Tools: Visual3D,
OpenSim (scale model → inverse kinematics → inverse dynamics → static optimisation/
CMC for muscle forces), or Python (`ezc3d` to read C3D). Report moments normalised to body
mass (N·m/kg) and state the reference frame (joint coordinate system vs lab/global) —
moments differ substantially between frames.

## 5. Surface EMG
- Follow **SENIAM** for electrode placement, inter-electrode distance and skin prep
  (shave, abrade, alcohol); check impedance.
- Processing: band-pass (~20–450 Hz) → full-wave rectify → low-pass envelope (e.g. 6–10 Hz)
  or RMS window.
- Normalise to maximal voluntary contraction (MVC) or a reference task; MVC is unreliable
  in some populations — state the choice.
- EMG amplitude ≠ force; crosstalk from neighbouring muscles is real for small muscles.

## 6. Analysis
Time-normalise to 0–100% of the cycle/stance. Use waveform methods (statistical
parametric mapping, SPM1D) rather than cherry-picked peaks to avoid regional focus bias.

## Gotchas
- Plate "targeting" (participants altering stride to hit the plate) changes gait — hide plates.
- Unit and axis-convention errors (mm vs m, Y-up vs Z-up) are common when exporting.
- Uncertain: cut-off and sampling-rate ranges are typical values; justify yours for the task.

## Verify
- [ ] Volume and force-plate calibration/zeroing logged; devices synchronised.
- [ ] Marker placement by consistent trained tester; static and functional trials collected.
- [ ] Cut-offs chosen by residual analysis; same cut-off for force and kinematics.
- [ ] Moment reference frame and normalisation stated.
- [ ] EMG prep, processing and normalisation reported per SENIAM.
