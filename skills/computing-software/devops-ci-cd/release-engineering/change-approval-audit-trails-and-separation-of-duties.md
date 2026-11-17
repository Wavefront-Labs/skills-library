---
id: computing-software.devops-ci-cd.release-engineering.change-approval-audit-trails-and-separation-of-duties
name: change-approval-audit-trails-and-separation-of-duties
category: computing-software
field: devops-ci-cd
product: release-engineering
tags: [release-engineering, change-approval, change-management, cab, change-advisory-board, lightweight-change-approval, peer-review-approval, itil-change, standard-change, normal-change, emergency-change, audit-trail, compliance-evidence, change-evidence, separation-of-duties, segregation-of-duties, sox, soc2, iso27001, pci-dss, four-eyes, branch-protection-evidence, deployment-records, servicenow-integration, jira-change, evidence-automation, auditor-questions, break-glass]
level: advanced
status: gated
description: "Replace the CAB with pipeline-enforced controls: peer review as approval, standard/normal/emergency changes, separation of duties via rulesets and deploy identities, evidence."
sources: ["https://dora.dev/capabilities/streamlining-change-approval/", "https://www.axelos.com/resource-hub/practice/itil-4-practice-guide-change-enablement", "https://cloud.google.com/architecture/devops/devops-process-streamlining-change-approval", "https://www.aicpa-cima.com/resources/landing/system-and-organization-controls-soc-suite-of-services"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Change approval, audit trails and separation of duties

**Goal:** every production change is reviewed, authorised, attributable and
reconstructable from records the pipeline produces automatically — and a CAB meeting is
no longer on the path to production.

## 1. What the research says (and what auditors actually need)
DORA recommends peer review during development, supplemented by automation, in place of heavyweight external approval (CAB), and peer review to meet segregation of duties. Auditors (SOX, SOC 2, ISO 27001, PCI DSS; confirm control wording with your auditor) typically need: changes are **authorised** before
deployment, **tested**, **documented**, **attributable** to an individual, and that no
single person can write *and* release code unchecked (separation of duties). None of
that requires a committee — it requires controls with evidence.

## 2. Change types (ITIL vocabulary, pipeline implementation) (gated: unconfirmed, source is paywalled or blocked)
| type | definition | approval |
|---|---|---|
| **Standard** (pre-approved) | low-risk, repeatable: app deploys through the full pipeline, config changes within policy, dependency bumps | none at deploy time; the *pipeline design* is approved once and reviewed yearly |
| **Normal** | higher risk or outside the pre-approved envelope: schema changes with downtime, infra topology, new third-party integration, security-relevant changes | peer review + designated approver (tech lead/owner) in the PR or environment gate; risk note in the PR template |
| **Emergency** | fix during an incident | break-glass path with *post-hoc* review within 24–48 h; everything logged |
Write down what qualifies as standard; most changes should. A change ticket per deploy
is replaced by the PR + deployment record.

## 3. Controls that implement the policy
- **Authorisation** = PR approval by someone other than the author, enforced by branch
  rulesets (required reviews, code-owner review, dismiss stale approvals, no admin bypass).
- **Testing** = required status checks (CI, security scans) on the protected branch;
  evidence is the check run.
- **Separation of duties** = the author cannot approve their own PR (platform-enforced);
  deploys run under a **pipeline identity** (OIDC/service account), not a human's creds;
  humans do not have write access to prod registries/clusters (read-only + break-glass);
  the environment gate for prod requires an approver from a defined group (with self-review prevented where the platform supports it). Developer who wrote it + reviewer who approved it + pipeline
  that deployed it = three distinct actors in the record.
- **Documentation** = PR description template (what/why/risk/rollback), release notes
  generated from merged PRs, deployment record with version + approver + time.
- **Emergency** = a `break-glass` team with temporary elevated rights (PIM/JIT access,
  alert on use), hotfix PRs allowed to merge with one approver and tests, mandatory
  retrospective review link within 48 h; audit log query proves it was used N times.
- **Infra and config** = same path: IaC in Git, plan output reviewed in the PR, apply
  by pipeline; manual console changes are detected (drift) and flagged.

## 4. Evidence you can hand over in minutes
Automate a monthly (or on-demand) evidence pack per system:
Use the platform APIs to export merged PRs with reviewers and check results, deployment records with approvers, and a ruleset or branch protection snapshot (see the GitHub REST and GraphQL docs and the organization audit log). Script it so the pack is repeatable.
GitLab and Jenkins expose equivalent approval, deployment and audit data (the Jenkins Audit Trail plugin records configured actions). Store the pack (JSON + a CSV summary) in an evidence bucket with
retention ≥ the audit cycle. Compliance-automation and change-management tools can collect this continuously; add a CMDB change record only if your organisation requires one, otherwise it is double bookkeeping.

## 5. Linking tickets without blocking
Require a ticket/issue reference in the PR title or branch name (lint in CI) for
traceability; do not require ticket *status* transitions as a deploy gate. If a
ServiceNow change record is mandated, create it *from* the pipeline at deploy time with
the PR link and auto-close on success — the pipeline is the source of truth.

## 6. Questions auditors ask and where the answer lives
| question | answer |
|---|---|
| How do you ensure changes are approved? | Ruleset export + sampled PRs with approvals (not author) |
| Can a developer deploy to prod alone? | No: prod deploy identity is the pipeline; env gate approvers list; IAM showing no human write |
| How are emergency changes handled? | Break-glass policy + audit-log evidence of each use + post-hoc review links |
| How do you know what is in production? | Deployment records with digest + provenance attestation (see SLSA skills) |
| Who can change the pipeline itself? | CODEOWNERS on `.github/workflows`/`Jenkinsfile`; push rulesets; shared workflow versioning |
| How are segregated duties maintained with a small team? | Reviewer ≠ author enforced; deploy by pipeline; monitoring by a third role; compensating control: all prod access logged and reviewed monthly |

## 7. Rolling it out
Pilot with one service: define standard change scope, turn on the rulesets/gates,
generate the first evidence pack, walk an internal auditor through it. Then retire the
CAB for that service's standard changes; keep a weekly 15-minute *change calendar* review
for coordination (not approval). Expand per service; measure lead time before/after.

## Verify
- [ ] Sampled 10 prod deploys: each traces to a PR with a non-author approval, green checks and a deployment record with digest.
- [ ] Attempting to self-approve or merge without checks fails (tested).
- [ ] Humans have no write to prod registry/cluster; break-glass use is logged and reviewed.
- [ ] Evidence pack for last month generated by a script, not by hand, in < 15 minutes.

## Checked

2026-10-28. Confirmed: DORA streamlining-change-approval page (peer review during development supplemented by automation instead of CAB approval; peer review to meet segregation of duties), GitHub secure-use page (required reviewers on environments, CODEOWNERS for workflow files), Jenkins Audit Trail plugin page. Gated: the ITIL standard/normal/emergency change types, because the AXELOS ITIL source is paywalled. Removed: control identifiers (SOX ITGC, SOC 2 CC8.1, ISO 27001 A.8.32, PCI DSS 6.5), the Humble & Farley non-URL source, the gh api evidence commands, GitLab API field names and named compliance vendors.

Method: documentation only; no commands were run.
