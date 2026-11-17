---
id: engineering-technology.aerospace-engineering.spacecraft-systems-design.antenna-gain-and-pointing
name: antenna-gain-and-pointing
category: engineering-technology
field: aerospace-engineering
product: spacecraft-systems-design
tags: [antenna-gain, antenna-beamwidth, pointing-loss, eirp, reflector-antenna, spacecraft-communications]
level: practitioner
status: verified
description: "Compute antenna gain, beamwidth and pointing loss for spacecraft links, and choose antenna types for the mission geometry."
sources:
  - "Wertz and Larson, Space Mission Analysis and Design"
  - "Fortescue et al., Spacecraft Systems Engineering"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Antenna gain

**Goal:** the gain and pointing needs that close the link.

## Relations
- Aperture antenna gain `G = eta * (pi D / lambda)^2` (linear), `eta` aperture efficiency (about 0.5 to 0.7 for reflectors (gated: unconfirmed, source is paywalled or blocked)); in dBi `10 log10(G)`.
- 3 dB beamwidth `theta_3dB` about `70 lambda / D` degrees.
- Pointing loss `L_p = 12 (e / theta_3dB)^2` dB for pointing error `e` (Gaussian beam approximation, valid for small `e`; it gives 3 dB at `e` = half the beamwidth).
- EIRP = transmit power (dBW) + antenna gain (dBi) - line losses.

## Example
A 1 m reflector at 8.4 GHz (`lambda = 0.0357 m`) with `eta = 0.55` has `G` = 36.3 dBi (4259 linear); beamwidth 2.5 degrees (computed).

## Selection
- Omnidirectional or low-gain (patch, helix, monopole/dipole): tolerates any attitude, gain a few dBi; use for TT&C in safe mode.
- Horn: medium gain, simple.
- Parabolic reflector or phased array: high gain, needs pointing or electronic steering.

## Procedure
1. Pick frequency (regulatory allocation, bandwidth, atmosphere).
2. Compute required gain from the link budget (see link-budget-and-margin).
3. Choose the aperture; check beamwidth against the pointing capability (the pointing error should be a fraction of the beamwidth).
4. Include polarisation mismatch and radome or structure blockage losses.

## Gotchas
- Antenna gain varies with angle off boresight; use the measured pattern for low-gain antennas on the spacecraft body (body scattering).
- High gain at the ground end needs tracking, high-gain flight antennas need gimbals or attitude manoeuvres.

## Verify
- [ ] Doubling the aperture diameter raises gain by 6 dB and halves the beamwidth.
