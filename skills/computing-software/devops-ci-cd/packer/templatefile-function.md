---
id: computing-software.devops-ci-cd.packer.templatefile-function
name: templatefile-function
category: computing-software
field: devops-ci-cd
product: packer
tags: [templatefile, pkrtpl, function, rendering, fn-templatefile]
level: practitioner
status: docs-checked
description: "Render a template file with variables using templatefile(path, vars) and the .pkrtpl.hcl convention."
sources:
  - "https://developer.hashicorp.com/packer/docs/templates/hcl_templates/functions/file/templatefile/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`templatefile(path, vars)` reads the file at `path` and renders its content as a template using the supplied template variables.

```hcl
provisioner "file" {
  content     = templatefile("${path.root}/conf.pkrtpl.hcl", { port = 8080, ip_addrs = var.hosts })
  destination = "/tmp/app.conf"
}
```

Inside the file, interpolation uses `${ ... }` and directives use `%{ ... }`, the same syntax as HCL2 string templates:

```text
%{ for addr in ip_addrs ~}
backend ${addr}:${port}
%{ endfor ~}
```

Rules from the docs:

- Use the `.pkrtpl.hcl` extension by convention. Packer treats HCL templates as a combination of file and template, so they have a slightly different feature set from `.pkr.hcl` templates, and the extension lets syntax highlighters understand the file.
- `vars` must be a map. Each key becomes a variable in the template; names start with a letter, followed by letters, digits or underscores.
- The template may use any other Packer function, but recursive calls to `templatefile` are not permitted.
- The file is read as UTF-8; invalid UTF-8 produces an error.
- It works only with files that already exist on disk at the beginning of a run.
- To generate JSON or YAML, write a template consisting of one interpolated `jsonencode(...)` or `yamlencode(...)` call rather than many interpolations; for small results call them inline in a local.

The `file` provisioner's `content` option accepts `templatefile` output, so generated configuration can be deployed without writing a temp file first.

## Checked

Method: docs-checked 2026-11-09 against the Packer templatefile function page and the file provisioner page (both read in full as published page source). Dropped the claim that `var.*` is invisible in templates and the render-once-into-a-local advice, which are not in the pages.
