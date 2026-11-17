---
id: computing-software.cloud-infrastructure-engineering.terraform.template-directives-strip-markers-and-escaping
name: template-directives-strip-markers-and-escaping
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, template-directives, template-for, strip-markers, indented-heredoc, template-escaping, templatefile, heredoc]
level: practitioner
status: verified
description: "Write templates with %{for}/%{if} directives, ~ strip markers and <<- indented heredocs, and escape $${ and %%{ for shell, Helm and other template languages."
sources: ["https://developer.hashicorp.com/terraform/language/expressions/strings#string-templates", "https://developer.hashicorp.com/terraform/language/expressions/strings#heredoc-strings", "https://developer.hashicorp.com/terraform/language/functions/templatefile"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Template directives, strip markers, escaping

## Directives
```
%{ for host in backends ~}
server ${host.name} ${host.ip}:${host.port} check
%{ endfor ~}
%{ if enable_tls ~}
ssl_certificate ${cert_path};
%{ else ~}
# TLS disabled
%{ endif ~}
```
Also `%{ for i, v in list }` (index) and `%{ for k, v in map }`.

## Strip markers `~`
`~` immediately inside a delimiter strips whitespace (including the newline) on that
side: `%{ for x in xs ~}` removes the newline after the directive; `${~ x}` strips
before and `${x ~}` after (`"a   ${~ "x" ~}   b"` renders `axb`). Without them, each directive line leaves a blank line in the output (`%{ for host in backends }...%{ endfor }` over two items renders `"\nserver a\n\nserver b\n\n"` as JSON).

## Heredocs
```hcl
locals {
  script = <<-EOT
    #!/bin/bash
    echo "env=${var.env}"
  EOT
}
```
`<<-` removes the common leading indentation (spaces) so heredocs can be indented in
HCL; `<<` keeps it verbatim. The closing marker may be indented with `<<-`.

## Escaping
| Want literally | Write |
|---|---|
| `${VAR}` (shell, Helm, CloudFormation) | `$${VAR}` |
| `%{` (e.g. printf, some DSLs) | `%%{` |
| `$VAR` (no brace) | `$VAR` — no escape needed |
A bash script through `templatefile`:
```bash
for f in $${FILES[@]}; do echo "$${f} -> ${bucket}"; done
```
Alternative: keep scripts free of Terraform syntax by using `file()` and passing
values via environment or a small `templatefile`-rendered config file.

## Gotchas
- `templatefile` variables must all be passed; a reference to an unpassed name errors
  (`vars map does not contain key`).
- Templates cannot call `templatefile` recursively ("cannot recursively call templatefile from inside another template function"); other functions are available, and `${file("x")}` inserts the file's text literally without evaluating its `${}`.
- Windows CRLF files keep `\r` (a CRLF template rendered with its `\r\n` intact); normalise line endings in `.gitattributes`.
- Rendering YAML by template is fragile; prefer `yamlencode()` of an HCL object.

## Verify
- [ ] `terraform console` → `templatefile("haproxy.cfg.tftpl", {...})` shows no stray blank lines.
- [ ] Rendered scripts pass `bash -n` / `shellcheck`.
