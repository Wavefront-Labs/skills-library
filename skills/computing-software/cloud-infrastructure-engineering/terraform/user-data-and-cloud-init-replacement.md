---
id: computing-software.cloud-infrastructure-engineering.terraform.user-data-and-cloud-init-replacement
name: user-data-and-cloud-init-replacement
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, user-data, user-data-replace-on-change, cloud-config, cloud-init, cloudinit-config, provisioners-alternative]
level: practitioner
status: docs-checked
description: "Bootstrap instances with user_data and cloud-config instead of provisioners: rendering, cloudinit_config multipart and user_data_replace_on_change."
sources: ["https://raw.githubusercontent.com/hashicorp/terraform-provider-aws/main/website/docs/r/instance.html.markdown", "https://raw.githubusercontent.com/hashicorp/terraform-provider-cloudinit/main/docs/data-sources/config.md", "https://cloudinit.readthedocs.io/en/latest/reference/examples.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# user_data and cloud-init

## Render a cloud-config
```hcl
data "cloudinit_config" "app" {
  gzip          = true
  base64_encode = true      # defaults for both are true; base64 cannot be disabled while gzip is true

  part {
    content_type = "text/cloud-config"
    content = "#cloud-config\n${yamlencode({
      package_update = true
      packages       = ["nginx"]
      write_files = [{
        path        = "/etc/app/app.env"
        permissions = "0640"
        content     = "DB_HOST=${var.db_host}\n"
      }]
      runcmd = [["systemctl", "enable", "--now", "nginx"]]
    })}"
  }
  part {
    content_type = "text/x-shellscript"
    content      = file("${path.module}/scripts/bootstrap.sh")
  }
}

resource "aws_instance" "app" {
  user_data_base64            = data.cloudinit_config.app.rendered
  user_data_replace_on_change = true
}
```
- `cloudinit_config` renders a multi-part MIME document; `part` blocks are included in order of declaration. `content_type` defaults to `text/plain`, so set it on every part. `filename` and `merge_type` (the `X-Merge-Type` header, see cloud-init merging) are optional.
- The cloud-init examples start with `#cloud-config`; the example above puts that line before the `yamlencode` output. `yamlencode` avoids indentation bugs of hand-written heredocs.
- Use `user_data_base64` for gzip or other binary data; the AWS provider says not to pass gzip-compressed data through `user_data`.

## Update behaviour (AWS)
- Changing `user_data` or `user_data_base64` triggers a **stop/start** of the instance by default.
- With `user_data_replace_on_change = true` the instance is destroyed and recreated instead. Pair with create-before-destroy or an ASG for availability.

## Gotchas
- Secrets in user data are readable through the instance metadata and console; fetch them at boot from a secret manager using the instance role.
- `templatefile` with `${}` inside shell scripts needs `$${VAR}` escaping.
- Check the current AWS user data size limit before embedding large scripts; fetch larger scripts from object storage instead.
- Inspect the rendered value with `terraform console` (`data.cloudinit_config.app.rendered`); it is base64 text when `base64_encode` is true.

## Verify
- [ ] On a fresh instance, cloud-init finished without errors (see the cloud-init documentation for the status and log commands for your distro).
- [ ] Changing the script shows the expected plan action (replace when `user_data_replace_on_change` is true).

## Checked
2026-10-28. Confirmed against the terraform-provider-cloudinit `cloudinit_config` docs (gzip and base64_encode defaults and constraint, `part` order, `content_type` default, `filename`, `merge_type`, `rendered`), the terraform-provider-aws `aws_instance` docs (`user_data`, `user_data_base64`, `user_data_replace_on_change` behaviour), and the cloud-init examples page (`#cloud-config` header, `write_files`, `packages`, `package_update`, `runcmd`, `permissions`).
Corrected: the claim that `cloudinit_config` adds the `#cloud-config` line (the docs do not say so; the example now writes it explicitly).
Removed: the 16 KB size figure, the "mixing user_data and user_data_base64 errors" claim, "runs only on first boot", Azure `custom_data` and GCE `metadata_startup_script` behaviour, launch-template behaviour, and the `cloud-init status --long`, `cloud-init schema --system` and log-path commands (not in the fetched pages).
Method: documentation only; no commands were run.
