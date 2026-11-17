---
id: computing-software.cloud-infrastructure-engineering.terraform.version-constraint-operators-for-modules-and-providers
name: version-constraint-operators-for-modules-and-providers
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, constraint-operators, pessimistic-constraint, tilde-constraint, module-provider-constraints, required-version, required-providers]
level: practitioner
status: verified
description: "Write version constraints (=, !=, >=, ~>) for Terraform, providers and registry modules; where to pin (root) vs where to set minimums (modules)."
sources: ["https://developer.hashicorp.com/terraform/language/expressions/version-constraints", "https://developer.hashicorp.com/terraform/language/modules/develop/providers#provider-version-constraints-in-modules"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Version constraints

## Operators
| Constraint | Meaning |
|---|---|
| `= 1.2.3` / `1.2.3` | exactly |
| `!= 1.2.4` | exclude a known-bad release |
| `>= 1.2`, `< 2.0` | ranges, comma = AND: `">= 1.2, < 2.0"` |
| `~> 1.2.3` | `>= 1.2.3, < 1.3.0` (rightmost component may increase) |
| `~> 1.2` | `>= 1.2, < 2.0` |
| `~> 1` | `>= 1.0, < 2.0` (run: `hashicorp/local` `~> 1` installed 1.4.0 although 2.9.1 exists) |
Prereleases are not matched by `>`, `>=`, `<`, `<=` or `~>`; to select one set the exact
version, with `=` or no operator (Terraform docs; no prerelease provider was available to run).

## Where to put what
**Reusable modules** — minimums only, plus an upper bound for known breaking majors:
```hcl
terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = { source = "hashicorp/aws", version = ">= 5.40, < 7.0" }
  }
}
```
Tight pins in modules make them impossible to combine (two modules pinning
different exact versions = unsatisfiable).

**Root modules** — pessimistic constraint; the **lock file** pins the exact version:
```hcl
terraform {
  required_version = "~> 1.9.0"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.70" }
  }
}
```

**Registry modules** in root:
```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.13"            # minors/patches; no automatic major
}
```
Module versions are **not** in the lock file (`init` of a module-only config created no
`.terraform.lock.hcl`) — the constraint is the only control;
pin exactly (`= 5.13.0`) if you need reproducibility and let Renovate bump it.

## Resolving
Terraform intersects all constraints across root and every module for each provider
(run: root `~> 2.5` plus child `< 2.6` installed 2.5.3). Error
`no available releases match the given constraints ~> 5.0` → find who asks for what:
`terraform providers` prints the tree with the constraint of each module.

## Gotchas
- `~> 5` (one component) is normalised to `~> 5.0` in the error message, i.e. any 5.x,
  not an unbounded `>= 5` (run: `~> 1` stayed on 1.4.0). Write `~> 5.0` to be explicit.
- `required_version` is checked before anything else; CI images must satisfy it.
- On 1.17.0, `required_version = "~> 1.9.0"`, `!= 1.17.0` and `< 1.17` failed with
  `Unsupported Terraform Core version`; `~> 1.9`, `~> 1`, `>= 1.2, < 2.0`, `1.17.0`,
  `= 1.17.0` and `~> 1.17.0` passed.

## Verify
- [ ] `terraform providers` shows no conflicting constraints.
- [ ] Modules use ranges: search `modules/` for `version = "` followed by a digit and review any exact pins.

## Checked
- Terraform 1.17.0 and the registry: `required_version` with `~> 1.9.0`, `~> 1.9`, `~> 1`, `>= 1.2, < 2.0`, `!= 1.17.0`, `1.17.0`, `= 1.17.0`, `~> 1.17.0`, `< 1.17`; provider constraints on `hashicorp/local` (`~> 1`, `~> 1.3`, `~> 2.5.0`, `~> 2.5`, range, `!=`, multiple `!=`, exact, `~> 5` error text) with the version list from registry.terraform.io; root + child provider constraint intersection and `terraform providers` tree; a registry module (`hashicorp/dir/template`) init produced no lock file.
- Version-constraints docs page: operator semantics, prerelease rule, reusable-module vs root-module advice. Correction: `~> 5` is bounded (any 5.x), not `>= 5`. Prerelease behaviour comes from the docs only (no prerelease available to run).
