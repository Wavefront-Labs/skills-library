---
id: engineering-technology.biomedical-engineering.medical-imaging-systems.gradient-coil-system
name: gradient-coil-system
category: engineering-technology
field: biomedical-engineering
product: medical-imaging-systems
tags: [gradient-coil, mri-gradients, slew-rate, eddy-currents, peripheral-nerve-stimulation]
level: advanced
status: draft
description: "Understand MRI gradient coil design and limits: strength and slew rate, eddy currents, linearity, acoustic noise, peripheral nerve stimulation and safety limits."
sources: ["Bushberg et al., The Essential Physics of Medical Imaging (MRI chapters)", "IEC 60601-2-33 Magnetic resonance equipment for medical diagnosis (confirm edition)", "https://www.iec.ch"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Gradient coil system

**Goal:** produce fast, linear field gradients for spatial encoding while keeping noise, heating and stimulation within limits.

## Basics
- Three orthogonal coils (x, y, z) add linear magnetic field variation along each axis to encode position. Performance is measured by **maximum amplitude** (clinical systems roughly tens of mT per metre; higher on research and head-only systems) and **slew rate** (tesla per metre per second), as well as linearity over the field of view.
- **Eddy currents:** switching gradients induce currents in conductive structures (cryostat), which distort fields. Active shielding coils cancel external fields, and pre-emphasis compensates residual eddy currents.
- **Lorentz forces** on the coil in the main field cause vibration and loud **acoustic noise**; mitigate with mounting, vacuum, quiet sequences.
- **Heating:** coil resistance and amplifier power; cooling with water channels.
- **Peripheral nerve stimulation (PNS):** rapidly changing gradient fields (dB/dt) induce currents in the body; the standard sets limits in operating modes to protect from stimulation and from cardiac effects; PNS often limits practical slew rate before hardware does.

## Verify (for acceptance and QA)
- [ ] Gradient linearity and eddy current compensation measured with phantoms.
- [ ] Acoustic noise and dB/dt limits met per operating mode.
- [ ] Cooling and interlock function tested.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
