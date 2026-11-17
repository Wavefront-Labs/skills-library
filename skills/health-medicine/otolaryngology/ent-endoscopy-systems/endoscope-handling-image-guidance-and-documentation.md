---
id: health-medicine.otolaryngology.ent-endoscopy-systems.endoscope-handling-image-guidance-and-documentation
name: endoscope-handling-image-guidance-and-documentation
category: health-medicine
field: otolaryngology
product: ent-endoscopy-systems
tags: [otolaryngology, ent-endoscopy-systems, endoscopy, rigid-endoscope, hopkins-rod, flexible-nasendoscope, distal-chip-endoscope, nasendoscopy, 0-degree, 30-degree, 70-degree, white-balance, light-source, camera-head, anti-fog, stroboscopy-system, videostroboscopy, image-guided-surgery, surgical-navigation, electromagnetic-navigation, optical-navigation, registration, target-registration-error, fess, endoscope-reprocessing, high-level-disinfection, sheath, image-capture, documentation, dicom]
level: practitioner
status: draft
description: "Running ENT endoscopy kit: rigid vs flexible scopes and angles, white balance and fog, stroboscopy setup, image-guidance registration and accuracy checks, reprocessing and image documentation."
sources: [manufacturer instructions for use (rigid/flexible ENT endoscopes, navigation systems), ENT UK guidance on decontamination of nasendoscopes, AAO-HNS position statement on intraoperative use of computer-aided surgery]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Endoscope handling, image guidance and documentation

> General clinical/professional reference, not a substitute for independent clinical judgement, manufacturer instructions for use, local decontamination policy, or current guidelines. Specific settings vary by vendor (Karl Storz, Olympus, Medtronic, Stryker, Brainlab and others); always follow the IFU for your system.

**Goal:** get a clear, correctly oriented, recorded image every time, use navigation only
when it is proven accurate, and never let a reprocessing gap put the next patient at risk.

## 1. Choosing the scope
| Scope | Use | Notes |
|---|---|---|
| Rigid 0° (2.7/4 mm) | Nasal cavity, most FESS steps | Least disorienting; start here |
| Rigid 30°/45° | Maxillary, frontal recess, skull base | Rotate the light post to aim the view |
| Rigid 70°/90° | Laryngeal stroboscopy (transoral), frontal sinus | Image is from a steep angle, so orient with care |
| Flexible fibre-optic | Clinic nasendoscopy | Cheaper; honeycomb image, lower resolution |
| Flexible distal-chip | Clinic + stroboscopy, NBI where available | Best clinic image; costs more |

Rigid scopes are **Hopkins rod-lens** optics. Dropping or bending one cracks the rods
(the image goes hazy or shows a half-moon), so carry them by the eyepiece/body, never by the shaft tip.

## 2. Image setup checklist
1. Connect camera head, light cable and scope. Check the light cable for broken fibres
   (dark spots when you hold the end to a light).
2. **White balance** against white gauze at working distance, **after** connecting the
   scope you'll use. Redo it if you change the scope or light source.
3. Focus and set orientation: the camera's "up" must match patient anatomy. Mark the
   camera head button if needed.
4. **Anti-fog:** warm the scope (warm saline or warmer) or use anti-fog solution. Wipe
   the lens on mucosa when it smears.
5. Light intensity: no higher than you need. Xenon/LED tips get hot, so don't rest the
   tip on drapes or skin (burn/fire risk).

## 3. Stroboscopy system
- Microphone (contact or air) picks up the fundamental frequency, and the strobe fires
  slightly out of phase to show an apparent slow-motion wave.
- **Stroboscopy fails with aperiodic voices** (severe dysphonia): the image looks jerky
  and the strobe can't lock. Note this and consider high-speed videoendoscopy where
  available rather than over-reading the images.
- Record sustained /i/ at comfortable pitch and loudness, plus high/low pitch. Save audio with video.

## 4. Image-guided surgery (navigation)
- Uses: revision FESS, frontal/sphenoid sinus surgery, distorted anatomy, skull base,
  CSF-leak repair. It is an **adjunct**, not a replacement for anatomical knowledge.
- **Optical** (camera tracks reflective markers; needs line of sight) vs
  **electromagnetic** (field generator; no line of sight, but metal nearby distorts it).
- Use a CT/MRI with the protocol the system needs (fine slices, full coverage of the
  registration landmarks). Load it and check patient identity and laterality.
- **Registration:** surface tracing or fiducials. Then **check accuracy on known landmarks**
  (nasal tip, medial canthus, middle turbinate head, posterior choana). Vendors often
  quote ~2 mm accuracy, but real-world error varies. If a landmark is off, **re-register**.
  Recheck after any head movement or if the reference frame gets bumped.
- If navigation disagrees with clear endoscopic anatomy, stop and recheck. Don't follow the cursor into the skull base.

## 5. Reprocessing (flexible scopes especially)
- Leak test, clean manually straight after use (dried biofilm resists disinfection), then
  automated high-level disinfection or sterilisation per IFU, then store dry and hanging.
- Keep **traceability**: link scope serial number to patient and cycle record. Disposable
  sheaths cut contamination but don't replace the reprocessing the IFU requires
  (check your local policy).
- Rigid scopes used in theatre: sterilise per IFU (check which methods each scope tolerates).

## 6. Documentation
- Capture key stills (each side, lesion close-ups) and video for stroboscopy and before/after
  surgery. Label with patient ID, side and date, and store in the record/PACS (DICOM where
  supported), not on a local USB stick.
- Write the findings in words too. An image without a report is often never looked at again.

## Gotchas
- Wrong white balance makes mucosa look pale or red, which leads to misread inflammation or leukoplakia.
- Using a 30° scope with the light post in the wrong direction gives a "missing" frontal recess.
- Trusting navigation registered before the head was repositioned.
- Patient images left on unencrypted local storage (privacy breach).

## Verify
- [ ] Correct scope angle selected; white balance done with that scope.
- [ ] Orientation checked; anti-fog in place.
- [ ] Navigation accuracy confirmed on ≥2 landmarks before use and after movement.
- [ ] Scope reprocessing cycle traceable to the patient.
- [ ] Images saved to the record with labels and a written report.
