---
id: engineering-technology.agricultural-and-biosystems-engineering.irrigation-design.deficit-irrigation-and-yield-response
name: deficit-irrigation-and-yield-response
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: irrigation-design
tags: [agricultural-and-biosystems-engineering, irrigation-design, deficit-irrigation, yield-response-factor, fao-33, regulated-deficit, water-stress-sensitivity, crop-water-production-function]
level: advanced
status: gated
description: "Plan deficit irrigation with the FAO yield-response factor Ky: relative yield loss from ET shortfall, sensitive growth stages, economics and salinity risks."
sources:
  - "Allen, Pereira, Raes & Smith, FAO Irrigation and Drainage Paper 56: Crop Evapotranspiration (https://www.fao.org/4/x0490e/x0490e00.htm)"
  - "FAO Irrigation and Drainage Paper 33, Yield Response to Water (Doorenbos & Kassam) (https://www.fao.org)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Deficit irrigation and yield response

**Goal:** decide whether and where to apply less than full crop water, and what yield you give up.

## Model
FAO 33 relates relative yield loss to relative ET deficit: 1 - Ya/Ym = Ky x (1 - ETa/ETm), where Ya and Ym are actual and maximum yield, ETa and ETm actual and maximum ET. Ky is crop and stage specific. Ky above 1 means the crop is sensitive (a 10 percent ET deficit costs more than 10 percent yield). Published Ky values (26 crops at various growth stages, per FAO Water Report 22 at fao.org/4/Y3655E/y3655e05.htm) are in FAO 33; read the table for your crop and stage. FAO Irrigation and Drainage Paper 66 (Steduto et al., 2012, Crop yield response to water, https://www.fao.org/4/i2800e/i2800e00.htm) replaces the seasonal equation with the daily AquaCrop model, confined to herbaceous crops.

## Practice
- Spare the sensitive stages (flowering, grain or fruit set for many crops) and stress the tolerant ones (vegetative growth, late ripening for some crops). Regulated deficit irrigation is used on tree and vine crops to control vigour and quality; wine grapes are a widely cited case (gated: unconfirmed, source is paywalled or blocked).
- Compare the saved water value and cost with the yield or quality loss using the water production function and crop price; the economic optimum is below full ET when water is expensive or limited.
- Cautions: salinity (less leaching raises root-zone salt), fruit quality (size, sunburn) and soil water reserve for the next season.

## Steps
1. Compute ETm from `single-and-dual-crop-coefficient-method`.
2. Choose the stage-wise ETa targets and the irrigation schedule that produces them (`checkbook-water-balance-scheduling`).
3. Estimate yield by the equation by stage, multiply across stages or use a seasonal Ky.
4. Check with soil moisture sensors that the deficit stays where planned.

## Verify
- [ ] Ky value and its source recorded.
- [ ] Observed yield compared to the prediction at season end to tune.
- Unconfirmed: Ky values for local varieties differ; use local trial data where it exists.
