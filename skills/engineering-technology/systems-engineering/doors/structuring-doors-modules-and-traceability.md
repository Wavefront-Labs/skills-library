---
id: engineering-technology.systems-engineering.doors.structuring-doors-modules-and-traceability
name: structuring-doors-modules-and-traceability
category: engineering-technology
field: systems-engineering
product: doors
tags: [doors, ibm-doors, doors-classic, doors-9, doors-next, dng, ibm-elm, jazz, formal-module, link-module, linkset, attributes, views, baselines, baseline-set, suspect-links, dxl, traceability, trace-matrix, requirements-management, reqif, coverage-report, impact-analysis, rm-tool]
level: practitioner
status: draft
description: "Lay out DOORS Classic 9.7 / DOORS Next modules, link rules, attribute schemes, views and baselines so trace and coverage reports are trustworthy; DXL basics for orphan checks."
sources: ["IBM Engineering Requirements Management DOORS 9.7 documentation", "IBM DOORS DXL Reference Manual", "IBM Engineering Lifecycle Management (ELM) DOORS Next documentation", "OMG Requirements Interchange Format (ReqIF) 1.2"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Structuring DOORS modules and traceability — a database the trace report can trust

**Goal:** set up a DOORS project so every requirement has one home, links mean one thing each, and a coverage/orphan report can be produced at any baseline in minutes.

## 1. Know which DOORS you are in
- **DOORS Classic (9.7.x)** — client/server database; *formal modules* hold objects (headings + text in a tree), *link modules* hold the links between them, scripted with **DXL**.
- **DOORS Next (DNG)** — web tool inside **IBM Engineering Lifecycle Management (ELM)** on Jazz. *Artifacts* live in folders and are *reused* into modules; links are typed relationships, reporting goes through Report Builder / Lifecycle Query Engine, and configuration management (streams, baselines, change sets) is optional per project area. Concepts below map across; mechanics differ. Check your ELM version.

## 2. Module layout (one module per specification level)
Typical programme spine, top to bottom:
`Stakeholder Needs → System Requirements → Subsystem Requirements → Component/SW Requirements`, plus side modules for `Verification` (test cases / VCRM) and `Interfaces`.
- One module = one controlled document; never mix levels in one module.
- Module prefix per module (e.g. `SYS-`, `PWR-`) so the *Object Identifier* (prefix + Absolute Number) is unique programme-wide. Absolute numbers are never reused — never "renumber".
- Headings are objects with *Object Heading* set and empty *Object Text*; give them `Object Type = Heading` so filters exclude them from coverage counts.

## 3. Attribute scheme (define once, reuse via a template module)
Minimum per requirement object: `Object Type` (enum: Heading, Requirement, Information, Rationale), `Verification Method` (enum: Inspection, Analysis, Demonstration, Test — multi-value), `Verification Level`, `Status` (Draft, Proposed, Approved, Deleted), `Priority`, `Rationale` (text), `Owner`, `Allocated To`. Mark deleted requirements with `Status = Deleted` rather than physically deleting — deletion breaks history and baselined links.

## 4. Link discipline
- Convention: **link from the lower level (source) to the higher level (target)** — child *satisfies* parent; test *verifies* requirement. Then "incoming links" on a parent = its children.
- One link module per meaning: `Satisfies`, `Verifies`, `Refines`, `Allocated`. Never use the default `DOORS Links` module for programme traces.
- In DOORS Classic set **linkset pairings** (folder/project Properties → Linksets) and tick the option that restricts linking to the listed pairings ("mandatory"), so a user cannot create `SYS → STK` links in the wrong link module. In DNG, constrain link types via the project's type system and link constraints.
- **Suspect links** flag a link whose other end changed. Review them at every change board; clearing a suspect link is a decision ("child still satisfies changed parent"), not housekeeping.

## 5. Views
Save shared views per role: *Author* (ID, text, rationale, status), *Trace* (ID, text, layout-DXL parent-ID column built with **Analysis → Traceability Wizard**), *Verification* (ID, method, level, linked test). Set one as the module default.

## 6. Baselines
Classic: **File → Baseline → Create** (major/minor + suffix, e.g. `2.0 SRR`). Use **Baseline Sets** to baseline all modules of a release together, so links resolve consistently. DNG: baseline the component configuration (or the global configuration across ELM apps).

## 7. DXL for an orphan/coverage check (Classic)
```dxl
Module m = current
Object o; LinkRef lr; int n
for o in m do {
  if (o."Object Type" "" != "Requirement") continue
  n = 0
  for lr in o <- "*" do n++      // incoming link refs, modules need not be open
  if (n == 0) print identifier(o) " has no children\n"
}
```
`for Link l in o <- "*"` only sees incoming links from **open** source modules; use `LinkRef` (as above), or open sources with `read(fullName(source lr), false)` before dereferencing.

## 8. Export
Excel/CSV of the saved view for reviewers, Word/RTF for formal documents, **ReqIF** for supplier exchange (agree attribute mapping first; pilot a 10-object round trip).

## Gotchas
- Users need write access to the link module to create links, even from modules they own.
- Copying objects between modules creates new absolute numbers; links do not follow. Use move or re-link.
- Traceability built on headings ("child links to section 3") cannot be verified — link object to object.
- DNG module context vs base artifact: editing reused text changes it in every module that reuses it.

## Verify
- [ ] Every requirement module has a unique prefix and a template-derived attribute scheme.
- [ ] Linkset pairings (or DNG link constraints) block links outside the agreed spine.
- [ ] Orphan DXL/report returns zero unlinked non-root requirements, or each is justified.
- [ ] Every requirement has a verification method and a `Verifies` link, feeding engineering-technology.systems-engineering.verification-validation.verification-cross-reference-matrix.
- [ ] Suspect links are zero (cleared with a recorded decision) at each milestone baseline.
- [ ] A baseline set exists for each review milestone and re-running the trace view on it reproduces the review report.
