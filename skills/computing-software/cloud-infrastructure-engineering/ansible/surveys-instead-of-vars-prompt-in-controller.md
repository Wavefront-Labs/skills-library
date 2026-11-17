---
id: computing-software.cloud-infrastructure-engineering.ansible.surveys-instead-of-vars-prompt-in-controller
name: surveys-instead-of-vars-prompt-in-controller
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, prompts-interactive, prompt-vs-survey, surveys, job-templates]
level: practitioner
status: docs-checked
description: "Replace vars_prompt with automation controller surveys: map prompts to survey questions, answer types, required and optional answers, and keep playbooks validated."
sources: ["https://raw.githubusercontent.com/ansible/aap-docs/main/downstream/modules/platform/proc-controller-create-survey.adoc", "https://raw.githubusercontent.com/ansible/aap-docs/main/downstream/modules/platform/ref-controller-optional-survey-questions.adoc", "https://raw.githubusercontent.com/ansible/aap-docs/main/downstream/modules/platform/ref-controller-extra-variables.adoc", "https://raw.githubusercontent.com/ansible/aap-docs/main/downstream/modules/platform/ref-controller-file-directory-structure.adoc", "https://raw.githubusercontent.com/ansible/awx/devel/awx_collection/plugins/modules/job_template.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Surveys instead of vars_prompt

The controller does not permit interactive questions, so the documentation says to avoid `vars_prompt`
(it is listed as "not supported" in the controller variable precedence table). Surveys are the
controller-native replacement: they prompt at launch and set extra variables, with input validation.

## Mapping
| vars_prompt | Survey question |
|---|---|
| `name` | Answer variable name (no spaces) |
| `prompt` | Question (plus optional description) |
| `default` | Default answer (pre-filled and used if no answer given) |
| `private: true` | Answer type Password (treated as sensitive) |
| choice by convention | Multiple choice, single or multiple select (options one per line) |
| free text | Text (single line) or Textarea, with min and max length |
| numbers | Integer or Float |
| `confirm` | no survey equivalent; validate with `assert` |

Answer types: Text, Textarea, Password, Multiple Choice (single select), Multiple Choice (multiple select), Integer, Float.
Survey answers are passed as `extra_vars`, so they sit at the top of the controller's variable precedence
(after play-level and task variables: job template extra vars, then survey defaults, then job launch extra vars)
and can override inventory or project variables. To keep a variable from being overridden, do not reuse its name in a survey.

## Required and optional answers
- Non-text answer type, optional and left blank: no `extra_var` is passed.
- Text or textarea, optional, blank, minimum length above 0: no `extra_var` is passed.
- Text or textarea, optional, blank, minimum length 0: the variable is passed as an empty string.
So guard optional answers with `| default(...)` or `is defined`.

## Launch via API
`extra_vars` sent to the launch API are honoured only if they correspond to variables in an enabled
survey or the template has `ask_variables_on_launch` set to true.

## Dual-mode playbook
```yaml
- hosts: "{{ target | default('nobody') }}"
  pre_tasks:
    - ansible.builtin.assert:
        that:
          - release is defined
          - release is match('^v[0-9]+\.[0-9]+\.[0-9]+$')
        fail_msg: "release must look like v1.2.3"
      run_once: true
```
Run it on the command line with `-e release=v1.2.3` and from the controller with a survey variable `release`; the assert validates both.

## Survey as code
The module takes `survey_enabled` and a `survey_spec` dict; the spec's JSON format is in the controller API documentation (the shape below is illustrative).
```yaml
- ansible.controller.job_template:
    name: Deploy app
    survey_enabled: true
    survey_spec:
      name: deploy
      description: ""
      spec:
        - {question_name: Release tag, variable: release, type: text, required: true, min: 2, max: 20}
        - {question_name: Environment, variable: env, type: multiplechoice, choices: [staging, prod], default: staging, required: true}
```

## Gotchas
- Use `no_log` on tasks that handle password answers.
- Renaming a survey variable breaks anything that passes the old name (schedules, workflows, API callers).

## Verify
- [ ] Launch from the controller and from the CLI with `-e release=v1.2.3`; both pass the assert.

## Checked

- Date: 2026-11-09. Sources: ansible/aap-docs main (create a survey, optional survey questions, extra variables, file directory structure).
- Confirmed: no interactive prompts in the controller; vars_prompt unsupported; survey answer types and options, name rules, default behaviour; optional-answer rules; survey values passed as extra_vars and precedence list; API launch extra_vars restriction.
- Removed unconfirmed claims: vars_prompt/pause prompts silently skipped or taking defaults, answers encrypted in the database and masked in output, extra var suppressing a same-named vars_prompt, the exact `survey_spec` JSON shape (the module takes a dict and points to the API documentation for its format, so the example is illustrative), `min`/`max` being numeric limits for integers (the docs describe them as length in characters).

Method: documentation only; no commands were run.
