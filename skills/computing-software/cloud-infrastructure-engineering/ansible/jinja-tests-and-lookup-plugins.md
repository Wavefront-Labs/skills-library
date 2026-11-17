---
id: computing-software.cloud-infrastructure-engineering.ansible.jinja-tests-and-lookup-plugins
name: jinja-tests-and-lookup-plugins
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, tests, jinja-tests, lookups, lookup-plugins, query, lookup, file-lookup, template-lookup, env-lookup, password-lookup, pipe-lookup, fileglob, first-found, with-first-found, ini-lookup, csvfile, url-lookup, vars-lookup, varnames, is-version, is-match, is-search, is-subset, is-abs, wantlist, errors-ignore, lookup-security, path-tests, vault-encrypted-test, truthy]
level: practitioner
status: docs-checked
description: "Use Ansible Jinja tests (is failed, is version, is match, is subset) in when/assert, and lookup plugins (file, template, env, password, first_found, pipe, url) to pull control-node data safely."
sources: ["https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/playbook_guide/playbooks_tests.rst", "https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/plugins/lookup.rst", "https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/plugins/lookup/password.py", "https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/plugins/lookup/first_found.py", "https://github.com/ansible/ansible/blob/v2.21.5/lib/ansible/plugins/test/core.py", "https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/porting_guides/porting_guide_core_2.19.rst"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Jinja tests and lookup plugins

**Goal:** conditions that read as English and never trip on a missing key, and data
pulled from the control node (files, env, secret stores) in the one expression that
needs it. Tests and lookups both run on the control node, not on the managed node.

## 1. Tests: `x is <test>`
Tests return booleans and belong in `when`, `assert`, and the `select`/`reject`/`selectattr`/`rejectattr` filters.
| Test | Use |
|---|---|
| `is defined` / `is undefined` | guard optional vars |
| `is failed` / `is succeeded` / `is changed` / `is skipped` / `is unreachable` | registered results (aliases include `success`, `change`, `skip`) |
| `is version('2.4', '>=')` (alias `version_compare`) | loose comparison by default; `strict=true` uses StrictVersion; `version_type` takes `loose`, `strict`, `semver`, `semantic`, `pep440` (mutually exclusive with `strict`) |
| `is match('^web')` / `is search('db')` / `is regex('...', ignorecase=true)` | `match` anchors at the start, `search` matches anywhere, `regex` defaults to search and also takes `multiline` and `match_type` (`match`, `search`, `fullmatch`) |
| `is subset(l)` / `is superset(l)` / `is contains(x)` | list relations; `contains` is the reverse of Jinja's `in` and is designed for `selectattr` |
| `is truthy` / `is falsy` | Python truthiness; add `convert_bool=true` to treat `yes`/`no`, `on`/`off`, `0`/`1` as booleans |
| `is exists` / `is directory` / `is link` / `is mount` / `is abs` (and `is file`) | paths on the **control node** |
| `is vault_encrypted` | detect an inline vaulted value |
| `is any` / `is all` | list of conditions |
| `is ansible.utils.in_network('10.0.0.0/8')` | IP test from the `ansible.utils` collection |
All standard Jinja2 tests (`string`, `mapping`, `iterable`, `none`, ...) are also available. Negate with `is not`.
Example: `when: openssl_version is version('3.0', '<')`.

## 2. Lookups: control-node data on demand
`lookup('plugin', arg, ...)` returns a string (comma-joined) unless `wantlist=True`;
`query('plugin', ...)` (short form `q()`) always returns a list, so use `query` with `loop`.
```yaml
pubkey: "{{ lookup('file', '~/.ssh/id_ed25519.pub') }}"
rendered: "{{ lookup('template', 'templates/motd.j2') }}"
api_key: "{{ lookup('env', 'API_KEY') | mandatory }}"
db_pass: "{{ lookup('password', 'credentials/' + inventory_hostname + '/db length=24 chars=ascii_letters,digits') }}"
git_sha: "{{ lookup('pipe', 'git rev-parse --short HEAD') }}"
config_src: "{{ lookup('first_found', params) }}"
# vars:
params:
  files: ["{{ inventory_hostname }}.conf", "{{ ansible_facts.os_family }}.conf", "default.conf"]
  paths: [files/]
  skip: true        # return an empty list instead of failing when nothing matches
value: "{{ lookup('ini', 'timeout section=server file=app.ini') }}"
row:   "{{ lookup('csvfile', 'db01 file=hosts.csv delimiter=, col=2') }}"
body:  "{{ lookup('url', 'https://ip.example/json', split_lines=false) | from_json }}"
val:   "{{ lookup('vars', 'port_' + env) }}"          # indirect variable by name
names: "{{ query('varnames', '^app_.*') }}"
```
- `password` stores the generated password in the given path on the control node and re-reads it on later runs, so it is repeatable. Options: `length` (default 20), `chars` (default letters, digits and `.,:-_`), `encrypt` (`md5_crypt`, `bcrypt`, `sha256_crypt`, `sha512_crypt`) for a hashed form. Keep that directory out of git or vault it.
- `first_found` takes `files`, `paths` and `skip`; `skip: true` returns an empty list instead of failing, which is what makes `with_first_found` skip the task.
- `pipe` runs a command on the control node each time the expression is evaluated.
- Every lookup accepts `errors=` with `ignore`, `warn` or `strict` (default `strict`). The `file` lookup has `rstrip` (default true) and `lstrip` (default false); `rstrip=false` keeps the trailing newline.
- External stores: `community.hashi_vault.hashi_vault`, `amazon.aws.secretsmanager_secret` (the old name `aws_secret` is a redirect), `community.general.onepassword`, `community.sops.sops`.

## 3. Lookups vs modules
Lookups run on the **control node** at template time, with no `changed` result. To read a file from a managed node use `ansible.builtin.slurp` (+ `| b64decode`) or `fetch`; to run a command there use `command`.

## 4. Safety
Since ansible-core 2.19 only strings from a trusted source are rendered as templates, and newly created string results (such as lookup output) do not get trust automatically, so a lookup of a file that contains `{{ ... }}` returns it unrendered. Printing a secret with `debug` still leaks it; put `no_log: true` on tasks that handle secret lookups.

## Gotchas
- `is version` with `strict=true` rejects versions that are not 2 or 3 numeric parts plus an optional `a`/`b` pre-release tag; use `version_type='semver'` or `'pep440'` when you need those rules.
- `lookup('env', 'HOME')` returns the environment of the process running Ansible: inside an execution environment that is the container's environment.
- `lookup('env', 'X')` has a `default` option; without it an unset variable gives an empty string, which `mandatory` does not catch (it only tests for undefined).

## Verify
- [ ] `first_found` returns the expected file for each OS family, and an empty list when `skip: true` and nothing matches.
- [ ] Two runs with the `password` lookup produce the same password and no `changed` on the user task.
- [ ] `ansible-doc -t test -l` lists the test you rely on in the core version you pin.

## Checked
Date 2026-10-24. Release: ansible-core 2.21.5 (source at tag v2.21.5) and the ansible-documentation main branch. Confirmed: test names, aliases and options (`version` strict and `version_type`, `regex` options, `truthy` `convert_bool`, `contains`, path tests including `directory`, not `dir`) in the plugin DOCUMENTATION blocks and the Tests page; lookup options for `password`, `first_found`, `file`, `csvfile`, `ini`, `url`, `env`, `vars`, `varnames`; the lookup `errors` setting and `query`/`wantlist` on the Lookups page; the 2.19 template trust model in the 2.19 porting guide; `aws_secret` redirecting to `secretsmanager_secret` in amazon.aws `meta/runtime.yml`.
Method: documentation only; no commands were run.
