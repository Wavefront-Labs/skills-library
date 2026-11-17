---
id: computing-software.cloud-infrastructure-engineering.terraform.rendering-cloud-init-with-templatefile
name: rendering-cloud-init-with-templatefile
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, cloud-init-template, templatefile, cloud-init, user-data, yamlencode]
level: practitioner
status: gated
description: "Render cloud-init user data with templatefile or yamlencode, combine multipart parts with the cloudinit provider, base64 handling, size limits and replacement behaviour."
sources: ["https://developer.hashicorp.com/terraform/language/functions/templatefile", "https://registry.terraform.io/providers/hashicorp/cloudinit/latest/docs/data-sources/config", "https://cloudinit.readthedocs.io/en/latest/reference/examples.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cloud-init with templatefile

## Prefer yamlencode for #cloud-config
```hcl
locals {
  cloud_config = "#cloud-config\n${yamlencode({
    package_update = true
    packages       = ["nginx", "jq"]
    write_files = [{
      path        = "/etc/app/config.json"
      permissions = "0640"
      content     = jsonencode({ db_host = aws_db_instance.db.address, env = var.env })
    }]
    runcmd = [["systemctl", "enable", "--now", "nginx"]]
  })}"
}
resource "aws_instance" "web" {
  user_data                   = local.cloud_config
  user_data_replace_on_change = true
}
```
yamlencode guarantees valid YAML and quoting; the `#cloud-config` header line must be first.
Rendered with `local` values on Terraform 1.17.0, the result starts `#cloud-config` and yamlencode quotes every key
(`"package_update": true`, `"packages":` with `- "nginx"`, nested runcmd as `- - "systemctl"`), and the `jsonencode` content is a quoted string with escaped inner quotes; PyYAML parsed it back to the original structure.

## templatefile for shell scripts
```hcl
user_data = templatefile("${path.module}/templates/bootstrap.sh.tftpl", {
  env      = var.env
  packages = ["nginx", "jq"]
})
```
```bash
#!/bin/bash
set -euo pipefail
ENV="${env}"
%{ for p in packages ~}
apt-get install -y ${p}
%{ endfor ~}
echo "done: $${HOSTNAME}"      # $${...} escapes for shell variables
```
Rendered with `env = "prod"`, `packages = ["nginx","jq"]`: `ENV="prod"`, one `apt-get install -y` line per package (the `~` strips the
newline after each directive, so no blank lines), and `echo "done: ${HOSTNAME}"` with the escape resolved.

## Multipart (script + cloud-config)
```hcl
data "cloudinit_config" "web" {
  gzip          = true
  base64_encode = true
  part {
    content_type = "text/cloud-config"
    content      = local.cloud_config
  }
  part {
    content_type = "text/x-shellscript"
    content      = file("${path.module}/scripts/extra.sh")
  }
}
resource "aws_launch_template" "web" {
  user_data = data.cloudinit_config.web.rendered     # launch templates need base64
}
```
`data.cloudinit_config` comes from the `hashicorp/cloudinit` provider (v2.4.1 was installed); with `gzip = false` and `base64_encode = false` the
`rendered` value is a `Content-Type: multipart/mixed; boundary="MIMEBOUNDARY"` MIME document with each part's `Content-Type`; with both true it is a
base64 string (448 characters for the two small parts above).

## Gotchas
- `aws_instance.user_data` takes plain text; `aws_launch_template.user_data` needs base64
  (`base64encode()` or `base64_encode = true`). Wrong choice = cloud-init ignores it.
- Size limit 16 KB (AWS) before base64; gzip helps.
- Changing user_data updates in place by default (runs only at first boot);
  `user_data_replace_on_change = true` forces replacement.
- Secrets in user_data are visible in the console/metadata; fetch at boot instead.

## Verify
- [ ] `cloud-init status --long` and `/var/log/cloud-init-output.log` show success on a test instance.

## Checked
- Terraform 1.17.0 with `hashicorp/cloudinit` 2.4.1: the `local.cloud_config` string, the `templatefile` template with `%{ for ... ~}` and `$${HOSTNAME}`, and the `cloudinit_config` data source (both gzip/base64 on and off) were all run; the YAML was parsed with PyYAML 6.0.3.
- AWS parts were not run: `aws_instance`/`aws_launch_template` `user_data` text versus base64 behaviour, the 16 KB limit, `user_data_replace_on_change`, in-place update on change, secrets visibility in metadata, and the `cloud-init status --long` check (gated: unconfirmed, source is paywalled or blocked). The reason is that no AWS account or cloud-init host was available. `aws_db_instance.db.address` is illustrative.
