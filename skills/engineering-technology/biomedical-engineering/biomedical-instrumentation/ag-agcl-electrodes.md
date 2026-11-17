---
id: engineering-technology.biomedical-engineering.biomedical-instrumentation.ag-agcl-electrodes
name: ag-agcl-electrodes
category: engineering-technology
field: biomedical-engineering
product: biomedical-instrumentation
tags: [ag-agcl, silver-chloride-electrode, ecg-electrode, non-polarizable-electrode, electrode-gel]
level: practitioner
status: draft
description: "Specify Ag/AgCl biopotential electrodes: electrochemistry, chloride gel, offset and noise, defibrillation recovery, shelf life and the electrode standards used."
sources: ["Webster (ed.), Medical Instrumentation: Application and Design (biopotential electrodes chapter)", "ANSI/AAMI EC12 Disposable ECG electrodes (confirm current status and edition)", "https://www.aami.org"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Ag/AgCl electrode chemistry

**Goal:** choose and verify electrodes that give low offset, low noise and fast recovery after defibrillation and stimulation.

## Chemistry
- The reaction Ag + Cl- <-> AgCl + e- at a silver surface coated with silver chloride, in a gel containing chloride (KCl or NaCl), behaves as a **non-polarizable** electrode: current passes by a reversible reaction rather than charging a capacitor, so it gives low noise and low offset.
- The standard potential of the Ag/AgCl couple is about +0.22 V versus the standard hydrogen electrode, set by the chloride activity; two matched electrodes cancel it in a differential measurement.

## Specification points
- **DC offset between a pair:** small (the electrode standard sets a limit on the order of 100 mV; confirm in the standard) so amplifier input range is not used up.
- **Impedance** at low frequency (the standard sets a limit of the order of kilohms at 10 Hz; confirm).
- **Offset instability and noise** after application and over time.
- **Defibrillation overload recovery:** polarisation after a shock must decay quickly so the ECG returns to usable.
- **Gel and adhesive:** chloride content, wet versus solid gel, skin irritation; shelf life and sealed packaging because gel dries out.
- **Pairing:** do not mix electrode types or ages on one patient, since mismatch increases offset.
- Biocompatibility of skin contact (see biocompatibility-evaluation-iso-10993).

## Verify
- [ ] Offset, impedance, noise and defibrillation recovery tested per the standard as claimed.
- [ ] Shelf life and packaging validated.
- [ ] Skin irritation and sensitisation evaluated for the wear duration.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
