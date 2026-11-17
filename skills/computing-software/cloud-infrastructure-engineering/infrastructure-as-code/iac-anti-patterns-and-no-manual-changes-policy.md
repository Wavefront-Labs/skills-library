---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.iac-anti-patterns-and-no-manual-changes-policy
name: iac-anti-patterns-and-no-manual-changes-policy
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, iac-fundamentals, iac-anti-patterns, no-manual-changes, change-freeze, break-glass, clickops]
level: practitioner
status: draft
description: "Recognise common IaC anti-patterns and enforce a no-manual-changes policy with read-only console access, break-glass procedures, drift checks and change freezes."
sources: ["Kief Morris - Infrastructure as Code, 2nd ed., O'Reilly (patterns and antipatterns)", "AWS Well-Architected Operational Excellence - Use infrastructure as code (https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_dev_integ_code_quality.html)", "HashiCorp - Terraform recommended practices (https://developer.hashicorp.com/terraform/cloud-docs/recommended-practices)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IaC anti-patterns and the no-manual-changes policy

## Anti-patterns to spot in review
| Anti-pattern | Symptom | Fix |
|---|---|---|
| ClickOps alongside code | drift alerts, "don't run apply, it'll undo X" | no-manual-changes policy (below) |
| Snowflake environments | prod differs from stage in undocumented ways | same code + per-env data only |
| Monolithic state / root | 20-minute plans, everyone blocked by one lock | split by blast radius/team |
| Copy-paste modules | the same fix needed in 12 places | versioned shared modules |
| Logic on env names | `count = var.env == "prod" ? 3 : 1` everywhere | feature variables in tfvars |
| Secrets in code/state outputs | passwords in Git or plan logs | secret stores, `sensitive`, ephemeral |
| `shell`/`command` everywhere in Ansible | always "changed", not idempotent | real modules, `changed_when` |
| Apply from laptops | unknown versions, no audit | apply only from CI with pinned tools |
| Unpinned versions | "worked yesterday" | lock files, pinned modules/collections |
| Long-lived feature branches per env | merges diverge | trunk + promotion pipeline |
| No tests | changes found broken in prod | lint, policy, plan checks, Molecule |
| `ignore_changes` / `--skip-tags` as permanent fixes | hidden drift | fix root cause, time-boxed exceptions |

## No-manual-changes policy
1. **Write path = pipeline.** Humans get read-only roles in consoles/APIs for prod (e.g. AWS `ReadOnlyAccess`, Azure Reader); the CI role is the only one with write.
2. **Break-glass**: a separate privileged role with MFA, alerting on use (CloudTrail/EventBridge → pager), time-limited sessions, and a mandatory follow-up: codify or revert within 24 h, ticket required.
3. **Detect**: scheduled drift detection; alerts on console write events by humans.
4. **Make the right way fast**: small PRs, quick pipelines, emergency fast-track lane with post-review — otherwise people bypass the process.
5. **Ansible-managed hosts**: banner `{{ ansible_managed }}` in files, config management on a schedule (AWX schedule / ansible-pull) to revert hand edits; disable direct root SSH.

## Change freezes
- Encode freeze windows in the pipeline (a calendar file or API check job that fails prod applies during freezes unless an `emergency` label + approver is present).
- Freezes do not stop drift detection; they stop non-emergency applies.
- Before a freeze: drain the queue of approved changes; after: apply in small batches, not a big bang.

## Gotchas
- Policies without tooling decay: if engineers still have admin in prod, they will use it under pressure.
- Some changes are legitimately manual (support case, vendor console) — record and import them.

## Verify
- [ ] Human IAM principals in prod have no write permissions (access analyzer / policy simulator).
- [ ] Break-glass use in the last quarter each has a linked ticket and codification PR.
