---
id: computing-software.cloud-infrastructure-engineering.ansible.awx-manage-commands-and-inventory-import
name: awx-manage-commands-and-inventory-import
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, controller-api-cli, awx-manage, inventory-import, awx-manage-inventory-import, controller-projects-inventories, cleanup-jobs]
level: advanced
status: docs-checked
description: "Use awx-manage on controller nodes for admin jobs: inventory_import from files or scripts, job and activity-stream cleanup, session expiry, analytics and host metrics."
sources: ["https://github.com/ansible/awx/blob/devel/docs/docsite/rst/rest_api/awx-manage.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# awx-manage commands and inventory_import

`awx-manage` accesses detailed internal information of AWX. Run it as the `awx` user only. Running `awx-manage`
through a playbook is not recommended or supported. The docs also say not to run other (cluster-management)
`awx-manage` commands unless Red Hat Ansible support instructs you to. Where the shell runs (a controller node or a
task pod) depends on how you installed: check your install's documentation.

## inventory_import
Synchronise a controller inventory with a text inventory file, a dynamic inventory script, or a directory of those.
Useful for one-time migrations from CLI Ansible:
```bash
awx-manage inventory_import --source=/ansible/inventory/ --inventory-id=1
awx-manage inventory_import --source=/ansible/inventory/ --inventory-id=1 --overwrite
awx-manage inventory_import --help
```
- Create the destination inventory in AWX first. Give either `--inventory-id` or `--inventory-name`, plus `--source`.
- By default imported data blends with what is already stored: new variables are added, existing keys are overwritten, and variables not from the external source are kept.
- `--overwrite` uses only the external data. `--overwrite_vars` (underscore) makes existing hosts take variable data exclusively from `--source`.
- Edits to host variables in the controller persist across a sync as long as `--overwrite_vars` is not set.
- Vaulted vars are not decrypted: keep secrets in credentials.
For ongoing sync, use an inventory **source** from a project instead (versioned, scheduled).

## Other commands in the AWX docs
| Command | Purpose |
|---|---|
| `awx-manage cleanup_jobs` | permanently delete job details and output older than a number of days (`--help` for options); also reachable as a Management Job |
| `awx-manage cleanup_activitystream` | trim old activity-stream data (`--help` for options) |
| `awx-manage expire_sessions [--user NAME]` | end all sessions, or one user's |
| `awx-manage clearsessions` | delete expired sessions (Django command) |
| `awx-manage gather_analytics --ship` | gather and ship analytics outside the predefined window |
| `awx-manage host_metric --since YYYY-MM-DD --until YYYY-MM-DD --json` | unique hosts automated in a period, for disconnected sites; `--since` or `--until` is required, `--json` optional |
| `awx-manage set_indirect_node_counting --disable` / `--enable` | support-directed toggle for indirect managed-node counting; no restart needed |

`awx-manage help` lists everything available in your version.

## Gotchas
- Restrict shell access to controller nodes; these commands bypass the API.

## Verify
- [ ] After inventory_import, the UI shows the expected host count, and stale hosts are removed only when `--overwrite` was intended.

## Checked
2026-10-28. Confirmed in the AWX docs page for awx-manage: run as `awx` user, playbook warning, `inventory_import` options (`--inventory-id`, `--inventory-name`, `--source`, `--overwrite`, `--overwrite_vars`) and default merge behaviour, `cleanup_jobs`, `cleanup_activitystream`, `expire_sessions --user`, `clearsessions`, `gather_analytics --ship`, `host_metric --since/--until/--json`, `set_indirect_node_counting`. Removed because not confirmed: `--keep-vars`, the pod exec line, `group_vars`/`host_vars` handling, `changepassword`/`createsuperuser`, `list_instances`, provision/deprovision/register_queue, `check_license`, `regenerate_secret_key`, `run_dispatcher`, `--days` values, `host_metric_summary_monthly`. The Red Hat 2.5 documentation pages were not readable text.
Method: documentation only; no commands were run.
