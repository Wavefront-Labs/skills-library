---
id: computing-software.cloud-infrastructure-engineering.terraform.moved-blocks-in-published-modules-and-chained-moves
name: moved-blocks-in-published-modules-and-chained-moves
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, moved-in-modules, module-refactor-moved, chained-moves, moved-cleanup, module-versioning, semver]
level: advanced
status: verified
description: "Ship refactors inside shared modules with moved blocks so callers upgrade without destroys; chain successive renames and decide when moved blocks can be deleted."
sources: ["https://developer.hashicorp.com/terraform/language/modules/develop/refactoring", "https://developer.hashicorp.com/terraform/language/block/moved"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# `moved` in published modules, chaining, and cleanup

## Refactoring inside a shared module
When you rename or restructure resources in a module other teams consume, put the
`moved` blocks **in the module itself**:
```hcl
# modules/bucket/moved.tf  (v3.0.0)
moved {
  from = aws_s3_bucket.this
  to   = aws_s3_bucket.main
}
moved {
  from = aws_s3_bucket_policy.this[0]
  to   = aws_s3_bucket_policy.main
}
```
Callers bump the version and their plan shows `has moved to` — no work on their
side (ran with a `count = 2` module: both instances showed `has moved to`, `0 to destroy`). Addresses in a module's moved block are relative to that module and may
refer to its child module calls (`module.inner.aws_x.y`).

## Chained moves
Successive releases rename again (`this` → `main` in v3, `main` → `primary` in v4).
Keep **both** blocks:
```hcl
moved {
  from = aws_s3_bucket.this
  to = aws_s3_bucket.main
}
moved {
  from = aws_s3_bucket.main
  to = aws_s3_bucket.primary
}
```
Terraform follows the chain, so a caller jumping from v2 straight to v4 still
moves correctly (ran: state created by the v2 code, then `this` -> `main` -> `primary` in one step gave `terraform_data.this has moved to terraform_data.primary`). Do not rewrite the first block to point at `primary`; either
works, but the chain documents history and avoids mistakes.

## When can moved blocks be deleted?
- **Root modules you own**: after every workspace/environment of that config has
  applied the change. Check each state (`terraform state list`) before deleting.
- **Published modules**: effectively never within a major version. Removing them is
  a breaking change — any caller who skipped the release gets destroy/recreate. If
  you must prune, do it in a major release and say so in the CHANGELOG with the
  minimum version callers must pass through first.
- Cost of keeping them is near zero; the cost of removing early is data loss.

## Release hygiene
- Treat a refactor *with* moved blocks as a minor release; without them (forcing
  replacement) it is a major.
- Add a test in `tests/` that plans against a fixture state from the previous
  version (or document a manual upgrade check) and asserts no destroys.
- CHANGELOG: list each address move.

## Gotchas
- `moved` in a module can only move objects that module declares (or its children);
  it cannot rename the caller's `module "x"` block — the caller writes that one (ran: `moved { from = module.b to = module.c }` inside the child module was silently ignored, with no error and no move).
- Module calls with `count`/`for_each`: the module's moved blocks apply to every
  instance automatically.
- A moved block whose `from` still exists as a resource errors (`Moved object still exists`, ran) — rename the block,
  do not duplicate.

## Verify
- [ ] Upgrading a consumer from the oldest supported version shows only `has moved to`, no destroys.
- [ ] CHANGELOG lists the moves and the minimum upgrade path.

## Checked
- Terraform 1.17.0 with a local module called with `count = 2` over `terraform_data`: chained moves across two renames plus `policy[0]` -> `policy_main` all planned as `has moved to` for both instances with 0 to add/change/destroy; a `from` that still exists gave `Moved object still exists`; a module-call `moved` inside the child was ignored. Release, CHANGELOG and test-fixture advice is process guidance, not a measured claim.
