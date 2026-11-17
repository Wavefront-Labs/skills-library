---
id: computing-software.cloud-infrastructure-engineering.ansible.play-level-module-defaults-for-cloud-auth
name: play-level-module-defaults-for-cloud-auth
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, module-defaults, module-defaults-play, group-aws, cloud-modules]
level: practitioner
status: docs-checked
description: "Set play-level module_defaults for cloud credentials and regions using action groups like group/aws and group/azure.azcollection.azure so every module call stays short."
sources: ["Module defaults (https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_module_defaults.html)", "amazon.aws meta/runtime.yml action groups (https://github.com/ansible-collections/amazon.aws/blob/main/meta/runtime.yml)", "community.aws meta/runtime.yml action groups (https://github.com/ansible-collections/community.aws/blob/main/meta/runtime.yml)", "azure.azcollection meta/runtime.yml action groups (https://github.com/ansible-collections/azure/blob/dev/meta/runtime.yml)", "google.cloud meta/runtime.yml action groups (https://github.com/ansible-collections/google.cloud/blob/main/meta/runtime.yml)", "kubernetes.core meta/runtime.yml action groups (https://github.com/ansible-collections/kubernetes.core/blob/main/meta/runtime.yml)", "community.vmware meta/runtime.yml action groups (https://github.com/ansible-collections/community.vmware/blob/main/meta/runtime.yml)", "amazon.aws common doc fragment (https://github.com/ansible-collections/amazon.aws/blob/main/plugins/doc_fragments/common.py)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Play-level module_defaults for cloud auth

```yaml
- name: Provision AWS resources
  hosts: localhost
  gather_facts: false
  module_defaults:
    group/amazon.aws.aws:
      region: eu-west-1
    group/community.aws.aws:
      region: eu-west-1
  tasks:
    - amazon.aws.ec2_vpc_net:
        name: core
        cidr_block: 10.20.0.0/16
    - amazon.aws.s3_bucket:
        name: acme-artifacts-prod
```
Every module in the action group gets `region` without repeating it.

## Action group names
| Collection | Group |
|---|---|
| amazon.aws | `group/amazon.aws.aws` |
| community.aws | `group/community.aws.aws` |
| azure.azcollection | `group/azure.azcollection.all` |
| google.cloud | `group/google.cloud.gcp` |
| kubernetes.core | `group/kubernetes.core.k8s` |
| community.vmware | `group/community.vmware.vmware` |
| ansible.builtin | no group for users (name the modules) |

Groups are defined in each collection's `meta/runtime.yml` under `action_groups`; read that file for the installed collection version, because group names and membership differ per collection. `module_defaults` ignores the `collections` keyword, so always use the fully qualified group name.

## Credentials
Prefer environment/instance-profile auth over values in module_defaults. If you must pass keys, reference vaulted vars and never print them:
```yaml
module_defaults:
  group/amazon.aws.aws:
    access_key: "{{ vault_aws_access_key }}"
    secret_key: "{{ vault_aws_secret_key }}"
```

## Precedence
Arguments given explicitly in a task override any default for that argument. `module_defaults` can be set on a play, block or task; an empty dict (`file: {}`) removes defaults previously established for a module. Play-level defaults also apply to roles used in the play (and block or task level ones to `include_role` and `import_role`), which can surprise role authors.

## Gotchas
- Only modules listed in the collection's `action_groups` entry receive the group defaults; a module missing from the group needs its own `module_defaults` entry.

## Verify
Run the play with `-vvv` and check that each task's `invocation.module_args` shows the default values (keep secrets out of output with `no_log`).

## Checked

Checked 2026-10-26 against ansible-documentation main (2026-10-21) and the `meta/runtime.yml` of each collection on GitHub (default branches, read 2026-10-26).
- Confirmed: `module_defaults` at play, block and task level, explicit task arguments override defaults, `{}` clears defaults, play-level defaults apply to roles, groups come from `meta/runtime.yml` `action_groups`, fully qualified group name required.
- Confirmed group names: amazon.aws `aws` (includes `ec2_vpc_net` and `s3_bucket`), community.aws `aws`, google.cloud `gcp`, kubernetes.core `k8s` (and `helm`), community.vmware `vmware`; amazon.aws documents `access_key`, `secret_key`, `profile`.
- Fixed: the azure.azcollection group is named `all` in its `runtime.yml`, not `azure`.
- Removed as unconfirmed: the short `group/aws` alias, `default(omit)` inside `module_defaults`, and the block-over-play ordering sentence.

Method: documentation only; no commands were run.
