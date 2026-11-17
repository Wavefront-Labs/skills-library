---
id: computing-software.cloud-infrastructure-engineering.terraform.state-lineage-and-serial-mismatch
name: state-lineage-and-serial-mismatch
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, lineage-mismatch, serial-mismatch, state-push, state-force-push, disaster-recovery]
level: advanced
status: verified
description: "Understand state lineage and serial, diagnose 'different lineage' and 'serial is lower' errors on state push, and decide safely when -force is justified."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/state/push", "https://developer.hashicorp.com/terraform/language/state", "https://developer.hashicorp.com/terraform/internals/json-format"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lineage and serial mismatches

## The two fields
```bash
terraform state pull | jq '{lineage, serial, terraform_version}'
```
- **lineage**: UUID assigned when a state is first created. Same lineage = same
  history. Different lineage = a different state entirely (e.g. someone ran `init`
  against an empty backend and applied).
- **serial**: increments on every write. Higher = newer within a lineage.

## Errors on push
```
Failed to write state: cannot overwrite existing state with serial 41 with a different state that has the same serial
Failed to write state: cannot import state with lineage "a1..." over unrelated state with lineage "b2..."
Failed to write state: cannot import state with serial 38 over newer state with serial 41
```
They are safety checks preventing you from overwriting newer or unrelated history. (All three messages were reproduced
verbatim with `terraform state push` against the local backend on Terraform 1.17.0; the first two lines above use
whatever serial or lineage your state has.)

## Diagnose before forcing
```bash
terraform state pull > remote.json
jq -r '.resources[] | "\(.module // "root") \(.type).\(.name)"' remote.json | sort > r.txt
jq -r '.resources[] | "\(.module // "root") \(.type).\(.name)"' candidate.json | sort > c.txt
diff r.txt c.txt
jq '{lineage,serial}' remote.json candidate.json
```
- **Lower serial, same lineage**: candidate is older. Only push (with `-force`) if you
  deliberately roll back — everything created after it becomes unmanaged.
- **Same serial, different content**: two writers diverged (lock bypassed). Merge
  manually: pick the newer base, `import` what only the other contains.
- **Different lineage**: wrong file or wrong backend key. Check you're pointing at the right
  workspace/key before anything else.

## Forcing
```bash
terraform state push -force candidate.json
```
Only with the lock held, the remote copy saved, and the diff understood. Afterwards
`terraform plan` must match expectations. `-force` overrides all three checks (an unrelated lineage was
accepted, and a lower serial was accepted); on the local backend the written serial came out one higher than the file's
(a pushed file with serial 3 left serial 4 in the backend), so do not rely on the serial in the file you pushed.

## Gotchas
- Editing a state JSON by hand requires bumping `serial` (else push refuses same-serial).
- Copying a state between two root modules carries the lineage — two states with the same
  lineage in different keys is confusing; it's fine for terraform but trips tooling.

## Verify
- [ ] Remote state saved before any forced push; `diff` reviewed and attached to the incident.
- [ ] Post-push plan matches the expected changes.

## Checked
- Terraform 1.17.0, `terraform_data` resources on the local backend: `state pull | jq '{lineage, serial, terraform_version}'` printed the three fields; pushing an older-serial file, a file with a different lineage, and a different file with the same serial each failed with exactly the three messages in the skill, exit code 1; `state push -force` accepted the different lineage and the older serial; the diagnostic `jq | sort | diff` snippet printed the added line `root terraform_data.b` for a candidate that had one more resource, and the `{lineage,serial}` comparison worked; after force-pushing the older file `plan` proposed the missing resource (`Plan: 1 to add`), showing the rollback leaves objects unmanaged.
- Hand-edited serial: earlier runs confirmed a state edited with a bumped serial pushes cleanly (see the deposed-objects skill run).
- Scope: all runs used the local backend; the advice to hold the lock and save the remote copy first is procedure, not a behavioural claim.
