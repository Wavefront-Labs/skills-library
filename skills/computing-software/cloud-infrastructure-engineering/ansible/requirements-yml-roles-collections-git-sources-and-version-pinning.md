---
id: computing-software.cloud-infrastructure-engineering.ansible.requirements-yml-roles-collections-git-sources-and-version-pinning
name: requirements-yml-roles-collections-git-sources-and-version-pinning
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, ansible-galaxy, requirements-roles-collections, role-install, roles-from-git, collection-pinning, version-ranges, requirements-yml]
level: practitioner
status: docs-checked
description: "Write one requirements.yml with roles and collections from Galaxy, Automation Hub and git, pin exact versions or ranges, and install both sections reliably in CI."
sources: ["Using collections: requirements file (https://docs.ansible.com/ansible/latest/collections_guide/collections_installing.html)", "Galaxy user guide: roles requirements (https://docs.ansible.com/ansible/latest/galaxy/user_guide.html)", "Configuring the ansible-galaxy client (https://docs.ansible.com/ansible/latest/galaxy/user_guide.html)", "ansible-galaxy CLI source (https://github.com/ansible/ansible/blob/devel/lib/ansible/cli/galaxy.py)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# requirements.yml: roles, collections, git sources and pinning

```yaml
---
collections:
  - name: ansible.posix
    version: "1.6.2"                 # exact pin (recommended for production)
  - name: community.general
    version: ">=9.0.0,<10.0.0"       # range: allows minor/patch updates
  - name: amazon.aws
    version: "8.2.1"
    source: https://hub.example.com/api/galaxy/     # Galaxy server URL for this entry
  - name: https://git.example.com/platform/acme.internal.git
    type: git
    version: v2.3.0                  # tag, branch or commit
  - name: acme.internal
    type: file
    source: ./collections/acme-internal-2.3.0.tar.gz

roles:
  - name: geerlingguy.docker         # Galaxy role (namespace.role)
    version: "7.4.1"
  - name: hardening
    src: https://git.example.com/platform/ansible-role-hardening.git
    scm: git
    version: "3.1.0"
  - name: legacy_role
    src: https://artifacts.example.com/roles/legacy_role-1.0.tar.gz
```
Version operators for collections: `==`, `!=`, `>=`, `>`, `<=`, `<`, `*` (default); several can be combined with a comma. Pre-releases are ignored unless you require one explicitly with `==` (or use `--pre`). Ranges are not supported for roles: `version` is a release tag, commit hash or branch name. Only one version of a collection can be installed at a time. Use a `.yml` extension on the file name; other extensions are read as the old basic format.

## Installing both sections
```bash
ansible-galaxy install -r requirements.yml                    # roles AND collections when both keys are present
ansible-galaxy collection install -r requirements.yml -p ./collections
ansible-galaxy role install -r requirements.yml -p ./roles
```
`ansible-galaxy install -r` installs both, but when you specify a custom collection or role install path with that form the collections are skipped and each entry is processed like `ansible-galaxy role install` — install each type separately when you need custom paths. `--force` overwrites an existing install; `--upgrade` (collections) upgrades to the newest version allowed.

## Galaxy servers
```ini
# ansible.cfg
[galaxy]
server_list = hub, galaxy
[galaxy_server.hub]
url = https://hub.example.com/api/galaxy/        # must end with /
auth_url = https://sso.example.com/auth/realms/myco/protocol/openid-connect/token   # Keycloak token endpoint (SSO); requires token
token = <set via env ANSIBLE_GALAXY_SERVER_HUB_TOKEN>
[galaxy_server.galaxy]
url = https://galaxy.ansible.com/
```
Servers are searched in `server_list` order; `source:` on an entry names the server for that requirement. The token can come from the environment variable `ANSIBLE_GALAXY_SERVER_<ID>_<KEY>` (for example `ANSIBLE_GALAXY_SERVER_HUB_TOKEN`).

## Pinning strategy
- Production: exact versions for everything + an EE image built from them.
- Libraries/roles you publish: ranges in `galaxy.yml` dependencies, exact pins in your own deploy repo.

## Gotchas
- A git collection source must contain `galaxy.yml` or `MANIFEST.json` at the repository top level, or in directories one level down; use a `#/path/` fragment before the optional `,version` to target a subdirectory.
- A range that allows a new major silently changes behaviour; ranges should cap the major.
- Collections installed in a user path (`~/.ansible/collections`) shadow or are shadowed by project ones depending on `collections_path` order — check with `ansible-galaxy collection list`.

## Verify
- [ ] `ansible-galaxy collection list -p ./collections` shows the pinned versions.
- [ ] Fresh CI runner installs from requirements.yml with no network access to unpinned sources.

## Checked

Checked 2026-10-26 against the Ansible collections guide installing snippets (requirements file, version ranges, git sources), the Galaxy user guide (roles requirements attributes, server list options `url`, `token`, `auth_url`, environment variable form) and `cli/galaxy.py`. Confirmed: collection entry keys `name`, `version`, `source`, `type` (`git`, `file`, `dir`, `galaxy`), role keys `name`, `src`, `scm`, `version`, no ranges for roles, range operators, pre-release rule, the custom-path caveat. Replaced vendor-specific Red Hat hub URLs with placeholders and removed the Renovate and git-binary claims.

Method: documentation only; no commands were run.
