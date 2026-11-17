---
id: engineering-technology.agricultural-and-biosystems-engineering.precision-agriculture-systems.gnss-guidance-and-variable-rate-setup
name: gnss-guidance-and-variable-rate-setup
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: precision-agriculture-systems
tags: [agricultural-and-biosystems-engineering, precision-agriculture-systems, precision-agriculture, precision-farming, gnss, gps, rtk, rtk-gnss, ntrip, rtcm, sbas, ppp, auto-steer, autosteer, guidance, terrain-compensation, isobus, iso-11783, task-controller, section-control, variable-rate, vra, prescription-map, management-zones, iso-xml, shapefile, yield-map, soil-ec, ndvi, ag-robotics]
level: practitioner
status: draft
description: "Set up GNSS guidance (RTK, NTRIP, SBAS), antenna and implement offsets, ISOBUS ISO 11783 section control, and variable-rate prescriptions with latency and zone-size checks."
sources:
  - "ISO 11783 series, Tractors and machinery for agriculture and forestry — Serial control and communications data network (ISOBUS)"
  - "Agricultural Industry Electronics Foundation (AEF), ISOBUS functionality definitions and conformance testing"
  - "RTCM 10403 Differential GNSS Services (RTCM 3.x) and the NTRIP protocol"
  - "Heege (ed.), Precision in Crop Farming: Site Specific Concepts and Sensing Methods"
  - "Stafford (ed.), Precision Agriculture for Sustainability"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# GNSS guidance and variable-rate setup — centimetres, offsets and latency

**Goal:** get a machine to drive repeatable lines, switch sections on and off at the
right place, and apply a prescription at the right rate in the right zone.

## 1. Choose the correction level
| Correction | Typical pass-to-pass | Repeatability year to year | Notes |
|---|---|---|---|
| Autonomous / SBAS (WAAS, EGNOS) | ±15–30 cm | poor (drifts) | Spreading, tillage |
| Satellite PPP services | ±3–5 cm after convergence | good | Convergence often 15–30+ min; vendor-specific |
| RTK (local base or network) | ±2–2.5 cm | ~±2.5 cm | Planting, strip-till, controlled traffic |

Figures are typical vendor claims; confirm in your receiver's specification.
RTK corrections arrive by **UHF radio** from a base station or over **cellular NTRIP**
from a network (RTCM 3.x messages, MSM preferred for multi-constellation). Single-base
accuracy degrades by roughly 1 ppm of baseline; keep baselines within about 10–20 km.

## 2. Base station and datum
- Survey the base position once and reuse exactly the same coordinates; moving or
  re-averaging the base shifts every saved line.
- Keep **one datum and epoch** across base, network, guidance lines and prescription maps.
  Mixing WGS 84 with a regional frame (NAD83, ETRS89, GDA2020) can shift lines by
  tens of centimetres to more than a metre.

## 3. Geometry and offsets
1. Measure antenna height above ground and its fore-aft and lateral offset from the
   tractor's control point (often the rear axle centre).
2. Calibrate the **terrain compensation** IMU on level ground (vehicle facing both
   directions). Without it, a 2 m antenna on a 5° side slope reports a lateral error of
   2 × sin 5° ≈ 17 cm.
3. Enter implement offsets: hitch-to-boom/row-unit distance, lateral offset, width,
   section widths. For towed implements, use implement steering or passive guidance
   offset learning if fitted.
4. Tune steering gains (aggressiveness, line acquisition) at working speed;
   oscillation means too much gain.

## 4. ISOBUS (ISO 11783)
- The virtual terminal function is now called **Universal Terminal (UT)**; the
  implement's ECU draws its screen on any compatible display.
- **Task Controller**: TC-BAS (totals), TC-GEO (position-based prescriptions,
  as-applied logging), TC-SC (automatic section control). **TIM** lets an implement
  command tractor functions.
- Check both the display and the implement for the same functionality in the AEF
  ISOBUS database before buying; "ISOBUS compatible" alone does not guarantee TC-SC
  or TC-GEO.
- Job data moves as **ISO-XML** (TASKDATA.XML plus binary log files); prescriptions
  often also arrive as shapefiles converted by the farm-management software.

## 5. Section control timing
Set **turn-on and turn-off look-ahead** to the system latency:
`lead distance (m) = speed (m/s) × latency (s)`.
At 20 km/h (5.6 m/s) a 0.5 s valve delay is 2.8 m. Measure latency with a field test
(paper or chalk marks at a headland edge) rather than trusting defaults. Overlap
setting (e.g. 0–50 % of a section) trades skips against double application.

## 6. Variable-rate prescriptions
1. Build zones from stable layers: multi-year normalised yield maps, apparent soil
   electrical conductivity (EM or contact sensors), elevation, soil tests, imagery
   indices (NDVI/NDRE). Clean yield data first (flow delay, start/stop, narrow passes).
2. Set rates per zone from agronomic response (soil test calibration, yield goal).
3. Check **minimum zone size** against machine resolution: zone length must exceed
   speed × rate-change response time (granular spreaders and air carts often 2–10 s;
   sprayer rate controllers 1–3 s, vendor-specific) plus the implement width.
4. Export in the controller's format (ISO-XML grid or shapefile with rate attribute),
   set units and a default/out-of-field rate, and load with the correct product.
5. After the job, compare the **as-applied map** with the prescription.

## Gotchas
- Correction loss (cellular dead spots, radio shadowing) drops to float or SBAS;
  set an alert and a fallback so planting does not silently degrade.
- Firmware mismatch between display and implement ECU causes object pool errors;
  update both together.
- Rate controllers cannot exceed physical limits: check the prescription's min and
  max against nozzle or metering range at the planned speed.
- Autonomous and robotic machines need a risk assessment and functional-safety design
  (e.g. the ISO 18497 series and local machinery regulations).

## Verify
- [ ] Correction type, datum and base coordinates are documented and consistent.
- [ ] Antenna, IMU and implement offsets were measured and calibrated on level ground.
- [ ] Section on/off look-ahead was set from a measured field latency test.
- [ ] Display and implement support the needed ISOBUS functions (UT, TC-SC, TC-GEO).
- [ ] Prescription zones exceed machine response distance; as-applied map matches.
