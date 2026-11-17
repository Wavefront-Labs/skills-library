---
id: computing-software.cloud-infrastructure-engineering.ansible.variables-and-runtime-targets-in-play-hosts
name: variables-and-runtime-targets-in-play-hosts
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, host-patterns, hosts-variable, dynamic-hosts, add-host, group-by]
level: practitioner
status: docs-checked
description: "Choose targets at runtime: variables in hosts with extra vars, add_host for newly created machines, and group_by to build groups from facts."
sources: ["Patterns, using variables in patterns (https://docs.ansible.com/ansible/latest/inventory_guide/intro_patterns.html)", "Developing collections, playbooks in a collection (https://docs.ansible.com/ansible/latest/dev_guide/developing_collections_structure.html)", "ansible.builtin.add_host source (https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/add_host.py)", "ansible.builtin.group_by source (https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/group_by.py)", "ansible.builtin.wait_for_connection source (https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/wait_for_connection.py)", "amazon.aws ec2_instance source (https://github.com/ansible-collections/amazon.aws/blob/main/plugins/modules/ec2_instance.py)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Runtime-selected targets

## Variable in hosts
```yaml
- hosts: "{{ target | default('none') }}"
  tasks: [...]
```
```bash
ansible-playbook deploy.yml -e target=web_canary
```
Default to a name that matches no group so a forgotten `-e` does not fall through to `all`; the collections developer guide recommends defining `hosts` as a variable for exactly this reason (its example is `hosts: '{{target|default("all")}}'`, and a narrower default is safer). Pass the value with `-e`.

## add_host: target machines created earlier in the run
```yaml
- hosts: localhost
  gather_facts: false
  tasks:
    - amazon.aws.ec2_instance:
        name: builder-{{ build_id }}
        image_id: ami-0abc
        instance_type: t3.small
        wait: true
      register: ec2
    - ansible.builtin.add_host:
        name: "{{ item.private_ip_address }}"
        groups: new_builders
        ansible_user: ec2-user
      loop: "{{ ec2.instances }}"

- hosts: new_builders
  tasks:
    - ansible.builtin.wait_for_connection: {timeout: 300}
```
`add_host` bypasses the host loop (it runs once for all hosts in the play) and does not support `become`, `connection` or delegation. Hosts it adds still obey `--limit`, so they must also match the command-line limit. It reports `changed` because it alters the in-memory inventory.

## group_by: group by facts
```yaml
- hosts: all
  tasks:
    - ansible.builtin.group_by:
        key: os_{{ ansible_facts['distribution'] | lower }}_{{ ansible_facts['distribution_major_version'] }}
- hosts: os_rhel_9
  tasks: [...]
```

## Gotchas
- `add_host`/`group_by` groups live in memory for the run only.

## Verify
```bash
ansible-playbook deploy.yml -e target=web_canary --list-hosts
```

## Checked

Checked 2026-10-26 against ansible-core 2.21.5 module sources, ansible-documentation main (2026-10-21) and amazon.aws main.
- Confirmed: `add_host` and `group_by` support `bypass_host_loop` fully and `add_host` does not support become, connection or delegation; added hosts do not bypass `--limit`; `add_host` alters the in-memory inventory and reports `changed`; `group_by` takes `key`; `wait_for_connection` `timeout` defaults to 600; `ec2_instance` has `name`, `image_id`, `instance_type`, `wait` and returns `instances` with `private_ip_address`; a playbook can take its `hosts` from a variable passed with `-e`.
- Removed as unconfirmed: the claim about which variables are available when `hosts:` is evaluated.

Method: documentation only; no commands were run.
