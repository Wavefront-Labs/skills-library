---
id: computing-software.cloud-infrastructure-engineering.ansible.workflow-surveys-and-prompted-extra-vars
name: workflow-surveys-and-prompted-extra-vars
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, automation-controller, awx, workflow-templates, workflow-survey, workflow-extra-vars, prompt-on-launch, set-stats, artifacts, variable-precedence]
level: advanced
status: docs-checked
description: "Collect input once with a workflow survey or prompted extra vars and flow it to every node: precedence, artifacts from set_stats, and the prompt settings nodes need."
sources: ["https://raw.githubusercontent.com/ansible/aap-docs/main/downstream/modules/platform/ref-controller-workflows-extra-variables.adoc", "https://raw.githubusercontent.com/ansible/aap-docs/main/downstream/modules/platform/ref-controller-extra-variables.adoc", "https://raw.githubusercontent.com/ansible/aap-docs/main/downstream/modules/platform/con-controller-workflow-job-surveys.adoc", "https://raw.githubusercontent.com/ansible/aap-docs/main/downstream/modules/platform/con-controller-workflow-scenarios.adoc", "https://raw.githubusercontent.com/ansible/awx/devel/docs/workflow.md", "https://raw.githubusercontent.com/ansible/awx/devel/awx_collection/plugins/modules/workflow_job_template.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Workflow surveys and prompted extra vars

Goal: an operator answers "which app, which version, which environment" once when launching the
workflow, and the jobs in it receive the same answers.

## Workflow survey
Workflows containing job types Run or Check can have a survey on the workflow job template, with the
same question types as job templates. Survey variables are combined with the workflow template's
`extra_vars` and saved to the workflow job's `extra_vars`; those are then combined with each spawned
job template's variables.
```yaml
- ansible.controller.workflow_job_template:
    name: Release app
    organization: Apps
    survey_enabled: true
    survey_spec: "{{ lookup('file', 'release_survey.json') }}"
    ask_variables_on_launch: false
```
The module's `survey_spec` is a dict whose JSON format is in the controller API documentation.
`ask_variables_on_launch: true` allows extra variables to be supplied at launch.

## Precedence
Workflows follow the job template precedence hierarchy plus three levels (last listed wins):
workflow job template extra variables, workflow job template survey defaults, workflow job launch extra variables.
These sit above the job template's own extra variables, survey defaults and launch variables,
so a workflow value overrides a same-named variable in the node's template. Nested workflows only
inherit variables that they prompt for or define in their own survey.

## Passing data forward with artifacts
```yaml
# playbook in node 1
- ansible.builtin.set_stats:
    data: {build_id: "{{ result.build_id }}"}
    per_host: false
```
Jobs and workflows in a workflow can inherit the `artifacts` of a parent job, combined with ancestors
further upstream on the branch; a nearer ancestor overrides a farther one, and cumulative artifacts can overwrite
the workflow `extra_vars` before they are applied. Keep the default `per_host: false`.
At a convergence node `set_stats` data merges in an undefined way, so use unique keys. Artifacts
from a sub-workflow pass to downstream nodes. Do not reuse survey variable names for artifacts.

## Node-level prompts
A node can carry launch configuration for its job. A prompt only takes effect if the node's job
template allows it (`ask_*_on_launch`); otherwise it is ignored and the template default is used.
When the workflow job and the node specify the same prompt, the workflow job's value wins.
Job templates with `ask_inventory_on_launch=true` use the workflow-level inventory; others use their own.

## Gotchas
- API-launched `extra_vars` are honoured only if they correspond to variables in an enabled survey or `ask_variables_on_launch` is true.
- Survey answers pass as extra vars and can override inventory variables; redefine any variable you must keep in the survey.

## Verify
- [ ] Each node job's details show the survey answer as an extra variable.
- [ ] A node template with a conflicting default still receives the workflow answer.

## Checked

- Date: 2026-11-09. Sources: ansible/aap-docs main (workflow extra variables, extra variables, workflow surveys, workflow scenarios), ansible/awx devel docs/workflow.md and workflow_job_template.py.
- Confirmed: survey support on workflows, combination of survey and template extra_vars, the three added precedence levels, nested workflow inheritance rule, artifacts inheritance and overwrite order, `per_host` setting, unique keys at convergence, node prompt rules, inventory prompt behaviour, API extra_vars restriction, `survey_spec` as a dict.
- Removed unconfirmed claims: the survey_spec example body and sample questions, the three-step precedence list placing artifacts below workflow vars with no qualification, password answers shown as `$encrypted$` in workflow jobs, text min/max being length limits for workflows specifically, nested workflows receiving all parent vars, relaunch reusing answers.

Method: documentation and collection source read from cloned repositories; no commands were run against a controller.
