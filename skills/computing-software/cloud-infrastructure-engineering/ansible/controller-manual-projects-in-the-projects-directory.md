---
id: computing-software.cloud-infrastructure-engineering.ansible.controller-manual-projects-in-the-projects-directory
name: controller-manual-projects-in-the-projects-directory
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, automation-controller, awx, manual-projects, projects-dir, project-base-dir, air-gapped, awx-operator-pvc]
level: practitioner
status: docs-checked
description: "Use controller manual projects (playbooks placed in the project base path) for air-gapped bootstraps: directory ownership, limits and the operator persistent volume."
sources: ["https://raw.githubusercontent.com/ansible/aap-docs/main/downstream/modules/platform/proc-projects-manage-playbooks-manually.adoc", "https://raw.githubusercontent.com/ansible/aap-docs/main/downstream/assemblies/platform/assembly-controller-projects.adoc", "https://raw.githubusercontent.com/ansible/awx-operator/devel/docs/user-guide/advanced-configuration/persisting-projects-directory.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Controller manual projects in the projects directory

Goal: run playbooks in a controller that cannot reach any git server yet (air-gapped bootstrap,
emergency fix), knowing the limitations so it does not become permanent.

## How it works
Playbooks can be placed manually under the **Project Base Path** on the controller server instead
of coming from source control. The documented default is `/var/lib/awx/projects`; an administrator
can change it (configured in `/etc/tower/conf.d/custom.py`, edit with caution).

Procedure from the documentation:
1. Create one or more directories under the Project Base Path.
2. Create or copy playbook files into the directory.
3. Make the directory and files owned by the same UNIX user and group the service runs as.
4. Set permissions appropriate for the directories and files.

```bash
sudo mkdir /var/lib/awx/projects/bootstrap
sudo cp -r site.yml roles/ collections/ /var/lib/awx/projects/bootstrap/
sudo chown -R awx:awx /var/lib/awx/projects/bootstrap   # the user/group the service runs as
```
If no playbook directories exist under the base path, the UI shows an error: create the
directories and check out playbooks from SCM, or copy playbooks in.

## Operator (Kubernetes)
The AWX operator can persist the projects directory with a PersistentVolume. Variables (defaults):
`projects_persistence` (false), `projects_storage_class` (empty), `projects_storage_size` (8Gi),
`projects_storage_access_mode` (ReadWriteMany), `projects_existing_claim` (empty; cannot be
combined with the `projects_storage_*` variables).
```yaml
spec:
  projects_persistence: true
  projects_storage_class: <STORAGE_CLASS>
  projects_storage_size: 8Gi
```

## Limits
- Projects of type Manual cannot update or schedule source control actions unless reconfigured as an SCM type.
- Manual projects have no versioning or audit trail of what changed; add collections and roles inside the project directory or in the execution environment yourself.
- The status **Missing** means the project directory is absent from the base path (applies to manual and SCM projects).

## Exit plan
As soon as a git server is reachable, create an SCM project, point templates at it and delete the manual directory. The documentation says production use should rely on source control.

## Verify
- [ ] The directory appears when you create a Manual project and its playbooks appear in the template.
- [ ] A test job succeeds; the project status is OK, not Missing.

## Checked

- Date: 2026-11-09. Sources: ansible/aap-docs main (manage playbooks manually, projects assembly) and ansible/awx-operator devel (persisting the projects directory).
- Confirmed: base path default and how it is changed, the four-step procedure, the no-directories error, Manual project restrictions, OK and Missing statuses, operator variables and defaults, the SCM-for-production note.
- Removed unconfirmed claims: restorecon/SELinux relabel step, multi-node replication and instance-group pinning advice, `kubectl cp` command, hidden-directory and empty-directory behaviour, "directory claimed by another project disappears from the dropdown", the PROJECTS_ROOT setting name, `requirements.yml` not run for manual projects (kept only as a generic caution).

Method: documentation only; no commands were run.
