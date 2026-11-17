---
id: engineering-technology.aerospace-engineering.flight-dynamics-control.load-factor-limiting
name: load-factor-limiting
category: engineering-technology
field: aerospace-engineering
product: flight-dynamics-control
tags: [load-factor-limiting, envelope-protection, fly-by-wire, nz-limiting, normal-law, protection-law]
level: practitioner
status: verified
description: "Implement load factor limiting in a fly-by-wire control law with a normal-acceleration command, soft limits and consistency with the certified structural envelope."
sources:
  - "Stevens and Lewis, Aircraft Control and Simulation"
  - "FAA 14 CFR 25.143, 25.337"
  - "EASA CS-25"
  - "https://www.law.cornell.edu/cfr/text/14/25.143"
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# Load factor limiting

**Goal:** keep normal load factor inside the structural manoeuvring envelope, whatever the pilot commands.

## Law
- The sidestick or column commands load factor (flight-path-rate) rather than elevator deflection (a C-star or load-factor demand law).
- Limit: clip the command to `n_z` bounds. One well-known transport FBW design limits clean-configuration load factor to +2.5 and -1 g (gated: unconfirmed, source is paywalled or blocked); other manufacturers use different limits, and the certified limit is set by the structural envelope (14 CFR 25.337(b) sets the positive limit manoeuvring load factor as a weight-dependent value that is not less than 2.5 and not more than 3.8, and a negative limit that is not less than -1.0 up to V_C and varies linearly to zero at V_D (25.337(c)); read the current text).
- Soft limiter: smoothly reduce authority near the limit rather than a hard clip, avoiding a discontinuity in feel.

## Procedure
1. Choose limits from the manoeuvre envelope and the structural design (see vn-manoeuvre-envelope).
2. Compute `n_z = 1 + V * gamma_dot / g` (flight-path-rate form) or from the accelerometer.
3. Implement the limiter on the command and add feedback (accelerometer) so the limit holds with gusts and weight changes.
4. Allow temporary excess in turbulence only within the structural margin; verify gust load alleviation separately (see gust-load-factors).
5. Coordinate with pitch-attitude and angle-of-attack protections (see stall-warning-and-alpha-protection).
6. Document with the safety assessment; envelope protection systems carry special certification considerations. Confirm requirements with the authority.

## Gotchas
- The limiter must continue to work after sensor and actuator failures or reversion (see control-law-reversion).
- Limiting by accelerometer needs vibration and structural-mode filtering.
- Pilot-induced behaviour near the limit changes with command shaping.

## Verify
- [ ] Full-stick pull-ups across the envelope peak at or below the limit with margin, with and without gusts.
