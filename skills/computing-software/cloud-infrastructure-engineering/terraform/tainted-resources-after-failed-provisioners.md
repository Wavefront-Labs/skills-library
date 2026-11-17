---
id: computing-software.cloud-infrastructure-engineering.terraform.tainted-resources-after-failed-provisioners
name: tainted-resources-after-failed-provisioners
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, untaint-provisioner, tainted-loop, tainted, untaint, provisioner-failure, on-failure]
level: practitioner
status: verified
description: "Recover when a creation provisioner fails and marks a resource tainted: decide between untaint and replace, and stop the taint-replace-fail loop."
sources: ["https://developer.hashicorp.com/terraform/language/resources/provisioners/syntax#failure-behavior", "https://developer.hashicorp.com/terraform/cli/commands/untaint", "https://developer.hashicorp.com/terraform/cli/commands/taint"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tainted after a failed provisioner

## What happened
A creation-time provisioner (`remote-exec`, `local-exec`, `file`) failed. The
object exists, but Terraform cannot trust it, so it is recorded as **tainted**:
```
Error: local-exec provisioner error ...
# terraform_data.web is tainted, so must be replaced
```
The next plan replaces it — and if the provisioner keeps failing you get a
**tainted loop**: create, fail, taint, replace, fail…

## Decide
1. Read the provisioner error; reproduce manually (SSH in, run the script).
2. If the object is actually fine (the failure was a flaky post-step you have since
   completed by hand):
```bash
terraform untaint 'aws_instance.web'
terraform untaint 'module.app.aws_instance.web[0]'
terraform plan     # should be No changes
```
3. If the object is half-configured, keep the taint and fix the cause first:
   network reachability, wrong user, host not finished booting, missing interpreter.

## Breaking the loop
- Fix the script, then apply once.
- If the provisioner is non-essential: `on_failure = continue` (the error is ignored and the
  resource is not tainted; on Terraform 1.17.0 it logged no warning at all, only the
  `Executing` line). Use sparingly.
- Better: move configuration to `user_data`/cloud-init or an image build (Packer)
  so creation does not depend on SSH at all.

## Gotchas
- `untaint` writes state immediately (no plan); take the lock, note it in the ticket.
- Destroy-time provisioners failing do not taint; they leave the resource in state
  and fail the destroy.
- A tainted object under `create_before_destroy` keeps serving traffic until its
  replacement succeeds — not so without CBD.
- `terraform show` lists `(tainted)` in the resource comment line, e.g. `# terraform_data.web: (tainted)`.

## Verify
- [ ] `terraform show | grep -i tainted` is empty after untaint/replace.
- [ ] A fresh `terraform apply` of the resource completes the provisioner without error.

## Checked
- Terraform 1.17.0, `terraform_data` with `local-exec` (`exit 1` on create): apply returned `local-exec provisioner error` and `terraform show` printed `# terraform_data.web: (tainted)`; the resource stayed in state. `untaint` printed `successfully untainted` and the next plan no longer said tainted (it proposed only the other unapplied resources); `untaint` on a missing address failed with `No such resource instance` (exit 1), and with `-allow-missing` exited 0 with a warning.
- `on_failure = continue`: apply succeeded, nothing tainted, and no warning appeared (the skill said "only warns").
- A destroy-time provisioner (`when = destroy`, `exit 1`) failed the destroy and the resource remained in state, not tainted.
- Under `create_before_destroy` the failed new object is tainted while the old one is kept as deposed (see the deposed-objects skill run). Windows ran provisioner commands via `cmd /C`.
- Removed the cloud-init and security-group specifics from the skill because no SSH or cloud target was run; the remote-exec items are advice about the target host, not Terraform behaviour.
