---
id: computing-software.cloud-infrastructure-engineering.ansible.capturing-existing-hosts-into-ansible-inventory-and-roles
name: capturing-existing-hosts-into-ansible-inventory-and-roles
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, brownfield-import, config-capture, host-discovery, adoption]
level: practitioner
status: docs-checked
description: "Adopt brownfield servers: discover hosts into inventory (cloud APIs, nmap), capture existing config files with fetch, then converge safely using check and diff mode."
sources: ["https://docs.ansible.com/ansible/latest/collections/ansible/builtin/fetch_module.html", "https://docs.ansible.com/ansible/latest/collections/community/general/nmap_inventory.html", "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_checkmode.html", "https://docs.ansible.com/ansible/latest/cli/ansible-inventory.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/template_module.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/setup_module.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Capturing existing hosts into Ansible

## 1. Discover hosts
- Cloud: use the cloud provider's inventory plugin (for example `amazon.aws.aws_ec2`) as the authoritative source.
- CMDB: use the CMDB's inventory plugin if the vendor ships one.
- Network scan for unknown estates:
```yaml
# discovery.nmap.yml
plugin: community.general.nmap
address: 10.20.0.0/22
exclude: [10.20.0.1]
```
```bash
ansible-inventory -i discovery.nmap.yml --list -y > discovered.yml
```
The nmap plugin needs the `nmap` CLI on the controller and the `community.general` collection (not in ansible-core); `ports` already defaults to true, and it can group hosts with `groups:` Jinja conditionals. Then classify hosts into groups from gathered facts (the `setup` module returns them under `ansible_facts`), and record ownership.

## 2. Capture current configuration
```yaml
- hosts: legacy_web
  gather_facts: false
  tasks:
    - ansible.builtin.fetch:
        src: "{{ item }}"
        dest: capture
      loop: [/etc/nginx/nginx.conf, /etc/nginx/conf.d/app.conf, /etc/sysctl.d/99-tuning.conf]
      become: true
```
`fetch` saves each file under `dest/<inventory hostname>/<remote path>` (default `flat: false`), so `src` must be a file, not a directory. With `become` it also uses `slurp` to checksum the file, which doubles the transfer, so avoid `become` where the file is readable without it. Diff the per-host trees against each other to find the common baseline and the per-host differences → template + host_vars.

## 3. Build the role, prove zero diff
```bash
ansible-playbook -i inventory web.yml --check --diff -l legacy_web
```
Check mode only reports changes for modules that support it, and skips output for tasks whose conditionals depend on registered results, so zero changes is evidence, not proof. Iterate until check mode shows **no changes** on the captured hosts: the role now describes reality. Only then start changing things (one change at a time, through code).

## 4. Read-only first
Start with fact gathering and reporting plays; then manage low-risk files; then services. Use `backup: true` on `template` and `copy` tasks (both take it) for the first real runs.

## Gotchas
- Captured files contain secrets (DB passwords): move them into vault before committing.
- Hosts that differ for no reason ("snowflakes") need an owner decision, not a host_vars entry per quirk.
- nmap discovery from the controller may trip IDS; coordinate with security.

## Verify
- [ ] `--check --diff` on all adopted hosts reports zero changes before the first managed change.

## Checked
Date: 2026-11-07. Pages read in full: ansible.builtin.fetch module, community.general.nmap inventory plugin, "Validating tasks: check mode and diff mode", ansible-inventory CLI; searched (not read in full) the template, copy and setup module pages for `backup` and fact parameters. Confirmed: nmap plugin options `address`, `exclude`, `ports`, `groups`, its `nmap` CLI requirement and that it is not in ansible-core; fetch parameters `src`/`dest`/`flat`, per-host directory layout and the become/slurp note; `--check`, `--diff`, `--limit`, `ansible-inventory --list` and `-y`; check mode skips output for tasks conditional on registered variables.
Corrected: the fetch example used `dest: capture/{{ inventory_hostname }}/` which would nest the hostname twice, now `dest: capture`; the claim that nmap `ports: true` needed setting (it is the default).
Removed as not on a cited page: the `azure_rm` and `vmware_vm_inventory` plugin names, the ServiceNow plugin (its docs page 404s), `group_by`, `package_facts` and `service_facts`, the `diff -r` command, and `serial: 1`.
Method: documentation only; no commands were run.
