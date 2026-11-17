---
id: computing-software.cloud-infrastructure-engineering.ansible.module-defaults-and-action-groups
name: module-defaults-and-action-groups
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, module-defaults, action-groups, group-aws, group-k8s, group-azure, defaults, dry, credentials-defaults, region-defaults, play-level-defaults, environment-keyword, proxy-settings, meta-runtime]
level: practitioner
status: docs-checked
description: "Set module_defaults at play/block/task level and via collection action groups (group/aws, group/k8s) so region, credentials, proxies and validate_certs are declared once, plus the environment keyword."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_module_defaults.html", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_environment.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# module_defaults and action groups

**Goal:** stop repeating `region`, `profile`, `kubeconfig`, `validate_certs`, `url` on
every task; declare them once where they apply and keep them out of role internals.

## 1. Per-module defaults
```yaml
- hosts: localhost
  module_defaults:
    ansible.builtin.uri:
      validate_certs: true
      headers: {Authorization: "Bearer {{ api_token }}"}
      return_content: true
    ansible.builtin.get_url:
      timeout: 60
    ansible.builtin.file:
      owner: app
      group: app
  tasks:
    - ansible.builtin.uri: {url: "https://api.example/v1/status"}   # inherits headers etc.
```
Scope: `play`, `block`, or `task` keyword. Any argument given explicitly in a task overrides the default (`validate_certs: false` on one task still works), and an empty dict removes earlier defaults for a module (`ansible.builtin.file: {}`). The documentation's examples use FQCN keys.

## 2. Action groups (whole collections at once)
Collections declare `action_groups` in `meta/runtime.yml`; you address them as `group/<name>`:
```yaml
module_defaults:
  group/aws:                     # amazon.aws + community.aws modules
    region: eu-west-1
    profile: platform-prod
    tags: {managed_by: ansible}
  group/k8s:                     # kubernetes.core
    kubeconfig: /etc/kube/prod.yaml
    validate_certs: true
  group/azure:                   # azure.azcollection
    subscription_id: "{{ az_sub }}"
```
Collections define groups under `action_groups` in `meta/runtime.yml`; a new group needs its fully qualified name (`group/ns.coll.my_group`), because `module_defaults` does not take the `collections` keyword into account. The short names `aws`, `azure`, `gcp`, `k8s`, `os`, `acme`, `docker`, `ovirt` and `vmware` are special historical groups that extend several collections (for example `aws` is `amazon.aws.aws` plus `community.aws.aws`; `k8s` includes `kubernetes.core.k8s`). Read the collection's documentation or `meta/runtime.yml` to see what a group contains.

## 3. Where it does not reach
- `module_defaults` supplies default arguments to modules and action plugins; it is not a mechanism for lookup or filter options.
- Roles: defaults set at play level (and at block or task level on `include_role`/`import_role`) apply to the tasks of any roles used, which can cause unexpected behaviour in the role. Setting `module_defaults` on a block inside the role keeps them role-local.

## 4. The `environment` keyword (process env on the target)
```yaml
- hosts: build
  environment:
    http_proxy: "http://proxy.example:3128"
    https_proxy: "http://proxy.example:3128"
    no_proxy: "localhost,127.0.0.1,.example"
  tasks:
    - ansible.builtin.dnf: {name: git}         # dnf sees the proxy
    - ansible.builtin.command: make
      environment: {PATH: "/opt/toolchain/bin:{{ ansible_env.PATH }}"}
```
`environment` sets variables for the **module's process on the managed node**; it does not affect Ansible itself, its configuration or plugins such as lookups and filters. `ansible_env` is only populated by gathered facts, so basing values on it is risky if the user changes.

## Gotchas
- Values can use `{{ }}` templates (the documentation sets `region: '{{ my_region }}'`).
- An argument written in a task replaces the default for that argument as a whole: a task that sets `headers: {X-Trace: 1}` replaces the default `headers` dict rather than merging with it. Build the dict in a variable and use `combine` if you need both.
- Inventory plugins such as `aws_ec2` take their own options in the inventory source, not from `module_defaults`.

## Verify
- [ ] Remove the per-task `region:` lines and confirm the tasks still target the intended region (the `invocation` key in results is only added when `inject_invocation` is enabled, a setting added in ansible-core 2.21 that defaults to false).
- [ ] A task that overrides a default uses its own value, not the default.

## Checked
Checked 2026-10-25 against ansible-documentation devel (commit of 2026-10-21) playbook_guide/playbooks_module_defaults.rst and playbooks_environment.rst, and ansible-core devel `config/base.yml` (INJECT_INVOCATION, 2.21, default false). Confirmed: play, block and task scope, task arguments overriding defaults, the empty-dict reset, action groups via `meta/runtime.yml`, the fully qualified group name requirement, the special group list, role propagation note, and `environment` scope. Removed unconfirmed claims about group-versus-module precedence, `ansible.netcommon.network_cli` as an action group, typo behaviour, deprecations, ad hoc limits and lookups, and the `module_args` verification.
Method: documentation only; no commands were run.
