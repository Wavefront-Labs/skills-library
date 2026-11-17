---
id: computing-software.cloud-infrastructure-engineering.terraform.tfcmt-plan-notifications
name: tfcmt-plan-notifications
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, tfcmt, pr-comment, github-actions, plan-review, ci-cd]
level: practitioner
status: docs-checked
description: "Post Terraform plan and apply results to GitHub PRs with tfcmt: target variable per root, labels for add-or-update, destroy, no-changes, deletion warning, patching comments."
sources: ["https://suzuki-shunsuke.github.io/tfcmt/", "https://github.com/suzuki-shunsuke/tfcmt", "https://suzuki-shunsuke.github.io/tfcmt/getting-started/", "https://suzuki-shunsuke.github.io/tfcmt/usage/", "https://suzuki-shunsuke.github.io/tfcmt/config/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# tfcmt plan notifications

tfcmt wraps `terraform plan` and `terraform apply`, parses the result, binds it to Go templates, updates pull request
labels and posts a comment to GitHub. It supports GitHub only; for GitLab the README points to `tfcmt-gitlab`, a
fork. It is a fork of mercari/tfnotify with Terraform 0.15+ support.

## Run
```bash
tfcmt -var target:payments-prod plan -- terraform plan -no-color -input=false
tfcmt -var target:payments-prod apply -- terraform apply -no-color -auto-approve tfplan
```
- Syntax: `tfcmt [global options] plan [--patch] [--skip-no-changes] -- terraform plan [options]` and
  `tfcmt [global options] apply -- terraform apply [options]`.
- Global options include `--owner`, `--repo`, `--sha`, `--build-url`, `--pr`, `--config`, `--var`, `--output`
  (write the result to a file instead of posting). Most have `TFCMT_*` environment variables.
- On AWS CodeBuild, CircleCI, Drone, GitHub Actions and Google Cloud Build tfcmt reads owner, repo and PR number from
  built-in environment variables; elsewhere supply them, and note it cannot always get the PR number.
- A GitHub token needs Pull Requests: Write (comments) and Issues: Write (labels). Pass it as `GITHUB_TOKEN`.
- The install page lists installation options; check it for the current version and method.

## Monorepo: the `target` variable
`--var target:<name>` (format `<name>:<value>`) puts the name in the comment title (`Plan Result (<name>)`) and in the
label prefix, so multiple roots in one repo get distinct comments and labels.

## What it posts
- The matched result line (`Plan: 1 to add, 0 to change, 0 to destroy` or `No changes`), a list of Create, Update,
  Delete, Replace, Import and Move resource paths, and the full output in a collapsible Details section.
- A deletion warning ("Resource Deletion will happen") when the plan contains deletions.
- Optional separate sections for changes made outside Terraform and for Terraform warnings; the plan result can
  exclude noisy "Refreshing state" lines (`ChangedResult`).
- Labels: `no-changes` (green), `add-or-update` (blue; resources created or updated, none destroyed or recreated) and
  `destroy` (red; resources destroyed or recreated). With a `target` var the labels become `<target>/no-changes` and so
  on. Disable labels with `--disable-label` or `terraform.plan.disable_label: true`. Use the `destroy` label with your
  repository rules if you want extra approval.

## Config
The configuration file is optional. Without `--config`, tfcmt searches `tfcmt.yaml` or `tfcmt.yml` (also with a
leading dot) from the current directory up to the root. A JSON Schema is available for validation. Templates use Go
templates with sprig functions plus `avoidHTMLEscape` and `wrapCode` (which omits too-long text).
```yaml
terraform:
  plan:
    when_destroy:
      label: "{{if .Vars.target}}{{.Vars.target}}/{{end}}destroy"
```

## Stale comments
- `plan --patch` updates the existing comment instead of creating a new one (or creates one if none exists).
- tfcmt itself does not hide old comments; it embeds metadata as an HTML comment so `github-comment hide` can.
- `plan --skip-no-changes` updates the label but posts no comment when there are no changes.

## Gotchas
- Comments show what Terraform prints, so treat plan output posted to a pull request as visible to everyone who can
  read that repository.

## Verify
- [ ] The PR shows one current plan comment per root and the expected labels.

## Checked
Confirmed 2026-11-08 against the tfcmt site index, Getting Started, Command Usage and Configuration pages and the
GitHub README. Removed: aqua installer versions, the `hide_old_comment` config key (not in the documented config), the
GitHub 65,536-character truncation claim and the `pull-requests: write` workflow permission name (page lists the PAT
permissions instead).
Method: docs-only read of cited pages, 2026-11-08
