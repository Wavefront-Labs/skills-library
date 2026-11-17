---
id: computing-software.cloud-infrastructure-engineering.ansible.generating-role-docs-from-argument-specs
name: generating-role-docs-from-argument-specs
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, iac-documentation, aar-doc, argument-specs, role-readme]
level: practitioner
status: docs-checked
description: "Generate role README documentation from meta/argument_specs.yml with aar-doc or ansible-doc -t role, keep it in sync in CI, and document defaults and examples."
sources:
  - "https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse_roles.html#role-argument-validation"
  - "https://github.com/telekom-mms/aar_doc"
  - "https://docs.ansible.com/ansible/latest/cli/ansible-doc.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Role docs from argument_specs

`meta/argument_specs.yml` (or `.yaml`) both validates role inputs at runtime and is the best source for docs. Role argument validation exists from Ansible 2.11: a validation task is inserted at the start of role execution, and the role fails if the parameters do not match the specification. The spec sits in a top-level `argument_specs` block, with one key per entry point (`main` when unspecified).

```yaml
# roles/nginx/meta/argument_specs.yml
argument_specs:
  main:
    short_description: Install and configure NGINX
    description: [Installs NGINX from distro packages and manages vhosts.]
    author: [Platform Team]
    options:
      nginx_port:
        type: int
        default: 80
        description: Port for the default server.
      nginx_vhosts:
        type: list
        elements: dict
        default: []
        description: Virtual hosts to configure.
        options:
          name: {type: str, required: true, description: Server name.}
          root: {type: path, description: Document root.}
```

## Read it with ansible-doc
`ansible-doc` accepts role as a target type (`-t role`) and `-r` / `--roles-path` for where to look:
```bash
ansible-doc -t role -r roles nginx
ansible-doc -t role acme.platform.nginx       # role inside a collection
```

## Generate README with aar-doc
`aar-doc` reads `meta/main.yml` and `meta/argument_specs.yml`; the only output format is Markdown. Usage is `aar-doc [OPTIONS] ROLE_PATH COMMAND`, with commands `markdown` and `defaults`.
```bash
pip install aar-doc
aar-doc roles/nginx markdown                       # injects into README.md
aar-doc --output-mode replace roles/nginx markdown # overwrites the whole file
```
Defaults: `--output-file README.md`, `--output-mode inject`, config file `.aar_doc.yml`. In `inject` mode it rewrites only the content between `<!-- BEGIN_ANSIBLE_DOCS -->` and `<!-- END_ANSIBLE_DOCS -->`, leaving hand-written text outside the markers; if the file does not exist it falls back to `replace`. A custom Jinja2 template (`--output-template`) must itself start and end with those marker comments for injection to work. The `defaults` command writes `defaults/main.yml` from the argument specs.

## Keep in sync
```yaml
# CI step
- run: |
    for r in roles/*/; do aar-doc "$r" markdown; done
    git diff --exit-code -- roles/*/README.md || (echo "Role docs out of date: run aar-doc" && exit 1)
```

## Gotchas
- `argument_specs` `default` is documentation only. The actual default always comes from the role's `defaults/`; the Ansible docs say to ensure the two match.
- If the spec defines the same option default more than once, aar-doc uses the first found unless you pass `--overwrite-duplicates` (for the `defaults` command).
- For ansible-lint compatibility, write booleans as `true` / `false`.

## Verify
- [ ] CI fails when argument_specs change without regenerated README.

## Checked

2026-11-09. Checked against the Ansible "Roles" page (role argument validation, 2.11 gate, spec format, default note), the aar-doc README on GitHub (usage line, defaults, inject/replace modes, markers, templating, defaults command) and the ansible-doc source (`-r/--roles-path`, `role` target type).

Removed as unsupported: the claim that antsibull-docs renders role argument specs on the docs site.

Method: documentation only; no commands were run.
