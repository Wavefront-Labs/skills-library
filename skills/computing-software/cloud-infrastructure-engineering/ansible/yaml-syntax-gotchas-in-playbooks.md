---
id: computing-software.cloud-infrastructure-engineering.ansible.yaml-syntax-gotchas-in-playbooks
name: yaml-syntax-gotchas-in-playbooks
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, playbook-syntax, yaml-syntax, yaml-quoting, folded-scalars, literal-block, yaml-booleans]
level: practitioner
status: docs-checked
description: "Avoid YAML traps in Ansible: quoting values that start with {{, colons in strings, yes/no booleans, octal modes, and choosing | literal vs > folded block scalars."
sources: ["YAML syntax (https://docs.ansible.com/ansible/latest/reference_appendices/YAMLSyntax.html)", "Configuration settings, DUPLICATE_YAML_DICT_KEY (https://github.com/ansible/ansible/blob/devel/lib/ansible/config/base.yml)", "ansible-lint rule risky-octal (https://github.com/ansible/ansible-lint/blob/main/src/ansiblelint/rules/risky_octal.md)", "ansible-lint yaml rules (https://github.com/ansible/ansible-lint/blob/main/src/ansiblelint/rules/yaml.md)", "yamllint truthy rule (https://github.com/adrienverge/yamllint/blob/master/yamllint/rules/truthy.py)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# YAML syntax gotchas in playbooks

## Quote a value that starts with {{
```yaml
app_path: {{ base }}/app        # WRONG: YAML parses { as a dict -> syntax error
app_path: "{{ base }}/app"      # right
```
Only the start matters: `msg: Path is {{ base }}` is fine unquoted.

## Colons and hashes
`: ` (colon-space) starts a mapping, ` #` starts a comment:
```yaml
msg: Error: disk full          # parse error -> quote it
msg: "Error: disk full"
url: http://x/#anchor          # '#' without leading space is fine; ' #' is not
```

## Booleans and implicit typing
Under YAML 1.1 rules `yes/no/on/off` as well as `true/false` (in several capitalisations) are booleans; the Ansible docs recommend lowercase `true`/`false`:
```yaml
country: NO          # becomes False
country: "NO"
enabled: true        # lowercase true/false only; ansible-lint flags other spellings as yaml[truthy]
```
Quote values that must stay strings, such as version numbers. For file modes, ansible-lint's
`risky-octal` rule notes that the YAML loader reads unquoted `0644` as the decimal number 420 and
`644` as something very different, so always write `mode: "0644"` (or a symbolic mode such as `u=rw,g=r,o=r`).

## Block scalars
```yaml
script: |              # literal: newlines kept -> use for shell scripts, file content
  set -e
  make install
description: >         # folded: newlines become spaces -> long prose, long when: lines
  This is one long
  line of text.
```
A `shell:` with `>` joins lines into one command — fine for one long command, wrong for multi-statement scripts.

## Jinja inside block scalars
`when:` and `that:` are already Jinja expressions — no `{{ }}`. Long conditions:
```yaml
when: >
  ansible_facts.os_family == 'RedHat'
  and ansible_facts.distribution_major_version | int >= 8
```

## Indentation and lists
Indent with spaces, never tabs (ansible-lint `no-tabs`). A list of dicts:
```yaml
loop:
  - {name: alice, uid: 1001}
  - name: bob
    uid: 1002
```
By default Ansible warns about a duplicate key in a mapping (`duplicate_dict_key` in `[defaults]` can be `warn`, `error` or `ignore`); ansible-lint reports `yaml[key-duplicates]`.

## Tools
- `ansible-playbook --syntax-check site.yml` — parse plus structure.
- `ansible-lint` runs yamllint-based rules (`yaml[truthy]`, `yaml[octal-values]`, `yaml[key-duplicates]`) as well as `risky-octal` and `no-tabs`.

## Verify
- [ ] `ansible-lint` and `--syntax-check` clean.
- [ ] No `risky-octal` or `yaml[truthy]` findings.

## Checked

Checked 2026-10-26 against ansible-documentation main (2026-10-21), ansible-core 2.21.5 and the ansible-lint and yamllint sources.
- Confirmed in the Ansible YAML page: `": "` starts a mapping and `" #"` a comment, a value starting with `{` must be quoted, `|` keeps newlines and `>` folds them, lowercase `true`/`false` is recommended.
- Confirmed: duplicate keys warn by default (`DUPLICATE_YAML_DICT_KEY`, `warn`/`error`/`ignore`); ansible-lint rules `risky-octal` (unquoted `0644` loads as decimal 420), `yaml[truthy]`, `yaml[key-duplicates]`, `yaml[octal-values]`, `no-tabs`; yamllint documents that YAML 1.1 treats `yes/no/on/off` as truthy.
- Removed as unconfirmed: the chomping indicators, the float example, the `python -c` and yamllint command lines, and the claim that unquoted octal values are fine for file modules.

Method: documentation only; no commands were run.
