---
id: computing-software.cloud-infrastructure-engineering.kubespray.use-kubespray-as-an-ansible-collection
name: use-kubespray-as-an-ansible-collection
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [ansible, collection, ansible-galaxy, requirements-yml, playbook]
level: practitioner
status: docs-checked
description: "Install Kubespray as the kubernetes_sigs.kubespray Ansible collection from git with ansible-galaxy and import its cluster playbook from your own playbook."
sources:
  - https://kubespray.io/docs/ansible/ansible_collection.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Kubespray can be consumed as an Ansible collection instead of a checkout.

1. Prepare an inventory with the right host groups and required group vars (see the inventory and Getting started docs).
2. Add Kubespray to `requirements.yml`:

```yaml
collections:
- name: https://github.com/kubernetes-sigs/kubespray
  type: git
  version: master # use the appropriate tag or branch for the version you need
```

3. Install the collection:

```ShellSession
ansible-galaxy install -r requirements.yml
```

4. Create a playbook that imports the cluster playbook from the collection:

```yaml
- name: Install Kubernetes
  ansible.builtin.import_playbook: kubernetes_sigs.kubespray.cluster
```

5. Point INVENTORY and PLAYBOOK at your files and run it with privilege escalation:

```ShellSession
ansible-playbook -i INVENTORY --become --become-user=root PLAYBOOK
```

Replace `master` in `version` with a release tag for a reproducible deployment, as the inline comment suggests.

## Checked

2026-11-04. All five steps and snippets were confirmed on the Ansible collection page. Removed an unverified remark about other playbooks.

Method: documentation only; no commands were run.
