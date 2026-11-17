---
id: computing-software.cybersecurity-defensive.threat-modelling.web-app-threat-modelling
name: web-app-threat-modelling
category: computing-software
field: cybersecurity-defensive
product: threat-modelling
tags: [web-app-threat-modelling, web-application-security, stride, dfd, threat-modelling]
level: practitioner
status: docs-checked
description: "Threat model an application with the OWASP cheat sheet: four questions, DFD with trust boundaries, STRIDE prompts, ranking, responses, review."
sources: ["https://raw.githubusercontent.com/OWASP/CheatSheetSeries/master/cheatsheets/Threat_Modeling_Cheat_Sheet.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Application threat modelling (OWASP cheat sheet)

Threat modelling is a structured, repeatable process: model the system from a security
perspective, identify applicable threats, and decide responses. Do it early, such as during
design, and maintain the model alongside the system. The four questions (Threat Modeling
Manifesto) drive four steps: what are we working on, what can go wrong, what are we going to
do about it, did we do a good enough job.

## 1. System modelling
- Data flow diagrams are arguably the most common technique. Show trust boundaries, data flows,
  data stores, processes and external entities; these often represent possible attack points.
  Keep them in a form the team can update; for complex systems use a high-level overview plus
  detailed component diagrams.
- Brainstorming is an alternative or complement, useful when less technical people take part
  and for agreeing terminology.
- Cloud-native systems need adaptation: shared responsibility, managed services and APIs,
  multi-tenant and identity federation, dynamic infrastructure (IaC, serverless, containers),
  virtual networks, IAM roles, storage buckets and data residency.

## 2. Threat identification (STRIDE)
| Category | Violates | Example from the cheat sheet |
|---|---|---|
| Spoofing | Authentication | Steals a legitimate user's authentication token to impersonate them |
| Tampering | Integrity | Abuses the application to make unintended database updates |
| Repudiation | Accounting | Manipulates logs to cover actions |
| Information disclosure | Confidentiality | Extracts user account data from a database |
| Denial of service | Availability | Locks a user out by many failed authentication attempts |
| Elevation of privilege | Authorization | Tampers with a JWT to change their role |

Use the six categories as prompts on each component, data flow and trust boundary. Ranking is
in theory likelihood times impact, which can be hard to calculate and ignores fix effort.

Technique choice (cheat sheet table): STRIDE for a technical design; attack trees for a
high-value attacker goal; misuse or abuse cases for abuse of a valid workflow (out of order,
repeated, concurrent); LINDDUN for privacy; PASTA for application threats with business
impact; OCTAVE for organisation-wide risk to critical assets; VAST for application and
operational threats across many teams. State why each technique fits and do not add techniques
only to look comprehensive.

## 3. Responses
Per Adam Shostack: mitigate, eliminate (remove the feature), transfer (contractual or
financial; it does not itself reduce likelihood or harm, so document who owns the remaining
controls and residual risk) and accept. Turn agreed mitigations into security requirements and
record why any remaining risk is accepted (NIST SP 800-218 practice PW.1.2).

## 4. Review and validation
Review with all stakeholders, not only dev and security. Ask: does the DFD match the system,
were all threats identified, does each have an agreed response, do mitigations reduce risk to
an acceptable level, is the model documented and stored for those who need it, and can the
mitigations be tested and measured.

## Verify
- [ ] Every trust boundary and data flow was walked with the six STRIDE prompts.
- [ ] Every threat has a response and an owner.

## Checked
Confirmed 2026-11-09 against the OWASP Threat Modeling Cheat Sheet (raw markdown, read in full).
Removed as unconfirmed: the web-specific element checklist (CDN, cookie flags, CSRF, CORS, CSP, SRI, SSRF, admin controls), mapping to OWASP Top 10 2021 and ASVS levels, the business logic abuse-case walk, the SPA and non-HTTP gotchas, and the ASVS and Top 10 sources, which are unreadable hosts.
Method: docs-checked 2026-11-09 against the OWASP Threat Modeling Cheat Sheet on raw.githubusercontent.com
