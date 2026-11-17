---
id: computing-software.cybersecurity-defensive.threat-modelling.threat-model-validation
name: threat-model-validation
category: computing-software
field: cybersecurity-defensive
product: threat-modelling
tags: [threat-modelling-process, threat-model-validation, security-testing, abuse-case-tests, mitigation-verification, pentest-scoping, threat-model-review]
level: practitioner
status: docs-checked
description: "Validate a threat model with the OWASP cheat sheet review questions: accurate model, every threat answered, testable mitigations, documented and kept current."
sources: ["https://raw.githubusercontent.com/OWASP/CheatSheetSeries/master/cheatsheets/Threat_Modeling_Cheat_Sheet.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Validating a threat model

**Goal:** answer the fourth Threat Modeling Manifesto question, "did we do a good enough job?", before relying on the model.

## Review questions (OWASP Threat Modeling Cheat Sheet)
The model must be reviewed by all stakeholders, not just the development or security teams. Ask:
- Does the DFD (or comparable model) accurately reflect the system?
- Have all threats been identified?
- For each identified threat, has a response been agreed (mitigate, eliminate, transfer or accept)?
- Where mitigation is the response, do the mitigations reduce risk to an acceptable level?
- Is the model formally documented, with artefacts stored so that those with a need to know can access them?
- Can the agreed mitigations be tested, and can their success or failure be measured?

## Transfer needs an owner
Risk transfer does not itself reduce likelihood or harm. Record who owns the remaining controls and the residual risk.

## Keep it current
A threat model is maintained, updated and refined alongside the system, and is not performed once and forgotten. Keep mitigation decisions current as the system changes. The cheat sheet cites NIST SP 800-218 practice PW.1.2 for this.

## Output
A review record: the six questions above with answers and evidence, reviewers named, gaps raised as follow-up tasks.

## Checked
Method: 2026-11-09 read the OWASP Threat Modeling Cheat Sheet (raw markdown, OWASP/CheatSheetSeries) and kept what its Review and Validation, response and maintenance text states. Removed as unconfirmed: the DFD-versus-infrastructure-code comparison, the specific threat-to-test table, pentest scoping and feedback loop, annual review and dashboard suggestions, and the SAMM and Manifesto sources (not read).
