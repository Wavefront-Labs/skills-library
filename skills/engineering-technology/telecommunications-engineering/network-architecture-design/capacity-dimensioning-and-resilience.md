---
id: engineering-technology.telecommunications-engineering.network-architecture-design.capacity-dimensioning-and-resilience
name: capacity-dimensioning-and-resilience
category: engineering-technology
field: telecommunications-engineering
product: network-architecture-design
tags: [telecommunications-engineering, network-architecture-design, capacity-planning, dimensioning, erlang-b, grade-of-service, busy-hour, bhca, oversubscription, contention-ratio, peak-to-mean, link-utilisation, growth-forecast, n-plus-1, diverse-routing, srlg, shared-risk-link-group, ring-topology, mesh-topology, availability, mtbf, mttr, five-nines, protection-switching, erps-g8032, mpls-frr, backbone-design]
level: practitioner
status: gated
description: "Dimension network links and nodes from busy-hour demand (Erlang B, oversubscription, peak-to-mean, growth) and design resilience with N+1, SRLG-diverse routing and series/parallel availability."
sources: ["ITU-T E.500 series (traffic engineering and grade of service)", "ITU-T G.8032 Ethernet ring protection switching", "ITU-T G.911 / reliability terminology for optical systems", "Iversen, Teletraffic Engineering and Network Planning (ITU/DTU handbook)", "Grover, Mesh-Based Survivable Networks", "RFC 4090 Fast Reroute extensions to RSVP-TE", "RFC 4202 Routing extensions in support of GMPLS (SRLG)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Capacity dimensioning and resilience — size links that survive their worst day

**Goal:** turn a demand forecast into link and node capacities, then make the design survive single failures without breaching utilisation or availability targets.

## 1. Build the busy-hour demand matrix

- Dimension for the **busy hour**, never the daily average. For call-like traffic, offered load A (Erlang) = BHCA x mean holding time (s) / 3600; for example, 3,600 calls/h x 120 s = 120 E.
- For packet traffic, take the 95th-percentile 5-minute rate per demand pair over the busiest week. If you only have averages, apply a **peak-to-mean** ratio: roughly 1.5-2 on aggregated backbone links and 3-10+ on small access aggregates (gated: unconfirmed, source is paywalled or blocked).
- Keep an A-Z matrix per service class (real-time, business, best effort) so QoS can be dimensioned per class.

## 2. Size call-limited resources with Erlang B

Compute blocking B(A,N) by recursion, not factorials:

`B(A,0) = 1;  B(A,n) = A*B(A,n-1) / (n + A*B(A,n-1))`

Increase n until B <= the target grade of service (typically 1% for trunks, 0.1-0.5% for emergency or interconnect (gated: unconfirmed, source is paywalled or blocked)). Check point: 10 E at 1% needs 18 circuits (recomputed with the recursion: B(10,17) = 1.29%, B(10,18) = 0.71%). Erlang B assumes Poisson arrivals with blocked calls cleared. Use Erlang C for queued systems. Overflow traffic is peaky, so size overflow routes with the equivalent random method rather than plain Erlang B.

## 3. Size packet links with contention and utilisation ceilings

- **Oversubscription** (sold capacity / uplink capacity) design points vary by operator; check your SLA. Common figures are 20:1-50:1 for residential aggregation, 4:1-10:1 for business, and 3:1 or better for data-centre leaf to spine (gated: unconfirmed, source is paywalled or blocked).
- **Busy-hour utilisation ceilings:** about **50% on protected links**, so the survivor stays under ~100% after a failure (2 x 50% = 100%, arithmetic), and **~70% on unprotected links** (policy figure, (gated: unconfirmed, source is paywalled or blocked)). Queueing delay rises steeply above ~80%, which is an alarm level, not a target.
- **Growth headroom:** months to exhaust = ln(ceiling / current) / ln(1 + monthly growth). At 30%/yr (~2.2%/month), a link at 35% hits 50% in about 16 months (recomputed 16.3). Fibre builds can take 6-18 months, so trigger upgrades early.
- Cap priority (EF) traffic at about 20-33% of link rate ((gated: unconfirmed, source is paywalled or blocked)) so lower classes are not starved.

## 4. Choose topology and protection

| Option | Spare capacity | Restoration | Use |
|---|---|---|---|
| Ring (SDH/OTN SNCP, G.8032 ERPS) | ~100% of working | under 50 ms ((gated: unconfirmed, source is paywalled or blocked)) | Metro, aggregation |
| Mesh, pre-planned (MPLS FRR, TI-LFA) | typically 40-70% ((gated: unconfirmed, source is paywalled or blocked)) | ~50 ms local repair ((gated: unconfirmed, source is paywalled or blocked)) | Core |
| Mesh, restoration (IGP, GMPLS) | lowest | sub-second to seconds | Cost-sensitive core |
| N+1 equipment (cards, PSUs, uplinks) | 1 spare per N | device dependent | Nodes |

Dual-home every aggregation node to two different core nodes and keep core node degree >= 3. Simulate every single link, node and SRLG failure, and confirm that no surviving link exceeds ~90-100%.

## 5. Availability maths

- Element: A = MTBF / (MTBF + MTTR). Series: A = A1 x A2 x ... Parallel: A = 1 - (1-A1)(1-A2).
- Downtime per year: 99.9% = 8.76 h; 99.99% = 52.6 min; 99.999% = 5.26 min (computed on 8,760 h).
- Fibre routes usually dominate. Buried cable is often quoted at a few cuts per 1,000 route-km per year, with an MTTR of 8-24 h (gated: unconfirmed, source is paywalled or blocked). These are placeholders, so use your own outage records. At 2 cuts/1,000 km/yr and 12 h MTTR, an unprotected 200 km route loses about 4.8 h/yr (99.95%) (computed 4.8 h, 99.945%). Two genuinely diverse routes in parallel reach better than 99.999% (computed 99.99997% for independent routes).

## Gotchas

- **Diverse on the map is not diverse in the ground.** Fibres that share a duct, bridge, landing station or riser share fate. Tag them with a **shared risk link group (SRLG)** and route protection SRLG-disjoint, not merely link-disjoint.
- The parallel formula assumes independent failures. Common power, a shared software release or a shared conduit makes real availability lower.
- Five-minute averages hide microbursts. A link at 40% can still drop packets on shallow-buffer switches, so check drop counters as well as utilisation.
- A mesh with spread protection can run above 50%, but only where failure simulation proves it.

Radio access demand comes from engineering-technology.telecommunications-engineering.radio-network-planning.lte-5g-coverage-and-capacity-planning. Optical spans are engineered in engineering-technology.telecommunications-engineering.fibre-transmission-design.optical-power-budget-and-dwdm-design.

## Verify

- [ ] Links are sized on busy-hour 95th-percentile demand plus growth to the planning horizon.
- [ ] The Erlang B tool reproduces the standard tables (10 E at 1% needs 18 circuits).
- [ ] Single-failure simulation (every link, node and SRLG) leaves no survivor above the agreed ceiling.
- [ ] Working and protection paths share no SRLG.
- [ ] The series/parallel availability meets the SLA using your own MTTR and cut-rate data.
- [ ] Upgrade triggers (50% protected, 70% unprotected) are set in monitoring, with lead time allowed for.
