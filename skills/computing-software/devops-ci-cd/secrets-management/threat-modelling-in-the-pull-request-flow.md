---
id: computing-software.devops-ci-cd.secrets-management.threat-modelling-in-the-pull-request-flow
name: threat-modelling-in-the-pull-request-flow
category: computing-software
field: devops-ci-cd
product: secrets-management
tags: [secrets-management, threat-modeling, stride, security-review, pr-template, codeowners, shift-left]
level: practitioner
status: docs-checked
description: "Fold lightweight threat modelling into pull requests: triggers for a review, STRIDE questions in the PR template, CODEOWNERS routing to security, and recording decisions as code."
sources:
  - https://owasp.org/www-community/Threat_Modeling_Process
  - https://www.threatmodelingmanifesto.org/
  - https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
  - https://github.com/OWASP/threat-dragon
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Threat modelling in the PR flow

Big up-front threat models go stale. The practical shift-left version: ask the four questions when a change alters the system's attack surface, in the PR where the change lives.

## The four questions
1. What are we working on? (diagram or a sentence: new endpoint, new data flow, new dependency)
2. What can go wrong? (STRIDE: Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege)
3. What are we going to do about it?
4. Did we do a good enough job?

## Trigger, don't tax every PR
Require the section only when the diff touches risk surfaces. Encode the triggers:
Typical trigger paths: auth code, API routes, IAM infrastructure files, Dockerfiles, API specs, crypto code. Apply a label from path rules (for example with a labeler action) and route the same paths through CODEOWNERS.
```
# CODEOWNERS - security reviewers required for the same paths
/src/auth/        @org/appsec
/infra/**/iam*.tf @org/appsec @org/platform
```
With branch protection "Require review from Code Owners", these PRs can't merge without AppSec.

## PR template section
```markdown
## Security impact (required when labelled needs-threat-model)
- New/changed entry points or trust boundaries:
- Data touched (classification):
- STRIDE: which apply and the mitigation for each
  - Spoofing:
  - Tampering:
  - Info disclosure:
  - Elevation:
- Residual risk accepted by (name) and ticket:
```
A CI check can fail when the label is present and the section is empty.

## Keep the model as code
- Store diagrams as code next to the service (`docs/threat-model/service.md` with Mermaid data-flow diagram, or OWASP Threat Dragon models).
- Update it in the same PR that changes the flow; review diffs like code.
- Link findings to issues with a `security` label; track mitigations as acceptance criteria.

## Facilitating quickly
- Draw the data flow with trust boundaries, walk each arrow crossing a boundary through STRIDE.
- Prefer concrete abuse cases ("an authenticated user changes another tenant's id in the URL") over category names.
- Output: 3-5 actionable mitigations, owners, and what's explicitly out of scope.

## Verify
- [ ] Risky-path PRs auto-labelled and blocked on AppSec review; template section filled.
- [ ] Threat model file changed in the same PR as the architectural change.

## Checked

2026-10-28. Confirmed: STRIDE as a threat categorisation mnemonic (OWASP Threat Modeling Process page); CODEOWNERS and the branch protection option Require review from Code Owners (GitHub About code owners page); OWASP Threat Dragon repository. Removed: attribution of the four questions to the Threat Modeling Manifesto (the manifesto page does not list them), the actions/labeler configuration, the gh pr view --json command, pytm and the 30-minute figure.

Method: documentation only; no commands were run.
