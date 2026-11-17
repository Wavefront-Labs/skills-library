---
id: computing-software.cloud-infrastructure-engineering.terraform.removed-blocks-with-destroy-provisioners
name: removed-blocks-with-destroy-provisioners
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, removed-provisioner, removed-block, destroy-provisioner, when-destroy, cleanup-hooks]
level: advanced
status: gated
description: "Keep destroy-time provisioners working after deleting a resource block by moving them into a removed block (Terraform 1.9+), with self, connection and failure rules."
sources: ["https://developer.hashicorp.com/terraform/language/resources/syntax#removing-resources", "https://developer.hashicorp.com/terraform/language/resources/provisioners/syntax#destroy-time-provisioners"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Destroy provisioners inside `removed` blocks

## The problem
A destroy-time provisioner lives in the resource block:
```hcl
resource "aws_instance" "worker" {
  provisioner "local-exec" {
    when    = destroy
    command = "./deregister.sh ${self.id}"
  }
}
```
Deleting the resource block to destroy the instance also deletes the provisioner,
so it **never runs** — the classic "destroy provisioners only run if the block is
still there" trap (you had to `terraform destroy -target` first).

## The fix (Terraform 1.9+)
```hcl
removed {
  from = aws_instance.worker

  lifecycle {
    destroy = true                # default; the object is destroyed
  }

  provisioner "local-exec" {
    when    = destroy
    command = "./deregister.sh ${self.id}"
  }

  connection {                    # if using remote-exec (gated: unconfirmed, source is paywalled or blocked) (SSH connection not run)
    type = "ssh"
    host = self.private_ip
    user = "ubuntu"
  }
}
```
- `self` refers to the object's **state** values (the config is gone; ran: `self.input` printed each instance's stored value).
- Only `when = destroy` provisioners are allowed here (ran: a provisioner without `when = destroy` gave `Only destroy-time provisioners are valid in "removed" blocks`).
- Works for every instance of a `count`/`for_each` resource; `from` has no index (ran: `terraform_data.worker["a"]` gave `Resource instance keys not allowed`).
- The Terraform 1.17 docs list `lifecycle` as required; a `removed` block without it was accepted and destroyed the objects in 1.17.0 (ran), but keep it to state intent.

## Rules for destroy provisioners generally
- They must reference only `self`, `count.index`, `each.key` — no other resources or
  variables (ran: `var.v` and `terraform_data.o.id` gave `Invalid reference from destroy provisioner`, in a resource and in a `removed` block). Pass needed values through `self` attributes or
  tags, or through `terraform_data.input`.
- Failure fails the apply (ran: `local-exec provisioner error ... exit status 1`, the object stayed in state); set `on_failure = continue` if cleanup is best-effort (ran: apply completed and the state was empty).
- On replacement they run for the **old** object being destroyed, but not when the resource uses `create_before_destroy` (Terraform provisioners doc; ran: nothing logged) and not for tainted objects (doc, not run (gated: unconfirmed, source is paywalled or blocked)).
- They never run when the removed block has `destroy = false` (ran: apply forgot the object, `Some objects will no longer be managed by Terraform`, and the provisioner did not run).

## Verify
- [ ] Plan shows `- destroy` for the resource; apply output shows `Provisioning with 'local-exec'... (destroy)`.
- [ ] The side effect (deregistration) happened.

## Checked
- Terraform 1.17.0, local-exec on Windows (cmd), `terraform_data` with `for_each`: the removed-block provisioner ran once per instance with `self.input`; reference restrictions, `when`, index, `on_failure`, `destroy = false`, replacement and create_before_destroy behaviours as quoted. The 1.9 introduction is in the changelog (`removed` blocks can now declare destroy-time provisioners).
- Gated: remote-exec/SSH `connection`, tainted-object behaviour, and the AWS deregistration example.
