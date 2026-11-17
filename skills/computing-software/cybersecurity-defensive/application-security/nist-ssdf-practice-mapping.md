---
id: computing-software.cybersecurity-defensive.application-security.nist-ssdf-practice-mapping
name: nist-ssdf-practice-mapping
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [secure-sdlc, nist-ssdf, sp-800-218, secure-software-development, practice-mapping]
level: advanced
status: docs-checked
description: "Map an engineering organisation's SDLC to NIST SP 800-218 SSDF v1.1 practices (PO, PS, PW, RV), recording owner and evidence per task so gaps are visible and dated."
sources: ["https://csrc.nist.gov/pubs/sp/800/218/final", "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NIST SSDF practice mapping

**Goal:** a living matrix that shows, for every SSDF task, what you do, who owns it and where the
evidence lives.

## The four groups (SP 800-218 v1.1)
| Group | Practices |
|---|---|
| PO Prepare the Organization | PO.1 security requirements, PO.2 roles and responsibilities, PO.3 supporting toolchains, PO.4 criteria for security checks, PO.5 secure development environments |
| PS Protect Software | PS.1 protect code from unauthorized access and tampering, PS.2 mechanism for verifying release integrity, PS.3 archive and protect each release |
| PW Produce Well-Secured Software | PW.1 design to meet security requirements, PW.2 design review, PW.4 reuse well-secured software, PW.5 secure coding, PW.6 compiler and build settings, PW.7 code review/analysis, PW.8 executable code testing, PW.9 secure default settings |
| RV Respond to Vulnerabilities | RV.1 identify and confirm vulnerabilities, RV.2 assess, prioritize and remediate, RV.3 analyze root causes |

PW.3 is marked "Moved to PO.1.3" and PW.3.2 moved to PW.4.4 in v1.1, so do not create rows for retired tasks.

## Procedure
1. Export the task list (PO.1.1 ... RV.3.4) into a sheet: columns `task id | implementation | owner | tool | evidence link | gap | target date`.
2. Walk each product team through it; write what actually happens, not policy aspirations.
   Evidence = pipeline config, branch protection export, signed release, vulnerability-disclosure policy (RV.1.3), threat model doc.
3. Mark tasks as Implemented / Partial / Not implemented / Not applicable (justify N/A).
4. Repeat quarterly; store the matrix in version control so history is auditable.

## Gotchas
- Third-party and open-source components: see PW.4.4 (verify acquired components) and PS.3.2 (provenance data).
- If you must attest to customers or regulators, take the current form and its scope from the issuing agency, not from this matrix.

## Verify
- [ ] Every task has an owner and either evidence or a dated gap.
- [ ] Release rows link to PS.2/PS.3 evidence.

## Checked
2026-11-01. Confirmed against the NIST SP 800-218 v1.1 PDF (Table 1): group names, practice titles PO.1-PO.5, PS.1-PS.3, PW.1-PW.9, RV.1-RV.3, task ids PO.1.1 through RV.3.4, and the retired PW.3 tasks; csrc page for the title and v1.1 (February 2022). Removed: CISA attestation details (signer level, POA&M, asserted items), SP 800-218A AI content, SBOM and outcome-based claims, no page read stating them.
Method: documentation only; no commands were run.
