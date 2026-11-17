---
id: computing-software.cloud-infrastructure-engineering.terraform.templatefile-and-heredoc-rendering
name: templatefile-and-heredoc-rendering
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, templatefile, heredoc, template-rendering, user-data, cloud-init, string-templates, jsonencode, yamlencode, indent, directives, tftpl]
level: practitioner
status: verified
description: "Render user-data and config files with templatefile() and heredocs: %{for}/%{if} directives, whitespace trimming, escaping ${ and %{, indent(), and when jsonencode/yamlencode beat a template."
sources: ["https://developer.hashicorp.com/terraform/language/functions/templatefile", "https://developer.hashicorp.com/terraform/language/expressions/strings", "https://developer.hashicorp.com/terraform/language/functions/indent"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# templatefile and heredoc rendering

**Goal:** generate multi-line text (cloud-init, nginx config, IAM policies, Kubernetes
manifests) from Terraform values without string-concatenation soup, and without
Terraform mangling the result.

## 1. Heredocs
```hcl
user_data = <<-EOT
  #!/bin/bash
  echo "env=${var.environment}" >> /etc/app.env
  %{ if var.enable_agent ~}
  systemctl enable --now agent
  %{ endif ~}
EOT
```
- `<<EOT` keeps leading whitespace literally; `<<-EOT` strips the common leading
  indentation of the content lines (the closing marker's own indentation is not counted:
  content indented 2 with `EOT` at column 0 still loses 2 spaces; checked).
- Caution with `<<-` plus `~`: literal text after a directive that ends in `~` keeps its
  original indentation (in the example above `systemctl enable --now agent` rendered with
  2 leading spaces on 1.9.8), so do not rely on dedent being uniform around directives.
- Interpolation `${...}` and directives `%{...}` work inside heredocs; `~` on either
  side of a directive strips adjacent whitespace/newlines.
- Literal `${` or `%{`: write `$${` and `%%{` (needed for shell `${VAR}` and Helm/Go
  templates).

## 2. `templatefile(path, vars)`
```hcl
user_data = templatefile("${path.module}/templates/cloud-init.yaml.tftpl", {
  hostname = local.name
  packages = var.packages
  users    = var.users          # list(object)
})
```
`templates/cloud-init.yaml.tftpl`:
```yaml
#cloud-config
hostname: ${hostname}
packages:
%{ for p in packages ~}
  - ${p}
%{ endfor ~}
users:
%{ for u in users ~}
  - name: ${u.name}
    ssh_authorized_keys: ${jsonencode(u.keys)}
%{ endfor ~}
```
- Only the variables in the map are visible inside the template; `var.`, `local.`,
  `path.module` are **not**. Pass everything explicitly.
- Template functions available: all built-in functions except `templatefile` itself.
- `.tftpl` is the conventional extension (editor support, `terraform fmt` ignores it).
- Always use `${path.module}`; a bare relative path resolves against the root
  working directory and breaks when the module is reused.

## 3. Directive cheatsheet
```
%{ if cond }...%{ else }...%{ endif }
%{ for k, v in map }...%{ endfor }
%{ for i, x in list }...%{ endfor }      # index available
```
Trim markers: `%{~ if x }` strips whitespace before, `%{ if x ~}` after. Without
them each directive line leaves a blank line in the output — harmless for shell,
fatal for YAML indentation.

## 4. Structured output: do not template it
For JSON/YAML, build the value in HCL and encode it; the output is always valid,
quoting is handled, and `terraform plan` diffs are readable:
```hcl
policy = jsonencode({
  Version   = "2012-10-17"
  Statement = [for b in var.buckets : {
    Effect = "Allow", Action = ["s3:GetObject"], Resource = "arn:aws:s3:::${b}/*"
  }]
})
content = yamlencode({ apiVersion = "v1", kind = "ConfigMap", data = var.data })
```
Template only when the target format is not JSON/YAML (shell, nginx, systemd, ini)
or when you need comments/exact layout. Mixing: render a template and embed
`jsonencode(...)` for the parts that are structured.

## 5. Indentation inside other text
```hcl
containers = <<-EOT
  spec:
    containers:
      ${indent(4, yamlencode(local.containers))}
  EOT
```
`indent(n, str)` indents every line **except the first**; place the interpolation
where the first line should already be at the correct column. This renders valid YAML
(`yamldecode` of the result gives `spec.containers[0] = {image, name}`).

## Gotchas
- On `aws_instance`, a `user_data` change stops and restarts the instance by default and
  replaces it only with `user_data_replace_on_change = true` (AWS provider docs); other
  clouds differ. A template whose output changes with `timestamp()` produces a diff on every
  apply. Maps iterate in key order (deterministic), lists in order; avoid `timestamp()` in templates.
- `templatefile` reads the file at plan time; a template error reports the line in
  the `.tftpl`, not the `.tf`.
- Size limits: EC2 user data is limited to 16 KB raw, before base64 (EC2 user guide); use `base64gzip()` for larger scripts
  with `user_data_base64`, or pull the script from S3.
- `%{ for k, v in x }` works over both objects and maps (keys in lexical order: `{ b = 1, a = 2 }` renders `a=2` then `b=1`); over a list `k` is the index.
- Windows line endings in a `.tftpl` reach the rendered output; `.gitattributes`
  with `*.tftpl text eol=lf`.
- The heredoc closing marker may be indented with `<<-`; trailing spaces after `EOT` were accepted by `terraform validate` on 1.9.8.

## Verify
- [ ] `terraform console` → `templatefile("templates/x.tftpl", {...})` prints the expected text with no stray blank lines.
- [ ] Rendered YAML passes `yamllint`/`kubectl apply --dry-run=client`; rendered JSON passes `jq .`.
- [ ] A second `terraform plan` after apply shows no `user_data` diff.
