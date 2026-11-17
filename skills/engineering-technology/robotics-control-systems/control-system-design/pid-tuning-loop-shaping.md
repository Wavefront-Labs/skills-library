---
id: engineering-technology.robotics-control-systems.control-system-design.pid-tuning-loop-shaping
name: pid-tuning-loop-shaping
category: engineering-technology
field: robotics-control-systems
product: control-system-design
tags: [control-system-design, pid, pi, pid-tuning, loop-shaping, bode, nyquist, crossover-frequency, bandwidth, phase-margin, gain-margin, sensitivity, peak-sensitivity, derivative-filter, anti-windup, integrator-windup, back-calculation, clamping, setpoint-weighting, cascade-control, feedforward, discretisation, sample-rate, tustin, frequency-response, feedback-control, servo-tuning, motor-control]
level: practitioner
status: draft
description: "Tune a PID loop by loop shaping: pick crossover from plant limits, hit 45-60 deg phase margin, filter the derivative, add anti-windup and discretise at 10-20x bandwidth."
sources:
  - "Astrom and Murray, Feedback Systems (2nd ed.), chapters on PID and loop shaping"
  - "Astrom and Hagglund, Advanced PID Control (ISA, 2006)"
  - "Franklin, Powell and Emami-Naeini, Feedback Control of Dynamic Systems"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PID tuning by loop shaping — margins first, gains second

**Goal:** a PID loop whose speed is chosen deliberately from the plant's limits, whose
robustness is measured (not hoped for), and which survives saturation, noise and a
digital implementation.

Notation: plant `G(s)`, controller `C(s)`, loop `L = CG`, sensitivity `S = 1/(1+L)`,
complementary `T = L/(1+L)`. Parallel PID with filtered derivative:
`C(s) = Kp + Ki/s + Kd·s/(Tf·s + 1)`.

## 1. Get a frequency response before touching gains
Use a model (first-principles or fitted), or measure one: inject a chirp or swept sine
at the actuator in closed loop with a gentle controller and compute `G = Y/U`. Note
three things on the Bode plot: the plant's gain slope near where you will cross over,
the **delay** (phase rolling off linearly with frequency), and the first **resonance**.

## 2. Choose the crossover `wc` from the limits
Crossover is where `|L(jw)| = 1`; closed-loop bandwidth is roughly 1-2× `wc`. Upper bounds:
- delay `θ`: it costs `wc·θ` rad of phase, so keep `wc ≤ ~0.5/θ` (about 30° lost);
- first structural resonance: stay below about 1/3 to 1/5 of it, or notch it;
- sensor noise and actuator saturation: higher `wc` means more `u` activity (`|C·S|`);
- sample rate: `wc` at most about 1/10 to 1/20 of the sample rate in rad/s.
Pick the lowest `wc` that meets the disturbance or tracking spec, not the highest that is stable.

## 3. Shape the loop around `wc`
- **P only:** set `Kp = 1/|G(jwc)|`. Read the phase margin `PM = 180° + ∠L(jwc)`.
- **Add I** for zero steady-state error: place the integral corner `wi = Ki/Kp` at
  about `wc/5` to `wc/10`. It then costs only ~6-11° of phase at `wc`.
- **Add D** only if PM is short: the derivative zero `wd = Kp/Kd` near `wc/3` to `wc`
  adds phase lead; always filter it with `Tf ≈ Kd/(N·Kp)`, `N` 5-20, so high-frequency
  gain is capped at `Kp(1+N)`. Unfiltered D amplifies encoder quantisation into actuator chatter.
- Re-scale `Kp` so `|L(jwc)| = 1` again after adding I and D.

Targets: **PM 45-60°**, **GM ≥ 6 dB** (2×), **Ms = max|S| ≤ 1.5-2** (Ms 2 guarantees
GM ≥ 6 dB and PM ≥ 29°). PM 45° gives roughly 20-25% step overshoot; 60° about 10%.

**Worked mini-example.** Velocity loop `G = 50/(s(0.01s+1))` (integrating plant, 100 rad/s
pole). Choose `wc = 30 rad/s`. `|G(j30)| ≈ 50/(30·1.044) ≈ 1.60`, so `Kp ≈ 0.63`.
Plant phase at 30 rad/s is `-90 - atan(0.3) ≈ -106.7°`, so PM with P only ≈ 73°. Add I
with `wi = 3 rad/s` (`Ki ≈ 1.9`): costs `atan(3/30) ≈ 5.7°`, PM ≈ 67°. No D needed.
Check the result in a tool before trusting hand arithmetic.

## 4. Two-degree-of-freedom and feedforward
Margins are set by the feedback loop; tracking can be improved separately:
- **Setpoint weighting:** apply P to `b·r - y` (b 0.3-1) and D to `-y` only, so a step
  in `r` doesn't kick the actuator ("derivative kick").
- **Feedforward:** for motion axes add velocity and acceleration feedforward
  (`u_ff = Kv·v_ref + Ka·a_ref`, from the identified friction and inertia). Feedforward
  does the tracking; feedback only corrects errors, so `wc` can stay modest.
- **Cascade:** inner current → velocity → position, each outer loop 3-5× slower than the inner.

## 5. Survive saturation
When the actuator saturates the integrator keeps growing ("windup") and causes large
overshoot. Fix one of two ways:
- **Clamping:** stop integrating while saturated and the error drives further into saturation.
- **Back-calculation:** feed `Kb·(u_sat - u)` into the integrator, with `Kb = 1/Tt` and the tracking time `Tt` between `Td` and `Ti` (a common choice is `Tt = sqrt(Ti·Td)`; for PI, `Tt ≈ Ti`).

## 6. Go digital
Sample at 10-20× closed-loop bandwidth. Zero-order hold plus one-sample compute delay
cost about `1.5·wc·Ts` rad of phase, so re-check PM at the real `Ts`. Discretise with
Tustin (or backward Euler for the derivative filter, which stays stable for any `Tf`).
Implement as:
```c
e   = r - y;
P   = Kp*(b*r - y);
D   = (Tf*D_prev - Kd*(y - y_prev)) / (Tf + Ts);   // backward-Euler filtered D on -y
u   = sat(P + I + D);
I  += Ki*Ts*e + Kb*Ts*(u - (P + I + D));          // integrate after, with back-calculation
```
Use floats or carefully scaled fixed point for `I`; small `Ki·Ts` products vanish in
16-bit integers.

## Verify
- [ ] `wc` is justified against delay, resonance, noise and sample rate in writing.
- [ ] Measured or modelled PM 45-60°, GM ≥ 6 dB, Ms ≤ 2 at the final discrete gains.
- [ ] Derivative is filtered (N 5-20) and acts on the measurement, not the error.
- [ ] A large step that saturates the actuator shows no windup overshoot.
- [ ] Tested with ±30% plant gain change and still stable with acceptable overshoot.
- [ ] Sample rate is ≥ 10× bandwidth and the code has a fixed, measured loop period.
