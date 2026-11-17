---
id: computing-software.cloud-infrastructure-engineering.kubespray.ansible-variable-layers-and-extra-vars
name: ansible-variable-layers-and-extra-vars
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [ansible, variables, group-vars, extra-vars, precedence, booleans]
level: practitioner
status: docs-checked
description: "Customise Kubespray through inventory group_vars first, use extra vars only for overrides, and pass booleans with JSON syntax because -e key=value always passes strings."
sources:
  - https://kubespray.io/docs/ansible/ansible.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Kubespray expects customisation from these sources only:

| Layer | Comment |
|---|---|
| inventory group_vars | most used |
| inventory host_vars | host-specific overrides; group_vars is usually more practical |
| extra vars | always win precedence; override with `ansible-playbook -e @foo.yml` |

Extra vars are best used to override Kubespray internal variables, such as those in `roles/vars/`. The page warns those are usually not expected to be modified by end users and are not part of the Kubespray interface, so they can change, disappear or break things unexpectedly.

A second warning concerns types: `-e key=value` always passes strings. Since Ansible 12 (ansible-core 2.19), conditionals must return booleans, so pass booleans in JSON syntax:

```
-e '{"drain_nodes": true}'
```

The node docs use the same form, for example `-e '{"reset_nodes": false, "allow_ungraceful_removal": true}'`.

Whole-cluster variables live under `<inventory>/group_vars/k8s_cluster/*.yml`, as the inventory page describes.

## Checked

2026-11-04. The layer table and both warnings were confirmed on the Customize Ansible vars section; the node-removal example is from the Adding/replacing a node page; the group_vars/k8s_cluster remark is from the Inventory page.

Method: documentation only; no commands were run.
