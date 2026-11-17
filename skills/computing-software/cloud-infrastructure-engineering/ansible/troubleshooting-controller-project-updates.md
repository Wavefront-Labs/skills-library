---
id: computing-software.cloud-infrastructure-engineering.ansible.troubleshooting-controller-project-updates
name: troubleshooting-controller-project-updates
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, controller-projects-inventories, project-update-failure, scm-projects, collections-requirements]
level: practitioner
status: docs-checked
description: "Diagnose failed controller project syncs: SCM auth, branch and refspec issues, requirements.yml collection install failures, galaxy credentials and project_update logs."
sources: ["https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html-single/using_automation_execution/", "https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html-single/configuring_automation_execution/", "https://docs.ansible.com/projects/awx/en/latest/rest_api/awx-manage.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Troubleshooting project updates

Project syncs run the internal `project_update.yml` playbook in an EE; open the failed **Project Update** job output and read the failed task.

| Failed task / message | Cause | Fix |
|---|---|---|
| `git clone ... Permission denied (publickey)` | SCM credential missing/wrong key, deploy key not on repo | attach Source Control credential; test with `git ls-remote` |
| `Authentication failed` for HTTPS | token expired / needs username | update credential (token as password) |
| `remote branch X not found` | branch renamed | fix SCM branch or allow override |
| `fatal: couldn't find remote ref refs/pull/...` | refspec | set SCM refspec e.g. `refs/pull/*:refs/remotes/origin/pull/*` |
| `SSL certificate problem` | private CA | add CA to the EE/control nodes or `GIT_SSL_CAINFO` via custom EE |
| `Failed to install collections ... 401/404` | Galaxy credential order/token, collection not synced to hub | org Galaxy credentials (Settings → Organization), sync remote |
| `ERROR! Neither the collection requirement entry key 'name'...` | malformed requirements.yml | validate locally with `ansible-galaxy collection install -r` |
| project update succeeds but playbook list empty | playbooks not at repo root/subdirs, YAML errors, files not ending in .yml | check the project's playbook directory, run a syntax check |

## Requirements handling
Controller installs `roles/requirements.yml` and `collections/requirements.yml` on sync (the
system-wide "Enable Role Download" and "Enable Collection(s) Download" settings control this).
Galaxy credentials of the **organization** are used in order.

## Debug steps
1. Re-run the sync with verbosity 3 (project update verbosity is in the project's job settings).
2. Reproduce locally in the same EE: run `ansible-galaxy collection install -r collections/requirements.yml`
   with `ansible-navigator` against the project's execution environment.
3. Check the project's default EE and its registry credential.

## Gotchas
- "Update revision on launch" + a broken repo makes every job fail at launch; disable temporarily to run the last good revision.
- Update revision on launch caches the revision between syncs; a project-level cache timeout avoids
  a git fetch per job.

## Verify
- [ ] Project status Successful and expected revision hash shown.

## Checked

- 2026-10-31: the internal `project_update.yml` playbook (and the "Run Project Updates With Higher
  Verbosity" `-vvv` setting), `ansible-galaxy role install -r roles/requirements.yml` at the end of
  project updates, collections/requirements support, the system-wide role/collection download
  settings, Update revision on launch, branch/tag/commit SCM fields and refspecs, `awx-manage`
  utilities and `ansible.containerized_installer` flows confirmed in AAP 2.5 Using automation
  execution, Configuring automation execution and the AWX awx-manage page.
- Removed: the `AWX_COLLECTIONS_ENABLED`/`AWX_ROLES_ENABLED` setting names (replaced with the
documented setting labels), the `scm_update_cache_timeout` field name and the specific
  `ansible-navigator exec` command form.
Method: documentation only; no commands were run.
