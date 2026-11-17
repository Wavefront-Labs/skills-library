---
id: computing-software.cloud-infrastructure-engineering.terraform.finding-tainted-instances-in-state
name: finding-tainted-instances-in-state
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, tainted-status, taint, untaint, state-inspection]
level: practitioner
status: verified
description: "Find which instances are tainted (or deposed) in state before a plan surprises you, via plan output, state show and jq, and decide whether to untaint or replace."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/untaint", "https://developer.hashicorp.com/terraform/cli/state/taint", "https://developer.hashicorp.com/terraform/cli/commands/state/show"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Finding tainted instances

## How things get tainted
- A create that failed partway (provider error after the object existed).
- A creation-time provisioner failed (`on_failure = fail`, the default).
- `terraform taint` (documented as deprecated since v0.15.2 in favour of `apply -replace=ADDR`).

## Detect
**Plan** shows:
```
  # terraform_data.web is tainted, so must be replaced
-/+ resource "terraform_data" "web" {
```
**State show** prints a comment:
```bash
terraform state show 'terraform_data.web' | head -3
# terraform_data.web: (tainted)
```
**All tainted instances at once**:
```bash
terraform state pull | jq -r '.resources[] | . as $r | .instances[]
  | select(.status == "tainted")
  | "\(if $r.module then $r.module + "." else "" end)\($r.type).\($r.name)\(if .index_key != null then "[\(.index_key|tojson)]" else "" end)"'
```
The jq prints `module.x.type.name` for module resources and `type.name["key"]` for `for_each`
instances. Deposed objects (from a failed `create_before_destroy` replacement) have a
`deposed` key (the 8-character deposed key) instead of `status`, so they do not match
`select(.status == "tainted")`; also check `.deposed` (see the deposed-objects skill).

## Decide
| Situation | Action |
|---|---|
| Object is broken/half-configured | let the plan replace it |
| Object is fine (provisioner failed for a transient reason, you fixed it manually) | `terraform untaint ADDR` |
| Stateful resource (DB) tainted | untaint first, investigate; never auto-replace data stores |

```bash
terraform untaint 'terraform_data.web["a"]'
terraform untaint -allow-missing module.app.terraform_data.this   # exit 0 with a warning if absent
```

## Prevention
- Make provisioners idempotent or move them to user_data/config management.
- CI: fail the PR plan job loudly when it contains `is tainted` on stateful types.

## Verify
- [ ] Tainted list is empty or each entry has an owner and a decision.

## Checked
- Terraform 1.17.0, `terraform_data` with a failing `local-exec` creation provisioner: the resource became tainted; `plan` printed `is tainted, so must be replaced` with a `-/+` header; `state show` first line was `# terraform_data.b["p"]: (tainted)` (same for a manual `terraform taint`); the jq (module prefix corrected here: the original printed a leading `.` for root resources) listed `terraform_data.b["p"]`; `untaint -allow-missing` on a missing address exited 0 with a warning, without the flag exit 1 with `No such resource instance`.
- A failed `create_before_destroy` replacement left the new object tainted and the old one with a `deposed` key and no `status`, so the tainted query misses it.
- Docs (developer.hashicorp.com/terraform/cli/commands/taint, untaint): taint is marked deprecated in favour of `-replace` from v0.15.2; `-allow-missing` wording confirmed.
