---
id: computing-software.cloud-infrastructure-engineering.terraform.sentinel-tfconfig-and-tfstate-imports
name: sentinel-tfconfig-and-tfstate-imports
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, tfconfig-v2, tfstate-v2, sentinel, policy-as-code, hcp-terraform]
level: practitioner
status: docs-checked
description: "Write Sentinel policies with tfconfig/v2 (module sources, provider configs, variables) and tfstate/v2 (existing resources), and know when to use them instead of tfplan/v2."
sources: ["https://developer.hashicorp.com/terraform/cloud-docs/policy-enforcement/import-reference/tfconfig-v2", "https://developer.hashicorp.com/terraform/cloud-docs/policy-enforcement/import-reference/tfstate-v2", "https://developer.hashicorp.com/sentinel/docs/imports/strings", "https://developer.hashicorp.com/terraform/cloud-docs/policy-enforcement/test/sentinel"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sentinel `tfconfig/v2` and `tfstate/v2`

| Import | Data | Use for |
|---|---|---|
| `tfplan/v2` | planned changes and values | most resource attribute rules |
| `tfconfig/v2` | the configuration (`*.tf` files): providers, resources, data sources, modules, variables, outputs | rules about **code**: naming conventions, required inputs/outputs, allowed modules, providers or resources |
| `tfstate/v2` | state recorded before the plan | what already exists; `planned_values` in `tfplan/v2` is often more useful because policy checks run at plan time |

Both imports are loaded by path with an alias, for example `import "tfconfig/v2" as tfconfig`, and need Terraform 0.12 or later.

## Only private-registry modules, pinned
`module_calls` is indexed by `module_address:name` (the module address and colon are omitted for the root module); each entry has `source` and `version_constraint`.
```python
import "tfconfig/v2" as tfconfig
import "strings"

module_calls = tfconfig.module_calls

allowed = rule {
  all module_calls as _, mc {
    strings.has_prefix(mc.source, "app.terraform.io/corp/") and
    mc.version_constraint is not ""
  }
}
main = rule { allowed }
```
(`app.terraform.io/corp/` is an example prefix.)

## No hard-coded provider credentials
`providers` is indexed by `[module_address:]provider[.alias]`; each entry has `name`, `alias`, `config` and `version_constraint`.
```python
import "tfconfig/v2" as tfconfig
no_static_keys = rule {
  all tfconfig.providers as _, p {
    p.name is not "aws" or
    ("access_key" not in keys(p.config) and "secret_key" not in keys(p.config))
  }
}
main = rule { no_static_keys }
```
`p.config` is a block expression representation: a map keyed by attribute, each value holding `constant_value` and/or `references`. This rule flags the presence of the argument at all, not whether it is a literal.

## tfstate/v2 example: limit total instances
```python
import "tfstate/v2" as tfstate
instances = filter tfstate.resources as _, r { r.type is "aws_instance" and r.mode is "managed" }
main = rule { length(instances) <= 50 }
```
`tfstate.resources` is indexed by address (fields include `mode`, `type`, `values`, `tainted`, `deposed_key`); `tfstate.outputs` holds root-module outputs only. Data sources always give up-to-date data here when they could be evaluated at plan time.

## Testing
Download Sentinel mocks from the run page (see the mock page). The bundle contains `mock-tfconfig-v2.sentinel` and `mock-tfstate-v2.sentinel`; reference them in a `mock "tfconfig/v2"` or `mock "tfstate/v2"` block in each `test/<policy>/*.hcl` file and run `sentinel test`.

## Gotchas
- tfconfig shows **expressions**, not evaluated values: a constant appears as `constant_value`, anything needing evaluation appears only as `references`, and partly constant strings such as `"foo${var.bar}"` lose their constant part.
- tfconfig addresses are pre-expansion: a resource using `count` has one `module.bar.null_resource.foo` entry there, versus `[0]`, `[1]` entries in `tfplan/v2` and `tfstate/v2`. Use `tfconfig.strip_index(rc.address)` to look up config from a plan address.
- `module_calls` covers declarations at all levels, so nested modules are included; `source` is the contents of the source field.

## Checked
Date: 2026-11-07. Read in full: tfconfig/v2 import reference (overview, address differences, strip_index, expression representations, providers, resources, variables, outputs, module_calls), tfstate/v2 import reference, Sentinel strings import (`has_prefix`) and the mock page. The Sentinel language spec was only searched for `keys`, `in`, `not in` and `filter`. Removed: the earlier claim that local `./` module sources "need allowing explicitly" and the Verify checklist (not stated by these pages); dropped the Sentinel language source (the page read does not mention these functions). The `app.terraform.io/corp/` prefix and the 50-instance limit are illustrative values.
Method: documentation only; no commands were run.
