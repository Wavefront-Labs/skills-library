---
id: engineering-technology.telecommunications-engineering.satellite-communications.satellite-link-budget-and-rain-fade
name: satellite-link-budget-and-rain-fade
category: engineering-technology
field: telecommunications-engineering
product: satellite-communications
tags: [telecommunications-engineering, satellite-communications, satcom, link-budget, g-over-t, c-over-n0, eb-n0, es-n0, slant-range, geo, leo, ku-band, ka-band, rain-fade, itu-r-p618, itu-r-p837, itu-r-p839, dvb-s2, dvb-s2x, modcod, acm, earth-station, antenna-sizing, noise-temperature, uplink-power-control, availability]
level: practitioner
status: gated
description: "Close a satellite link: GEO slant range, uplink/downlink C/N0 with G/T, combined C/N, ITU-R P.618 rain fade and noise rise, DVB-S2X MODCOD choice, dish sizing and LEO vs GEO trade-offs."
sources: ["ITU-R P.618 Propagation data for Earth-space telecommunication systems", "ITU-R P.837 Characteristics of precipitation for propagation modelling", "ITU-R P.839 Rain height model", "ITU-R S.580 Radiation diagrams for earth-station antennas", "ETSI EN 302 307-1 DVB-S2 and EN 302 307-2 DVB-S2X", "Maral and Bousquet, Satellite Communications Systems", "Pratt and Allnutt, Satellite Communications"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Satellite link budget and rain fade — clear sky is the easy case

**Goal:** show that a forward or return satellite carrier meets its Es/N0 threshold at the required MODCOD for the target availability, including rain on both legs, and size the earth-station antenna accordingly.

## 1. Geometry

- GEO altitude 35,786 km, Re 6,378 km. Slant range d = sqrt((Re + h)^2 - (Re cos E)^2) - Re sin E, where E is the elevation angle. At E = 30 degrees, d is about 38,600 km (recomputed 38,612 km).
- FSPL = 20 log d_km + 20 log f_MHz + 32.44. At 12 GHz and 38,600 km it is about **205.8 dB** (recomputed 205.76); at 14 GHz uplink, about 207.1 dB (recomputed 207.09).

## 2. Each leg

`C/N0 (dBHz) = EIRP - FSPL - L_atm - L_point - L_pol + G/T + 228.6`

- 228.6 is -10 log10(Boltzmann). Es/N0 = C/N0 - 10 log10(Rs); Eb/N0 = C/N0 - 10 log10(Rb).
- **G/T** = G_rx - 10 log10(T_sys), where T_sys = T_antenna (about 30-60 K at Ku, clear sky (gated: unconfirmed, source is paywalled or blocked)) + T_LNB (NF 0.7 dB is about 50 K, computed 50.7 K) + feed-loss noise.
- Dish gain = 10 log10(eta (pi D f / c)^2), with eta about 0.6-0.7. A 1.2 m dish at 12 GHz is about 41.3-42.0 dBi (computed; 41.7 at eta 0.65); beamwidth about 70 lambda / D, roughly 1.5 degrees.
- Take satellite EIRP and G/T from the operator's footprint contours. Multicarrier back-off (IBO/OBO) costs several dB of EIRP.

## 3. Combine the legs

Add the noise-to-carrier ratios in linear terms:

`(C/N)_total^-1 = (C/N)_up^-1 + (C/N)_down^-1 + (C/I)_adjacent^-1 + (C/I)_xpol^-1 + (C/IM)^-1`

Example: Ku downlink with satellite EIRP 52 dBW, a 1.2 m dish, G/T about 21.7 dB/K and 0.8 dB of other losses gives C/N0 of about 95.7 dBHz. At 30 Msym/s (74.8 dB) the downlink Es/N0 is about 20.9 dB. Combined with an uplink of 25 dB and interference of 22 dB, the total is about **17.5 dB** (all recomputed: 95.70, 20.93, 17.56). The weakest term dominates.

## 4. Rain: ITU-R P.618

Steps: R0.01 (P.837), rain height (P.839), slant path below it, specific attenuation (P.838 k, alpha), horizontal reduction and vertical adjustment factors, A0.01, then scale to the target p (0.1% for 99.9%, 0.01% for 99.99%).

- Temperate climates at 99.9%: Ku about 1-3 dB, Ka about 5-10 dB (gated: unconfirmed, source is paywalled or blocked). Tropics and low elevations are far worse, so always compute it.
- **Downlink rain also raises sky noise:** delta T is approximately T_m (1 - 10^(-A/10)) with T_m about 275 K ((gated: unconfirmed, source is paywalled or blocked)). A 2 dB fade adds about 100 K (computed 101 K), so a 100 K system loses roughly another 3 dB. **Total downlink degradation is therefore about 5 dB, not 2.**
- Uplink fades are handled with uplink power control (UPLC); downlink fades are handled with ACM and margin. End-to-end unavailability is roughly the sum of the two legs' unavailabilities.

## 5. MODCOD selection (DVB-S2/S2X)

Ideal AWGN Es/N0 thresholds from ETSI EN 302 307 V1.2.1 Table 13 (normal frames, quasi error free; all eight values below were checked against the PDF and match to 0.05 dB, e.g. QPSK 1/4 is -2.35 and 32APSK 9/10 is 16.05; add 0.5-1 dB implementation margin (gated: unconfirmed, source is paywalled or blocked)):

| MODCOD | Es/N0 (dB) | | MODCOD | Es/N0 (dB) |
|---|---|---|---|---|
| QPSK 1/4 | -2.4 | | 8PSK 3/4 | 7.9 |
| QPSK 1/2 | 1.0 | | 16APSK 3/4 | 10.2 |
| QPSK 3/4 | 4.0 | | 32APSK 3/4 | 12.7 |
| 8PSK 2/3 | 6.6 | | 32APSK 9/10 | 16.1 |

DVB-S2X adds finer steps, tighter roll-offs (0.05/0.10/0.15) and very-low-SNR modes down to about -10 dB ((gated: unconfirmed, source is paywalled or blocked), EN 302 307-2 not fetched). Occupied bandwidth = Rs (1 + roll-off). Clear-sky MODCOD sets throughput; faded MODCOD sets availability.

## 6. LEO vs GEO

A 550 km LEO at 25 degrees elevation has a slant range of about 1,120 km, about **30 dB less path loss** than GEO (computed: 1,123 km slant, 30.7 dB). Round-trip latency is around 20-50 ms instead of about 500 ms or more for GEO (propagation-only bent-pipe RTT computes to about 15 ms LEO and 477 ms GEO; the 20-50 ms and 500 ms figures include processing and (gated: unconfirmed, source is paywalled or blocked)). The costs are tracking antennas, handovers every few minutes, Doppler of hundreds of kHz at Ku (gated: unconfirmed, source is paywalled or blocked), and a whole constellation plus gateways. GEO wins for broadcast and fixed-dish wide-area coverage.

## Gotchas

- Small uplink dishes are limited by off-axis EIRP density rules (sidelobe envelope 29 - 25 log theta dBi: confirmed for 1.5 to 7 degrees in 47 CFR 25.209(a)(1); ITU-R S.580 not fetched, (gated: unconfirmed, source is paywalled or blocked)), not by the link budget.
- Rain depolarisation degrades C/I_xpol during the fade.
- Equinox sun outages are predictable minutes-long events; budget them separately from rain.

## Verify

- [ ] Slant range, FSPL and C/N0 recompute by hand to within 0.5 dB.
- [ ] Satellite EIRP, G/T and back-off come from the operator's data for the actual transponder and site.
- [ ] Combined C/N includes uplink, downlink, interference and intermodulation terms in linear form.
- [ ] Rain fade uses P.618 at the site's elevation, polarisation and frequency, with downlink noise rise included.
- [ ] Faded Es/N0 still exceeds the chosen MODCOD threshold plus implementation margin at the target availability.
- [ ] The antenna meets the off-axis EIRP density mask.
