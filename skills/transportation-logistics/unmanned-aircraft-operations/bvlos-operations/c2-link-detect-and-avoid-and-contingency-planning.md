---
id: transportation-logistics.unmanned-aircraft-operations.bvlos-operations.c2-link-detect-and-avoid-and-contingency-planning
name: c2-link-detect-and-avoid-and-contingency-planning
category: transportation-logistics
field: unmanned-aircraft-operations
product: bvlos-operations
tags: [bvlos, beyond-visual-line-of-sight, c2-link, command-and-control, link-budget, lte, 4g, 5g, satcom, detect-and-avoid, daa, adsb-in, ground-based-radar, electronic-conspicuity, visual-observers, contingency-volume, ground-risk-buffer, lost-link, flight-termination, part-108, sora, operational-authorisation, waiver]
level: advanced
status: gated
description: "BVLOS craft: sizing and monitoring the C2 link, choosing a detect-and-avoid method, defining contingency volumes and lost-link behaviour, and building the case for an approval."
sources: ["https://www.federalregister.gov/documents/2026/01/28/2026-01644/normalizing-unmanned-aircraft-systems-beyond-visual-line-of-sight-operations-reopening-of-comment", "https://www.faa.gov/uas", "https://jarus-rpas.org/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# C2 link, detect-and-avoid and contingency planning

**Goal:** fly where you can't see the aircraft while keeping three things true: you
can always control it (or it does something safe), it won't hit another aircraft, and
it stays inside the volume you were approved for. *Regulatory frameworks are changing
(e.g. FAA Part 108: proposed rule published August 2025, comment period closed 11 February 2026, final rule not yet published as of 25 October 2026); confirm current status.*

## 1. Command-and-control (C2) link
- **Options:** direct radio (line-of-sight, range limited by terrain), cellular
  (LTE/5G — coverage at altitude differs from on the ground), satcom (latency,
  bandwidth limits), often combined for redundancy.
- **Link budget:** transmit power + antenna gains − path loss − margins ≥ receiver
  sensitivity. Keep a fade margin (often 10 dB+) and check Fresnel-zone clearance over
  terrain/obstacles for direct radio.
- **Survey the route**: fly or drive with a test modem to log signal strength (RSRP/SINR
  for cellular) at operating altitude; mark dead zones.
- Monitor in flight: RSSI/link quality, latency, packet loss, and the **time since last
  good packet**. Alert before you lose it, not after.

## 2. Detect and avoid (DAA)
Choose a method proportionate to the airspace and the risk:
- **Strategic mitigation:** fly low (below ~120 m), in atypical/segregated airspace,
  near structures (shielded), at times when crewed traffic is rare; publish NOTAMs.
- **Electronic conspicuity:** ADS-B In receivers detect equipped aircraft (not all are).
- **Ground-based surveillance:** radar or acoustic systems covering the corridor.
- **Visual observers (VOs)** stationed along the route with radios — classic but
  labour-intensive.
- **Onboard DAA** (radar/vision) — emerging; check what performance standard your
  regulator accepts.
Define the **avoid manoeuvre**: typically descend and/or hold, land, or alter course;
know the time from detection to completing it.

## 3. Volumes and buffers (SORA-style)
- **Flight geography:** where you intend to fly.
- **Contingency volume:** around it, where abnormal procedures bring the aircraft back.
- **Ground risk buffer:** beyond that, to contain the aircraft if it must terminate
  (e.g. the 1:1 rule — buffer ≥ max height — for simple cases (gated: unconfirmed, source is paywalled or blocked), or ballistic/glide
  calculations).
- Containment: geofencing plus a flight termination system (parachute, motor cut) that
  triggers before leaving the operational volume, depending on the risk class.

## 4. Lost-link and emergency procedures
- Pre-programme lost-link behaviour per route segment: continue to next waypoint and
  land, return, or loiter then land at a designated site. Timeouts set from link
  analysis (e.g. 5–30 s).
- Brief what crewed traffic will see (a predictable path), and how ATC/airspace users
  are informed of a lost link (notify ATC by phone per your approval).
- Emergency landing sites mapped along the route.

## 5. The approval case
- Concept of operations, risk assessment (SORA in EU/UK and many others; FAA waiver
  or Part 108 equivalent in the US), DAA and C2 performance evidence, crew training,
  maintenance, and the operations manual.
- Evidence comes from your test flights and logs — keep them.

## Gotchas
- Cellular networks prioritise ground users; tower antennas point down — coverage at
  100 m can be patchy.
- A VO's "clear" is only as good as their sightline and attention; rotate them.
- Mixing DAA alerts with a high pilot workload — automate alerts, keep one person
  dedicated to traffic.

## Verify
- [ ] C2 survey shows margin along the whole route at operating altitude.
- [ ] DAA method defined with a detection-to-avoid time shorter than the closure time.
- [ ] Flight geography, contingency volume and ground risk buffer drawn on the map.
- [ ] Lost-link behaviour set per segment; emergency landing sites mapped.
- [ ] Approval conditions printed and briefed to the crew.

## Checked

Jurisdiction: United States (FAA) with JARUS/EASA references. Checked 2026-10-25: FAA Part 108 BVLOS was proposed in August 2025, comments closed 11 February 2026 and no final rule had issued by late October 2026 (Federal Register and FAA pages). SORA v2.5, EASA AMC, ASTM F3442 and RTCA DO-362 content is paywalled or was not read; the buffer rule is marked gated and the link-budget and fade-margin figures are generic engineering practice, not regulatory claims.

Method: documentation only; no commands were run.
