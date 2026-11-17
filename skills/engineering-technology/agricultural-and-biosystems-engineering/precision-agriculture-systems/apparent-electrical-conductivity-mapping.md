---
id: engineering-technology.agricultural-and-biosystems-engineering.precision-agriculture-systems.apparent-electrical-conductivity-mapping
name: apparent-electrical-conductivity-mapping
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: precision-agriculture-systems
tags: [agricultural-and-biosystems-engineering, precision-agriculture-systems, ec-mapping, apparent-conductivity, veris, em38, electromagnetic-induction, soil-salinity-survey, management-zones]
level: advanced
status: draft
description: "Map soil apparent electrical conductivity with contact or EMI sensors: instrument choice, survey pattern, moisture conditions, temperature correction, calibration sampling."
sources:
  - "Geonics EM38 (https://geonics.com/html/em38.html)"
  - "USDA-ARS ESAP (https://www.ars.usda.gov/pacific-west-area/riverside-ca/agricultural-water-efficiency-and-salinity-research-unit/docs/model/esap-model/)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Apparent electrical conductivity mapping

**Goal:** a repeatable map of soil apparent electrical conductivity (ECa) that reflects texture, moisture, salinity and organic matter, used for zones and for directed soil sampling.

## What ECa measures
ECa is the bulk electrical conductivity of soil to the depth sensed; it increases with clay content, water content, salinity (dissolved salts) and in some cases cation exchange capacity. Sand and dry soil read low; wet clay and saline soil read high. ECa is not a direct measure of any single property; interpret it with ground truth.

## Instruments
- Contact (galvanic) sensors with coulter electrodes pulled through the soil (such as Veris sensors) give shallow and deep readings (roughly the top 0.3 m and 0.9 m).
- Electromagnetic induction (EMI) instruments (such as the Geonics EM38 family and similar) are non-contact and work in vertical and horizontal dipole modes with different depth responses (for the EM38-MK2 with the 1 m coil, effective depth about 1.5 m in vertical dipole and 0.75 m in horizontal dipole mode, per Geonics).

## Survey
1. Choose a time when the soil moisture is fairly uniform and near field capacity (not frozen, not freshly irrigated in patches), because moisture variation confounds the map. Repeat surveys in different conditions to test stability.
2. Drive parallel passes at a steady speed (spacing often 10-20 m depending on the desired resolution) with a GNSS receiver (RTK or good DGPS) and log the readings at 1 s or similar.
3. Record soil temperature and correct ECa to a standard temperature, 25 C, using the standard formula or the instrument software.
4. Calibrate EMI instruments in a known location and check drift (zero readings in the air for EMI per manufacturer).
5. Clean data: remove points at field edges, turns and with GNSS faults; interpolate.
6. Directed sampling: choose soil sample sites to span the range of ECa (software such as the USDA ESAP tools exists for salinity surveys) and analyse texture, moisture, salinity, organic matter; build the relationship between ECa and the property of interest.

## Use
Management zones for variable-rate seeding, lime or irrigation; salinity mapping (`sodicity-and-infiltration-hazard-sar` for water quality); soil boundary inference; interpret with yield and elevation layers.

## Verify
- [ ] Repeat survey tracks correlate (r above about 0.8 for the same conditions).
- [ ] Ground-truth correlation reported.
- Unconfirmed: depth responses; confirm in the instrument manual.
