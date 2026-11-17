---
id: computing-software.qa-testing-engineering.test-case-design.non-functional-and-defect-based-test-design
name: non-functional-and-defect-based-test-design
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [non-functional-testing, security-testing, localization-testing, i18n, l10n, defect-based-testing, defect-taxonomy, error-guessing, fault-seeding, owasp-top-ten, checklist-based-testing, iso-25010, quality-characteristics, input-validation]
level: advanced
status: draft
description: "Design test cases for non-functional quality characteristics (security, localization, usability-adjacent NFRs) and defect-based techniques that target known bug categories directly."
sources: ["https://www.iso.org/standard/35733.html", "https://owasp.org/www-project-top-ten/", "Boris Beizer, Software Testing Techniques (Van Nostrand Reinhold, 1990)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Non-functional and defect-based test design

**Goal:** two techniques that sit outside the usual functional
partition/boundary/decision-table toolkit: deriving cases from a non-functional
quality model (security, i18n) instead of a spec, and deriving cases from *known
defect categories* instead of requirements at all.

## 1. Non-functional testing from a quality model, not a guess
ISO/IEC 25010 names the characteristics beyond "does it compute the right output":
security, usability, reliability, maintainability, portability, compatibility,
performance efficiency. Performance has its own field here
(`performance-testing`); for the others, derive cases per characteristic
deliberately rather than testing only whichever one someone happened to think of:
- **Security**: walk the OWASP Top Ten against every input and auth boundary —
  injection (SQL/command/template), broken access control (can user A fetch user
  B's resource by changing an ID in the URL?), auth/session flaws, security
  misconfiguration (verbose errors leaking stack traces, default credentials
  left on). This is functional-boundary testing aimed specifically at *abuse*
  inputs rather than valid-but-extreme ones.
- **Localization (l10n)**: text expansion (German/Finnish strings run 30-50%
  longer — check for truncation/overlap, not just translation accuracy), RTL
  layout mirroring (Arabic/Hebrew), date/number/currency formatting per locale,
  sort order (collation differs by locale even for the same alphabet), and the
  classic bug class — hardcoded assumptions about name order, address format, or
  pluralization rules baked in from the source language.
- **Compatibility**: not just browser/OS matrices — check interop with the
  specific external systems/versions the integration spec names, not an assumed
  "latest."

## 2. Defect-based testing: start from known bug categories, not the spec
Where the other techniques start "what does the spec say should happen," defect-
based testing starts "what categories of bug does this *kind* of code tend to
have," drawn from a **defect taxonomy** built from the team's own bug history or
a general one (Beizer's categories: boundary, data, logic, interface, checking/
error-handling). For each category relevant to the code under test, write a case
that specifically targets it:
- **Boundary**: off-by-one at loop/array edges — covered more thoroughly by
  `test-case-design.partitioning-boundaries-and-risk-based-coverage`, but defect-
  based testing adds the ones unique to the team's own history (e.g., "we've shipped
  three off-by-one bugs in pagination specifically — test pagination edges every time").
- **Error handling**: does every caught exception path actually get exercised, or
  only the happy path plus one generic failure? Each distinct error branch is its
  own case, not one "error case" covering all of them.
- **Interface/integration**: mismatched assumptions between two components about
  units, encoding, null-handling, or ordering — these are rarely visible from
  either component's spec alone, only from the pairing.

## 3. Error guessing, formalized
"Error guessing" sounds unsystematic but becomes a real technique once it's fed
by a defect taxonomy and a project's own bug database: query the bug tracker for
the most recurring root-cause categories in the last N releases, and write new
test cases that target those categories in the current feature, even where the
current spec gives no hint they're relevant. This converts "the testers' gut
feeling" into a rule: whatever broke before, in a category, test for again.

## 4. Fault seeding as a design-time (not CI-time) sanity check
Deliberately inject a plausible bug (off-by-one, wrong operator, swapped
parameter) into a copy of the code and confirm the planned test cases catch it,
before the real tests are finalized. This is a manual, small-scale precursor to
automated mutation testing (`jest-pytest.property-based-and-mutation-testing`) —
useful specifically at design time, when deciding whether a planned case set is
adequate before writing all the test code.

## Unconfirmed / notes
OWASP Top Ten and i18n checklists are necessarily generic; always confirm against
the actual tech stack's known CVE history and the actual target locale list before
treating either as exhaustive.

## Verify
- [ ] At least one case per relevant ISO 25010 characteristic beyond pure function, for release-critical features.
- [ ] OWASP Top Ten walked against every externally reachable input/auth boundary.
- [ ] Locale cases include text expansion and RTL layout, not only translated strings.
- [ ] Current feature tested against the team's own top recurring defect categories, not just a generic taxonomy.
- [ ] A seeded fault was caught by the planned case set before calling the design complete.
