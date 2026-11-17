---
id: computing-software.cloud-infrastructure-engineering.terraform.file-provisioner-connection-blocks-and-bastion-ssh
name: file-provisioner-connection-blocks-and-bastion-ssh
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, file-provisioner, connection-block, bastion-host, ssh-connection, remote-exec, winrm]
level: practitioner
status: docs-checked
description: "Write connection blocks for file and remote-exec provisioners over SSH (keys, agent, host keys) and through a bastion host, plus WinRM basics."
sources: ["https://developer.hashicorp.com/terraform/language/provisioners", "https://developer.hashicorp.com/terraform/language/block/resource"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `file` provisioner, `connection`, and bastions

HashiCorp strongly recommends purpose-built solutions (images, configuration
management) over provisioners; use them only when nothing else works.

## Connection block
```hcl
resource "aws_instance" "app" {
  # ...
  connection {
    type        = "ssh"
    host        = self.private_ip          # use self.*, never aws_instance.app.* (cycle)
    user        = "ubuntu"
    private_key = file(var.ssh_key_path)   # contents of the key, not a path
    host_key    = var.app_host_key         # optional: verify against a specific key or CA
    timeout     = "5m"

    bastion_host        = var.bastion_public_ip
    bastion_user        = "ec2-user"
    bastion_private_key = file(var.bastion_key_path)
  }

  provisioner "file" {
    source      = "${path.module}/files/app.conf"
    destination = "/tmp/app.conf"
  }
  provisioner "file" {
    content     = templatefile("${path.module}/env.tftpl", { db = var.db_host })
    destination = "/tmp/app.env"
  }
  provisioner "remote-exec" {
    inline = [
      "sudo install -m 0640 /tmp/app.conf /etc/app/app.conf",
    ]
  }
}
```
- A `connection` block in the resource sets defaults for all its provisioners; inside
  a provisioner it is specific to that provisioner.
- Terraform does not validate SSH host keys by default; set `host_key` (or
  `bastion_host_key` for the bastion) to verify.
- `type` is `ssh` (default) or `winrm`; `host` is required. SSH defaults: user `root`,
  port 22, `timeout` `"5m"`. `private_key` takes precedence over `password`.
- Bastion: `bastion_host` is the bastion's address; the provisioner connects to it
  before `host`. `bastion_port`, `bastion_user`, `bastion_password`,
  `bastion_private_key` and `bastion_certificate` default to the corresponding
  non-bastion values (`port`, `user`, ...). Proxies use `proxy_scheme` (`http`,
  `https`, `socks5`), `proxy_host`, `proxy_port`, `proxy_user_name`,
  `proxy_user_password`.
- Uploads over SSH need the `scp` program installed on the remote system.

## SSH agent
`agent` is documented as "Set to false to disable using ssh-agent", with a default of
`false`; `agent_identity` picks a preferred identity. On Windows the only supported
agent is Pageant. Check the reference before relying on agent behaviour.

## File provisioner rules
- Use `source` or `content`, never both. With `content` and a directory as
  `destination`, Terraform creates a file named `tf-file-content` inside it.
- A `source` directory with a trailing slash copies the directory's contents; without
  it, the directory itself is created under `destination`.
- Over SSH with a directory `source`, the destination directory must already exist
  (create it with a `remote-exec` provisioner). Over WinRM Terraform creates it.
- `destination` is passed as-is to the remote `scp`, which runs as the connection
  user in that user's home directory by default; permissions may stop writes outside
  the home directory.
- Windows: `type = "winrm"` (default port 5985); `https = true` uses HTTPS, `insecure`
  skips validating the HTTPS certificate chain. HashiCorp strongly recommends SSH
  (OpenSSH server) over WinRM on modern Windows.

## Gotchas
- Expressions in `connection` and `provisioner` blocks cannot refer to the parent
  resource by name; use `self`.
- A failed creation-time provisioner marks the resource tainted. `on_failure = continue`
  changes that; `when = destroy` runs a provisioner at destroy time.
- To run provisioners without a resource, or to re-run them, attach them to a
  `terraform_data` resource and use its `triggers_replace`.

## Checked
Date: 2026-11-07
Read in full: "Use provisioners to perform post-apply operations" (language/provisioners; the cited connection, file and remote-exec URLs all redirect to this page) and the resource block reference (language/block/resource), whose connection table and provisioner argument sections I read; I did not read the remote-exec/local-exec argument sections beyond the argument table.
Confirmed: connection table defaults and arguments, bastion/proxy arguments, host key behaviour, `self` rule, scp requirement, source/content/destination rules, WinRM behaviour, tainting and `on_failure`, `terraform_data` with `triggers_replace`.
Corrected: `agent` was claimed to default to true when SSH_AUTH_SOCK is set (the reference table says default false), now stated as documented; the MaxAuthTries claim, the "no sudo" claim, the `cloud-init status --wait` step, the TF_LOG debugging error strings, the TRACE-log key-leak claim and the Verify checklist were removed (not on the pages).
Method: documentation only; no commands were run.
