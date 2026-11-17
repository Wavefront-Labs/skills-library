---
id: computing-software.devops-ci-cd.release-engineering.pci-dss-change-control
name: pci-dss-change-control
category: computing-software
field: devops-ci-cd
product: release-engineering
tags: [release-engineering, pci-dss-change, pci-dss, change-control, cde, segregation-of-duties, audit-evidence]
level: practitioner
status: draft
description: "Meet PCI DSS v4 change control requirements in CI/CD: approvals, impact and rollback, separation of duties, CDE scope and testing evidence from the pipeline."
sources:
  - https://www.pcisecuritystandards.org/document_library/
  - https://docs-prv.pcisecuritystandards.org/PCI%20DSS/Standard/PCI-DSS-v4_0_1.pdf
  - https://docs.github.com/en/actions/managing-workflow-runs-and-deployments/managing-deployments/managing-environments-for-deployment
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# PCI DSS change control

PCI DSS v4.0.1 requirement 6.5 covers changes to system components in the cardholder data environment (CDE) and connected systems. Pipelines can produce the evidence automatically instead of spreadsheets.

## What 6.5.1 asks for every change
- Reason for and description of the change.
- Documentation of security impact.
- Documented change approval by authorised parties.
- Testing to verify the change doesn't adversely affect security.
- For bespoke and custom software, testing for compliance with 6.2.4 (secure coding) before production.
- Procedures to address failures and return to a secure state (rollback).
Plus: 6.5.2 confirm applicable PCI requirements are in place after significant changes; 6.5.3 pre-production separated from production; 6.5.4 roles and functions separated between production and pre-production (separation of duties); 6.5.5 live PANs not used in pre-production; 6.5.6 test data and accounts removed before go-live.

## Mapping to the pipeline
| Requirement | Pipeline evidence |
|---|---|
| reason/description | PR description template + linked ticket ID (enforced by a check) |
| security impact | PR template section; SAST/SCA/IaC scan results attached |
| approval | required reviewers (not the author) on PR; protected `production` environment with required reviewers from a change-approver team |
| testing | CI test reports, DAST on staging, retained as build artifacts |
| rollback | documented rollback job; previous artifact digest recorded in deployment record |
| separation of duties | developers can't approve their own PRs (`require_last_push_approval`), can't deploy to prod without approval, no direct prod access |
| confirm controls | post-deploy checks (config scan, CIS benchmark, WAF rules present) |

## Practical controls
- GitHub: environment `production` with required reviewers and "prevent self-review", deployment branch policy `main` only; rulesets on main.
- GitLab: protected environments with approval rules; merge request approval rules excluding author and committers.
- Keep deployment logs and approvals for at least 12 months (requirement 10.5.1 audit log retention), 3 months immediately available.
- Emergency changes: allowed with retrospective approval within a defined time; still recorded.
- Infrastructure changes (Terraform) go through the same path; console changes in CDE accounts alert (CloudTrail -> SIEM).

## Scope
Systems that store, process or transmit card data, plus connected-to and security-impacting systems (including the CI/CD platform deploying to the CDE: runners and credentials are in scope). Tokenisation or hosted payment pages reduce scope dramatically.

## Verify
- [ ] For a sampled production change, an assessor can see ticket, approval by someone other than the author, test results, deploy record and rollback plan from the pipeline alone.
- [ ] Nobody can deploy to production without an approval recorded in the platform.
