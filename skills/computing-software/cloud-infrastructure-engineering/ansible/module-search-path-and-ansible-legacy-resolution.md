---
id: computing-software.cloud-infrastructure-engineering.ansible.module-search-path-and-ansible-legacy-resolution
name: module-search-path-and-ansible-legacy-resolution
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, modules-fqcn, module-search-path, ansible-legacy-namespace, library-path]
level: advanced
status: docs-checked
description: "Understand how Ansible resolves module names: FQCN, the collections keyword, ansible.legacy, library dirs and role library folders, and how shadowing happens."
sources: ["https://docs.ansible.com/ansible/latest/dev_guide/developing_locally.html", "https://docs.ansible.com/ansible/latest/collections_guide/collections_using_playbooks.html", "https://docs.ansible.com/ansible/latest/reference_appendices/config.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Module search path and ansible.legacy

## How a short name resolves
- The `collections:` keyword (play, role or block; a role's `meta/main.yml` can set its own) is an ordered search path for unqualified module and action names. Roles do not inherit the calling playbook's list, and roles inside a collection search their own collection first.
- If you omit `ansible.builtin` from the list, ansible-core builtin content and support for older third-party plugin paths remain available by default.
- Standalone local modules are picked up from `library/` next to the playbook, `library/` inside a role, and the `DEFAULT_MODULE_PATH` setting (`[defaults] library`, env `ANSIBLE_LIBRARY`, `-M`). The default path is `~/.ansible/plugins/modules:/usr/share/ansible/plugins/modules` (under the Ansible home directory).
- To use your own version of a builtin module such as `copy`, call it as `ansible.legacy.copy`; the docs say `ansible.legacy` is required to override an `ansible.builtin` module when using FQCNs.

## Inspect
```bash
ansible-doc -F copy                         # which file 'copy' resolves to
ansible-config dump | grep -E 'DEFAULT_MODULE_PATH|COLLECTIONS_PATHS'
```

## Local modules on purpose
```
project/
  library/my_check.py          # standalone module, available to playbooks in this directory
  filter_plugins/acme.py       # non-module plugins live in a directory named for the plugin type
```
Better long term: move them into a collection (`acme.ops.my_check`) so they are versioned and testable.

## Gotchas
- A collection named in `collections:` that also has `copy` wins over builtin for short names.

## Verify
- [ ] `ansible-doc -F <name>` points to the file you intend for every short-name module still in use.

## Checked

- Date: 2026-10-26. Documentation release: ansible-core stable-2.22 documentation and source (docs and lib/ branch stable-2.22, checked 2026-10-26; 2.21 is the latest GA release, 2.22 GA is scheduled for Nov 2026).
- Confirmed in docs/docsite/rst/dev_guide/developing_locally.rst: DEFAULT_MODULE_PATH and ANSIBLE_LIBRARY, adjacent library directories for playbooks and roles, plugin directories named for the plugin type, `ansible.legacy` is needed to access a custom version of an `ansible.builtin` module (for example `ansible.legacy.copy`).
- Confirmed in collections_guide/collections_using_playbooks.rst: the collections keyword is an ordered search path, roles do not inherit the playbook list, collection roles search their own collection first, builtin content and older third-party plugin paths remain available when ansible.builtin is omitted; in config/base.yml: DEFAULT_MODULE_PATH default and env ANSIBLE_LIBRARY, COLLECTIONS_PATHS.
- Removed unconfirmed claims: the exact resolution order across legacy and builtin, shadowing of short names, module_utils import path, ansible-lint and execution-environment remarks, the `ansible --version` module path line.

Method: documentation only; no commands were run.
