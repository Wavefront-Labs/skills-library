---
id: computing-software.cloud-infrastructure-engineering.ansible.deprecated-modules-and-collection-redirects
name: deprecated-modules-and-collection-redirects
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, modules-fqcn, module-redirects, deprecated-modules, fqcn, runtime-yml, plugin-routing]
level: practitioner
status: docs-checked
description: "Find which collection a short module name now routes to, fix deprecation warnings, and migrate playbooks after modules move or are removed between collection versions."
sources: ["Collection structure, meta/runtime.yml (https://docs.ansible.com/ansible/latest/dev_guide/developing_collections_structure.html)", "ansible-core builtin runtime routing (https://github.com/ansible/ansible/blob/devel/lib/ansible/config/ansible_builtin_runtime.yml)", "ansible-core plugin loader (https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/loader.py)", "ansible-lint fqcn rule (https://github.com/ansible/ansible-lint/blob/main/src/ansiblelint/rules/fqcn.md)", "Using collections in playbooks (https://docs.ansible.com/ansible/latest/collections_guide/collections_using_playbooks.html)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deprecated modules and collection redirects

Since Ansible 2.10, most modules live in collections. ansible-core ships
`lib/ansible/config/ansible_builtin_runtime.yml`, which redirects old short names
(e.g. `mysql_user` → `community.mysql.mysql_user`). Collections have their own
`meta/runtime.yml` with `plugin_routing` entries: `redirect`, `deprecation` (warning text plus removal version or date) and `tombstone` (fatal error message plus removal version or date).

## Find out where a name resolves
```bash
ansible-playbook site.yml -vvv 2>&1 | grep -i redirect   # "redirecting (type: modules) ... to ..." (logged at -vv or -vvv)
```
Inspect routing directly by reading `ansible_builtin_runtime.yml` inside the installed `ansible/config/` directory (look under `plugin_routing` → `modules`).

## Messages you will see
- `[DEPRECATION WARNING]: ... has been deprecated.` followed by the collection's warning text and removal version or date — plan the change before upgrading the collection past that version.
- `The 'foo' module has been removed.` followed by the tombstone text — the plugin is tombstoned. If the name does not resolve at all, the collection may not be installed. Check `meta/runtime.yml` of the collection.
- Collection split (e.g. `community.general` docker modules → `community.docker`): install the new collection and update FQCNs.

## Migration procedure
1. Pin current collection versions in `requirements.yml`.
2. Run `ansible-lint` with the `fqcn` rule; `ansible-lint --fix` can autofix it (rule ids include `fqcn[action-core]`, `fqcn[action]`, `fqcn[canonical]`, `fqcn[keyword]`).
3. Run the playbook with `-vvv` in check mode and grep for `redirecting` and `DEPRECATION`.
4. Read the collection changelog for "Removed Features" / "Breaking Changes" between pinned and target versions (`changelogs/changelog.yaml` or the Ansible package porting guide).
5. Bump versions, fix, re-test in Molecule/CI.

Turn deprecation warnings into a CI signal: keep `ANSIBLE_DEPRECATION_WARNINGS` at its default (true) and fail the job when the log contains `DEPRECATION WARNING`.

## Gotchas
- Short names resolve through the `collections:` keyword search list first; a role with `collections: [community.general]` can pick a different module than you expect. FQCN removes ambiguity.
- `ansible.legacy` refers to the plugin-finding behaviour used before collections existed (built-in plugins plus local ones); prefer FQCNs.
- A redirect or tombstone change in a new ansible-core release can break playbooks that still use the short name even though nothing in your repo changed — FQCN everywhere prevents that.

## Verify
- [ ] No `redirecting` lines at `-vvv`; no deprecation warnings in a full check-mode run.
- [ ] ansible-lint `fqcn` clean.

## Checked

Checked 2026-10-26 against ansible-core devel (`ansible_builtin_runtime.yml`, `plugins/loader.py`, `config/base.yml`), the collection structure documentation and the ansible-lint `fqcn` rule page. Confirmed: builtin redirects such as `mysql_user` to `community.mysql.mysql_user`, `plugin_routing` keys `redirect`, `deprecation`, `tombstone`, the "redirecting (type: ...)" log line, deprecation and removal message wording, `ANSIBLE_DEPRECATION_WARNINGS` default, `fqcn[...]` rule ids and `--fix`. Removed unconfirmed `ansible-doc` output claims, the `couldn't resolve` error text and the inline Python snippet.

Method: documentation only; no commands were run.
