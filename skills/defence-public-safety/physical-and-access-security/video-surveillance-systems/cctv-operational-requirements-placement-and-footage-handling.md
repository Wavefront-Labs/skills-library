---
id: defence-public-safety.physical-and-access-security.video-surveillance-systems.cctv-operational-requirements-placement-and-footage-handling
name: cctv-operational-requirements-placement-and-footage-handling
category: defence-public-safety
field: physical-and-access-security
product: video-surveillance-systems
tags: [physical-and-access-security, video-surveillance-systems, cctv, vss, ip-camera, nvr, vms, operational-requirement, drri, detect-observe-recognise-identify, pixels-per-metre, ppm, en-62676, iec-62676, field-of-view, wdr, ir-illumination, retention-period, gdpr, data-protection, surveillance-camera-code, dpia, signage, evidential-export, chain-of-custody, footage-request, subject-access-request, control-room]
level: practitioner
status: draft
description: "Specifying CCTV from an operational requirement (detect, observe, recognise, identify), camera placement and pixel density, retention, privacy law, and evidential export with continuity."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CCTV operational requirements, placement and footage handling

**Goal:** install cameras that produce usable images for a stated purpose, run them
lawfully, and export footage that stands up as evidence. Reference for security
managers and installers (UK/EU terminology, with notes for elsewhere).

## 1. Start with an operational requirement (OR)
For each camera, write down **what** you need to see, **where**, **when**, and
**what for**:
- The task level, commonly expressed (IEC/EN 62676-4) as **Detect, Observe,
  Recognise, Identify (DORI)** or similar scales.
- Rough pixel-density targets by task (from EN 62676-4; confirm the current table):
  detect ~25 px/m, observe ~63 px/m, recognise ~125 px/m, identify ~250 px/m.
  Licence-plate reading and facial comparison may need more.
- The action that follows: alarm response, investigation, deterrence. A camera
  with no defined use is cost and privacy risk without benefit.

## 2. Placement
- Calculate field of view against the target pixel density at the distance you care
  about (manufacturer or design tools). Wide-angle "see everything" views usually fail
  to identify anyone.
- **Identification** cameras at choke points (entrances, tills), at head height-ish
  angles (shallow downward angle, not straight down), facing the direction people walk.
- Lighting: backlit doorways need WDR or added lighting; IR range is often overstated —
  test at night.
- Protect cameras from tampering and weather; check for obstructions as trees grow.
- Avoid capturing areas you have no right to monitor (neighbours' windows, private
  spaces). Privacy masking is available on most cameras.

## 3. Lawful operation
- **UK/EU:** CCTV that captures identifiable people is personal data processing under
  GDPR/UK GDPR: a lawful basis, a **DPIA** for large or intrusive systems, signage, a
  defined retention period, and a process for **subject access requests**. Public
  bodies in England & Wales also follow the Surveillance Camera Code of Practice
  (current status of the code and commissioner role has changed over time — check).
- **US and elsewhere:** rules differ by state/country, especially around **audio**
  recording, which may require consent; disable audio unless clearly lawful.
- Retention: set a period that matches the purpose (commonly ~30 days for many sites;
  justify yours), and delete automatically.

## 4. Monitoring
Control room operators lose attention quickly when watching multiple screens; use
analytics or alarm-triggered call-ups, rotate tasks, and keep a log of incidents and
actions.

## 5. Footage export for evidence
1. Note the incident time and confirm the **system clock** offset against a reliable
   time source (record the difference).
2. Export in the native format **plus** the manufacturer's player, and a commonly
   playable copy if possible. Hash files where your process supports it.
3. Record who exported what, when, from which camera, the time window and the offset;
   seal and hand over with a continuity (chain of custody) record.
4. Preserve the original before retention overwrites it — act quickly on police requests.

## Gotchas
- Daylight-saving changes and drifted clocks break timelines.
- Re-encoding footage can lose detail and metadata.
- Cloud VMS and remote access must be secured — default passwords and exposed web
  interfaces are common weaknesses.

## Verify
- [ ] Each camera has a written OR with task level and target px/m.
- [ ] Image tested by day and night at the target distance.
- [ ] DPIA/signage/retention in place where required; audio disabled unless lawful.
- [ ] Export procedure records clock offset, hashes and continuity.
