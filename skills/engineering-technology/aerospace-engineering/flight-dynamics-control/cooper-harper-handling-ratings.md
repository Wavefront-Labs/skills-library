---
id: engineering-technology.aerospace-engineering.flight-dynamics-control.cooper-harper-handling-ratings
name: cooper-harper-handling-ratings
category: engineering-technology
field: aerospace-engineering
product: flight-dynamics-control
tags: [flight-dynamics, handling-qualities, cooper-harper, pilot-rating, flying-qualities, evaluation-task, test-pilot]
level: practitioner
status: gated
description: "Use the Cooper-Harper rating scale properly in simulation and flight evaluation: task definition, pilot decision tree, levels, and reporting of comments."
sources:
  - "Cooper and Harper, The use of pilot rating in the evaluation of aircraft handling qualities (NASA TN D-5153, 1969), https://ntrs.nasa.gov/api/citations/19690013177/downloads/19690013177.pdf"
  - "MIL-STD-1797"
  - "Hodgkinson, Aircraft Handling Qualities"
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# Cooper-Harper handling ratings

**Goal:** a defensible numeric rating of handling qualities for a defined task.

## The scale
Ratings 1-10 via a decision tree: Is the aircraft controllable? Is adequate performance attainable with a tolerable pilot workload? Is it satisfactory without improvement? Source: Cooper and Harper, NASA TN D-5153, April 1969 (title and authors confirmed on NTRS; the PDF is a scanned image so the descriptors below are unconfirmed (gated: unconfirmed, source is paywalled or blocked)). Resulting levels: 1-3 satisfactory (Level 1), 4-6 adequate performance but deficiencies warrant improvement (Level 2), 7-9 adequate performance not attainable, improvement mandatory (Level 3), 10 control will be lost during some portion of the task.

## How to run an evaluation
1. Define the task with objective performance bands: for example "capture and hold pitch attitude within +/-0.5 degrees; desired" and "+/-2 degrees; adequate".
2. Brief the pilot; record the pilot's workload, compensation and comments, then rating, with the decision-tree path.
3. Repeat with several pilots and configurations (failure states, gust levels).
4. Compile ratings with comments; look for spread, since ratings are subjective (spread of 1-2 points is normal).

## Use in design
- Link configurations to the criteria (CAP, bandwidth) and to piloted simulator ratings.
- The Level 1/2/3 terminology comes from the military handling-qualities specifications (MIL-STD-1797, not read) (gated: unconfirmed, source is paywalled or blocked). Level 1 is the design target for normal operations; degraded modes accept Level 2 or 3 as set by the requirements.

## Gotchas
- A rating without a task and the performance standards is meaningless.
- Pilot-induced oscillation tendencies are rated separately (PIO rating scale).

## Verify
- [ ] Report lists the task, performance standards, configurations, pilots, ratings and comment summary.
