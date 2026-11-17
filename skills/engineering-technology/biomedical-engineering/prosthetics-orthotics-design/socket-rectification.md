---
id: engineering-technology.biomedical-engineering.prosthetics-orthotics-design.socket-rectification
name: socket-rectification
category: engineering-technology
field: biomedical-engineering
product: prosthetics-orthotics-design
tags: [socket-rectification, digital-rectification, cad-socket, shape-capture, socket-modification]
level: advanced
status: draft
description: "Digitally rectify a prosthetic socket model: shape capture, landmark alignment, relief and compression zones, volume reduction, and verification with check sockets."
sources: ["Journal and clinical literature on digital socket design (confirm citations)", "Smith, Michael and Bowker (eds.), Atlas of Amputations and Limb Deficiencies", "https://www.o-p.org"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Digital socket rectification

**Goal:** turn a scan of the residual limb into a socket shape that loads tolerant tissue and relieves sensitive areas. The prosthetist is responsible for the final design.

## Workflow
1. **Capture:** scan the limb with a liner or sock as it will be worn (handheld or fixed structured-light or photogrammetry); orient the limb in the position used in the casting protocol.
2. **Align and trim:** mark landmarks (patellar tendon, fibular head, tibial crest, ischium) and set trimlines.
3. **Rectify:** apply local volume changes. Relief at pressure-sensitive bony areas (fibular head, tibial crest, distal end), compression (volume reduction) over tolerant tissue (patellar tendon, popliteal fossa), and overall volume reduction as the limb volume and liner thickness require.
4. **Check:** compare the rectified shape with the scan and adjust.
5. **Fabricate** a check socket (clear thermoplastic) by CNC or printing; evaluate fit, pressures, pistoning and gait; revise.
6. **Definitive:** laminate or print the definitive socket.

## Practice
- Use a library of templates for starting shapes, a record of rectification parameters for repeatability and learning.
- Keep scan quality control: no limb movement, correct scale and liner state.
- Document software version and the process used.

## Verify
- [ ] Check socket trial result recorded and rectification adjusted.
- [ ] Volume and landmark positions compared with scan.
- [ ] Digital files archived with the patient record.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
