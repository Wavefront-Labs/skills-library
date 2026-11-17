---
id: computing-software.firmware-embedded-development.bare-metal-programming.misra-deviation-records
name: misra-deviation-records
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [misra-deviation, misra-compliance-2020, deviation-permit, guideline-recategorization-plan, guideline-enforcement-plan, misra-c, compliance-summary, safety-critical, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Manage MISRA C deviations per MISRA Compliance:2020: deviation records and permits, GRP and GEP, mandatory vs required vs advisory, and the compliance summary."
sources:
  - https://www.misra.org.uk/app/uploads/2021/06/MISRA-Compliance-2020.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MISRA deviation records and permits

**Goal:** a project can claim MISRA C compliance while still violating specific guidelines where justified,
through a clearly defined process supported by deviation records. MISRA Compliance:2020 says compliance can
be claimed for a project, not for an organisation.

## Categories decide what is negotiable
| Category | Rule (MISRA Compliance:2020 section 5) |
|---|---|
| Mandatory | Violation never permitted |
| Required | Can only be violated when supported by a deviation defining clear restrictions, requirements and precautions |
| Advisory | Followed as far as reasonably practical; violations are identified but need no deviation |
The guideline re-categorization plan (GRP) is agreed at the outset between acquirer and supplier. It may
raise some Required guidelines to Mandatory and some Advisory ones to Required or Mandatory, or mark an
Advisory guideline "Disapplied" (ignored altogether; the rationale must be documented). A Mandatory
guideline cannot be re-categorized, and a Required one cannot be made Advisory or Disapplied.

## Documents
1. **Guideline enforcement plan (GEP)**: lists every guideline and how compliance is checked (compiler,
   analysis tool and check, or manual review procedure). The supplier makes it available to the acquirer.
2. **Guideline re-categorization plan (GRP)**: described above. Adopted code that cannot be modified may need
   a separate, more permissive GRP.
3. **Deviation permits**: an approved use case, with the documentation and process requirements a deviation
   record must supply. Sources are public permits published by MISRA, acquirer permits and supplier permits.
   MISRA says publishing a permit does not make it acceptable in a particular project.
4. **Deviation records**: each deviation, optionally referring to a permit.
5. **Guideline compliance summary (GCS)**: produced at the end of the project with one entry per guideline
   claiming Compliant (no violations), Deviations (all violations covered by deviations), Violations (some
   uncovered) or Disapplied (not checked). Mandatory and Required guidelines can only claim Compliant or,
   for Required, Deviations.

## A deviation record contains
1. The guideline(s) violated.
2. A concise description of the circumstances in which the violation is acceptable.
3. The reason the deviation is required.
4. Background information explaining the context and language issues.
5. Requirements, including any risk assessment procedures and precautions to be observed.
You must be able to identify every place the deviation is applied: a register of file and line locations, a
description of the context (specific files or a macro expansion), or a unique identifier tagging locations
in the code. One deviation can cover many similar violations that share a use case.

## Justifying a deviation
Deviations must not be permitted for developer convenience, when a reasonable alternative coding strategy
would avoid the violation, without considering effects on other guidelines, without a suitable process, or
without the consent of a designated technical authority. Approval is on one or more of these reasons:
code quality (only if safety and security are maintained and better overall quality is achieved), access to
hardware (compiler-specific extensions for low-level access, encapsulated and isolated), adopted code
integration, and non-compliant adopted code.

## Adopted code
Vendor HAL, RTOS and generated code are "adopted code". MISRA Compliance:2020 asks whether it was developed
to an adequate level of safety and security and whether to MISRA guidelines, and notes claims of compliance
are compromised if adopted code was not developed to the same criteria. Use a separate GRP and record its
status rather than blanket-suppressing inside your own code.

## Verify
- [ ] Every analyser suppression maps to a deviation record or permit.
- [ ] A GCS is produced for each release and agrees with the GRP categories.

## Checked
Checked 2026-11-09 against MISRA Compliance:2020 (converted with pdftotext; read sections 3.3, 4, 5, 7.3 and
the adopted code discussion). Removed: the cppcheck suppression comment and `--suppressions-list` advice (the
cppcheck manual was not read), the MISRA C:2012 Rule 11.4 permit example, the ISO 26262 and IEC 61508
assessor claim, the advice about tracking deviation counts over time, and the Rule 17.7 gotcha, none of
which the document confirms.
Method: docs-checked 2026-11-09 against MISRA Compliance:2020.
