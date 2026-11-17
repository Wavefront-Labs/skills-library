---
id: engineering-technology.agricultural-and-biosystems-engineering.controlled-environment-systems.nutrient-solution-ec-and-ph-management
name: nutrient-solution-ec-and-ph-management
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: controlled-environment-systems
tags: [agricultural-and-biosystems-engineering, controlled-environment-systems, nutrient-solution-management, ec-ph-control, hydroponic-nutrients, stock-solution, fertilizer-injector, alkalinity, meter-calibration, hydroponics]
level: practitioner
status: draft
description: "Manage hydroponic nutrient solution: EC and pH targets, stock A and B separation, injector setup, alkalinity, meter calibration, top-up and periodic lab analysis."
sources:
  - "ASABE Standards, Engineering Practices and Data (https://www.asabe.org)"
  - "Keller & Bliesner, Sprinkle and Trickle Irrigation"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Nutrient solution EC and pH management

**Goal:** a solution with the right strength, balance and pH for the crop, kept stable by measurement.

## Targets (typical; take the crop's own guide first)
- pH in the root zone: about 5.5-6.5 for most hydroponic crops (many growers aim for the middle of the range); outside this, iron, phosphorus and other nutrients become less available.
- EC (electrical conductivity, in mS/cm): leafy greens often about 1.2-2.0 and fruiting crops such as tomato higher, about 2-3.5 depending on stage and climate; high light and low humidity usually mean lower EC targets and vice versa. Use the breeder or extension recommendation.

## Stock solutions
- Concentrated stocks in separate tanks (commonly A with calcium nitrate and iron chelate, B with phosphates and sulphates, plus acid or base) so that calcium does not precipitate with phosphate or sulphate in concentrate. Use fertiliser-grade salts and a recipe tuned to the crop and the water analysis.
- Dosing: proportional injectors or EC/pH controllers with dosing pumps; calibrate the dosing rates by volumetric tests.
- Water quality: analyse source water for alkalinity (bicarbonate), Na, Cl, Ca, Mg and other ions, and subtract them from the recipe. High alkalinity needs acid (nitric or phosphoric, which count as nutrients) to bring the pH down; high sodium or chloride accumulates in a recirculating system.

## Measurement
- Calibrate pH meters with fresh buffers (for example pH 4 and 7) before use and replace the electrode when response slows; calibrate EC meters with a standard (for example a 1.413 mS/cm potassium chloride standard at 25 C) with temperature compensation.
- Check the controller sensors against a hand meter weekly.
- Send solution samples for ion analysis every few weeks (more often at the start); adjust the recipe because the crop takes up ions at different rates and the solution drifts.

## Recirculating systems
EC rises as water is lost and falls as the crop takes up nutrients faster than water; top up with water or a diluted feed according to EC and the lab ion analysis; flush or replace the solution on a schedule or when the unwanted ions build up.

## Verify
- [ ] Meter calibration log.
- [ ] Lab ion analysis compared with the target recipe.
- Unconfirmed: recipes and targets per crop; use the crop guides.
