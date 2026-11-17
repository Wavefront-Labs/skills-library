---
id: engineering-technology.aerospace-engineering.flight-dynamics-control.longitudinal-autopilot-design
name: longitudinal-autopilot-design
category: engineering-technology
field: aerospace-engineering
product: flight-dynamics-control
tags: [flight-dynamics, flight-control, autopilot, stability-augmentation, sas, pitch-rate-damper, altitude-hold, pitch-attitude-hold, short-period, phugoid, stability-derivatives, handling-qualities, mil-std-1797, mil-f-8785c, cap, gain-margin, phase-margin, loop-shaping, root-locus, gain-scheduling, anti-windup, matlab, control-system-toolbox, gnc]
level: advanced
status: draft
description: "Design longitudinal stability augmentation and autopilot loops from linearised aircraft models: short-period/phugoid, pitch-rate SAS, altitude hold, margins."
sources:
  - "Stevens, Lewis and Johnson, Aircraft Control and Simulation"
  - "Etkin and Reid, Dynamics of Flight: Stability and Control"
  - "Nelson, Flight Stability and Automatic Control"
  - "MIL-STD-1797A, Flying Qualities of Piloted Aircraft; MIL-F-8785C"
  - "MIL-F-9490D, Flight Control Systems - Design, Installation and Test of Piloted Aircraft"
  - "Blakelock, Automatic Control of Aircraft and Missiles"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Longitudinal SAS and autopilot — inner pitch damper to outer altitude hold

**Goal:** a cascaded pitch control law (rate damper → attitude hold → altitude/speed
hold) with adequate damping, stability margins and handling qualities across the
flight envelope, verified on the nonlinear model.

## 1. Get a trustworthy linear model
- Trim the nonlinear model at each design point (altitude, speed, weight, CG) and
  linearise. Longitudinal states `x = [V α q θ]` (or `[u w q θ]`, plus `h`), inputs
  `[δe δT]`.
- Read the modes: `damp(A)`. Short period: typically ζ 0.3–0.8 and a few rad/s for
  transports (higher for fighters); phugoid: lightly damped, period of tens of seconds
  (roughly `ω_ph ≈ sqrt(2)·g/V`).
- Check the model: static margin positive (unless designing a relaxed-stability
  aircraft deliberately), signs of `M_α` (negative for static stability), `M_q` negative.
- Add **actuator** (first order ~20–40 rad/s, or second order with rate limits) and
  **sensor** dynamics plus computational delay. Margins without them are fiction.

## 2. Handling-qualities targets (MIL-STD-1797A / MIL-F-8785C, Level 1)
- Short-period damping ζ_sp: ~0.35–1.30 for Category A and C (precision tasks, terminal),
  ~0.30–2.0 for Category B (cruise) (gated: unconfirmed, source is paywalled or blocked).
- Phugoid: ζ_ph ≥ 0.04 for Level 1.
- Control Anticipation Parameter `CAP = ω_sp² / (n/α)`: Level 1 roughly 0.28–3.6
  (Cat A) (gated: unconfirmed, source is paywalled or blocked). Bounds vary with category; check the tables in the standard before signing off.
These are piloted-aircraft criteria; UAV programmes often adopt them as guidance only.

## 3. Inner loop: pitch-rate damper (SAS)
- Feed back q to elevator: `δe = K_q · q_washout` (K_q > 0 in the convention below).
  Washout `s/(s + 1/τ)` with τ ≈ 0.5–2 s so the damper does not fight steady pull-ups or turns.
- Sign: with trailing-edge-down positive δe, `M_δe < 0`, so a nose-up rate (q > 0) must
  command TE-down (positive) elevator to oppose it: K_q > 0, and the q/δe transfer
  function has negative gain. Many textbooks flip the elevator sign instead; whatever the
  convention, check that the loop adds damping. Get it wrong and the loop destabilises
  immediately.
- Pick K_q from root locus to raise ζ_sp to ~0.6–0.7 without pushing the actuator mode
  into poor damping.

```matlab
sys  = ss(A,B,C,D);                    % from linearize
act  = tf(30,[1 30]);                  % actuator, 30 rad/s
G_qe = minreal(act * sys(3,1));        % q / de_cmd  (state 3 = q)
wo   = tf([1 0],[1 1]);                % washout, tau = 1 s
rlocus(-G_qe*wo); grid on              % de = +Kq*q, so poles solve 1 - Kq*G = 0
Kq   = 0.3;                            % example; read from locus
Lq   = -Kq * G_qe * wo;                % loop transfer, broken at actuator input
margin(Lq)                             % GM, PM
```

## 4. Middle and outer loops
- **Pitch attitude hold:** PI on θ error commanding the rate loop. Bandwidth ~1/3–1/5 of
  the rate loop.
- **Altitude hold:** outer loop on h (and h-dot for damping) commanding θ or flight-path
  angle. Again separate bandwidths by 3–5×; altitude bandwidth is typically well below
  1 rad/s for transports.
- **Speed/autothrottle:** close the speed loop with throttle; without it, altitude hold on
  the back side of the power curve drifts in speed.
- Integrators need **anti-windup** (back-calculation or clamping) against elevator and
  rate limits; test with a large step to saturation.

## 5. Robustness and scheduling
- Margins at the actuator input (break each loop there): classical guidance ≥ 6 dB gain
  and ≥ 45° phase margin (MIL-F-9490D-style; exact requirements depend on mode frequency
  and the standard your programme follows). Also check disk margins or the minimum of
  `|1 + L|` for simultaneous gain-phase variation.
- Repeat at corners of the envelope: low/high dynamic pressure, forward/aft CG, light/heavy.
  Schedule gains on dynamic pressure (and Mach) when one set cannot cover the envelope;
  interpolate smoothly and check frozen-point margins between schedule points.
- Include time delay: 50–100 ms of total delay is enough to erase a marginal design.

## 6. Nonlinear verification
Run the control law in the 6-DOF model: step commands, gust and turbulence (Dryden or von
Kármán), engine failure if relevant, and Monte Carlo on aero and mass uncertainty. Watch
for actuator rate saturation, which causes pilot-induced-oscillation-like behaviour.

## Verify
- [ ] Linear model modes match hand estimates/published data for the aircraft class.
- [ ] Augmented short-period and phugoid meet the chosen handling-quality levels.
- [ ] Each loop, broken at the actuator, has ≥ 6 dB / 45° (or programme requirement)
      with actuator, sensor and delay models included.
- [ ] Loop bandwidths separated by about 3–5× from inner to outer.
- [ ] Anti-windup tested with saturating commands.
- [ ] Nonlinear sim across the envelope confirms linear predictions.
