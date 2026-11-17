---
id: computing-software.devops-ci-cd.packer.legacy-json-template
name: legacy-json-template
category: computing-software
field: devops-ci-cd
product: packer
tags: [json-template, legacy, user-variables, template-engine, json-templates]
level: intro
status: docs-checked
description: "Structure of legacy JSON templates: keys, user variables, the template engine and moving to HCL2."
sources:
  - "https://developer.hashicorp.com/packer/docs/templates/legacy_json_templates/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Legacy JSON templates are still read by Packer, but the docs carry a legacy warning and point to HCL2 (supported from Packer 1.6.0).

Top-level keys:

- `builders` (required), an array of builder definitions
- `description`, shown only by the inspect command
- `min_packer_version`; no maximum can be set
- `post-processors`
- `provisioners`
- `variables`
- `sensitive-variables`, a list of variable names whose values the UI and logs hide

```json
{
  "variables": { "region": "us-east-1", "secret": null },
  "builders": [{ "type": "null", "communicator": "none" }]
}
```

User variables: a `null` default means the variable is required, and validation fails if no value is given. Use them as {{user `region`}} in any value except `type`; set them with `-var` and `-var-file`. The `env` function (and `consul_key`) works only inside the default value of a user variable.

The template engine processes every string in `{{ }}`. Functions include `user`, `env`, `timestamp`, `isotime`, `uuid`, `clean_resource_name`, `build_name`, `build_type`, `build`, `lower`, `upper`, `replace`, `replace_all`, `split`, `pwd`, `template_dir` and `packer_version`. `timestamp` and `isotime` can differ slightly between plugins because they are evaluated when each plugin starts; set the value as a user variable for a consistent one. `clean_resource_name` does not truncate names or validate their start and end.

Comments: JSON has none, and unknown keys are validation errors. Only root-level keys may be underscore-prefixed, such as `_comment`.

Migration: `packer fix` updates backward-incompatible JSON templates and prints the result to standard output (redirect it to a file; `-validate=false` skips validation). `packer hcl2_upgrade` converts a JSON template to HCL2. `packer fmt` does not modify JSON files, and `packer init` does not support legacy JSON templates, so convert to HCL to use `required_plugins`.

## Checked

2026-11-09. Checked against the Packer v1.15 pages for JSON templates (configuration reference, template engine, user variables) and the `fix`, `fmt`, `init` and `hcl2_upgrade` command pages: key list and required flags, `null` defaults, `env` restriction, engine function names, timestamp caveat, comment rule, and command behaviour for JSON.

Removed: the unsupported statement that plugin installation for JSON templates is manual (the init page only says JSON is not supported).

Method: documentation only; no commands were run.
