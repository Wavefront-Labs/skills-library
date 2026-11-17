---
id: computing-software.devops-ci-cd.packer.variable-values
name: variable-values
category: computing-software
field: devops-ci-cd
product: packer
tags: [var-file, pkrvars, environment-variable, precedence, variables-input]
level: practitioner
status: docs-checked
description: "Pass variable values with -var, -var-file, auto.pkrvars.hcl files and PKR_VAR_ environment variables."
sources:
  - "https://developer.hashicorp.com/packer/docs/templates/hcl_templates/variables/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Values for declared input variables can be set several ways. You cannot change the value of an input variable after the initial override.

```bash
packer build -var="image_id=ami-abc123" -var-file="testing.pkrvars.hcl" .
export PKR_VAR_image_id=ami-abc123
```

Sources:

- `-var name=value` on the command line, usable any number of times.
- `-var-file` pointing at a variable definitions file whose name ends in `.pkrvars.hcl` or `.pkrvars.json`. It uses HCL syntax and only holds names and assigned values.
- Files ending in `.auto.pkrvars.hcl` or `.auto.pkrvars.json` are loaded automatically. Names ending `.json` are parsed as JSON objects whose root properties are variable names.
- Environment variables named `PKR_VAR_` followed by the declared variable name; the name is matched exactly as written in the configuration, so case matters on case-sensitive systems.
- The `default` in the `variable` block, if present.

Precedence, later wins:

1. Environment variables (lowest)
2. `*.auto.pkrvars.hcl` and `*.auto.pkrvars.json` files, in lexical filename order
3. `-var` and `-var-file` options, in the order given (highest)

The same variable cannot get multiple values within a single source. Map and object values behave like any other: the last value found replaces the earlier one.

Complex values: in a variable definitions file use normal HCL syntax (lists, maps). `-var` and env values default to literal strings needing no quotes, but if the variable has a type constraint of list, set, map, object or tuple, Packer parses the value with the definitions-file syntax, for example `export PKR_VAR_availability_zone_names='["us-west-1b","us-west-1d"]'`. The docs recommend setting complex values through definitions files to avoid shell escaping.

Variables used in a definitions file must be declared in a `*.pkr.hcl` template first, otherwise Packer reports an unknown variable. Behaviour for undeclared variables:

- `bar=yz` in a `.pkrvars.hcl` file: error with `packer validate`, warning with other commands.
- `var.bar` in a template or `-var bar=yz` on the command line: error with all commands.
- `PKR_VAR_bar` set but not declared: no error.

If a variable has no default and no value, Packer errors with "needs to be set".

## Checked

Method: docs-checked 2026-11-09 against the Packer Input variables page and the included assignment and must-be-set sections (read in full as published page source). Dropped the claims about packer init skipping var files, the -warn-on-undeclared-var flag and the secrets-via-CI advice.
