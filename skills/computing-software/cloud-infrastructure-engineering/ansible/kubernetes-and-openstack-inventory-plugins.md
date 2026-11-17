---
id: computing-software.cloud-infrastructure-engineering.ansible.kubernetes-and-openstack-inventory-plugins
name: kubernetes-and-openstack-inventory-plugins
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, dynamic-inventory, k8s-inventory, openstack-inventory, inventory-plugins]
level: practitioner
status: docs-checked
description: "Reach Kubernetes pods with add_host and the kubectl connection (the k8s inventory plugin was removed) and build OpenStack inventory with openstack.cloud.openstack."
sources: ["https://github.com/ansible-collections/kubernetes.core/blob/main/CHANGELOG.rst", "https://github.com/ansible-collections/kubernetes.core/blob/main/plugins/connection/kubectl.py", "https://github.com/openstack/ansible-collections-openstack/blob/master/plugins/inventory/openstack.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Kubernetes and OpenStack inventory plugins

## Kubernetes pods as hosts
The `kubernetes.core.k8s` inventory plugin was removed in kubernetes.core 6.0.0 (deprecated earlier). Build the
inventory at run time instead: list pods with `kubernetes.core.k8s_info`, then add them with
`ansible.builtin.add_host` and the `kubernetes.core.kubectl` connection.
```yaml
- hosts: localhost
  gather_facts: false
  tasks:
    - kubernetes.core.k8s_info:
        kind: Pod
        namespace: payments
        label_selectors: [app=api]
      register: pods
    - ansible.builtin.add_host:
        name: "{{ item.metadata.name }}"
        groups: api_pods
        ansible_connection: kubernetes.core.kubectl
        ansible_kubectl_namespace: payments
        ansible_kubectl_pod: "{{ item.metadata.name }}"
      loop: "{{ pods.resources }}"
      loop_control: {label: "{{ item.metadata.name }}"}
```
The kubectl connection takes `ansible_kubectl_container` (pick a container in a multi-container pod),
`ansible_kubectl_namespace` and `ansible_kubectl_context`.

Running config management inside pods is usually wrong; use it for diagnostics.

## OpenStack servers
```yaml
# inventory/openstack.yml   (file name openstack.yml or openstack.yaml)
plugin: openstack.cloud.openstack
expand_hostvars: false
fail_on_errors: true
all_projects: false
only_clouds: [prod]
private: true                 # prefer private interfaces for ansible_host
compose:
  ansible_user: "'cloud-user'"
keyed_groups:
  - key: openstack.metadata.role
    prefix: role
```
- Credentials come from the standard `clouds.yaml` files (override the path with `clouds_yaml_path`); select clouds with `only_clouds`.
- `legacy_groups` (default true) creates groups from host variables; `show_all: false` (default) lists only servers with an IP address.
- `expand_hostvars: true` adds Cinder and Neutron queries and is slow on clouds with many servers (default false).
- `server_filters` takes compute list-servers query parameters.

## Gotchas
- `inventory_hostname` is `name` by default; when servers share a name their IDs are used. Set `inventory_hostname: uuid` to always use the ID.
- `use_names: false` (the default) uses a server's first floating IP for `ansible_host`.
- The plugin supports inventory caching (`cache: true`, `cache_timeout`) and constructed options (`compose`, `groups`, `keyed_groups`).

## Verify
```bash
ansible-inventory -i inventory/openstack.yml --graph
```

## Checked

Checked 2026-10-26 against the kubernetes.core changelog and kubectl connection plugin, and the openstack.cloud inventory plugin source (main). Confirmed: the `k8s` inventory plugin was removed in kubernetes.core 6.0.0; the kubectl connection variables `ansible_kubectl_pod`, `ansible_kubectl_container`, `ansible_kubectl_namespace`, `ansible_kubectl_context`; `k8s_info` exists; openstack inventory options `all_projects`, `clouds_yaml_path`, `expand_hostvars` (default false), `fail_on_errors`, `inventory_hostname` (name or uuid, default name), `legacy_groups` (default true), `only_clouds`, `private`, `server_filters`, `show_all`, `use_names`; the plugin accepts cache and constructed options. Replaced the Kubernetes inventory section and removed the claim that `use_names: false` selects UUID hostnames.

Method: documentation only; no commands were run.
