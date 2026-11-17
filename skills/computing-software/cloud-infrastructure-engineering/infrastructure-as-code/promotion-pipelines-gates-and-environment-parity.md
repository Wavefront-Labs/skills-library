---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.promotion-pipelines-gates-and-environment-parity
name: promotion-pipelines-gates-and-environment-parity
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, environment-promotion, promotion-pipeline, promotion-gates, environment-diff, parity-check, manual-approval]
level: advanced
status: docs-checked
description: "Promote the same infrastructure change through dev, stage and prod with gated pipeline stages, using GitHub environment or GitLab deployment approvals."
sources: ["https://docs.github.com/en/actions/managing-workflow-runs-and-deployments/managing-deployments/managing-environments-for-deployment", "https://docs.gitlab.com/ee/ci/environments/deployment_approvals.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Promotion pipelines, gates and environment parity

## Promote one change, not three edits
The change merged to main is applied to dev, then stage, then prod, in order, from the same commit.
Pin module and collection versions so "same commit" means the same behaviour. Apply the saved plan
file that reviewers saw rather than re-planning at apply time. (Practitioner guidance.)

## Approval gates on the CI platform
**GitHub Actions environments**
- A job that references an environment must satisfy that environment's protection rules before it runs or can access the environment's secrets.
- Required reviewers: up to 6 people or teams; only one of them needs to approve. "Prevent self-review" stops the person who triggered a run from approving it.
- A wait timer (minutes) can delay jobs; "Allow administrators to bypass configured protection rules" can be switched off; deployment branches and tags can be restricted to name patterns.
- Environment secrets and variables are available only to jobs using that environment. Secrets only after the rules pass.
- Referencing a non-existent environment in a workflow creates it with no protection rules, and anyone who can edit workflows can do that, but only repository admins can configure it. Create prod's environment and rules before any workflow uses it.
- Environments, and rules such as required reviewers and wait timers, are available in public repositories on all current plans; for private or internal repositories they need GitHub Pro, Team or Enterprise.

**GitLab deployment approvals** (Premium and Ultimate)
- Approvals apply to deployments to protected environments; deployments are blocked until all required approvals are given.
- By default the user who triggered the pipeline cannot approve the deployment job; a project setting allows the pipeline triggerer to approve.
- A user can give only one approval per deployment even if in several approver groups. After approval, the deployment job must still be run manually.
- Keep the number of required approvals lower than the number of users allowed to deploy.

## Gates worth automating (practitioner judgement)
- Static checks (format, validate, lint, policy) before plan.
- Plan inspection for unexpected deletes before the human approval step.
- Post-apply smoke tests before moving to the next environment.
- A human approval on prod with the plan visible.
A failed gate stops the pipeline; fix forward with a new commit that goes through all stages again.

## Environment parity
Environments should differ only in intended values such as sizes, counts, names and address ranges. Compare variable key sets, pinned module versions and inventory structure across environments in CI, and require every difference to be explained in an allowlist.

## Gotchas
- Hotfixes applied straight to prod break the "same commit" rule; backport immediately.
- Long-lived per-environment branches cause merge drift; prefer one trunk plus promotion.
- Approval fatigue: if every trivial change needs approval, reviewers rubber-stamp.

## Verify
- [ ] The prod job cannot start until stage tests pass and an approver accepts.

## Checked
Method: docs-checked 2026-11-09 against the GitHub Actions "Managing environments for deployment" page and the GitLab "Deployment approvals" page.
The HashiCorp recommended-practices source is only an index page and was dropped. Removed as unconfirmed: the reusable-workflow YAML sketch, the example 24 h soak and "N minutes" thresholds, and the shell and ansible-inventory diff scripts. The gate and parity lists are practitioner judgement, not source-backed.
