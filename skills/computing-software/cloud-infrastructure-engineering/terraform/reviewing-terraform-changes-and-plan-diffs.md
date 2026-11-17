---
id: computing-software.cloud-infrastructure-engineering.terraform.reviewing-terraform-changes-and-plan-diffs
name: reviewing-terraform-changes-and-plan-diffs
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, code-review, plan-review, change-review, pull-request, atlantis, hcp-terraform, review-checklist, speculative-plan, setup-terraform]
level: practitioner
status: docs-checked
description: "Put the plan in the Terraform PR: HCP Terraform speculative plans, Atlantis comments and setup-terraform PR comments, with documented limits and a reviewer checklist."
sources: ["https://developer.hashicorp.com/terraform/cloud-docs/workspaces/run/ui", "https://www.runatlantis.io/docs/using-atlantis.html", "https://github.com/hashicorp/setup-terraform", "https://developer.hashicorp.com/terraform/language/style"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reviewing Terraform changes and plan diffs

**Goal:** approve infrastructure changes on the basis of what Terraform will do, not
what the HCL diff looks like. Make a machine-posted plan part of every PR.

## 1. Get the plan into the PR
**HCP Terraform / Terraform Enterprise (UI and VCS-driven):**
- A workspace is linked to one branch. HCP Terraform runs a speculative plan when a PR is
  opened against that branch, posts a link to the plan in the PR, and re-runs it when the
  PR is updated. One PR can carry links to several plans, one per connected workspace.
- Only PRs from the same repository trigger speculative plans; PRs from forks do not
  (on Terraform Enterprise administrators can allow them). Workspaces limited to certain
  directories are skipped for PRs that do not touch them, and still get a passing status.
- Only HCP Terraform organization members with permission to read runs can open the full
  plan output; any repo contributor sees the status indicator.
- Status checks are not updated with the apply result, so a successful plan with an errored
  apply still shows passing.
- A speculative plan uses the PR head branch against the workspace's current state. If the
  destination branch has moved, rebase or merge it into the head to get an accurate plan.
- By default plans need "Confirm & Apply"; auto apply is optional per workspace.

**Atlantis (PR comments):**
- `atlantis plan` runs `terraform plan` on the PR branch; `-d`, `-p` and `-w` select
  directory, project or workspace; extra Terraform flags go after `--`. Flags that move
  where Terraform runs or writes (`-out`, `-state`, `-chdir` and similar) are blocked.
- `atlantis apply` applies the plan that matches the directory, project or workspace;
  without arguments it applies all unapplied plans of the PR. Because it applies a saved
  plan file, plan-changing flags such as `-target` or `-var` are ignored at apply time.
- A bare `atlantis plan` (like autoplan) discards plans previously created with
  `-p`/`-d`/`-w`. `atlantis unlock` removes the PR's locks and discards its plans.
- `-- -destroy` creates a destroy plan; the docs warn applying it can cause data loss.

**GitHub Actions with `hashicorp/setup-terraform`:**
- The action installs the CLI and, by default, a wrapper exposing `stdout`, `stderr` and
  `exitcode` as step outputs. The README example posts fmt, init, validate and plan results
  as a PR comment with `actions/github-script` (needs `permissions: pull-requests: write`)
  and shows how to update an existing bot comment instead of adding new ones.
- GitHub comments are limited to 65535 characters, so a long plan can fail the workflow even
  though the plan succeeded; the README suggests appending to `$GITHUB_STEP_SUMMARY`.
- A saved plan that is applied later must be the one the reviewer saw (see
  `terraform-jobs-in-azure-pipelines-and-jenkins` for saved-plan handling).

## 2. Reviewer checklist (practice, not from a single source)
- [ ] Summary counts match the PR description; every destroy or replacement is named.
- [ ] Nothing stateful is replaced without a plan for its data.
- [ ] Security-relevant attributes unchanged unless intended.
- [ ] `terraform fmt` and `terraform validate` pass (the HashiCorp style guide says to run
      both before committing).
- [ ] The plan is current: rebased on the destination branch, planned against current state.
- [ ] The apply uses the reviewed plan file or run, not a fresh plan.

## 3. Gotchas
- Plan output pasted into a PR comment is visible to everyone who can read the PR, so
  restrict it where plans can include sensitive data. A saved plan file holds values in
  cleartext even when the terminal output hides them.
- Large plans can exceed the comment limit; link to a run or upload an artifact.

## Verify
- [ ] Every PR to the infra repo has a machine-posted plan the reviewer can read.
- [ ] Destroys and replacements are listed in the PR description.

## Checked
Checked 2026-11-08 against HashiCorp's UI and VCS-driven run workflow page, the Atlantis "Using Atlantis" page, the setup-terraform README and the Terraform style guide.
Removed as not stated by the pages: Atlantis `repos.yaml` `--require approved,mergeable`, directory locking claim, CODEOWNERS and branch-protection advice, the 50-resource threshold, `moved`-block and `ignore_changes` review rules, the `count` feature-flag trick and provider-upgrade claims. The checklist in section 2 is kept as marked practice, not as a documented requirement.
Method: docs-only read of cited pages, 2026-11-08
