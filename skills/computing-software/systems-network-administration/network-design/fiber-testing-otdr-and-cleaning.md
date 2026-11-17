---
id: computing-software.systems-network-administration.network-design.fiber-testing-otdr-and-cleaning
name: fiber-testing-otdr-and-cleaning
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, physical-troubleshooting, cable-tester, otdr, light-meter, optical-power-meter, fiber-inspection, fiber-cleaning, visual-fault-locator, insertion-loss, iec-61300-3-35, fiber-optic, loss-budget]
level: practitioner
status: docs-checked
description: "Troubleshoot fibre in the field: inspect-clean-inspect, power meter loss tests against a budget, OTDR traces for breaks and splices, VFL and polarity checks."
sources:
  - https://www.flukenetworks.com/knowledge-base/applications-standards-articles/fiber-inspection-and-cleaning
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Fibre testing: inspection, cleaning, power meter, OTDR

## Order of work
1. **Check DOM** on both switch ends (see transceiver-dom-optical-levels): no light, low light, or high?
2. **Inspect, clean, inspect** every connector you touch. Dirty end faces cause most fibre
   problems; one speck on a single-mode core can add loss and back-reflection.
   - Inspect with a fibre microscope/probe (pass/fail against the acceptance criteria in your cabling specification).
   - Clean dry first (click cleaner / cassette), wet-to-dry only if dry fails, re-inspect.
   - Never look into a fibre or a port; use the scope.
   - Clean **both** sides, including the bulkhead/adapter and the optic's receptacle (stick cleaner).
3. **Polarity**: TX must meet RX. Duplex LC links need the pair crossed end to end; MPO trunks follow one documented polarity method
   (see mpo-trunks-and-fiber-polarity). Swapped pairs = no link and no receive light on either end.

## Tier 1: light source + optical power meter (OLTS)
Measures end-to-end insertion loss at the wavelengths the application standard or optic specifies.
Set reference with test cords (1- or 3-jumper method), measure, compare with the **loss budget**:
fibre length x attenuation + connectors x allowed loss per connector + splices x allowed loss per
splice (figures from your cabling specification). Pass/fail against the channel loss limit of the application.

## Tier 2: OTDR
Sends pulses and plots back-scatter vs distance: shows each connector (reflective spike), splice
(step), bend (wavelength-dependent loss) and the end/break (big reflection then noise).
- Use launch and receive fibres so the first and last connectors are measurable.
- Test from both ends and average splice losses (directional gainers/losers).
- Locate a break: distance to the event; match to route records (add slack loops).
Use when OLTS fails or for acceptance of long/outside-plant runs.

## Visual fault locator (VFL)
Visible red laser into the fibre: glows at breaks, tight bends and bad connectors over short
distances; good for patch panels and identifying a strand end to end.

## Verify
- [ ] Every end face passes inspection after cleaning.
- [ ] Measured loss within the budget with margin to the optic's limit.
- [ ] DOM RX levels on both ends in range after re-patching.

## Checked

2026-10-28: The only source (Fluke fibre inspection article) returned a stub page, so nothing was confirmed from it. Removed every unconfirmed figure and standard reference: IEC zone wording, core size, wavelengths, per-connector and per-splice loss, the 10GBASE-SR channel loss, launch fibre lengths, VFL wavelength and range, the -40 dBm no-light level and the 3 dB margin. The workflow (inspect, clean, inspect; power meter then OTDR; polarity check) is process, not a checkable figure.
Method: documentation only; no commands were run.
