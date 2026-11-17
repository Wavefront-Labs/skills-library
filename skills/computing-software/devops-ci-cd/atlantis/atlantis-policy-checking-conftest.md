---
id: computing-software.devops-ci-cd.atlantis.atlantis-policy-checking-conftest
name: atlantis-policy-checking-conftest
category: computing-software
field: devops-ci-cd
product: atlantis
tags: [policy-checking, conftest, rego, policy-owners, sticky-approvals, approve-policies]
level: advanced
status: docs-checked
description: "Enforce Conftest Rego policies on Atlantis plans with policy sets, owner approvals and sticky approvals."
sources: ["https://www.runatlantis.io/docs/policy-checking"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Atlantis policy checking conftest

Atlantis can run server-side Conftest (OPA/Rego) against the JSON plan. Failing policies block apply until fixed in a later commit or approved by policy owners; policy approvals are separate from normal PR approval.

Enable with `--enable-policy-checks`. If you use `--gh-team-allowlist`, also allow `policy_check` (for example `*:plan,*:policy_check,*:unlock,myteam:apply`) or manual `atlantis plan` skips the check (autoplans still run it).

```yaml
policies:
  owners:
    users: [nishkrishnan]
  policy_sets:
  - name: deny_local_exec
    path: /path/to/policies/deny_local_exec/
    source: local
    approve_count: 2
    owners:
      users: [pseudomorph]
```

Policy set keys: `name`, `path`, `source` (only `local`), `owners`, `approve_count` (default 1), `prevent_self_approve`, `sticky_policy_approvals`, `policy_item_regex`. Top-level also supports `conftest_version`.

Conftest runs only the `main` package unless you add `--namespace` or `--all-namespaces` through `extra_args` of a `policy_check` workflow step. Remote policies work with `--update` and go-getter sources (S3, git, OCI) but host auth must be configured separately. `extra_args` are split on whitespace and run without a shell.

Sticky approvals keep approvals across re-plans while no new items appear in the output matched by `policy_item_regex` (default `(?s).+` treats the whole output as one item; `.+` tracks each line). Fixing a violation does not invalidate approvals; adding or changing one does. Exempt a repo with `policy_check: false`. `atlantis approve_policies --clear-policy-approval` clears approvals. `--quiet-policy-checks` comments only on failure.

## Checked

2026-11-03. Prose and identifiers confirmed against the official Atlantis docs page(s): Conftest Policy Checking, Server Side Repo Config (Policies). Removed or fixed: nothing needed removing.

Method: documentation only; no commands were run.
