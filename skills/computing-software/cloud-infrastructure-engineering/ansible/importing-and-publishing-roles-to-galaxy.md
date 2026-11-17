---
id: computing-software.cloud-infrastructure-engineering.ansible.importing-and-publishing-roles-to-galaxy
name: importing-and-publishing-roles-to-galaxy
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, ansible-galaxy, role-import, galaxy-role-publish, standalone-roles, meta-main, galaxy-api-key, github-actions]
level: practitioner
status: docs-checked
description: "Publish a standalone role to Galaxy: meta/main.yml requirements, ansible-galaxy role import from GitHub, tagging versions, CI-triggered imports and when to ship a collection instead."
sources: ["Galaxy developer guide (https://docs.ansible.com/ansible/latest/galaxy/dev_guide.html)", "Galaxy user guide (https://docs.ansible.com/ansible/latest/galaxy/user_guide.html)", "ansible-galaxy CLI source (https://github.com/ansible/ansible/blob/devel/lib/ansible/cli/galaxy.py)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Importing and publishing roles to Galaxy

Goal: a standalone role in a public GitHub repo becomes installable as
`ansible-galaxy role install <namespace>.<role>` at a pinned version.

## 1. Make the repo importable
- One role per repo, role content at the repo root (`tasks/`, `defaults/`, `meta/`).
- `meta/main.yml`:
```yaml
galaxy_info:
  role_name: nginx_hardened       # overrides the role name Galaxy would otherwise use
  namespace: acme                 # Galaxy namespace
  author: Platform Team
  description: Hardened nginx with TLS defaults
  license: MIT
  min_ansible_version: "2.15"
  platforms:
    - {name: EL, versions: ["8", "9"]}
    - {name: Ubuntu, versions: [jammy, noble]}
  galaxy_tags: [web, nginx, tls]
dependencies: []
```
- Add a README and a licence; run `ansible-lint` before importing.

## 2. Version with git tags
When the Galaxy server imports a role it imports any Git tags matching the Semantic Version format as versions. Tag and push before importing:
```bash
git tag 1.4.0 && git push origin 1.4.0
```

## 3. Import
The `import` command needs your Galaxy API token (from the Galaxy website's API token page; the token can also be saved in the path set by `GALAXY_TOKEN_PATH`). Keep it as a CI secret.
```bash
ansible-galaxy role import --token "$GALAXY_API_KEY" acme-org ansible-role-nginx-hardened
# args: <github_user_or_org> <github_repo>; --branch imports a non-default branch; --role-name overrides the name;
# --no-wait does not wait for results; --status checks the most recent import
```
CI on tag push (GitHub Actions):
```yaml
on: {push: {tags: ["*"]}}
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - run: pip install ansible-core
      - run: ansible-galaxy role import --token "${{ secrets.GALAXY_API_KEY }}" "${{ github.repository_owner }}" "${{ github.event.repository.name }}"
```
`ansible-galaxy role info acme.nginx_hardened` confirms the published versions.

## 4. Consumers pin it
```yaml
roles:
  - name: acme.nginx_hardened
    version: 1.4.0
```

## When to publish a collection instead
New shareable content usually belongs in a collection (modules, plugins, multiple roles). Galaxy role imports work from GitHub repositories.

## Gotchas
- Import pulls from GitHub, not your local checkout; unpushed commits are not published.
- Set `role_name` explicitly if the repository name differs from the role name you want (or pass `--role-name`).
- The old `ansible-galaxy login` command was removed in late 2020; an API token is required to publish roles or collections.

## Verify
- [ ] `ansible-galaxy role install acme.nginx_hardened,1.4.0 -p /tmp/r` succeeds in a clean venv.
- [ ] `ansible-galaxy role info acme.nginx_hardened` lists the role and the Galaxy page shows the new version.

## Checked

Checked 2026-10-26 against the Galaxy developer and user guides (import, versions from Semantic Version tags, `role info`) and ansible-core `cli/galaxy.py` (import options `--branch`, `--role-name`, `--no-wait`, `--status`, `--token`/`--api-key`, removal of `login`). Confirmed that import reads the GitHub repository, not a local checkout. Removed unconfirmed claims about role name derivation, tag character limits, lint scoring, `v` prefixed tags, repository rename behaviour, private hub role support and the import log location.

Method: documentation only; no commands were run.
