---
id: health-medicine.allied-health-technologies.mri-systems.mri-safety-screening-coil-setup-and-artifact-correction
name: mri-safety-screening-coil-setup-and-artifact-correction
category: health-medicine
field: allied-health-technologies
product: mri-systems
tags: [allied-health-technologies, mri-systems, mri, mri-technologist, mri-safety, zone-iv, mr-conditional, mr-unsafe, implant-screening, projectile, sar, rf-burns, quench, coil-selection, receive-coils, sequence-parameters, motion-artifact, aliasing, wrap-around, susceptibility-artifact, chemical-shift, metal-artifact-reduction, gadolinium]
level: practitioner
status: draft
description: "MRI technologist practice: zone-based safety screening, MR Conditional implant checks, burn prevention, coil choice, and fixing motion, aliasing, susceptibility and chemical-shift artifacts."
sources: [ACR Manual on MR Safety (2020 and later updates), MRI safety guidance from national regulators (e.g. MHRA), MRIsafety.com implant reference (Shellock), standard MRI physics texts on artifacts]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# MRI safety screening, coil setup and artifact correction

> General clinical/professional reference, not a substitute for your site's MR safety policy, the MR Safety Officer/Expert, or implant manufacturer conditions.

**Goal:** nobody and nothing ferromagnetic reaches the magnet unscreened, and every
sequence is diagnostic — the magnet is always on.

## 1. Safety screening (every patient, every time)
- Site zones (ACR model): I public → II screening → III restricted, controlled access →
  IV magnet room. Only screened people beyond Zone III.
- **Written questionnaire plus verbal review** by trained MR staff: pacemaker/ICD,
  neurostimulators, cochlear implants, aneurysm clips, programmable shunts, drug pumps,
  metallic foreign bodies (especially **orbital** — metalworkers get orbit X-ray per
  policy), recent surgery, tattoos/patches, pregnancy.
- For each implant: identify the exact model → look up its labelling: **MR Safe / MR
  Conditional / MR Unsafe**. Conditional means *only* under stated field strength,
  spatial gradient, SAR/B1+rms limits, and sometimes device mode (e.g. MR mode on a
  pacemaker). Not known → don't scan until resolved.
- Unconscious/unable to answer: escalate to the MR safety process; look for scars and use
  records/imaging.
- Change into site clothing; remove medication patches with metallic backing.
- Ferromagnetic detectors help but **do not replace screening**.

## 2. RF heating and burns
- Avoid skin-to-skin loops (hands clasped, thighs touching, arms against the bore): use
  padding.
- Cables straight, no loops, not touching the patient; remove unused coils.
- Stay within the SAR mode allowed (normal vs first level); conditional implants often
  require stricter limits.
- Give the patient the squeeze ball and **hearing protection** (earplugs + headphones
  for loud sequences).

## 3. Emergencies
- Cardiac arrest: start CPR and **remove the patient from Zone IV** to resuscitate;
  never bring the crash trolley in.
- Quench (deliberate loss of field) only for a person pinned by a ferromagnetic object
  or fire; it is costly and does not happen instantly. Know where the button is.

## 4. Coils and setup
- Choose the coil closest to the anatomy with the right coverage; centre the anatomy in
  the coil and the coil at isocentre. Activate the right elements.
- Comfort reduces motion: padding, warm blanket, clear time estimates.

## 5. Common artifacts and fixes
| Artifact | Looks like | Fixes |
|---|---|---|
| Motion / pulsation | Ghosting along phase direction | Coach breath-hold, respiratory/cardiac gating, swap phase direction, saturation bands, faster or radial sequences |
| Aliasing (wrap) | Anatomy outside FOV folded in | Enlarge FOV, phase oversampling, swap phase/frequency |
| Susceptibility | Signal void/distortion near metal or air | Use fast spin echo not gradient echo, higher bandwidth, metal artifact reduction sequences, lower field (1.5 T) |
| Chemical shift | Bright/dark band at fat–water edge | Increase bandwidth, fat suppression |
| Zipper/RF noise | Line across image | Close door properly; report to engineering |
| Fat-sat failure | Patchy suppression | Shim, use STIR or Dixon near metal |

## 6. Gadolinium points
Screen renal function per policy (group II agents carry very low NSF risk), previous
reactions, pregnancy; use macrocyclic agents per local formulary. Watch the cannula site.

## Gotchas
- "It was scanned before" is not clearance — field strength or device may differ.
- Oxygen cylinders, wheelchairs, cleaning carts and visitors' phones are the classic
  projectiles.
- Wrong coil element selection mimics pathology as signal drop-off.

## Verify
- [ ] Screening form complete, reviewed verbally and signed by MR staff.
- [ ] Each implant's MR status and conditions documented before entry.
- [ ] No loops, padding placed, hearing protection on, call bell tested.
- [ ] Images reviewed for artifacts before the patient leaves; repeats done.
