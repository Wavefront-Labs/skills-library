---
id: computing-software.cloud-infrastructure-engineering.ansible.controller-projects-and-inventory-sources
name: controller-projects-and-inventory-sources
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, awx, automation-controller, awx-projects, awx-inventories, projects, scm-projects, project-sync, update-on-launch, scm-branch, inventory-sources, sourced-from-project, cloud-inventory-source, constructed-inventory, smart-inventory, overwrite, overwrite-vars, update-on-project-update, host-filter, collections-requirements, roles-requirements, project-signing]
level: practitioner
status: docs-checked
description: "Configure AWX/controller projects (git SCM, update on launch, requirements.yml) and inventories: project and cloud sources, constructed inventories, overwrite rules."
sources: ["https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html-single/using_automation_execution/", "https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html-single/configuring_automation_execution/", "https://github.com/redhat-cop/infra.aap_configuration"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Controller projects and inventory sources

**Goal:** the controller runs exactly the commit you expect, with collections and roles
resolved the same way every time, against an inventory that is generated from the
cloud or the repo — never hand-edited in the UI.

## 1. Projects
A project = a git (or svn, archive, or manual) checkout the controller owns.
- **SCM URL/branch/credential**: use a deploy token or read-only key. `SCM Branch/Tag/Commit` can be a branch, tag or SHA; `SCM Refspec` (`refs/pull/*/head:refs/remotes/origin/pr/*`) for PR testing.
- **Options**: `Clean` (discard local changes), `Delete` (fresh clone each update), `Track submodules`, **`Update Revision on Launch`** (git fetch before every job; set a `Cache Timeout` of e.g. 60 s to avoid a fetch storm), `Allow Branch Override` (templates can set their own branch — only for dev projects).
- **Requirements**: if `collections/requirements.yml` or `roles/requirements.yml` exists at the project root, the controller runs `ansible-galaxy` during the update using the org's Galaxy/Hub credentials in order. Pin versions there; the system-wide "Enable Role Download"/"Enable Collection(s) Download" settings toggle this.
- **Default EE** per project (falls back to org, then global).
- **Content signing** (AAP): `ansible-sign` + a "GPG Public Key" credential verifies a `MANIFEST.in`-based checksum before any job runs the content.
- Playbooks appear in the template dropdown only after a successful sync; a project in `Failed` state blocks templates.

Manual projects (`/var/lib/awx/projects/<dir>`) are for air-gapped bootstrap only; with the operator the directory is a PVC.

## 2. Inventories
Three kinds:
- **Inventory** with **Sources** (the normal one). Each source is one of: Sourced from a Project (an inventory file/dir/plugin YAML in the repo), Amazon EC2, GCE, Azure RM, VMware, OpenStack, Red Hat Satellite, Insights, Controller (another AWX), or a custom inventory script via project — see the inventory source documentation for the full current list.
- **Smart inventory** (older host-filter mechanism; constructed inventories are the newer approach).
- **Constructed inventory**: takes one or more input inventories and applies `ansible.builtin.constructed` logic (`groups`, `keyed_groups`, `compose`) plus a `limit`; this is how you build "prod web hosts in eu" without duplicating sources.

Source options:
| Option | Meaning |
|---|---|
| Overwrite | hosts/groups not returned by this sync are removed (needed for decommissioning) |
| Overwrite variables | source vars replace, not merge, host/group vars |
| Update on launch | sync before each job using it (with cache timeout) |
| Update on project update | sync whenever the project it is sourced from syncs |
| Enabled variable / value | mark hosts disabled from a variable (`status` == `running`) |
| Host filter | regex on host names to include |
| Source variables | the inventory plugin YAML (e.g. `regions`, `filters`, `keyed_groups`) |
| Verbosity | 2 shows the plugin's own output when debugging |
Cloud sources need a matching credential; "Sourced from a Project" uses the project's checkout, and a file named `*.yml` that starts with `plugin:` runs as an inventory plugin inside the EE (which must contain the collection).

## 3. Patterns
- One inventory per environment (`stage`, `prod`), each with a cloud source + a project source for static extras (bastions), then constructed inventories per app/team with `limit`.
- Group vars for the controller come from the repo (project source `group_vars/`), not from UI-edited variables; set UI vars only as a break-glass and migrate them.
- Inventory sync job templates can be put in workflows (sync → deploy) when `update on launch` latency is unwanted.
- Host counting: licensed "managed nodes" count unique hostnames across all inventories; delete dead hosts (`Overwrite`) to stay in licence.

## 4. Automate
```yaml
- infra.aap_configuration.controller_projects:
    name: platform
    organization: platform
    scm_type: git
    scm_url: https://git.example/acme/platform.git
    scm_branch: main
    scm_credential: git-deploy
    scm_update_on_launch: true
    scm_update_cache_timeout: 60
    default_environment: ee-platform
- infra.aap_configuration.controller_inventories: {name: prod, organization: platform}
- infra.aap_configuration.controller_inventory_sources:
    name: prod-ec2
    inventory: prod
    source: ec2
    credential: aws-ro
    overwrite: true
    update_on_launch: true
    source_vars: {regions: [eu-west-1], filters: {"tag:env": prod}, keyed_groups: [{key: tags.role, prefix: role}]}
```

## Gotchas
- A project update failing on `ansible-galaxy` shows "Failed" with the galaxy error in the sync output — check the org's Galaxy credentials order and the hub's `server_list` before blaming the repo.
- `Update Revision on Launch` without a cache timeout adds a git fetch per job; with hundreds of jobs an hour this hammers the git server.
- Inventory source sync with `Overwrite` off never removes hosts; with it on, a bad filter wipes the inventory (and any UI-set host vars). Test filters with verbosity 2 and `Overwrite` off first.
- Constructed inventory `limit` uses host patterns (`web:&prod`), not JMESPath; `compose` runs Jinja in the controller context.
- Smart inventories ignore group vars; migrate to constructed.
- Hosts created manually in a sourced inventory are deleted at the next `Overwrite` sync.

## Verify
- [ ] Project sync succeeds and the playbook list in a template shows the repo's playbooks at the pinned branch (`/api/v2/projects/<id>/` shows `scm_revision`).
- [ ] An inventory source sync with `Overwrite` adds a new cloud host and removes a terminated one; hosts show the `keyed_groups` you declared.
- [ ] A constructed inventory's host list equals the expected subset (`ansible-inventory --graph` equivalent in the UI's Hosts tab).

## Checked

- 2026-10-31: SCM branch/tag/commit and refspec fields, Allow branch override, Track submodules,
  Update revision on launch, roles/collections requirements handling (ansible-galaxy run at the end
  of project updates, system-wide download settings), the internal project_update.yml playbook,
  ansible-sign project gpg-sign, smart (KIND=smart) and constructed inventories
  (ansible.builtin.constructed), overwrite/overwrite_vars inventory-source options, cloud inventory
  source types, `scm_revision` on jobs/projects and the `infra.aap_configuration` role names
  (controller_projects, controller_inventories, controller_inventory_sources) confirmed in AAP 2.5
  Using automation execution, Configuring automation execution and the redhat-cop roles listing.
- Removed: the `AWX_COLLECTIONS_ENABLED`/`AWX_ROLES_ENABLED` names (replaced with the documented
  setting labels), the smart-inventory "deprecated" claim (still documented in 2.5) and the
  long-tail inventory source types (trimmed to the documented list).
Method: documentation only; no commands were run.
