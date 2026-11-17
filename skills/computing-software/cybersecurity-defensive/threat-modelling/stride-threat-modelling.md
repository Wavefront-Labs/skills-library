---
id: computing-software.cybersecurity-defensive.threat-modelling.stride-threat-modelling
name: stride-threat-modelling
category: computing-software
field: cybersecurity-defensive
product: threat-modelling
tags: [threat-modelling, threat-modeling, stride, data-flow-diagram, dfd, trust-boundaries, spoofing, tampering, repudiation, information-disclosure, denial-of-service, elevation-of-privilege, microsoft-threat-modeling-tool, owasp-threat-dragon, pytm, threat-modeling-manifesto, attack-trees, linddun, pasta, secure-design, security-requirements, stride-per-element, threat-mitigation-mapping]
level: practitioner
status: docs-checked
description: "Run a STRIDE threat model on a system: draw a DFD with trust boundaries, enumerate threats per element, rank them, pick mitigations and land them as tickets."
sources: ["https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html", "https://www.threatmodelingmanifesto.org/", "https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# STRIDE threat modelling — find design flaws before they're code

**Goal:** with the people who build the system, answer the four questions of the Threat
Modeling Manifesto and OWASP cheat sheet — *what are we working on, what can go wrong,
what are we going to do about it, did we do a good enough job* — and leave with tracked
work items, not a PDF.

## 1. Scope and people
One feature or service per session. Invite an engineer who knows the code, the
product owner, someone from ops, and a facilitator (OWASP: security staff in the room
help developers). Bring architecture docs, the API spec and the deployment diagram.
Timebox; a model that takes weeks is never updated.

## 2. Draw the data flow diagram
Show external entities, processes, data stores, data flows and trust boundaries
(OWASP: these are the likely attack points). Label each flow with protocol and data
(e.g. "HTTPS, JWT + order JSON"). Draw a trust boundary wherever privilege, owner or
trust level changes: internet to DMZ, tenant A to tenant B, your cloud account to a vendor.
Use a high-level overview plus detail diagrams for complex components, kept in a form
the team can update. Tools: whiteboard or the Microsoft Threat Modeling Tool.

## 3. Enumerate threats with STRIDE
Each category violates a desirable property (OWASP cheat sheet):
| Threat | Violates |
|---|---|
| **S**poofing | Authentication |
| **T**ampering | Integrity |
| **R**epudiation | Accounting (non-repudiation) |
| **I**nformation disclosure | Confidentiality |
| **D**enial of service | Availability |
| **E**levation of privilege | Authorization |
Use the six categories as prompts on each component, data flow and especially every flow
**crossing a trust boundary**, and record which elements each threat affects. Prompt
questions: Can a caller claim to be another tenant (S)? Can a message on the queue be
altered or replayed (T)? Could a user deny placing an order — do we log who did what
(R)? Do error messages or logs leak tokens/PII (I)? What happens under a flood of
requests or an oversized upload (D)? Can a normal user call an admin endpoint or modify
their role claim (E)? Write each as "attacker does X to Y, resulting in Z".

## 4. Rank
Rank by likelihood x impact (OWASP notes both are hard to estimate and ignore the cost of
the fix), using one simple, consistent scale or your risk matrix. Note existing controls
before scoring. Mark boundary-crossing threats with no existing control as top candidates.

## 5. Decide and ticket
For each threat: **mitigate**, **eliminate** (remove the feature/data), **transfer**
(e.g. to a managed service with contractual terms), or **accept** (named owner, recorded).
Typical mitigations: S → strong authn, mTLS, signed tokens with audience checks;
T → integrity checks, signing, parameterised queries, immutable storage; R → append-only
audit logs with actor IDs and time sync; I → encryption, field-level minimisation,
log scrubbing; D → rate limits, quotas, size limits, autoscaling caps; E → server-side
authz on every request, least-privilege roles.
Create a ticket per mitigation with: threat ID, DFD element, acceptance criteria that
are testable (e.g. "request with another tenant's ID returns 404"), and a security
label so you can query open threat-model work.

## Gotchas
- Missing the boring flows: admin consoles, CI/CD deploy path, backups, support
  tooling, log pipelines — these often cross the most sensitive boundaries.
- Treating the DFD as the deliverable; the tickets are the deliverable.
- Threats phrased as "SQL injection" with no target can't be tested; name the element.
- Models rot. Re-run on significant design changes (new boundary, new data type, new
  third party) — add a checkbox to the design-review template.
- STRIDE misses privacy harms; use LINDDUN alongside it for personal data.

## Verify
- [ ] The DFD reflects the system and every trust boundary is drawn and labelled.
- [ ] Each boundary-crossing flow has STRIDE threats considered and recorded.
- [ ] Threats are ranked with a stated, consistent method.
- [ ] Every non-accepted threat has a ticket with testable acceptance criteria.
- [ ] Accepted risks have a named owner.
- [ ] The model is stored next to the code and has a re-review trigger.

## Checked
2026-11-01. Confirmed in the OWASP Threat Modeling Cheat Sheet: four questions, DFD elements and trust
boundaries, STRIDE properties, likelihood x impact ranking, mitigate/eliminate/transfer/accept responses,
review questions incl. testable mitigations, LINDDUN for privacy; Microsoft Learn Threat Modeling Tool
STRIDE page and Manifesto for the questions. Removed: session length, DFD shapes, per-element
applicability table, Threat Dragon/pytm/Threagile tool claims, DREAD claim, numeric scale, book citation.
Method: documentation only; no commands were run.

Related: computing-software.cybersecurity-defensive.application-security.secure-code-review
