---
id: computing-software.cloud-infrastructure-engineering.ansible.network-and-hardware-facts
name: network-and-hardware-facts
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, facts-magic-vars, default-ipv4, hardware-facts, ansible-devices, gather-subset]
level: intro
status: docs-checked
description: "Use network and hardware facts: default_ipv4, all_ipv4_addresses, interfaces, memtotal_mb, processor_vcpus, mounts and devices, with subsets to gather them fast."
sources: ["https://docs.ansible.com/projects/ansible/latest/collections/ansible/builtin/setup_module.html", "https://docs.ansible.com/projects/ansible/latest/playbook_guide/playbooks_vars_facts.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Network and hardware facts

## Network
```yaml
ansible_facts['default_ipv4']['address']        # IP of the interface holding the default route
ansible_facts['default_ipv4']['interface']      # e.g. ens192
ansible_facts['default_ipv4']['gateway']
ansible_facts['all_ipv4_addresses']             # list
ansible_facts['interfaces']                     # list of interface names
ansible_facts['fqdn'], ansible_facts['hostname'], ansible_facts['domain']
ansible_facts['dns']['nameservers']
```
On hosts without a default route, do not rely on `default_ipv4`; fall back to `ansible_host`.

## Hardware
```yaml
ansible_facts['memtotal_mb']
ansible_facts['processor_vcpus'], ansible_facts['processor_cores'], ansible_facts['processor_count']
ansible_facts['devices']                         # block devices: size, model, partitions, holders
ansible_facts['mounts']                          # list: mount, device, fstype, size_total, size_available
ansible_facts['virtualization_type'], ansible_facts['virtualization_role']   # e.g. role: guest
ansible_facts['product_name'], ansible_facts['system_vendor']
```

## Gather only what you need
```yaml
- hosts: all
  gather_facts: true
  module_defaults:
    ansible.builtin.setup:
      gather_subset: ['!all', '!min', network, hardware]
```
```bash
ansible web01 -m ansible.builtin.setup -a 'gather_subset=network filter=ansible_default_ipv4'
```

## Recipes
```yaml
nginx_workers: "{{ ansible_facts['processor_vcpus'] }}"
java_heap_mb: "{{ (ansible_facts['memtotal_mb'] * 0.5) | int }}"
root_free_gb: "{{ (ansible_facts['mounts'] | selectattr('mount','eq','/') | first).size_available // 1024**3 }}"
```

## Gotchas
- `gather_timeout` (default 10 seconds) bounds individual fact gathering in the `setup` module.
- Re-run `setup` after adding interfaces so the facts refresh.

## Verify
```bash
ansible web01 -m ansible.builtin.setup -a 'filter=ansible_default_ipv4'
```

## Checked
2026-10-28. Confirmed in the `ansible.builtin.setup` module documentation (`gather_subset` values including `network`, `hardware`, `all_ipv4_addresses`, `default_ipv4`; `filter`; `gather_timeout` default 10) and the sample facts output in "Discovering variables: facts" (`nameservers`, `size_available`, `processor_cores`, `virtualization_role`, `system_vendor`). Removed: the per-interface fact line and dash-to-underscore note, the docker/bridge remark, the empty `default_ipv4` claim, the NFS-hang claim and the once-per-play claim.
Method: documentation only; no commands were run.
