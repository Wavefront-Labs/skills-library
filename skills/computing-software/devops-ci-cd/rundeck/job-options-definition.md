---
id: computing-software.devops-ci-cd.rundeck.job-options-definition
name: job-options-definition
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, job-options, option-validation, required-option, multivalued-option]
level: practitioner
status: docs-checked
description: "Define Rundeck job options: types, input types, default and required behaviour, allowed values with enforced restrictions, regex validation and multi-valued delimiters."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/manual/jobs/job-options.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Options prompt the user (or API/CLI caller) for input. Reference them as `${option.NAME}` or `@option.NAME@`. Add them on a stored job's edit page via the options editor, or in a job definition (YAML or XML) loaded with `rd`.

Option types: Text, File (upload), Multiline Text.

Text option fields:
- Name: the variable name used in steps. Label: optional display name.
- Default Value: applied when none is given, even via CLI or API. Passing an explicit blank over the CLI or API overrides the default.
- Input Type: Plain, Date (momentjs format string), Plain Text with Password Input, Secure Remote Authentication. Non-Plain types disable multi-valued.
- Allowed values: comma separated list, or a remote URL returning values.
- Restrictions: "Enforced from values" true shows only a menu; false also shows a text field. "Match Regular Expression" is evaluated at run time.
- Required: Yes means the job fails on a blank or missing value. A default is used when nothing is provided, unless a blank is allowed and given explicitly.
- Multi-valued: user may select or enter several values; the Delimiter string joins them. "Select All Values by Default" applies when no default is set.

Gotcha: the `run` command does not prompt for required options, so pass them on the command line.

## Checked

2026-11-04: option types, text option fields, input types, restrictions, required and default behaviour, multi-valued fields, the run warning and the variable syntax confirmed against the Job Options page. Removed the unsourced Verify line.
Method: documentation only; no commands were run.
