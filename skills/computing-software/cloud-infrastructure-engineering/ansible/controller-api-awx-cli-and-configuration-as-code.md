---
id: computing-software.cloud-infrastructure-engineering.ansible.controller-api-awx-cli-and-configuration-as-code
name: controller-api-awx-cli-and-configuration-as-code
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, awx, automation-controller, awx-cli, controller-api, awx-api, rest-api, api-v2, oauth2-token, application-token, awxkit, awx-awx-collection, ansible-controller-collection, infra-aap-configuration, controller-configuration-as-code, casc, export-import, awx-export, awx-import, gitops-controller, api-pagination, filtering]
level: advanced
status: docs-checked
description: "Treat AWX/controller as code: REST API v2 with tokens and filters, the awx CLI (export/import, launch), the ansible.controller collection and infra.aap_configuration from git."
sources: ["https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html-single/automation_execution_api_overview/", "https://legacy-controller-docs.ansible.com/automation-controller/latest/html/controllercli/", "https://docs.ansible.com/projects/awx/en/latest/rest_api/filtering.html", "https://github.com/redhat-cop/infra.aap_configuration", "https://docs.ansible.com/projects/awx/en/latest/rest_api/authentication.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Controller API, awx CLI and configuration as code

**Goal:** every organization, credential, project, inventory, template, schedule and
role grant is defined in a git repo and applied idempotently; the UI is for looking
and for emergencies.

## 1. API basics
`https://ctl.example/api/v2/` is browsable (DRF). Auth: OAuth2 **application token** (`Users →
Tokens`, scope `read`/`write`, with or without an Application for refresh) — or session/basic for scripts you will delete.
```bash
export CONTROLLER_HOST=https://ctl.example CONTROLLER_OAUTH_TOKEN=<TOKEN>
curl -s -H "Authorization: Bearer $CONTROLLER_OAUTH_TOKEN" "$CONTROLLER_HOST/api/v2/job_templates/?name__icontains=deploy&page_size=200" | jq '.results[] | {id, name}'
curl -s -H "Authorization: Bearer $CONTROLLER_OAUTH_TOKEN" "$CONTROLLER_HOST/api/v2/jobs/?status=failed&finished__gt=2026-10-01" | jq .count
curl -s -H "Authorization: Bearer $CONTROLLER_OAUTH_TOKEN" "$CONTROLLER_HOST/api/v2/jobs/123/stdout/?format=txt"
```
Filters: Django-style `field__lookup=` (`exact`, `icontains`, `in`, `gt`, `isnull`), `or__`, `not__`,
`chain__`; `order_by=-finished`; `page_size` max 200 — follow `next`. Related endpoints under each
object (`/job_templates/42/launch/`, `/credentials/`, `/access_list/`, `/activity_stream/`).
Responses include `summary_fields` (names of related objects) so you rarely need extra calls.
AAP 2.5 serves controller resources under `/api/controller/v2/` (set `AWXKIT_API_BASE_PATH=/api/controller/` for the awx CLI); platform-wide users, teams and organizations are managed through the platform gateway.

## 2. awx CLI
```bash
pip install awxkit            # provides the `awx` command (there is no `awxcli` package on PyPI); same env vars as above, or --conf.host/--conf.token
awx config                    # show
awx job_templates list --name "app-a deploy (prod)" -f human
awx job_templates launch 42 --extra_vars '{"release_tag":"v1.2.3"}' --limit web --monitor   # streams output, exits with job status
awx jobs stdout 1234
awx projects update 7 --monitor
awx export --job_templates "app-a deploy (prod)" > jt.json       # dependencies by name, not id
awx import < jt.json                                              # into another controller
awx export > all.json                                             # whole config (no secrets)
```
`-f jq --filter '.results[].name'` for output shaping. `awx export`/`import` is the quick
migration tool; it does not carry credential secrets (they come out as `$encrypted$`) or
users' passwords.

## 3. Collections
`infra.aap_configuration` (Red Hat CoP, AAP 2.5+) drives the certified `ansible.controller` modules
(and `awx.awx` upstream) through one role per object type: `controller_organizations`, `controller_teams`,
`controller_roles`, `controller_credentials`, `controller_credential_types`, `controller_projects`,
`controller_inventories`, `controller_inventory_sources`, `controller_job_templates`, `controller_schedules`,
`controller_notification_templates`, `controller_settings`, `controller_instance_groups`,
`controller_job_launch`, `controller_workflow_launch`, `controller_bulk_host_create` and more.
```yaml
controller_job_launch:            # infra.aap_configuration role input
  - name: launch app-a deploy
    job_template: "app-a deploy (prod)"
    extra_vars: {release_tag: "{{ tag }}"}
    wait: true
```
Connection with `aap_hostname` plus `aap_username`/`aap_password` or `aap_token`; see the `ansible.controller`
and `awx.awx` collection docs (console.redhat.com / Galaxy) for calling modules directly.

## 4. Configuration as code with infra.aap_configuration
The redhat-cop pattern: a repo of YAML lists per object type, one dispatcher playbook:
```
controller-config/
  group_vars/all/controller_organizations.yml   # controller_organizations: [...]
  group_vars/all/controller_credential_types.yml
  group_vars/all/controller_credentials.yml      # secrets as {{ vault_... }}
  group_vars/all/controller_projects.yml
  group_vars/all/controller_inventories.yml / controller_inventory_sources.yml
  group_vars/all/controller_templates.yml / controller_workflows.yml
  group_vars/all/controller_schedules.yml / controller_notifications.yml / controller_roles.yml
  playbooks/configure.yml
```
```yaml
- hosts: localhost
  connection: local
  roles:
    - infra.aap_configuration.dispatch       # runs every object role in dependency order
```
Run from CI on merge, against stage controller first, then prod.
`infra.aap_configuration_extended` exports a live controller into this format (`filetree_create`, then `filetree_read`) for brownfield adoption.

## 5. Secrets and tokens
- Create a dedicated service user with the minimal org roles for CI; its token in the CI secret store; rotate via `awx tokens create`/`delete`.
- Credentials' secret inputs come from Ansible Vault in the config repo; the API cannot read secrets back, so the repo is the only full copy — protect it.
- `settings` module (`ansible.controller.settings: {name: AWX_TASK_ENV, value: {...}}`) for system settings; LDAP/SAML settings too (2.4) — treat them as code.

## Gotchas
- Object lookups are by **name within organization**; two credentials named `ssh` in different orgs confuse modules without `organization:`; duplicates within an org break idempotency.
- `job_template` module replaces the credential list wholesale; forgetting one detaches it.
- Importing a template that references a playbook not yet synced fails; sync projects first (dispatch does).
- API tokens with `write` scope on a superuser are root for the whole platform; scope CI tokens to a non-superuser.
- A config run that creates thousands of hosts should use the bulk API (`/api/v2/bulk/host_create/`, or `awx bulk host_create`) rather than one call per host.
- `awx export` output of a job template includes survey specs but password defaults as `$encrypted$`.

## Checked

- 2026-10-31: API filters (`exact`, `icontains`, `in`, `gt`, `isnull`, `or__`, `not__`, `chain__`), `order_by=-field`, `page_size` max 200 and `/api/v2/bulk/host_create/` confirmed in the AWX REST API filtering/pagination pages and the AAP 2.5 Automation execution API overview. `awx` CLI subcommands (`config`, `job_templates launch --monitor`, `jobs stdout`, `export`, `import`, `bulk host_create`, `tokens`), `pip install awxkit`, `--conf.host`/`--conf.token` and the CONTROLLER_HOST/CONTROLLER_OAUTH_TOKEN env vars confirmed in the AWX CLI reference (usage/examples). `infra.aap_configuration` role names and `filetree_create` confirmed in the redhat-cop repo (roles listing, README). `$encrypted$` in exports and AWX_TASK_ENV via settings confirmed in Configuring automation execution.
- Removed: the `/api/gateway/v1/` endpoint claim (undocumented; replaced with the documented `/api/controller/v2/` base path and AWXKIT_API_BASE_PATH), the `controller_configuration_async_*` variables and `controller_configuration_*_enforcement` roles (not in the current collection), the `controller_api` lookup and the unconfirmed per-module name list (replaced with confirmed role names).
Method: documentation only; no commands were run.

## Verify
- [ ] `awx job_templates list -f jq --filter '.count'` works with the CI token and a `write` call to an object outside the token user's org is rejected (403).
- [ ] The config-as-code playbook runs twice; second run reports `changed=0`.
- [ ] Deleting a template in the UI and re-running the playbook restores it identically (survey, credentials, notifications, RBAC).
