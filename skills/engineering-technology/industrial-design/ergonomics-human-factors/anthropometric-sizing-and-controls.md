---
id: engineering-technology.industrial-design.ergonomics-human-factors.anthropometric-sizing-and-controls
name: anthropometric-sizing-and-controls
category: engineering-technology
field: industrial-design
product: ergonomics-human-factors
tags: [industrial-design, ergonomics-human-factors, ergonomics, human-factors, anthropometrics, anthropometry, percentiles, 5th-percentile, 95th-percentile, grip-design, handle-diameter, power-grip, precision-grip, reach, controls, push-button, control-force, feedback, population-stereotypes, inclusive-design, universal-design, accessibility, usability, iso-9241, iec-62366, mil-std-1472, bodyspace, ansur, colour-blindness, color-blindness]
level: practitioner
status: draft
description: "Fitting handheld and tabletop products to people: percentile anthropometrics, grip diameters, reach, control size/force/feedback and inclusive design checks."
sources: ["Pheasant & Haslegrave, Bodyspace: Anthropometry, Ergonomics and the Design of Work", "Tilley / Henry Dreyfuss Associates, The Measure of Man and Woman", "US DoD MIL-STD-1472 Human Engineering", "Kroemer, Ergonomics: How to Design for Ease and Efficiency", "University of Cambridge, Inclusive Design Toolkit", "ISO 9241 series; IEC 62366-1"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Anthropometric sizing and controls — products that fit the hands that use them

**Goal:** size grips, reaches and controls for the real user population, make every
control's function, force and feedback obvious, and check nobody is needlessly excluded.

## 1. Define the population, then pick percentiles
- Decide who: adults of which regions, children, older users, gloved workers. Body
  dimensions differ markedly by sex, age and nationality, so use a dataset that matches
  (e.g. national surveys, ANSUR II for military populations, tables in *Bodyspace*).
- **Design for the range**, typically 5th-percentile female to 95th-percentile male:
  - **Clearance** (finger hole, handle gap): size for the **large** user (95th male) plus
    clothing or glove allowance.
  - **Reach** (button reach, span, stretch): size for the **small** user (5th female).
  - **Adjustable** where one size can't cover the range.
- Percentiles don't add: a "95th-percentile hand" isn't 95th in every dimension. Test
  with real people across the range.

## 2. Grip and handle sizing (typical values)

| Feature | Typical value |
|---|---|
| Power grip cylinder diameter | 30-50 mm, ~35-40 mm often best |
| Precision (pen) grip diameter | ~8-16 mm |
| Handle length, bare hand | >= 100-120 mm |
| Handle length, gloved | >= 125 mm |
| Two-handle tool span (pliers) | ~50-90 mm, ~65-80 mm comfortable |
| Thumb/finger clearance around a handle | >= ~25-30 mm, more for gloves |

Values are textbook ranges; check against the dataset for your population.
- **Bend the tool, not the wrist:** keep the wrist near neutral in the working posture.
- Round handle cross-sections are more forgiving than sharp polygons; avoid finger
  grooves sized for one hand, they fit the median and hurt everyone else.
- Keep sustained grip force low (a common guide is ~10-15% of the user's maximum) and
  keep one-handed product weight modest.

## 3. Controls: size, force, travel, feedback
Typical military-human-factors guidance for a fingertip push button (confirm in the
current MIL-STD-1472 or your sector standard):
- diameter >= ~10 mm (larger for gloves or thumbs, ~19 mm+ for thumb or palm use)
- force ~2.8-11 N; travel ~2-6 mm
- spacing between adjacent buttons ~13 mm+ edge to edge for single-finger use

Touch targets on screens: >= ~9 mm physical (platform guides: 44 pt iOS, 48 dp
Android); WCAG 2.2 sets 24 CSS px minimum.

**Feedback:** every actuation gives tactile (snap/detent), audible and/or visual
response; response within ~0.1 s feels immediate.

**Population stereotypes** (expected direction):
- clockwise / up / right / forward = increase or on
- **Light switches differ by country** (US up = on; UK and many others down = on).
- Valves: clockwise closes. Don't fight these for styling.

**Layout:** group by function, order by sequence of use, put the most frequent and
critical controls in the best reach zone, and guard controls whose accidental use is
harmful (recess, two-step, cover).

## 4. Inclusive design checks
- **Vision:** ~8% of men have red-green colour vision deficiency; never encode state by
  red/green alone. Labels with good contrast and adequate size.
- **Dexterity and strength:** older or arthritic users struggle with twist caps, small
  latches and high forces; give leverage, larger features, lower torque.
- **Hearing:** don't rely on beeps alone.
- **Cognition:** one obvious first action; consistent mapping.
- Use an exclusion estimate (e.g. the Cambridge Inclusive Design Toolkit approach) to
  see how many people each demand excludes.

## 5. Validate with people
Foam or printed 1:1 models early; observe tasks rather than ask opinions. For regulated
products (medical devices) follow a usability engineering process such as IEC 62366-1
with formative and summative evaluation.

## Gotchas
- Designing for the "average user" fits almost nobody in every dimension.
- Gloves, cold, wet or one hand occupied change every number above.
- Left-handed users (~10%) are excluded by asymmetric grips and one-sided triggers.
- Soft-touch coatings feel great on day one and get sticky; check durability with CMF.
- Data from older surveys underestimates current body sizes.

## Verify
- [ ] Target population and dataset named; clearance sized large, reach sized small.
- [ ] Grip diameters and lengths fall in the typical ranges, checked with 1:1 models.
- [ ] Each control has stated size, force, travel and feedback.
- [ ] Control directions follow population stereotypes for the target market.
- [ ] No function depends on colour alone, fine dexterity, or hearing alone.
