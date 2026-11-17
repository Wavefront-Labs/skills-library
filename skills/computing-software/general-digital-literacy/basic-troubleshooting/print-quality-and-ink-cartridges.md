---
id: computing-software.general-digital-literacy.basic-troubleshooting.print-quality-and-ink-cartridges
name: print-quality-and-ink-cartridges
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, ts-printers, print-quality, ink-cartridges, printhead-cleaning]
level: intro
status: draft
description: "Fix faded, streaky, banded or wrong-colour prints with nozzle checks, head cleaning and alignment, choose genuine or compatible ink, and stop cartridge rejected errors."
sources:
  - https://support.hp.com/us-en/document/ish_1805178-1478908-16
  - https://www.epson.co.uk/en_GB/faq
  - https://support.brother.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Ink cartridges and print quality

## Diagnose with a test page
- Printer menu or app (HP Smart, Epson Smart Panel, Canon PRINT) › Maintenance › **Print Quality Report / Nozzle Check**.
- Gaps in one colour block = clogged nozzles; all faint = low ink/toner or Draft mode; misaligned lines = alignment.

## Inkjet fixes
1. **Head cleaning** from the maintenance menu, then another nozzle check. Max 2-3 cleanings in a row (each uses ink); wait a few hours if still patchy and try again.
2. **Align printheads** after a new cartridge.
3. Check the print setting isn't *Draft/EconoMode*, the paper type matches (photo paper vs plain), and you print on the correct side.
4. Printers unused for weeks dry out; print a colour page weekly.

## Laser fixes
- Faded: shake the toner cartridge side to side. Streaks or repeating marks: drum unit dirty or worn (repeating every ~94 mm points at the drum). Smudges that rub off: fuser problem → service.

## Cartridges
- *Cartridge not recognised/incompatible*: remove and reseat; clean contacts with a dry lint-free cloth; remove protective tape. Firmware updates on some HP/Epson models block third-party chips: turn off auto firmware updates if you use compatibles, or HP **Dynamic Security** printers expect HP cartridges.
- Ink subscriptions (HP Instant Ink): cancelling disables subscription cartridges in the printer.
- Running costs: ink-tank printers (EcoTank, MegaTank) cost more upfront, far less per page.

## Verify
- [ ] Nozzle check prints every line in every colour; a normal page looks crisp.
