---
id: computing-software.cloud-infrastructure-engineering.ansible.string-filters-split-join-regex-and-quoting
name: string-filters-split-join-regex-and-quoting
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, filters, string-filters, split-join, regex-replace, regex-search, quote, b64encode]
level: practitioner
status: docs-checked
description: "Transform strings in Ansible with split, join, replace, regex_replace, regex_search, regex_findall, trim, quote, b64encode and hash filters, with the common capture-group traps."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_filters.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/split_filter.html", "https://github.com/ansible/ansible-documentation", "https://github.com/ansible/ansible"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# String filters

## Split and join
```yaml
"{{ 'a,b,c' | split(',') }}"          # ['a','b','c']   (ansible.builtin.split, added in 2.11)
"{{ my_list | join(',') }}"
"{{ path | basename }}" / "{{ path | dirname }}" / "{{ fname | splitext }}"
"{{ 'k1=v1;k2=v2' | split(';') | map('split', '=') | community.general.dict }}"   # → {k1: v1, k2: v2}
```

## Replace and regex
```yaml
"{{ hostname | replace('-', '_') }}"
"{{ url | regex_replace('^https?://([^/]+).*$', '\\1') }}"         # host part
"{{ version_string | regex_search('(\\d+)\\.(\\d+)', '\\1', '\\2') }}"  # list of groups
"{{ log | regex_findall('ERROR: (.*)') }}"                          # all matches
"{{ name is match('^web\\d+$') }}"  /  is search('...')  /  is regex('...')    # tests, not filters
```
- Escaping: inside a YAML double-quoted value, YAML consumes one level of backslashes, so the regex `\d` is written `\\d` (as above). In a YAML single-quoted or block scalar value, write `\d`. Test the exact string with `debug` before trusting it.
- `regex_search` returns `None` when nothing matches — wrap with `| default('')` if you need a string.
- With group arguments, `regex_search` returns a **list** of the requested groups.
- `regex_search`, `regex_findall` and `regex_replace` accept `multiline=True` and `ignorecase=True`, or inline flags such as `(?im)`.
- Named groups work in the group arguments: `'\\g<host>'`.

## Trimming and case
`trim`, `lower`, `upper`, `capitalize`, `title`, `center(80)`, `truncate(20)`, `wordcount`,
`"{{ s[:8] }}"` slicing, `"{{ 'x' ~ number }}"` to concatenate non-strings (`~`, not `+`).

## Shell and data safety
```yaml
"{{ user_input | quote }}"            # shell-escape for command/shell
"{{ secret | b64encode }}" / b64decode
"{{ 'text' | hash('sha256') }}" / checksum / password_hash('sha512', salt)
"{{ s | urlencode }}", "{{ path | urlsplit('hostname') }}"
"{{ s | to_json }}" for embedding a string safely in JSON
```

## Gotchas
- `replace` is literal; for patterns use `regex_replace`.
- `regex_replace` backreferences are written `'\\1'` or, for named groups, `'\\g<name>'`.
- `urlsplit` with no argument returns a dictionary of all URL fields (scheme, netloc, hostname, port, path, query, fragment, username, password).

## Verify
- [ ] A `debug` task printing the filter expression on sample input gives the expected string before you use it in a real task.

## Checked
Date: 2026-10-24. Documentation: Ansible playbook guide, Filters (playbooks_filters.rst), ansible-core plugins/filter docs, Templating now() page, Jinja filters.py; Tests page.
Confirmed:
- split added 2.11; regex_search returns None on no match and a list with group arguments; regex_findall, regex_replace and regex_search take multiline and ignorecase or inline flags; named group references; urlsplit fields; match, search and regex are tests.
- Removed the Python .split method claim, whitespace-split claim and CR/trailing-space note.

Method: documentation only; no commands were run.
