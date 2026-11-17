---
id: computing-software.cloud-infrastructure-engineering.terraform.provisioners-and-their-pitfalls
name: provisioners-and-their-pitfalls
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, provisioners, local-exec, remote-exec, terraform-data, config-management, packer, triggers, destroy-time-provisioner, on-failure, anti-pattern]
level: practitioner
status: docs-checked
description: "Know when local-exec/remote-exec provisioners are the wrong tool, what HashiCorp recommends instead, and how to limit the blast radius when you must use one."
sources: ["https://developer.hashicorp.com/terraform/language/provisioners", "https://developer.hashicorp.com/terraform/language/resources/provisioners/syntax", "https://developer.hashicorp.com/terraform/language/resources/terraform-data"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Terraform provisioners and their pitfalls

**Goal:** know why HashiCorp's docs treat provisioners as a last resort, reach for a purpose-built alternative first, and when a provisioner is unavoidable, limit what a failure can break.

## 1. Why they are a last resort
- Terraform is designed mainly for immutable infrastructure. The docs "strongly recommend using purpose-built solutions" for post-apply work and exhausting alternatives such as machine images or configuration management first.
- Terraform cannot model what a provisioner does, and provisioners usually need network access and credentials to your servers.
- A failed creation-time provisioner fails the apply and taints the resource, so it is destroyed and recreated on the next apply (even if the resource itself was created fine). `on_failure = continue` ignores the error and does not taint.

## 2. Prefer a purpose-built tool
| Need | Use instead |
|---|---|
| A fully configured, versioned base image | Bake a machine image ahead of time (for example with Packer) and reference it from the resource |
| Ongoing configuration of servers | A configuration management tool run separately |
| Work not tied to a real resource | `terraform_data` (its `triggers_replace` argument reruns provisioners when a referenced value changes) |

## 3. When you need one
Types: `file` (copy files to the resource), `local-exec` (run on the machine running Terraform), `remote-exec` (run on the resource).
```hcl
resource "aws_instance" "bastion" {
  # ...
  provisioner "remote-exec" {
    inline = ["sudo systemctl restart sshd"]
    connection {
      type        = "ssh"
      host        = self.public_ip
      user        = "ec2-user"
      private_key = file("<KEY_PATH>")
    }
  }
  provisioner "local-exec" {
    when       = destroy
    command    = "echo ${self.id} >> decommissioned.log"
    on_failure = continue
  }
}
```
- Provisioner and connection blocks must reference the parent through `self`, not by resource name (that creates a dependency cycle).
- A `connection` block (SSH or WinRM) can sit on the resource or the provisioner; bastion host and proxy options exist. SSH host key checking is off by default: set `host_key` to verify.
- Multiple provisioners run in the order defined. Creation-time and destroy-time ones can share a resource block; only those valid for the operation run.
- `terraform_data` hosts provisioners that are not tied to a real resource; `triggers_replace` makes the reason for a rerun explicit.

## Gotchas
- Destroy-time provisioners (`when = destroy`) run before the resource is destroyed. If one fails, apply errors and it runs again on the next apply, so write it to be safe to repeat.
- Destroy-time provisioners do not run on tainted resources, and `create_before_destroy` on the resource prevents them from running.
- Deleting a resource block that has a destroy-time provisioner removes the provisioner too, so it never runs. The docs' workaround: set `count = 0`, apply, then remove the block.
- Leave `on_failure` at its default (fail) unless the step is truly optional, so a broken bootstrap is visible.
- Remote scripts upload to `/tmp/terraform_%RAND%.sh` (unix) or a terraform_%RAND%.cmd file in the Windows temp directory by default; override with `script_path`. SSH file upload needs `scp` on the remote system.
- Sensitive and ephemeral values are supported in provisioner and connection blocks and kept out of logs, plans and state; ephemeral values need Terraform 1.10 or later.

## Verify
- [ ] No provisioner covers a need that a machine image or configuration management already covers.
- [ ] Destroy-time provisioners are safe to run twice.
- [ ] `on_failure` is set deliberately.
- [ ] `plan` shows no unexpected replacements from tainted resources after adding a provisioner.

## Checked
Method: docs-only read of cited pages, 2026-11-08
Confirmed on the Terraform provisioners, provisioner syntax and terraform_data pages. Removed: cloud-init and cloud-vendor claims, null_resource comparison and the Terraform 1.4 note, the claim that secrets land in logs and state (the docs say sensitive and ephemeral values are kept out), the local_file remark, and the non-URL source labels.
