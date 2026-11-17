---
id: computing-software.cloud-infrastructure-engineering.terraform.references-to-named-values-path-self-count-each
name: references-to-named-values-path-self-count-each
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, named-values, path-root, path-module, expressions, references]
level: practitioner
status: verified
description: "Use Terraform's named values correctly: path.module vs path.root vs path.cwd, self in provisioners and conditions, count and each contexts, terraform.workspace."
sources: ["https://developer.hashicorp.com/terraform/language/expressions/references"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Named values

| Reference | Meaning |
|---|---|
| `var.<name>` / `local.<name>` | input variable / local value |
| `<type>.<name>` | managed resource (`aws_vpc.main`) |
| `data.<type>.<name>` | data source |
| `module.<name>.<output>` | child module output |
| `ephemeral.<type>.<name>` | ephemeral resource (1.10+) |
| `path.module` | directory of the module containing the expression |
| `path.root` | directory of the root module |
| `path.cwd` | directory terraform was run from (absolute path; with `-chdir` it is the invocation directory, not the `-chdir` target) |
| `terraform.workspace` | current workspace name |
| `count.index` | in a `count` resource/module |
| `each.key` / `each.value` | in a `for_each` resource/module |
| `self` | the current resource, only in provisioner, connection and postcondition blocks |

## path.* rules
```hcl
templatefile("${path.module}/templates/user-data.sh.tftpl", {...})   # inside modules: always path.module
file("${path.root}/config/global.json")                               # root-level shared files
```
- Use `path.module` in modules; `path.root` breaks when the module is reused elsewhere.
- `path.module` and `path.root` are **relative** paths (a root-module expression gives `.`;
  a local child module `./mod` gives `mod`), while `path.cwd` is absolute
  (an absolute path, printed with forward slashes on Windows). Do not store them in resources (state then differs between
  machines); the Terraform docs also advise against `path.module` in write operations. Use
  `abspath()` only for local tooling (`abspath(path.module)` printed the absolute path).
- With `terraform -chdir=envs/prod`, `path.cwd` is where you invoked terraform, not `envs/prod`
  (`path.root` stayed `.`).

## self
```hcl
provisioner "remote-exec" {
  connection { host = self.public_ip }        # `self` is the supported way to name the resource here
}
lifecycle {
  postcondition {
    condition     = self.encrypted
    error_message = "Volume must be encrypted."
  }
}
```

## count/each availability
`count.index`, `each.*` exist only inside the block with that meta-argument (including
its nested blocks and `dynamic` content); elsewhere they fail validation (`Reference to
"each" in context without for_each`, `Reference to "count" in non-counted context`) and
you reference instances explicitly. `self` outside provisioner, connection and
postcondition blocks fails with `Invalid "self" reference`.

## Verify
- [ ] Modules reference their own files via `path.module`.
- [ ] No absolute paths end up in resource arguments or state.

## Checked
- Terraform 1.17.0 on Windows with a root `envs/prod` and a local module: `path.module` = `.` in the root and `mod` in the child, `path.root` = `.` in both, `path.cwd` = the absolute run directory; `terraform -chdir=envs/prod console` printed `path.cwd` as the directory the command was started in; `terraform.workspace` printed `default`; `self.input` in a `postcondition`, `self.id` in a local-exec provisioner worked; `self.id` in a plain argument, `each.key` without `for_each` and `count.index` without `count` produced the errors quoted. Referencing the resource by its own address inside its provisioner also applied without a cycle error in this version, so the old "(cycle)" warning was dropped.
- `ephemeral.<type>.<name>` references work from Terraform 1.10 (changelog); the reference table matches the Terraform "References to named values" page (fetched).
