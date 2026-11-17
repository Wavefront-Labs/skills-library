---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.iac-documentation-and-runbooks
name: iac-documentation-and-runbooks
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, iac, iac-documentation, terraform-docs, readme, runbooks, architecture-decision-records, adr, module-readme, role-readme, argument-specs, ansible-doc, diagrams-as-code, diagrams, pre-commit-docs, docs-in-repo, operational-runbook, ownership-file, codeowners, changelog, documentation-drift]
level: practitioner
status: draft
description: "Document infrastructure code so it stays true: generated module/role READMEs (terraform-docs, argument_specs), root README with ownership, ADRs, tested runbooks, diagrams as code, CI doc checks."
sources: ["terraform-docs documentation (https://terraform-docs.io/)", "Ansible documentation - Role argument validation (meta/argument_specs.yml) and ansible-doc for roles", "Michael Nygard - Documenting Architecture Decisions (ADR); adr-tools", "Google SRE Workbook - On-call and runbooks guidance", "Diagrams (mingrammer) and Structurizr DSL documentation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IaC documentation and runbooks

**Goal:** a new engineer can find who owns a stack, how to plan/apply it, why it is
shaped the way it is, and what to do at 3 am — from the repo, and the docs cannot
silently rot because the parts that can be generated are generated and checked in CI.

## 1. What goes where
| Doc | Lives | Generated? |
|---|---|---|
| Module / role interface (inputs, outputs, requirements, examples) | `README.md` next to the module/role | yes: `terraform-docs`, `ansible-doc -t role` from `argument_specs.yml` |
| Repo overview: purpose, ownership, layout, how to run, environments, links | root `README.md` + `CODEOWNERS` | hand-written, short, linked |
| Decisions (why X not Y) | `docs/adr/NNNN-title.md` | hand-written, immutable once accepted |
| Runbooks (how to do operational task Z) | `docs/runbooks/<task>.md`, linked from alerts | hand-written, tested |
| Architecture diagram | `docs/architecture.{py,dsl}` → rendered image in CI | diagrams as code |
| Change history | `CHANGELOG.md` | generated from conventional commits / changelog fragments |
Keep docs next to code in the same PR; a wiki page is where documentation goes to die.

## 2. Generated interface docs
```yaml
# .terraform-docs.yml
formatter: markdown table
output: {file: README.md, mode: inject, template: "<!-- BEGIN_TF_DOCS -->\n{{ .Content }}\n<!-- END_TF_DOCS -->"}
sort: {enabled: true, by: required}
settings: {anchor: false, lockfile: false}
```
`terraform-docs .` injects between the markers; pre-commit hook `terraform-docs/terraform-docs` with
`--hook-config=--path-to-file=README.md --add-to-existing-file=true`, and CI runs it with
`--output-check` (fails if the README would change). Put a worked `examples/` directory and reference
it; `description` on every `variable`/`output` is the real documentation — lint for missing ones (`tflint` rule `terraform_documented_variables`).

Ansible roles: `meta/argument_specs.yml` with `description`, `type`, `required`, `default`, `choices`
per option is both validation and docs (`ansible-doc -t role -r roles/ myrole`); keep `README.md`
with a usage example and generate the variables table from the spec with a small script, or keep
the spec as the single source and link it. Collections: `antsibull-docs` builds a docs site.

Pulumi/CDK: docstrings on component resources + `README.md`; `pulumi package get-schema` for packaged components.

## 3. The root README (one screen)
```
# acme-platform-infra
Owner: platform-team (#platform-infra) · On-call: PagerDuty "Platform" · CODEOWNERS enforced
What: network, EKS, RDS for prod/stage in eu-west-1 (Terraform 1.9, OpenTofu-compatible)
Layout: envs/<env>/<stack> (state per dir, see state skill) · modules/ · docs/
Run:  make plan ENV=stage STACK=network   # wraps terraform init/plan with the right backend+role
      Apply only via CI (Atlantis/pipeline) — see docs/runbooks/apply.md
Links: ADRs docs/adr · Runbooks docs/runbooks · Dashboard <url> · Cost report <url>
```
`CODEOWNERS` makes review ownership real; `.github/PULL_REQUEST_TEMPLATE.md` asks "docs/runbook updated?".

## 4. ADRs
```
# 0007 Use S3 lockfile instead of DynamoDB for state locking
Status: Accepted 2026-10-01 (supersedes 0003)
Context: Terraform 1.10 native lockfile; DynamoDB table was an extra resource per account...
Decision: use_lockfile = true in all backends; drop the lock table after migration.
Consequences: requires TF >= 1.10 on all runners; older pipelines must upgrade first.
```
One decision per file, numbered, never edited after acceptance (supersede instead). Record the rejected options briefly. `adr-tools` or a template is enough.

## 5. Runbooks
Each alert links to a runbook; each runbook has: *trigger* (alert name/symptom), *impact*, *checks*
(exact commands/queries with expected output), *actions* (exact commands, including the IaC way —
"bump `desired_capacity` in `envs/prod/web/main.tf` and apply via pipeline", not console clicks),
*rollback*, *escalation*, *last tested date*. Prefer runbooks that execute: a Makefile target, an
Ansible playbook, a controller job template — the doc then says "run X with these inputs" and
describes what it does. Test runbooks in game days; a runbook not run in a year is fiction.

## 6. Diagrams as code
```python
# docs/architecture.py  (mingrammer/diagrams)
from diagrams import Diagram, Cluster
from diagrams.aws.network import ALB
from diagrams.aws.compute import EKS
from diagrams.aws.database import RDS
with Diagram("prod eu-west-1", filename="docs/architecture", show=False):
    with Cluster("vpc"):
        ALB("alb") >> EKS("eks") >> RDS("postgres")
```
CI renders `docs/architecture.png`; reviewers see the diagram diff with the code diff. Structurizr DSL/C4 for bigger systems; `terraform graph | dot` or Rover/Inframap for a generated resource graph when you need "what is actually there".

## 7. CI for docs
- `terraform-docs --output-check`, `antsibull-docs lint-collection-docs`, markdown lint, link checker (`lychee`), ADR numbering uniqueness.
- A PR touching `envs/prod` without a change to `docs/` or a `no-docs-needed` label prompts a bot comment (cheap nudge).
- Runbook `last tested` older than 180 days surfaces in a monthly report.

## Gotchas
- Hand-maintained variable tables are wrong within a month; generate or delete them.
- A README that explains Terraform itself is noise; link the tool docs and write only what is specific to this repo.
- Secrets and internal hostnames in runbooks leak when the repo is shared; use placeholders and link to the secret store.
- Diagrams that try to show everything show nothing; one diagram per stack/boundary.
- ADRs for trivial choices bury the important ones; write one when someone would plausibly ask "why?" in a year.

## Verify
- [ ] `terraform-docs --output-check` (or the role spec check) passes in CI and fails when a variable description is removed.
- [ ] A new joiner can run `make plan` for stage from the README alone, without asking anyone.
- [ ] Every paging alert links to a runbook whose commands were executed in the last game day.
- [ ] The three most contested design choices in the repo each have an ADR.
