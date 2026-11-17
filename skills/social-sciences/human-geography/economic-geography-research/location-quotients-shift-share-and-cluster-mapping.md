---
id: social-sciences.human-geography.economic-geography-research.location-quotients-shift-share-and-cluster-mapping
name: location-quotients-shift-share-and-cluster-mapping
category: social-sciences
field: human-geography
product: economic-geography-research
tags: [economic-geography-research, economic-geography, location-quotient, lq, shift-share-analysis, industrial-clusters, agglomeration, cluster-mapping, naics, nace, isic, sic, county-business-patterns, qcew, bres, regional-development, global-production-networks, gpn, global-value-chains, gvc, comtrade, tiva, labour-geography, economic-complexity, relatedness, smart-specialisation, disclosure-suppression, firm-interviews]
level: practitioner
status: draft
description: "Mapping regional economies: location quotients, shift-share decomposition, cluster identification and global production network tracing with interviews and trade data."
sources: ["Porter, 'Location, Competition, and Economic Development' (2000)", "Delgado, Porter & Stern, 'Defining Clusters of Related Industries' (2016)", "Coe & Yeung, Global Production Networks (2015)", "Hidalgo et al., 'The Product Space Conditions the Development of Nations' (2007)", "US BLS QCEW and Census County Business Patterns documentation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Location quotients, shift-share and cluster mapping

**Goal:** describe what a region specialises in, why it grew or shrank, and how it
plugs into wider production networks.

## 1. Data
Employment (or establishments, wages) by industry × region × year:
US County Business Patterns or QCEW; UK BRES; Eurostat structural business
statistics. Industry codes: NAICS (US), NACE (EU), ISIC (UN), SIC (UK, older US).
- **Suppression gotcha:** small cells are suppressed or reported as ranges to protect
  firm confidentiality. Many zeros are really "not disclosed". Use imputed versions
  where available, aggregate up a level, or flag.
- Industry classification revisions (e.g. NAICS 2017 → 2022) break time series;
  apply official concordances.

## 2. Location quotient (LQ)
LQ = (e_ir / e_r) ÷ (E_i / E), where e_ir is regional employment in industry i, e_r is
total regional employment, E_i and E national.
- LQ > 1: more concentrated than the nation; ≥1.25 is a common "specialisation" rule
  of thumb (a convention, not a test).
- Small regions + small industries → volatile LQs. Pair LQ with absolute employment.
- LQ says nothing about productivity or export orientation by itself.

## 3. Shift-share decomposition
Splits a region's employment change in industry i into:
- **National share:** growth if it grew at the national all-industry rate.
- **Industry mix:** extra from the industry's national rate vs all-industry rate.
- **Regional (competitive) shift:** the residual — local performance above/below
  the industry nationally.
Gotchas: results depend on start year and industry detail; the regional shift is a
residual, not an explanation. Dynamic shift-share (year-by-year) reduces start-year bias.

## 4. Identifying clusters
- **Co-location/benchmark definitions:** US Cluster Mapping Project groups industries
  that co-locate and link by input–output and skills (Delgado–Porter–Stern).
- Combine LQ, employment size and growth to classify regional cluster strengths.
- **Relatedness / economic complexity:** product-space style measures indicate which
  new industries a region could plausibly diversify into (used in EU smart
  specialisation). Measures are correlational; treat as hints.
- Validate with interviews: firms, trade associations, universities — clusters are
  relationships, not just co-location.

## 5. Global production networks (GPN) / value chains
- Trace a product's chain: lead firms, tier-1/2 suppliers, logistics, retailers.
  Sources: company reports, supplier lists, customs/bill-of-lading data, UN Comtrade
  (bilateral trade by HS code), OECD **TiVA** (trade in value added).
- Ask who captures value (margins, rents), who governs (standards, buyer power),
  and how labour and states shape it.
- Interview across nodes; elite interviews need careful access and anonymity.
- **Labour geographies:** workers as agents (strikes, organising) shape networks too —
  include union and worker interviews.

*Uncertainty:* the 1.25 LQ threshold and cluster definitions are conventions; check
those used in your target literature.

## Verify
- [ ] Industry codes harmonised across years; suppressed cells flagged or imputed.
- [ ] LQs reported with absolute employment and a stated threshold rationale.
- [ ] Shift-share start year justified and robustness checked.
- [ ] Cluster claims supported by linkage evidence, not co-location alone.
- [ ] Value-chain mapping triangulates trade data with interviews or documents.
