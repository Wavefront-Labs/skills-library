---
id: engineering-technology.biomedical-engineering.biomechanics.opensim-model-scaling
name: opensim-model-scaling
category: engineering-technology
field: biomedical-engineering
product: biomechanics
tags: [opensim-scaling, musculoskeletal-modeling, opensim, scale-tool, marker-registration, subject-specific-model, marker-error]
level: practitioner
status: verified
description: "Scale an OpenSim musculoskeletal model with the Scale Tool: static-pose marker data, measurement sets, mass scaling, marker adjustment and error targets before inverse kinematics."
sources: ["OpenSim documentation, How to Use the Scale Tool (https://opensimconfluence.atlassian.net/wiki/spaces/OpenSim/pages/53087627)", "OpenSim documentation, Checklist - Evaluating your Simulation (https://opensimconfluence.atlassian.net/wiki/spaces/OpenSim/pages/53114566)", "Delp et al., OpenSim: open-source software to create and analyze dynamic simulations of movement (IEEE Trans Biomed Eng 2007)", "Hicks et al., Is my model good enough? Best practices for verification and validation of musculoskeletal models and simulations of movement (J Biomech Eng 2015)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# OpenSim model scaling

**Goal:** a subject-specific model whose segment lengths, masses and marker positions match the participant.

## Inputs
- A generic model (for example a gait model) with a marker set that matches your experimental markers.
- A static trial (TRC file) of the participant in a neutral pose, with the same marker names as the model.
- Participant mass.

## Steps in the Scale Tool
1. **Load model and static TRC.**
2. **Scale factors from markers:** define measurement pairs (marker pairs along each segment) and choose which body segments they scale; the tool computes the ratio of experimental to model marker distance, with optional uniform or non-uniform scaling per axis.
3. **Mass scaling:** set the subject mass and tick "Preserve mass distribution during scale" so the total mass equals the subject mass while relative segment masses are kept; if unticked, segment masses scale only by the segment scale factors and the total will not match the subject mass (OpenSim Scale Tool documentation).
4. **Static pose:** the tool can run inverse kinematics on a static frame range and adjust model marker positions to match experimental marker locations (marker placer).
5. **Save** the scaled model and marker set.

## Quality targets (OpenSim guidance)
The OpenSim checklist asks that the **maximum marker error** for bony landmarks and functional joint centres be below 2 cm and the **RMS error** below about 1 cm. Larger errors indicate mismatched marker names, poor measurement definitions or non-neutral pose.

## Checks
- Visual inspection of the scaled model in the GUI overlaid on the markers.
- Compare segment lengths against anthropometric measurements.
- After scaling, review muscle-tendon properties: scaled muscle optimal fibre lengths and tendon slack lengths change with segment length; verify the muscle force-length operating ranges in a range of motion test.

## Gotchas
- Marker naming errors cause silent failure.
- Foot and pelvis markers dominate error; check placement.
- Scaling cannot represent bone deformities or amputations; use specialised models.

## Verify
- [ ] Marker RMS and max errors recorded for the static pose.
- [ ] Joint ranges in the scaled model cover the experimental motion.
- [ ] Settings (XML) saved for reproducibility.
