---
id: computing-software.it-support-helpdesk.desktop-support.print-quality-and-paper-path-faults
name: print-quality-and-paper-path-faults
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, printer, printing, print-quality, paper-jam, laser-printer, fuser, imaging-drum, toner, inkjet, thermal-printer, comptia-a-plus, printer-maintenance]
level: practitioner
status: draft
description: "Map print defects and jams to the failing part: laser imaging stages (streaks, ghosting, smearing), inkjet clogs, thermal fades and paper path jams."
sources:
  - "https://www.comptia.org/certifications/a"
  - "https://support.hp.com/"
  - "https://support.brother.com/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# print-quality-and-paper-path-faults

Goal: map a visible defect to the component that causes it, so you replace
the cartridge or fuser that's actually bad.

## Laser imaging process (A+ order)
Processing → charging → exposing → developing → transferring → fusing →
cleaning. Defects map to stages:
| Symptom | Likely component |
|---|---|
| Repeating marks at fixed interval | roller/drum — measure the gap; vendor charts map spacing (e.g. ~75 mm drum, ~56 mm fuser on many models) to the roller |
| Vertical white line | blocked/scratched drum, laser shutter dirt, low toner |
| Vertical black line | scratched drum or dirty charging roller |
| Smearing / toner rubs off | fuser not hot enough or wrong paper type setting |
| Ghost image (faint repeat) | fuser or drum cleaning failure; also wrong media |
| Blank page | no toner, sealing tape left on, transfer roller fault |
| All black page | charging roller failure |
| Faded overall | toner low, economode on, damp paper |
| Speckles | toner leak, dirty interior — clean with toner vac only |
Print the printer's **cleaning page** and **supplies status / configuration
page** first; most MFPs also have a print-quality diagnostic page.

## Inkjet
Banding/missing colours → nozzle check, then head clean (max 2–3 cycles; each
uses ink). Prints fine after sitting? Clogs from disuse — schedule a weekly
test print. Misaligned colours → alignment routine.

## Thermal (labels, receipts)
Fading = dirty printhead (isopropyl wipe) or wrong darkness/heat setting;
direct-thermal labels also fade with heat/sunlight (use thermal-transfer
ribbons for long-life labels). Vertical white lines = burned-out head
elements → replace head.

## Paper jams
- Open the doors the panel indicates; pull paper in the direction of travel;
  look for torn scraps (a fragment causes repeat jams).
- Repeat jams in one tray: worn pickup/separation rollers (consumables kit),
  wrong paper size guides, damp or curled paper, labels/envelopes in a tray
  not rated for them.
- Duplex-only jams → duplex unit rollers.

## Safety
Fuser runs ~200 °C — let it cool. Don't vacuum toner with a normal vacuum
(fire/ dust); use a toner vacuum. Power off before reaching in.

## When to stop
Fuser and transfer kits on managed print contracts are vendor jobs; log the
page count and error code from the panel and raise a vendor ticket.

## Verify
Configuration/test page is clean, the user's actual document prints from
the problem tray 10 pages without defect or jam.
