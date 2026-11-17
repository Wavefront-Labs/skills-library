---
id: engineering-technology.agricultural-and-biosystems-engineering.precision-agriculture-systems.machine-vision-for-weeds-and-fruit
name: machine-vision-for-weeds-and-fruit
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: precision-agriculture-systems
tags: [agricultural-and-biosystems-engineering, precision-agriculture-systems, ag-machine-vision, weed-detection, fruit-detection, object-detection, semantic-segmentation, spot-spraying, model-validation, agricultural-robotics]
level: advanced
status: draft
description: "Build or evaluate machine vision for weeds or fruit: camera and lighting choices, dataset collection, labelling, model split by field, metrics, latency and field validation."
sources:
  - "ASABE Standards, Engineering Practices and Data (https://www.asabe.org)"
  - "ISO standards catalogue (https://www.iso.org)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Machine vision for weeds and fruit

**Goal:** a vision system that detects targets reliably enough to act (spot-spray, pick, count) under real field conditions.

## Choose sensing
- Camera: global-shutter sensors or short exposure to avoid motion blur at working speed; check the required exposure for the ground speed and resolution (the target must not move by more than a fraction of a pixel during exposure).
- Lighting: sunlight changes in minutes; shrouded or enclosed camera bays with artificial lighting (often LED strobe) give consistent images by day and night. Use filters or NIR bands where they add contrast (green-on-brown can use simple vegetation indices; green-on-green needs learned models for weeds in crop).
- Position and height: mount for a clear view of the crop row with a defined field of view; protect from dust, water and vibration.

## Data and models
1. Collect images across the whole range of conditions: growth stages, soil colours, moisture, light, crop varieties, weed species and densities, and locations; the model will fail on conditions it did not see.
2. Label carefully with clear rules (what counts as a weed, whether partial fruit counts); use two reviewers for a subset to check agreement.
3. Choose the task: classification, object detection (boxes), or segmentation (pixels); detection or segmentation is typical for weeds and fruit. Start from pretrained backbones and fine-tune.
4. Split the data into training, validation and test sets by field and date, not by random frames, since adjacent frames are almost identical and random splits give inflated scores.
5. Metrics: precision, recall, F1, and mean average precision for detection; per-class and per-condition results; the cost of each error type matters (a missed weed versus a sprayed crop plant).
6. Latency budget: camera to nozzle or actuator, at the working speed; choose edge hardware (embedded GPU or accelerator) and measure the end-to-end time under load; pulse-width-modulated nozzles or valves actuate on the result.

## Field validation
Count the target truth in plots by hand, compare to the system's decisions per plot, compute the hit rate and the herbicide or labour saved, and test in different fields and times. Monitor drift: retrain when conditions change. Spraying decisions fall under the pesticide label and regulations, so the application remains the operator's legal responsibility.

## Verify
- [ ] Test results reported on a held-out field and date.
- [ ] End-to-end latency measured at the maximum speed.
- Unconfirmed: hardware and model choices; evolve rapidly.
