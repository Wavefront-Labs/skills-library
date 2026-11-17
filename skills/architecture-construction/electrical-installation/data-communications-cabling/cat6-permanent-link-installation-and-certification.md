---
id: architecture-construction.electrical-installation.data-communications-cabling.cat6-permanent-link-installation-and-certification
name: cat6-permanent-link-installation-and-certification
category: architecture-construction
field: electrical-installation
product: data-communications-cabling
tags: [electrical-installation, data-communications-cabling, structured-cabling, cat6, cat6a, cat5e, utp, permanent-link, channel, horizontal-cabling, patch-panel, keystone-jack, punch-down, t568a, t568b, untwist, bend-radius, cable-certification, certifier, next, insertion-loss, wire-map, poe, tia-568, iso-11801]
level: practitioner
status: draft
description: "Install a Cat6/6A horizontal permanent link: route with power separation, keep bend radius and untwist limits, terminate T568A/B, and certify with a field tester."
sources: ["ANSI/TIA-568 Commercial Building Telecommunications Cabling Standard", "ANSI/TIA-569 Telecommunications Pathways and Spaces", "ISO/IEC 11801 Information technology - Generic cabling", "EN 50174-2 Installation planning and practices inside buildings"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cat6 permanent link installation and certification

**Goal:** install a horizontal copper link (patch panel to wall outlet) that certifies
first time to its category and will carry 1/10 Gb Ethernet and PoE for the life of
the building.

> **Licensing varies by jurisdiction.** Many places license data cablers separately
> from electricians (e.g. AU ACMA cabling registration; some US states have
> low-voltage licences). Data cabling shares ceilings and risers with mains wiring, so
> the electrical-safety steps below still apply. Values are typical; confirm against
> the standard edition and your manufacturer's warranty conditions.

## 1. Plan the link
- **Length budget:** permanent link ≤90 m (295 ft); total channel ≤100 m including
  ≤10 m of patch and equipment cords.
- **Category:** Cat6 for 1 Gb (10 Gb only to ~55 m in good conditions); Cat6A for 10 Gb at
  100 m and heavy PoE. Keep every component (cable, jacks, panel) the same category and,
  for a warranty, the same system vendor.
- **Pathway:** J-hooks/basket tray every ~1.2–1.5 m (4–5 ft); never lie on ceiling tiles
  or tie to ceiling-grid wires or pipes.
- **Separation from power:** cross mains at 90°; run parallel only with separation per
  TIA-569/EN 50174-2 — the required distance depends on screening and containment
  (figures such as 50 mm with a metal divider and ~200 mm unscreened are often quoted —
  unverified, confirm against your edition of the standard).

## 2. Safety before entering ceilings and risers
- Treat ceiling voids as containing live mains: if you must open or move power
  containment, have the circuits **isolated, locked off and tagged**, the tester proved,
  conductors **tested dead**, tester re-proved — by the electrician responsible.
- Watch for damaged/unsupported mains cables and live luminaire tails; report, don't move.
- PoE-powered links carry up to ~90 W (802.3bt) — low voltage but enough to arc on
  disconnection under load.

## 3. Pulling
1. Pull from boxes/reels via a pull-spool; label both ends **before** pulling.
2. Max pulling tension for 4-pair UTP: 25 lbf (110 N).
3. Minimum installed bend radius: 4× cable OD for UTP (8× for some screened types —
   check the datasheet). No kinks, no tight cable-ties: hook-and-loop ties, snug not cinched.
4. Leave a service loop at the rack (~3 m) and outlet (~300 mm), per site spec.

## 4. Terminate
- Pick **T568A or T568B** for the whole site and use it both ends (A is preferred by many
  government specs; B common in commercial practice).
  - T568B: 1 white/orange, 2 orange, 3 white/green, 4 blue, 5 white/blue, 6 green,
    7 white/brown, 8 brown. T568A swaps the orange and green pairs.
- Strip only what the jack needs; **pair untwist ≤13 mm (0.5 in)**; keep the jacket to the
  termination point.
- Punch down with the correct 110/Krone/LSA tool or use the vendor's tool-less cap;
  trim cleanly. Screened systems: bond the drain/foil to the jack shield 360°, and the
  panel to the telecom bonding busbar.
- Dress cables into the panel in numbered order; label panel port = outlet label.

## 5. Certify
1. Use a field certifier (Level IIe/III/IV per category) with **permanent-link adapters**
   (channel adapters for channel testing); reference/calibrate per the maker.
2. Select the correct limit (e.g. "TIA Cat 6 Perm. Link") and the cable's NVP.
3. Autotest every link. Key results: wire map, length, insertion loss, NEXT/PS NEXT,
   return loss, ACR-F, propagation delay/skew. Save with the outlet ID.
4. **Fail or marginal (*) pass:** usually termination — re-terminate before
   suspecting the cable. NEXT failures at one end point to excess untwist there; return
   loss to kinks or over-tight ties; wire map to a split pair (passes continuity, fails NEXT).
5. Hand over the full report, not a summary.

## Gotchas
- A "continuity tester" pass is not certification; split pairs pass a simple tester.
- Exceeding 90 m with a long service loop — measure it.
- Mixing T568A and B ends creates a crossover.
- Fibre in the same run: inspect-clean-inspect every connector; never look into a fibre.

## Verify
- [ ] Ceiling/riser mains isolated and proved dead by the responsible electrician before disturbing it.
- [ ] Every link ≤90 m, same category components throughout.
- [ ] Bend radius, tension, untwist ≤13 mm respected; no cinched ties.
- [ ] One wiring scheme (A or B) used site-wide; labels match at both ends.
- [ ] 100% of links certified PASS with permanent-link adapters; reports saved.
