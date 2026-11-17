---
id: engineering-technology.automotive-vehicle-engineering.chassis-suspension-design.body-bending-stiffness-and-load-paths
name: body-bending-stiffness-and-load-paths
category: engineering-technology
field: automotive-vehicle-engineering
product: chassis-suspension-design
tags: [bending-stiffness, load-paths-body, body-structure, biw, shear-panel, sill, floor-structure, body-bending, bending-mode, specific-stiffness]
level: practitioner
status: draft
description: "Specify body bending stiffness and design its load paths: test set-up, closed sections, shear panels, and trade-offs against mass, packaging and crash paths."
sources:
  - "Happian-Smith, Introduction to Modern Vehicle Design (chapter list)"
  - "Reimpell, Stoll and Betzler, The Automotive Chassis (chapter list)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Body bending stiffness and load paths

## 1. Definition and test
Support the body at the axle mounting points and apply vertical load at the seat or floor centre (or distributed in a defined way); bending stiffness K_B = F / deflection at the reference point (N/mm). Document supports and loading with the number. A first bending mode (typically a bit higher in frequency than the first torsion mode, though this varies by car) shows the same property dynamically.

## 2. Why it matters
Low bending stiffness leads to sagging, door and glass fit problems, and low first bending mode that couples with powertrain and road inputs to cause floor and steering wheel vibration (see NVH targets and body modal FEA).

## 3. Load paths
Trace load from where it enters (suspension mounts, powertrain mounts, seat mounts, belt anchorages, jacking points) to where it reacts. The main longitudinal paths are the sills (rockers), floor tunnel, side rails and roof rails; cross-members and shear panels connect them. Rules of thumb:
- Keep load paths continuous: avoid sudden section changes and offsets.
- Use closed sections for bending and torsion efficiency.
- Provide shear panels (cowl, rear package shelf, rear seat panel, floor) to close the box.
- Terminate beams into stiff nodes, not into thin panels.
- Align crash load paths with bending paths where possible, but check that stiff bending members do not carry crash loads into the passenger cell uncontrolled (see load path design).

## 4. Tools
Beam-and-shell simplified models early (SSS: simple structural surfaces method) for concept stage; full shell FEA later. Review strain-energy distribution (modal strain energy and static strain energy) to find inefficient areas and adjust mass where it is carrying load.

## 5. Mass
Aim for stiffness per mass. Techniques: tailor-welded or tailored-rolled blanks, higher strength steels for gauge reduction (stiffness depends on section geometry and modulus, not on strength, so higher-strength steel does not stiffen a section by itself), structural adhesives, aluminium and composites with deeper sections.

## Verify
- [ ] Test supports and load point documented.
- [ ] Load paths mapped from every major input to reaction.
- [ ] Strain-energy review done; low-efficiency regions addressed.
- [ ] Stiffness per mass tracked.
