---
id: engineering-technology.agricultural-and-biosystems-engineering.precision-agriculture-systems.gnss-accuracy-classes-pass-to-pass-and-absolute
name: gnss-accuracy-classes-pass-to-pass-and-absolute
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: precision-agriculture-systems
tags: [agricultural-and-biosystems-engineering, precision-agriculture-systems, pass-to-pass-accuracy, gnss-positioning, rtk-gnss, accuracy-classes, repeatable-accuracy, sbas, ppp]
level: practitioner
status: draft
description: "Choose a GNSS correction level for a farm job: pass-to-pass versus year-to-year accuracy, typical accuracy of SBAS, PPP and RTK, and what each can support."
sources:
  - "Pierce, Precision Agriculture (and related precision agriculture references)"
  - "Zhang, Precision Agriculture Technology for Crop Farming (CRC Press)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# GNSS accuracy classes: pass-to-pass and absolute

**Goal:** buy or configure the cheapest correction that meets the job's tolerance.

## Two kinds of accuracy
- **Pass-to-pass (relative)**: how far apart successive passes are placed over minutes to an hour, which matters for spraying, tillage and seeding in one session.
- **Absolute / repeatable (year-to-year)**: whether you can return to the same line next season; this needs a fixed reference (the same RTK base position and datum, or a network) because satellite-based corrections drift with time and the datum.

## Typical levels (order of magnitude; vendors quote their own figures)
| Correction | Pass-to-pass | Typical use |
|---|---|---|
| Autonomous or SBAS (WAAS, EGNOS) | decimetre-class (vendor-quoted, unconfirmed) | spraying, mapping, light tillage |
| Subscription satellite or PPP-based services | a few cm to about 10 cm after convergence | spraying, row-crop work where convergence time is acceptable |
| RTK (own base or network) | about 2-3 cm | planting on rows, strip-till, controlled traffic, drip tape laying |

## Selection
1. Define the tolerance: seeding within a row needs about 2-3 cm; boom spraying tolerates 10-30 cm.
2. Check coverage and signal reliability on the farm (cellular for network RTK; line of sight for radio base).
3. Consider repeatability needs (controlled traffic or sub-surface drip requires RTK with fixed coordinates).
4. Consider convergence time of PPP services at start-up and after signal loss.

## Gotchas
- A receiver labelled "RTK ready" can be run in a lower mode if the subscription lapses.
- Datum and epoch mismatches shift lines by tens of cm between systems.

## Verify
- [ ] Drive the same AB line on two days and measure offset against the claimed repeatability.
