---
id: creative-arts.film-live-action.color-grading.qc-automated-tools-reports-and-dcp-screening
name: qc-automated-tools-reports-and-dcp-screening
category: creative-arts
field: film-live-action
product: color-grading
tags: [color-grading, film-live-action, automated-qc, baton, vidchecker, qc-report, qc-failures, qc-fix, dcp-qc, screening-check, theatrical-qc, harding-test, photosensitivity, flash-testing]
level: practitioner
status: draft
description: "QC a master: automated QC tools (Baton, Vidchecker), reading QC reports and fixing failures, photosensitivity/Harding testing, and the theatrical DCP screening check."
sources:
  - "https://www.interrasystems.com/baton.php (Interra Systems BATON - automated QC)"
  - "https://www.telestream.net/vidchecker/ (Telestream Vidchecker - automated QC and correction)"
  - "https://www.hardingfpa.com (Harding FPA - photosensitive epilepsy analysis)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# QC: automated tools, reports and the DCP screening

**Goal:** catch every technical and visible fault before the distributor does - and fix
it properly.

## 1. Automated QC
- **BATON**, **Vidchecker**, **Aurora**, **Venera Pulsar**: file-based checks against a
  template matching the delivery spec - container/ codec conformance, metadata, levels
  (gamut, luma), black frames, freeze frames, field order, audio levels/ loudness/ silence/
  phase, timecode continuity, dropouts, digital hits.
- Run on the final master files (not intermediates); build **templates per spec**
  (Netflix, DPP, broadcaster).
- Automated QC catches technical issues; it does **not** replace a human eyes-and-ears pass.

## 2. Human QC pass
A trained QC operator watches/listens to the whole programme on a reference monitor and
speakers, logging: picture artefacts (dead pixels, compression blocking, banding, dust,
boom/crew in shot, VFX errors), sync drift, audio clicks/dropouts, subtitle errors,
continuity of titles. Rate each issue (e.g. 1-5 severity) with TC.

## 3. QC report and fixes
- Report columns: TC in/out, issue, severity, channel/ layer, action (fix/ waiver).
- Fix at the **source** (grade, VFX, mix), re-render the affected section or whole master,
  re-QC the fixed sections (and spot-check around them).
- Request **waivers** for creative intent (e.g. intentional noise, black frames for effect)
  - document with the distributor.

## 4. Photosensitivity (Harding)
UK broadcast (Ofcom) and many distributors require a **Harding FPA** (or equivalent)
test for flashing and patterns that could trigger photosensitive epilepsy. Run on the
final picture; fix failing sections (reduce flash luminance/ frequency, fewer red flashes)
or add warnings per policy. Keep the certificate.

## 5. Theatrical DCP screening check
Before release/festival:
- Play the DCP in a cinema (or a calibrated DCI projector room): check picture start/
  end, reels, colour (vs grading reference), aspect ratio/ masking, subtitles placement and
  timing, audio channel routing (5.1/7.1 - each channel in the right speaker), level at
  reference (Dolby 7.0 fader), sync.
- Test the KDM window if encrypted; check content title naming.

## Gotchas
- Automated QC only; visible errors (a boom mic) pass.
- Fixing in the QC'd file instead of the source - next re-render reintroduces the fault.
- Harding test on a pre-final version.
- DCP never played in a real cinema before the premiere.

## Verify
- [ ] Automated QC with spec template on final files.
- [ ] Human QC full pass logged with severities.
- [ ] Fixes at source, re-QC done, waivers documented.
- [ ] Harding certificate; DCP screened in a cinema.
