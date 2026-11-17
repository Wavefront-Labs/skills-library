---
id: computing-software.devops-ci-cd.semaphore-ui.survey-variables
name: survey-variables
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [survey-variables, extra-vars, task-parameters, templates, input, semaphore-ui]
level: practitioner
status: docs-checked
description: "Add custom input fields to a template with survey variables of six types, passed as extra vars or environment."
sources:
  - https://semaphoreui.com/docs/user-guide/task-templates/survey-vars
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Survey variables

Goal: collect values from the person starting a task instead of hard-coding them.

Survey variables are custom fields you define; prompts are predefined template options (Ansible `--limit`, `--tags`, Terraform workspaces). Survey values pass as Ansible `--extra-vars` (a temporary YAML file, every value a quoted string) or Terraform `-var`, and shell apps get `name=value` command-line arguments. Schedules and integrations (via extractors) can also supply values.

Add: Task Templates, select the template, Survey Variables section, Add Survey Variable, then set:
- Name: the variable name used in code.
- Title: label shown in the form.
- Type.
- Pass variable as: extra variable (default) or environment variable.
- Default value (optional, pre-filled) and Required.

Types (six): String, Integer, Text (multiline), Enum (dropdown, exactly one option, each with label and value), Select (multi-select, delivered as a JSON array such as `["staging","production"]`) and Secret (hidden input; in Ansible it reaches the playbook in a Vault-encrypted file).

Example: a String named `environment` prompts the user to type production, staging or development; an Enum named `deployment_type` offers rolling, blue-green, canary.

```yaml
- debug:
    msg: "Deploying to {{ environment }}"
```

Environment-variable target: the value is set as a process environment variable with the variable's name and is not duplicated in extra-vars, `-var` or arguments. To feed Terraform a `TF_VAR_` input, name the survey variable `TF_VAR_instance_type` and pick the environment target.

Gotchas:
- Use the environment target only when the script or tool reads the process environment.
- Validate values in your code; the page recommends an `assert` in playbooks.

## Checked

2026-11-07. Read in full: the Survey variables page (user-guide/task-templates/survey-vars.md in the semaphore-docs repository, including its code examples). Confirmed: add steps and fields, six types, Select as JSON array, Secret via Ansible Vault, Pass variable as, defaults, delivery per app, schedules and integrations as sources. Removed: "API calls" as a value source (that section is commented out in the page), "Required fields block the launch; the API must supply them", the claim that the example String offers fixed choices (the page says the user enters the value), and the invented Verify step.
Method: documentation only; no commands were run.
