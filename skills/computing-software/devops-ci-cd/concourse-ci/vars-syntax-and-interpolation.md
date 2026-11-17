---
id: computing-software.devops-ci-cd.concourse-ci.vars-syntax-and-interpolation
name: vars-syntax-and-interpolation
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [vars, syntax, interpolation, local-var, credential-manager, yaml-merge, templating]
level: practitioner
status: docs-checked
description: "Read and write ((var)) syntax: source, path and field, quoting special characters, local vars, and interpolation rules including the YAML merge trap."
sources:
  - https://concourse-ci.org/docs/vars/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Vars substitute values into YAML config with `((vars))`, keeping credentials out of source control and allowing generic templating such as `((branch_name))`.

**Syntax.** `((source-name:secret-path.secret-field))`.
- `source-name` is optional. If omitted (with the colon), the cluster-wide credential manager is used, or a static value. The name `.` is the local var source; any other name is a var source defined in the pipeline.
- `secret-path` is required and its meaning depends on the source. For Vault, `foo` is looked up under `/concourse/(team name)/(pipeline name)/foo`. For Kubernetes, it is a secret name.
- `secret-field` is optional; managers may read a default field. Vault returns the `value` field if present, so `((foo))` works for simple credentials.
- Quote parts containing `.` or `:`: `((source:"my.secret"."field:1"))` has path `my.secret` and field `field:1`.

**Local vars (`.`)** come from three mechanisms: a `load_var` step (available to later steps in the build), an `across` modifier (only inside that step), and a `get` step (a var named after the step holding the resource metadata).

**Interpolation is structural.** `foo: ((bar))` puts whatever `((bar))` resolves to into the field: a bool, a string, a multi-line certificate or a nested structure, so a value cannot break YAML syntax. When adjacent to other text, as in `hello-((bar))-goodbye`, it is concatenated, and a non-string value raises an error. To merge with the YAML `<<` operator, quote it: `"<<": ((foobars))`, otherwise you get a cryptic "map merge requires map" error.

## Checked

Checked 2026-11-09 against the raw docs source of the Vars page (read in full): syntax, quoting, local var sources and interpolation rules all match.

Method: docs-checked 2026-11-09 against concourse docs vars page (github.com/concourse/docs source); documentation only, no commands were run.
