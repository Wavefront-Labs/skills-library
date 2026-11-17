---
id: computing-software.cybersecurity-defensive.threat-modelling.rapid-threat-modelling
name: rapid-threat-modelling
category: computing-software
field: cybersecurity-defensive
product: threat-modelling
tags: [threat-modelling-process, rapid-threat-model, lightweight-threat-modelling, design-review, user-story-threats, timeboxing]
level: practitioner
status: docs-checked
description: "Run a small threat model for a feature or change using the four Manifesto questions, a DFD of the change, STRIDE prompts and a recorded response per threat."
sources: ["https://raw.githubusercontent.com/OWASP/CheatSheetSeries/master/cheatsheets/Threat_Modeling_Cheat_Sheet.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rapid threat modelling

A focused session during design, scoped to a change, using the process in the OWASP Threat Modeling Cheat Sheet. The cheat sheet says threat modelling is ideally done early, such as in the design phase, and treated as a standard SDLC step.

## Session outline
1. **What are we working on?** Draw a data flow diagram of the change and its neighbours. It must show trust boundaries, data flows, data stores, processes and external entities.
2. **What can go wrong?** Walk each component, flow and boundary with the STRIDE prompts, brainstorming with the team and recording which element each threat affects:
   - Spoofing: violates authentication (stolen token used to impersonate a user).
   - Tampering: violates integrity (unintended database updates).
   - Repudiation: violates accounting (manipulated logs).
   - Information disclosure: violates confidentiality (data extracted from a database).
   - Denial of service: violates availability (lockout through repeated failed logins).
   - Elevation of privilege: violates authorisation (tampered JWT role).
   Rank threats by likelihood times impact if the team wants a ranking; the cheat sheet notes both are hard to estimate and ignore the cost of the fix.
3. **What are we going to do about it?** Give every threat one response: mitigate, eliminate, transfer or accept. Turn agreed mitigations into actionable security requirements and record why any residual risk is accepted.
4. **Did we do a good enough job?** Check the model reflects the system, all threats have a response, and mitigations are testable.

## Notes from the cheat sheet
- Technique choice: start with STRIDE for a technical design; use attack trees, misuse or abuse cases, LINDDUN, PASTA, OCTAVE or VAST when the scope needs a different view. Do not add techniques only to look comprehensive.
- Developers often lack security experience; inviting security staff to sessions and regular training help.
- Brainstorming can replace or supplement a DFD when less technical people take part.

## Checked
Method: 2026-11-09 read the OWASP Threat Modeling Cheat Sheet (raw markdown, OWASP/CheatSheetSeries). Kept only its content. Removed as unconfirmed: the 30 to 60 minute timeboxes and per-step minutes, the ticket and QA outputs, BOLA wording, the design-template checkbox, the quarterly sampling check, and the Manifesto and shostack.org sources (not read).
