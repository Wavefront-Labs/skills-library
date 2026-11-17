---
id: computing-software.cloud-infrastructure-engineering.ansible.using-collection-filters-lookups-and-tests-by-fqcn
name: using-collection-filters-lookups-and-tests-by-fqcn
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, collections-usage, collection-filters-fqcn, filters, lookups]
level: intro
status: docs-checked
description: "Call filters, tests and lookups from collections by FQCN (ansible.utils.ipaddr, community.general.json_query), find their docs, and handle the collections keyword limits."
sources: ["https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/collections_guide/collections_using_playbooks.rst", "https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/config/ansible_builtin_runtime.yml", "https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/cli/doc.py", "https://github.com/ansible-collections/ansible.utils/blob/main/plugins/filter/ipaddr.py", "https://github.com/ansible-collections/community.general/blob/main/plugins/filter/json_query.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Collection filters, lookups and tests by FQCN

```yaml
- ansible.builtin.debug:
    msg:
      - "{{ '192.0.2.0/24' | ansible.utils.ipaddr('network') }}"
      - "{{ servers | community.general.json_query('[?state==`running`].name') }}"
      - "{{ lookup('community.hashi_vault.hashi_vault', 'secret=secret/hello:value') }}"
      - "{{ my_ip is ansible.utils.in_network('10.0.0.0/8') }}"
      - "{{ data | community.general.dict_kv('name') }}"
```

## Rules
- Builtin filters and tests (`default`, `regex_replace`, `to_json`, `version`) work without a prefix; the FQCN form such as `ansible.builtin.regex_replace` also works.
- Collection plugins need their FQCN. The `collections:` keyword only gives modules, action plugins and roles a search path: the Using collections in playbooks page states that "an FQCN is still required for non-action or module plugins (for example, lookups, filters, and tests)".
- Some names that were once in core moved to collections. ansible-core keeps redirects in its built-in runtime metadata, for example `json_query` redirects to `community.general.json_query`, but use the FQCN in new content. The IP filters are in `ansible.utils` (`ansible.utils.ipaddr`).

## Find them
```bash
ansible-doc -t filter -l community.general
ansible-doc -t filter ansible.utils.ipaddr
ansible-doc -t test -l ansible.utils
ansible-doc -t lookup -l community.general
```
`ansible-doc -l` and `-F` accept collection names to restrict the listing.

## Python dependencies
Many collection filters need libraries on the **control node** (or in the execution environment): `json_query` needs `jmespath` (error: `You need to install "jmespath" prior to running json_query filter`), and `ipaddr` needs `netaddr`.

## Gotchas
- Filter, test and lookup plugins run on the controller; install their dependencies there, not on targets.
- The collection must be installed (or present in the execution environment) for the FQCN to resolve.

## Verify
```bash
ansible localhost -m ansible.builtin.debug -a "msg={{ '192.0.2.10/24' | ansible.utils.ipaddr('address') }}"
```

## Checked
Date 2026-10-24. Release: ansible-core 2.21.5 (source at tag v2.21.5) and the ansible-documentation main branch. Confirmed: the FQCN-required statement on the Using collections in playbooks page; the `json_query` redirect in `lib/ansible/config/ansible_builtin_runtime.yml`; the existence of `ansible.utils` ipaddr, nthhost and in_network, `community.general` json_query and dict_kv, and the hashi_vault `secret=path:key` form in the collection sources on GitHub; the jmespath error text in json_query source; `ansible-doc` collection filtering in `cli/doc.py`. Removed the claim that `collections:` applies to filters and lookups (it does not) and the `ansible.netcommon.ipaddr` statement.
Method: documentation only; no commands were run.
