---
id: computing-software.cloud-infrastructure-engineering.ansible.rendering-templates-and-inventory-without-applying
name: rendering-templates-and-inventory-without-applying
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, render-test, template-render-check, ansible-inventory, check-mode, golden-files, jinja2, ci-testing]
level: practitioner
status: docs-checked
description: "Render Jinja templates and resolved inventory variables locally without touching hosts, diff them against golden files in CI, and catch undefined variables before deploy."
sources: ["https://docs.ansible.com/projects/ansible/latest/cli/ansible-inventory.html", "https://docs.ansible.com/projects/ansible/latest/collections/ansible/builtin/template_module.html", "https://docs.ansible.com/projects/ansible/latest/reference_appendices/config.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Rendering templates and inventory without applying

Goal: see exactly what config each host would get and which variable values it resolves —
on a laptop or in CI, with no SSH to production.

## 1. Inventory: resolved variables per host
```bash
ansible-inventory -i inventories/prod --host web01 --yaml          # one host
ansible-inventory -i inventories/prod --list --yaml --output prod-inventory.yml
ansible-inventory -i inventories/prod --graph --vars                # tree with vars
```
`--vars` only has an effect together with `--graph`. `--host` and `--graph` ignore `--limit`.
With `--list`, `--export` gives a representation optimised for export rather than an
accurate picture of how Ansible processed the inventory. Vault-encrypted vars can be
supplied with `--vault-id` or `--vault-password-file`.

## 2. Templates: render to a local directory
`render.yml`:
```yaml
- hosts: "{{ target | default('all') }}"
  gather_facts: false          # facts come from the committed fact cache below
  tasks:
    - ansible.builtin.file: {path: "rendered/{{ inventory_hostname }}", state: directory}
      delegate_to: localhost
    - ansible.builtin.template:
        src: roles/nginx/templates/nginx.conf.j2
        dest: "rendered/{{ inventory_hostname }}/nginx.conf"
      delegate_to: localhost
```
Facts: point a jsonfile fact cache at a committed directory so rendering is deterministic and
needs no connection (verify on your version that cached facts are used with `gather_facts: false` before relying on this):
```bash
export ANSIBLE_CACHE_PLUGIN=jsonfile ANSIBLE_CACHE_PLUGIN_CONNECTION=tests/facts
ansible -i inventories/stage web01 -m setup > /dev/null     # once, from a reachable host; sanitise and commit tests/facts/
ansible-playbook -i inventories/prod render.yml -e target=web
diff -ru tests/golden rendered
```
The fact cache expires after `ANSIBLE_CACHE_PLUGIN_TIMEOUT` seconds (default 86400), so
set a long timeout for a committed cache.

## 3. Fail on undefined variables
Undefined variables fail templating by default (`error_on_undefined_vars` / `ANSIBLE_ERROR_ON_UNDEFINED_VARS`
is deprecated and documented as no longer used). Watch `default()` filters masking typos: `{{ prot | default(80) }}`.

## 4. Check mode + diff against real hosts (when allowed)
`ansible-playbook site.yml --check --diff --limit web01` renders on the target and shows
the diff without writing — but it needs connectivity and modules that support check mode.

## CI pattern
Render for every inventory (dev, stage, prod), commit golden files, and fail the PR when the
rendered output changes unexpectedly; reviewers see the real config diff in the PR, not just
the Jinja diff.

## Gotchas
- Templates using `lookup()` against live services (Vault, DNS) need stubs or env-specific test vars in CI.
- Rendering without `hostvars` of other hosts (e.g. upstream lists built from `groups['web']`) requires the full inventory, not `--limit`.
- `ansible_managed` can describe the template name, host and modification time (configurable in the `defaults` section of `ansible.cfg`); use a static string so golden files do not change every run.

## Verify
- [ ] `ansible-inventory --host` output for a sample host matches expectations from group_vars/host_vars.
- [ ] Changing a group var causes the golden diff to fail in CI for exactly the affected hosts.

## Checked
2026-11-01. Confirmed against the ansible-inventory CLI page (`--host`, `--list`, `--graph`, `--vars` graph-only, `--export`, `--yaml`, `--output`, vault options, limit ignored), the config reference (`ANSIBLE_CACHE_PLUGIN`, `_CONNECTION`, `_TIMEOUT` default 86400; `error_on_undefined_vars` deprecated), the template module page (`ansible_managed`) and the check mode and diff mode page (`--check --diff --limit`, modules without check mode do nothing). Removed: `--vars` with `--list`, vault failure claim, undefined-facts claim, cache timeout of 0.
Method: documentation only; no commands were run.
