---
id: computing-software.it-support-helpdesk.desktop-support.esd-and-electrical-safety-for-technicians
name: esd-and-electrical-safety-for-technicians
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, laptop-hardware, esd-safety, electrostatic-discharge, antistatic-wrist-strap, electrical-safety, psu-hazard, lifting-technique, sds, msds, comptia-a-plus]
level: intro
status: draft
description: "Work safely on hardware: ESD controls, mains and PSU hazards, laser and toner cautions, lifting, battery handling and safety data sheets (A+ 220-1202 4.4)."
sources:
  - "https://www.comptia.org/certifications/a"
  - "https://www.osha.gov/electrical"
  - "https://www.osha.gov/hazcom"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# esd-and-electrical-safety-for-technicians

Goal: don't damage the hardware, don't hurt yourself (A+ 220-1202 4.4
safety procedures).

## ESD (protects the equipment)
- Static discharges you can't feel (< 3,000 V) still damage RAM, CPUs and
  boards — latent failures show up weeks later.
- Controls: antistatic **wrist strap** clipped to the chassis bare metal (or
  mat ground), **antistatic mat**, parts kept in **antistatic bags** (the
  shiny/pink ones) until fitted; handle boards by edges.
- Low humidity (winter, air-conditioned rooms) increases risk; carpets too.
- No strap available: unplug the device, then touch bare chassis metal
  before and often while handling parts (self-grounding). It's a fallback,
  not the standard — A+ guidance is strap plus mat.

## Electrical (protects you)
- **Disconnect power** before opening; for laptops also disconnect the
  battery.
- **Never open a PSU** or monitor/CRT — capacitors hold lethal charge after
  unplugging. PSUs are replace-not-repair.
- Never use a wrist strap when working on high-voltage equipment (PSUs,
  CRTs) — it provides a path to ground through you.
- Check cords for damage; no daisy-chained power strips; trip hazards from
  cables taped/covered.
- Electrical fire: Class C (US) / electrical-rated CO₂ extinguisher, never
  water.

## Other hazards
- **Lasers** in printers/optical drives — don't look into the beam path.
- **Toner**: fine powder, irritant and explosive in a normal vacuum; use a
  toner vacuum, cold water for skin.
- **Batteries**: lithium cells — swollen/punctured cells are fire risks.
- **Lifting**: bend knees, keep back straight, load close; team lift heavy
  servers/printers (follow site weight limit, often ~23 kg / 50 lb).
- **Safety Data Sheets (SDS/MSDS)** for chemicals (cleaners, toner,
  batteries): handling, PPE, first aid, disposal — know where they are
  kept.

## Workspace
Clear area, good lighting, screws tracked (magnetic tray), photos of cable
routing before disassembly, compliance with local government regulations
(electrical work above technician scope goes to licensed electricians).

## Verify
Before opening any device: power disconnected, strap connected and tested
(strap tester if available), parts in bags, SDS location known.
