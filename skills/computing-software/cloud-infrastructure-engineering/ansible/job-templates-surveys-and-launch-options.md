---
id: computing-software.cloud-infrastructure-engineering.ansible.job-templates-surveys-and-launch-options
name: job-templates-surveys-and-launch-options
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, awx, automation-controller, job-templates, job-template, surveys, survey-spec, extra-vars, prompt-on-launch, limit, job-tags, skip-tags, verbosity, forks, job-slicing, concurrent-jobs, timeout, diff-mode, check-mode-job, privilege-escalation, fact-storage, labels, webhooks, launch-api, ask-on-launch]
level: practitioner
status: docs-checked
description: "Build AWX/controller job templates safe to hand to others: fixed vs prompt-on-launch fields, surveys with validation and secrets, limit/tags, slicing, concurrency, timeouts."
sources: ["https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html-single/using_automation_execution/", "https://legacy-controller-docs.ansible.com/automation-controller/latest/html/controllercli/examples.html", "https://github.com/redhat-cop/infra.aap_configuration"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Job templates, surveys and launch options

**Goal:** a template is a product: a named, reviewed way to run one playbook with
guard rails, where the launcher can change only what you decided they may change.

## 1. The fields that matter
| Field | Choose |
|---|---|
| Job Type | `Run`; `Check` for a permanent dry-run twin of the same playbook (`ask_job_type_on_launch` lets one template do both) |
| Inventory / Project / Playbook / EE | fixed for prod; `Prompt on launch` only on dev/sandbox templates |
| Credentials | machine + vault + cloud; prompting lets the user pick any they can `Use` |
| Limit | leave blank + prompt on launch when operators need to target a subset; surveys can constrain it |
| Variables (`extra_vars`) | JSON/YAML; these are **highest precedence** and override vault/group vars |
| Forks / Timeout / Verbosity | forks 0 = controller default; timeout in seconds kills the job; verbosity 0-1 in prod |
| Job Slicing | split the inventory into N parallel jobs (creates a workflow); for independent hosts only |
| Options | Privilege Escalation (`become`), Provisioning Callbacks, Enable Webhook, Concurrent Jobs, Enable Fact Storage, Diff Mode |
| Instance Groups | pin to nodes with the right network reach |
| Labels | for filtering/reporting and workflow organisation |
"Prompt on launch" on **extra variables** is the big one: it lets the user submit arbitrary
`-e` values, which override anything — leave it off on prod templates and expose inputs via a survey.

## 2. Surveys
A survey is a validated form whose answers become `extra_vars`:
```yaml
# survey_spec (API) / infra.aap_configuration survey_spec
name: ""
description: ""
spec:
  - {variable: release_tag, question_name: Release tag, type: text, required: true, min: 5, max: 40, default: ""}
  - {variable: target_env, question_name: Environment, type: multiplechoice, choices: ["stage", "prod"], required: true}
  - {variable: app_components, question_name: Components, type: multiselect, choices: ["web", "worker", "cron"], default: "web\nworker"}
  - {variable: db_admin_password, question_name: DB admin password, type: password, required: false}
  - {variable: batch_size, question_name: Batch size %, type: integer, min: 1, max: 100, default: 25}
```
Types: `text`, `textarea`, `password` (masked, stored encrypted, redacted in job output as `$encrypted$`),
`integer`, `float`, `multiplechoice`, `multiselect`. Surveys only run when the template's
`Survey Enabled` is on. Template `extra_vars` override survey values **unless** "prompt on launch" for variables is enabled; design accordingly
(typically: survey on, prompt-on-launch for extra_vars on, fixed vars elsewhere).

Use survey values as **selectors** in the playbook (`limit` via `-l "{{ target_env }}"` is not possible —
instead `hosts: "{{ target_env }}"` in the play, or a `limit` prompt constrained by `ask_limit_on_launch`).

## 3. Launching
- UI, schedule, workflow node, webhook (GitHub/GitLab payload becomes payload is delivered to the job; a generated webhook key signs payloads), API:
```bash
curl -s -X POST -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  https://ctl.example/api/v2/job_templates/42/launch/ \
  -d '{"extra_vars": {"release_tag": "v1.2.3"}, "limit": "web"}'
# extra_vars are only honoured for survey variables or when ask_variables_on_launch is true
awx job_templates launch 42 --extra_vars '{"release_tag":"v1.2.3"}' --monitor
```
- **Provisioning callback**: a new host POSTs to `/api/v2/job_templates/42/callback/` with `host_config_key`; the controller runs the template limited to that host (if it exists in the inventory). Cloud-init bootstrap pattern.
- Concurrent Jobs off (default) queues a second launch until the first finishes — the safe default for deploys.

## 4. Operate
- Job output: filter by host/task, download stdout, `Relaunch` (same vars) and `Relaunch on failed hosts`.
- Fact storage: `Enable Fact Storage` stores gathered facts on hosts (visible under Hosts → Facts) and reuses them with `gathering = smart`.
- Instance group pinning for network-restricted zones; `Timeout` so a hung host cannot occupy a fork forever.
- Notifications per template (start/success/failure/approval) — see the schedules/notifications skill.
- Template copy for a prod/stage pair; better: one template + survey env choice **only** when the credentials are identical; prod with distinct credentials should be a distinct template with distinct RBAC.

## 5. Automate
```yaml
- infra.aap_configuration.controller_job_templates:
    name: app-a deploy (prod)
    organization: platform
    project: platform
    playbook: deploy.yml
    inventory: prod
    execution_environment: ee-platform
    credentials: [prod-ssh, prod-vault]
    become_enabled: true
    forks: 25
    job_timeout: 3600
    ask_limit_on_launch: true
    ask_variables_on_launch: true
    survey_enabled: true
    survey_spec: "{{ lookup('file', 'surveys/app-a.yml') | from_yaml }}"
    labels: [app-a, prod]
```

## Gotchas
- A template's `extra_vars` are visible to anyone with Read; never put secrets there (use credentials or `password` survey questions).
- `ask_variables_on_launch: false` **also** blocks survey values from reaching the job in some versions — enable it when a survey is used and test.
- Changing the playbook path requires a project sync first; the dropdown shows the last synced list.
- Job slicing + `run_once`/cross-host logic breaks (each slice is its own play run).
- Webhook launches ignore surveys' `required` validation (defaults are used); validate inside the playbook with `assert`.
- `Limit` left blank runs on the whole inventory; prod templates should either fix a limit or require it via `ask_limit_on_launch` + an `assert` on `ansible_limit`.

## Verify
- [ ] A user with Execute only sees the survey questions, cannot edit the template, and a launch with disallowed fields via API returns 400.
- [ ] Password-type survey answers show as `$encrypted$` in the job's extra vars and are masked in output.
- [ ] Launching twice back-to-back queues the second job (Concurrent Jobs off) and both complete.
- [ ] The `infra.aap_configuration` playbook is idempotent against the live controller (`changed=0` on re-run).

## Checked

- 2026-10-31: job template fields (Job type Run/Check, Forks, Limit, Verbosity, Job slicing, Timeout, Show changes, Job/Skip tags, Extra variables, Privilege escalation, Provisioning callback, Enable webhook, Concurrent jobs, Enable fact storage), prompt-on-launch behaviour, survey question types (Textarea, Multiple Choice single/multiple select, password entries stored `$encrypted$`), the callback URL form `/api/v2/job_templates/<id>/callback/` with `host_config_key`, relaunch including failed-only, and the rule that launch `extra_vars` are only honoured for survey variables or `ask_variables_on_launch` all confirmed in AAP 2.5 Using automation execution. `awx job_templates launch --monitor`/`--extra_vars` confirmed in the AWX CLI reference. `infra.aap_configuration.controller_job_templates` role name confirmed in the redhat-cop roles listing.
- Removed: the `tower_webhook_payload` extra-variable name and the 400-response claim for non-prompted fields (replaced with the documented honouring rule).
Method: documentation only; no commands were run.
