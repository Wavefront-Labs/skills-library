---
id: engineering-technology.telecommunications-engineering.fibre-transmission-design.optical-power-budget-and-dwdm-design
name: optical-power-budget-and-dwdm-design
category: engineering-technology
field: telecommunications-engineering
product: fibre-transmission-design
tags: [telecommunications-engineering, fibre-transmission-design, fiber-optics, optical-power-budget, link-loss-budget, attenuation, splice-loss, connector-loss, dwdm, cwdm, itu-t-g652, itu-t-g657, itu-t-g694-1, flexgrid, chromatic-dispersion, pmd, osnr, edfa, raman, coherent, otdr, bidirectional-otdr, acceptance-testing, span-design, fibre]
level: practitioner
status: gated
description: "Engineer fibre links: loss budgets at 1310/1550 nm with splice/connector allowances and margins, dispersion limits, DWDM on the G.694.1 grid, EDFA span OSNR, and OTDR acceptance."
sources: ["ITU-T G.652 Characteristics of a single-mode optical fibre and cable", "ITU-T G.657 Bending-loss insensitive single-mode fibre", "ITU-T G.694.1 Spectral grids for WDM applications: DWDM frequency grid", "ITU-T G.698.2 Amplified multichannel DWDM applications with single-channel optical interfaces", "IEC 61280-4-2 Single-mode attenuation and optical return loss measurement", "ANSI/TIA-568.3 Optical fiber cabling and components standard", "Agrawal, Fiber-Optic Communication Systems"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Optical power budget and DWDM design — make every span close, then every channel

**Goal:** prove that each fibre span has enough optical budget, and that each DWDM channel has enough OSNR and dispersion tolerance end to end, with documented margins and OTDR acceptance.

## 1. Loss budget (unamplified link)

Link loss = fibre km x attenuation + splices x splice loss + connectors x connector loss + passive devices (mux/demux, splitters) + margin.

Typical design allowances for cabled G.652.D (check your cable spec and operator rules; every value in this table is (gated: unconfirmed, source is paywalled or blocked)):

| Item | Design value |
|---|---|
| Fibre at 1310 nm | 0.35 dB/km |
| Fibre at 1550 nm | 0.25 dB/km (0.20 dB/km typical measured) |
| Fusion splice | 0.1 dB (typical measured 0.02-0.05) |
| Mated connector pair | 0.5 dB (TIA-568 maximum 0.75 dB) |
| Repair/ageing margin | 3 dB, or a per-km allowance for long routes |

The link closes if **Tx minimum launch - Rx sensitivity (or overload checks) - path penalties >= link loss**. Example: 40 km at 1310 nm with 10 splices and 2 connector pairs gives 14 + 1 + 1 + 3 = 19 dB (recomputed: 40 x 0.35 + 10 x 0.1 + 2 x 0.5 + 3 = 19.0). On short links, attenuate if Prx exceeds the receiver's maximum input.

## 2. Dispersion

- G.652 fibre has zero dispersion near 1310 nm and about 17 ps/(nm km) at 1550 nm (gated: unconfirmed, source is paywalled or blocked). Accumulated dispersion = D x L.
- **Direct-detect NRZ** at 10 Gb/s tolerates roughly 800-1,600 ps/nm (about 50-100 km at 1550 nm at 17 ps/nm/km, arithmetic checked) depending on the transmitter (gated: unconfirmed, source is paywalled or blocked); beyond that you need dispersion-compensating fibre/modules or a different design. At 25G+ direct detect, reach in the C-band shrinks to a few km, which is why short-reach optics use O-band.
- **Coherent** transponders (100G-800G) compensate tens of thousands of ps/nm electronically. Do not deploy DCMs on coherent-only lines; they add loss and nonlinearity. Check PMD (mean DGD) against the transponder limit on old fibre.

## 3. DWDM grid and amplified spans

- **ITU-T G.694.1** (version 10/20 is in force per itu.int) anchors the grid at 193.1 THz. Fixed spacings are 12.5/25/50/100 GHz. Flexgrid uses central frequencies 193.1 + n x 0.00625 THz and slot widths of m x 12.5 GHz (for example 75 GHz for many 400G coherent signals) (the grid parameters (gated: unconfirmed, source is paywalled or blocked); the itu.int page did not reproduce the text).
- C-band EDFAs cover roughly 1530-1565 nm (about 4.4 THz by c/lambda: 196.1 - 191.7 THz, computed; the skill's former 4.8 THz is a common rounded planning figure). Spans are typically 80-100 km with 20-25 dB loss. Amplifier noise figure is about 5-6 dB (both (gated: unconfirmed, source is paywalled or blocked)). Use Raman to extend long or lossy spans.
- **OSNR per span chain** (0.1 nm reference bandwidth, identical spans):
  `OSNR (dB) = 58 + P_ch(dBm) - L_span(dB) - NF(dB) - 10 log10(N_spans)`
  Example: 0 dBm per channel, 22 dB spans, NF 5.5 dB, 10 spans gives about 20.5 dB (recomputed 20.5; the constant 58 dB is the standard 0.1 nm reference-bandwidth term, (gated: unconfirmed, source is paywalled or blocked)).
- Compare with the transponder's required OSNR at its post-FEC threshold (about 12-13 dB for 100G DP-QPSK (gated: unconfirmed, source is paywalled or blocked); considerably higher for 16QAM 400G; take vendor data). Then add margins for ageing, nonlinearity, PDL, filtering through ROADMs, and repairs (often 3-5 dB in total (gated: unconfirmed, source is paywalled or blocked)).
- Launch power trades ASE noise against nonlinearity; optimum per-channel power is typically about 0 to +3 dBm on G.652 for coherent channels (gated: unconfirmed, source is paywalled or blocked). Use the vendor planning tool or a GN-model calculation and do not exceed it.

## 4. OTDR acceptance

- Test at **1310 and 1550 nm** (add 1625 nm for bend-sensitive routes) with launch and tail cords longer than the dead zone (often 0.5-1 km (gated: unconfirmed, source is paywalled or blocked)).
- Report splice loss as the **bidirectional average**. A single-direction trace shows "gainers" where fibres with different backscatter coefficients meet.
- Typical acceptance (contract specific): splice average <= 0.1 dB, total link loss within the budget, connector reflectance <= -35 dB UPC / <= -55 dB APC (all (gated: unconfirmed, source is paywalled or blocked)), and no unexplained events. Confirm the overall figure with an LSPM (light source and power meter) insertion-loss test.

## Gotchas

- **Loss higher at 1550/1625 nm than at 1310 nm at one point means a macrobend**, usually in a tray or duct entry. Splice defects show similar loss at both wavelengths.
- Dirty connectors cause most field failures. Inspect and clean before every mating.
- A design checked only at full load can fail at day-one low channel count. Run amplifiers in constant-gain mode and check partial loading and add/drop transients.
- Use the worst-case datasheet values (minimum launch, worst sensitivity), not typical values.
- Route diversity and SRLGs are covered in engineering-technology.telecommunications-engineering.network-architecture-design.capacity-dimensioning-and-resilience.

## Verify

- [ ] Every span closes with the agreed margin using worst-case optics, and short spans do not overload receivers.
- [ ] Accumulated dispersion and PMD are within transponder tolerance (or the line is coherent).
- [ ] End-of-life OSNR exceeds required OSNR plus margins on the worst channel.
- [ ] Channel plan is on the G.694.1 grid and fits the ROADM/filter passbands.
- [ ] OTDR bidirectional averages and LSPM loss meet acceptance at every specified wavelength.
