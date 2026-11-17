---
id: engineering-technology.aerospace-engineering.propulsion-engineering.electric-propulsion-power-thrust-isp
name: electric-propulsion-power-thrust-isp
category: engineering-technology
field: aerospace-engineering
product: propulsion-engineering
tags: [propulsion, electric-propulsion, power-thrust-isp, ion-thruster, hall-thruster, xenon, gridded-ion, specific-impulse]
level: practitioner
status: verified
description: "Size electric propulsion (ion and Hall thrusters) from power, efficiency and Isp: thrust, propellant mass, and the Isp optimum for a mission."
sources:
  - "Goebel and Katz, Fundamentals of Electric Propulsion: Ion and Hall Thrusters (JPL)"
  - "Jahn, Physics of Electric Propulsion"
  - "Wertz and Larson, SMAD"
  - "NASA Small Spacecraft Technology State of the Art, in-space propulsion chapter (2021): https://www.nasa.gov/wp-content/uploads/2021/10/4.soa_in-space_propulsion_2021.pdf"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Electric propulsion: power, thrust and Isp

**Goal:** first-order sizing of an electric propulsion system.

## Relations
- Jet power `P_jet = 1/2 m_dot V_e^2 = 1/2 T V_e`; with total efficiency `eta`: `P_in = P_jet/eta`.
- Thrust per power: `T/P_in = 2 eta/(g0 Isp)`, so higher Isp costs more power per newton.
- Gridded ion thruster: ideal exhaust speed from beam voltage `V_b`: `V_e = sqrt(2 q V_b/m_i)`. For singly charged xenon at 1000 V this is 38.3 km/s (Isp 3909 s ideal, computed from the elementary charge and xenon 131.293 u); actual Isp is reduced by beam divergence and ionisation losses.
- Hall thruster: NASA small-spacecraft survey lists Hall thrusters at about 800-1950 s Isp and 1-60 mN (larger Hall thrusters reach higher Isp); efficiency about 50-60% (gated: unconfirmed, source is paywalled or blocked); higher thrust density than gridded ion thrusters but lower Isp.
- Propellant is usually xenon; krypton and others are in use.

## Mission trade
For a fixed `Delta v`, higher Isp saves propellant but needs more power (larger solar arrays, more mass) and longer burn time; there is an optimum Isp for a given trip time and specific mass of the power system `alpha` (kg/kW).

## Procedure
1. Fix power available to propulsion `P_in` (array sizing in the power budget).
2. Choose thruster type and operating point (Isp, efficiency) from vendor data.
3. Compute thrust, propellant flow, burn time for the `Delta v`.
4. Include power processing unit mass and efficiency, tank and feed mass.
5. Check spacecraft constraints (plume, thermal, eclipse operation).

## Verify
- [ ] 1 kW at Isp 1600 s and efficiency 0.55 gives `T = 2 x 0.55 x 1000/(9.81 x 1600)` = 70.1 mN (recomputed).
